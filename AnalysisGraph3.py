import chess
import chess.engine
import os
import matplotlib.pyplot as plt
import numpy as np
import chess.pgn
from copy import deepcopy
from multiprocessing import Pool

# stockfishpath = os.path.abspath("stockfish_13_linux_x64_bmi2/stockfish_13_linux_x64_bmi2/sto ckfish_13_linux_x64_bmi2") #Path to stockfish binary
stockfishpath = os.path.abspath("stockfish_13_win_x64_bmi2\stockfish_13_win_x64_bmi2.exe") #Path to stockfish binary
pgnstring = 'pgnstring.txt' #Put the pgn string in this file
timelimit = 15 #time limit for evaluation of each board position. in s
multipv = 3 #How many main lines does the engine goes through

with open(pgnstring) as pgn:
	first_game = chess.pgn.read_game(pgn) # Read the pgn

engine = chess.engine.SimpleEngine.popen_uci(stockfishpath) #Instantiate the engine

def getevaluation_par(mv_fen):
	'''
	mv_fen[1] is the fen representation of the board position
	mv_fen[0] is the move number of that board position. This is needed here because the multiprocessing map function 
	does not return the outputs sequentially and thus is needed to know the output score corresponds to which move number.
	Returns the move number and evaluation.
	'''
	movenum = mv_fen[0]
	print(movenum)
	fen = mv_fen[1]
	board = chess.Board(fen=fen)
	infopvlist = engine.analyse(board, chess.engine.Limit(time=timelimit), multipv=multipv)
	idx = np.argmax([info["score"].pov(info["score"].turn) for info in infopvlist]) #Find which main line has the best score
	info=infopvlist[idx]
	return [movenum,info]


def main():
	board = chess.Board()

	movenumlist = []
	scorelist = []
	matelist = []

	fenlist = []
	movenum = 0.5
	movenumlist.append(movenum)
	fen = board.fen()
	fenlist.append(fen)
	# Getting the fen representation of each board position
	for move in first_game.mainline_moves():
		movenum = movenum +0.5
		movenumlist.append(movenum)
		board.push(move)
		fen = board.fen()
		fenlist.append(fen)


	# #################### single process #########################################
	# def getevaluation(fen):
	# 	board = chess.Board(fen=fen)
	# 	infopvlist = engine.analyse(board, chess.engine.Limit(time=0.1), multipv=3)
	# 	idx = np.argmax([info["score"].pov(info["score"].turn) for info in infopvlist])
	# 	info=infopvlist[idx]
	# 	return info

	# movenumlist = []
	# scorelist = []
	# matelist = []

	# movenum = 0
	# for fen in fenlist:
	# 	movenum = movenum+0.5
	# 	print(movenum, end='\r')
	# 	movenumlist.append(movenum)
	# 	info = getevaluation(fen)
	# 	# print(info)
	# 	score = info["score"].white().score(mate_score=10000)/100
	# 	scorelist.append(score)
	# 	if info["score"].is_mate():
	# 		matelist.append([movenum, str(info["score"].white().mate())])

	# #############################################################

	####################### parallel processes #######################

	pool = Pool(processes=os.cpu_count()-2) #opening processes
	infolist = pool.map(getevaluation_par, zip(movenumlist,fenlist)) #This maps the function to all the fen we got above

	movenumlist = []
	#Extract the score from all the other information in the returned infolist variable
	for i,mv_info in enumerate(infolist):
		movenum = mv_info[0]
		movenumlist.append(movenum)
		info = mv_info[1]
		score = info["score"].white().score(mate_score=10000)/100 # The actual evaulation scores
		scorelist.append(score)
		if info["score"].is_mate():
			matelist.append([movenum, str(info["score"].white().mate())]) #Checks if the evaluation is mate in X and stores X if yes.

	pool.terminate()
	##############################################################
		
	print(movenumlist)
	print(scorelist)
	print(matelist)

	#Plotting the score at each movenumber
	plt.bar(movenumlist, scorelist, width=0.5, edgecolor='grey')
	plt.ylim(-10,10)
	plt.xlabel('Move number')
	plt.ylabel('Evaluation')
	plt.grid()

	for mmm, MMM in matelist:
		plt.text(mmm-0.25, 9, 'M'+MMM, fontsize='small', rotation='vertical')

	plt.show()

	engine.quit()

if __name__ == '__main__':
	main()
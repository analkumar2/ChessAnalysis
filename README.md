# ChessAnalysis

This code plots the evaluation graph of any standard chess game. Uses multiprocessing to speed up the process.
This script was made because:
* I do not know of any offline gui chess software which plots analysis graph of a game
* Chess.com free version only provides depth 10 analysis graph. Even the premium version depth 18 analysis seems weak to me. I need at least 30.
* Lichess does not provide analysis graph for imported games. It does provide analysis graphs of games played on thier platform but those again are too weak to detect brilliant moves if any.
* The reason I need analysis graph is because I sometimes only want to know where I went wrong and doing the self analysis move by move takes buttload of time.
* Doing the analysis one move at a time is super boring and an ineffcient use my time.

# Requirements

* Python3
* Python3 packages - chess, matplotlib, numpy. Install using 'python3 -m pip install chess matplotlib numpy'
* Stockfish. Download from https://stockfishchess.org/download/

# Usage

* Specify the path to the stockfish binary in the stockfishpath variable.
* Replace the contents of pgnstring.txt with your own pgn
* Specify the time limit (in seconds) each move is evaluated for, in the timelimit variable. Default is 15
* I've set multipv to 3. You can change it in the multipv variable
* Modify the script as you like by going through the chess package doc - https://python-chess.readthedocs.io/en/latest/index.html

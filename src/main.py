from board import Board, bcolors
from settings import *

# Initialize chess board
board = Board()

# Exit while loop on Ctrl+C (KeyboardInterrupt)
try:
    while True:
        #print(board.read_multiplexer(M1))
        #print(board.read_multiplexer(M2))
        #print()
        #board.print_board()
        board.play_game()
                
except KeyboardInterrupt:
    pass

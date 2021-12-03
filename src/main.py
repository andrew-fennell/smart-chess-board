from board import Board

# Initialize chess board
board = Board()

# Exit while loop on Ctrl+C (KeyboardInterrupt)
try:
    while True:
        board.print_board()
except KeyboardInterrupt:
    pass

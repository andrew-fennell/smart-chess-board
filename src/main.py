from board import Board, bcolors
from settings import *

date = input (f"{bcolors.OKGREEN}Enter the current date (Ex: YYYY.MM.DD): {bcolors.ENDC}")
white = input (f"{bcolors.OKGREEN}Player 1 (Last, First): {bcolors.ENDC}")
black = input (f"{bcolors.OKGREEN}Player 2 (Last, First): {bcolors.ENDC}")

# Initialize chess board
board = Board()

output_pgn = ""

if date:
    if len(date.split('.')) == 3:
        date_input = '[Date "' + date + '"]\n'
        output_pgn += date_input
        
if white:
    white_input = '[White "' + white + '"]\n'
    output_pgn += white_input

if black:
    black_input = '[Black "' + black + '"]\n'
    output_pgn += black_input

# Exit while loop on Ctrl+C (KeyboardInterrupt)
try:    
    while True: 
        pgn = board.play_game()
        
except KeyboardInterrupt:
    print()
    result = input(f"Enter the result ( 1-0, 0-1, or 1/2-1/2 ): ")
    
    if result:
        result_input = '[Result "' + result + '"]\n\n'
        output_pgn += result_input
        
        output_pgn += pgn
        
        print(output_pgn)
    
    with open('../output/chess_game.txt', 'w+') as f:
        f.write(output_pgn)

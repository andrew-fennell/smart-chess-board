import os
from time import sleep
import RPi.GPIO as gpio

from settings import *

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Board:

    def __init__(self):
        """Initiates chess board variables."""

        # Setup the initial position of the board
        self.board = [
            ['R','N','B','Q','K','B','N','R'],
            ['p','p','p','p','p','p','p','p'],
            ['-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-'],
            ['p','p','p','p','p','p','p','p'],
            ['R','N','B','Q','K','B','N','R']
        ]

        self.possession = [
            ['b','b','b','b','b','b','b','b'],
            ['b','b','b','b','b','b','b','b'],
            ['-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-'],
            ['w','w','w','w','w','w','w','w'],
            ['w','w','w','w','w','w','w','w']
        ]
        
        self.turn = 'w'
        
        self.moving_piece = None
        self.moving_piece_type = None

        # Setup initial gpio parameters
        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)

        # Initiate the select pins
        gpio.setup(S0, gpio.OUT)
        gpio.setup(S1, gpio.OUT)
        gpio.setup(S2, gpio.OUT)
        gpio.setup(S3, gpio.OUT)

        # Initiate multiplexer output pins
        gpio.setup(M1, gpio.IN)
        gpio.setup(M2, gpio.IN)
        gpio.setup(M3, gpio.IN)
        gpio.setup(M4, gpio.IN)
    
    def move_piece(self, old_row, old_col, new_row, new_col):
        """Moved piece from old position to new position."""
        # Step 1: Check if there is a piece at the position given (old_row, old_col)
        if self.board[old_row][old_col] != ' ':
            # Step 2: Check if the piece being moved is the correct color
            if self.possession[old_row][old_col] == self.turn:
                # Step 3: Delete piece on board at (old_row, old_col), replace piece at
                # (new_row, new_col) with the piece that was deleted
                
                # Determine piece to move
                piece = self.board[old_row][old_col]
                
                # Move piece to new location
                self.board[new_row][new_col] = piece
                
                # Delete previous piece
                self.board[old_row][old_col] = ' '

                # Step 4: Update possession map to reflect the new board
                self.possession[old_row][old_col] = ' '
                self.possession[new_row][new_col] = self.turn
                
                if self.turn == 'w':
                    self.turn = 'b'
                else:
                    self.turn = 'w'
                
            else:
                print('This piece cannot be moved by this player.')
        else:
            print('There is not a piece at the position specified.')
    
    def read_multiplexer(self, multiplexer):
        """Scans each channel of the multiplexer."""
        
        # Setup variables
        channel_values = [
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', '']
        ]

        # Scan through each channel of the multiplexer
        for channel in range(16):
            gpio.output(S0, channel_select[channel][S0])
            gpio.output(S1, channel_select[channel][S1])
            gpio.output(S2, channel_select[channel][S2])
            gpio.output(S3, channel_select[channel][S3])
            
            output = not gpio.input(multiplexer)

            # Read channel value and store it in channel_values
            row = 0
            if channel < 8:
                row = 0
                if output:
                    channel_values[row][channel] = 'X'
                else:
                    channel_values[row][channel] = '-'
            else:
                row = 1
                if output:
                    channel_values[row][channel-8] = 'X'
                else:
                    channel_values[row][channel-8] = '-'
        
        return channel_values
    
    def scan_board(self):
        """Returns the current position of the board."""
        current_board = [
            ['-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-']
        ]

        #for m in [M1, M2, M3, M4]:
        for m in [M1,M2,M3,M4]:
            channel_values = self.read_multiplexer(m)
            
            # Update appropriate board values with the corresponding multiplexer channel_values
            if m == M1:
                current_board[0] = channel_values[0]
                current_board[1] = channel_values[1]
            elif m == M2:
                current_board[2] = channel_values[0]
                current_board[3] = channel_values[1]
            elif m == M3:
                current_board[4] = channel_values[0]
                current_board[5] = channel_values[1]
            elif m == M4:
                current_board[6] = channel_values[0]
                current_board[7] = channel_values[1]
            
        return current_board
    
    def print_board(self):
        """Prints the current board."""
        
        # Clear terminal window
        os.system('cls' if os.name == 'nt' else 'clear')
        # Print the current board
        for i in range(len(self.board)):
            for j in range(len(self.board[i])-1,-1,-1):
                if self.possession[i][j] == 'w':
                    print(f"{bcolors.WARNING}{self.board[i][j]}{bcolors.ENDC}", end=" ")
                elif self.possession[i][j] == 'b':
                    print(f"{bcolors.OKBLUE}{self.board[i][j]}{bcolors.ENDC}", end=" ")
                else:
                    print(f"{bcolors.OKGREEN}{self.board[i][j]}{bcolors.ENDC}", end=" ")
            print()
    
    def play_game(self):
        board_map = [
            ['-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-','-']
        ]
        
        possible_pieces = ['R','N','B','Q','K','p']
        
        for i in range(len(board_map)):
            for j in range(len(board_map[i])):
                if self.board[i][j] in possible_pieces:
                    board_map[i][j] = 'X'
        
        current_board_map = self.scan_board()
        
        # A move is occuring
        if board_map != current_board_map:
            
            current_board = [
                ['-','-','-','-','-','-','-','-'],
                ['-','-','-','-','-','-','-','-'],
                ['-','-','-','-','-','-','-','-'],
                ['-','-','-','-','-','-','-','-'],
                ['-','-','-','-','-','-','-','-'],
                ['-','-','-','-','-','-','-','-'],
                ['-','-','-','-','-','-','-','-'],
                ['-','-','-','-','-','-','-','-']
            ]
            
            current_possession = [
                ['-','-','-','-','-','-','-','-'],
                ['-','-','-','-','-','-','-','-'],
                ['-','-','-','-','-','-','-','-'],
                ['-','-','-','-','-','-','-','-'],
                ['-','-','-','-','-','-','-','-'],
                ['-','-','-','-','-','-','-','-'],
                ['-','-','-','-','-','-','-','-'],
                ['-','-','-','-','-','-','-','-']
            ]
            
            for i in range(len(current_board_map)):
                for j in range(len(current_board_map[i])):
                    
                    piece_found = True if current_board_map[i][j] == 'X' else False
                    prev_on_board = True if self.board[i][j] in possible_pieces else False
                    
                    if piece_found and prev_on_board:
                        current_board[i][j] = self.board[i][j]
                        current_possession[i][j] = self.possession[i][j]
                    elif piece_found and not prev_on_board:
                        current_board[i][j] = self.moving_piece
                        current_possession[i][j] = self.moving_piece_type
                        self.moving_piece = None
                    elif not piece_found and prev_on_board:
                        current_board[i][j] = '-'
                        current_possession[i][j] = '-'
                        self.moving_piece = self.board[i][j]
                        self.moving_piece_type = self.possession[i][j]
                    elif not piece_found and not prev_on_board:
                        current_board[i][j] = '-'
                        current_possession[i][j] = '-'
            
            self.board = current_board
            self.possession = current_possession
        
            self.print_board()

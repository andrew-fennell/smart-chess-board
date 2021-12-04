import os
from time import sleep
import RPi.GPIO as gpio

from settings import *

class Board:

    def __init__(self):
        """Initiates chess board variables."""

        # Setup the initial position of the board
        self.board = [
            ['R','N','B','Q','K','B','N','R'],
            ['p','p','p','p','p','p','p','p'],
            [' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' '],
            ['p','p','p','p','p','p','p','p'],
            ['R','N','B','Q','K','B','N','R']
        ]

        self.possession = [
            ['b','b','b','b','b','b','b','b'],
            ['b','b','b','b','b','b','b','b'],
            [' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' '],
            ['w','w','w','w','w','w','w','w'],
            ['w','w','w','w','w','w','w','w']
        ]

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

        # Step 2: Check if the piece being moved is the correct color

        # Step 3: Delete piece on board at (old_row, old_col), replace piece at
        #         (new_row, new_col) with the piece that was deleted

        # Step 4: Update possession map to reflect the new board
    
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

            # Read channel value and store it in channel_values
            row = 0
            if channel < 8:
                row = 0
            else:
                row = 1

            channel_values[row][channel] = not gpio.input(multiplexer)
        
        return channel_values
    
    def scan_board(self):
        """Returns the current position of the board."""
        current_board = [
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','','']
        ]
    
    def print_board(self):
        """Prints the current board."""
        # Clear current terminal window
        os.system('cls' if os.name == 'nt' else 'clear')

        # Print the current board
        for i in reversed(self.board):
            for j in reversed(i):
                print(j, end=" ")
            print()

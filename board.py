"""
This modules defines the board of the game based on the configuration the user has requested
"""
import numpy as np
import pawn

class Board:
    # Initialize the board based on the config the user requested
    def __init__(self, numOfSquares):
        self.board = np.zeros((numOfSquares, numOfSquares))
        self.p1_pawns = {}
        self.p2_pawns = {}
        self.num_of_pawns = ((numOfSquares - 2) / 2) * (numOfSquares / 2)
        self.initialize_players(0, 1)
        self.initialize_players(int(numOfSquares - ((numOfSquares - 2) / 2)), 0, False)
    # Initialize player pawns and populate the board with their positions
    def initialize_players(self, start_row, start_index, p1 = True):
        print(f"params: {start_row}, {start_index}")
        rows, cols = self.board.shape
        print(f"shape of board is {rows}, {cols}")
        num_rows_to_fill = int((rows - 2) / 2)
        print(num_rows_to_fill)
        pawn_id = 1
        for row in range(start_row, start_row + num_rows_to_fill):
            for col in range(start_index, cols, 2):
                print(f"Row Col {row}, {col}")
                if(p1):
                    self.board[row, col] = pawn_id
                    self.p1_pawns[pawn_id] = pawn.Pawn(pawn_id, row, col, start_row)
                    pawn_id += 1
                else:
                    self.board[row, col] = -pawn_id
                    self.p1_pawns[-pawn_id] = pawn.Pawn(-pawn_id, row, col, start_row)
                    pawn_id += 1
            if start_index == 0:
                start_index = 1
            else:
                start_index = 0
    # This method is used to search for all the movable pawns of the players
    def check_available_pawns_to_move(self, p1=False):
        """
        :param p1 boolean 
        :return array array of pawns that can move forward/backward
        """
    # This method is used to check the possible coordinates that the pawn can move to
    def get_moves(self, pawn):
        """
        :param pawn Pawn object
        :return array array of coordinates the pawn can move to
        """
    # This method is used to analyze the move when the pawn is selected
    def check_move_type(self, pawn):
        """
        :param pawn Pawn object
        :return boolean  True for simple move and False capturing move
        """
    # This method controls the pawn's movement
    def move_pawn(self, pawn_id):
        """
            This method handle the pawn movement inside the board
            :param pawn_id int
            Changes the position of the pawn selected and state of board
        """
    # This method is used when the move type is a capturing move
    def move_capture_pawn(self, pawn):
        """
        :param pawn Pawn object
        """
    # This method is used when the move type is simple, move the pawn diagonally, change the state of board and coordinate of given pawn
    def simple_move(self, pawn):
        """
        :param pawn Pawn object

        """
    # This method checks if the game is over or not.
    def check_game_status(self):
        """
            This method checks the status of the game
            Returns true if the game is over and false if the game is still active in progress
        """
    # String representation of the Board object
    def __str__(self):
        return f"Object details: \n{self.board}\n {self.p1_pawns} \n {self.p2_pawns}"


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
    def check_move_type(self, pawn, direction):
        """
        :param pawn Pawn object
        :return int  0 for simple move, 1 capturing move and -1 if the move cannot be made
        """
        new_x, new_y = self.get_new_coordinates(direction)
        new_id = self.board[new_x, new_y]
        if new_id == 0
            return 0
        elif new_id > 0 and pawn.id > 0 or new_id < 0 and pawn.id < 0:
            return -1
        else:
            return 1
    # This method controls the pawn's movement
    def move_pawn(self, pawn, direction):
        """
            This method handle the pawn movement inside the board
            :param pawn_id int
            Changes the position of the pawn selected and state of board
        """
        if self.check_move_type(pawn, direction) == 0:
            self.simple_move(pawn, direction)
        elif self.check_move_type(pawn, direction) == 1:
            self.move_capture_pawn(pawn, direction)
            #  Check if the move can be chained by another capture
            # return not self.check_move_type(pawn, NORTHEAST) or not self.check_move_type(pawn, NORTHWEST)
    # This method is used when the move type is a capturing move
    def move_capture_pawn(self, pawn, direction):
        """
        :param pawn Pawn object
        """
        pawn_id = pawn.id
        pawn_coordinates = pawn.coordinates
        rival_pawn_coordinates = self.get_new_coordinates(direction, pawn)
        rival_pawn = self.p1_pawns[self.board[rival_pawn_coordinates] if self.board[rival_pawn_coordinates] > 0 else self.p2_pawns[self.board[rival_pawn_coordinates]
        new_x, new_y = self.get_new_coordinates(direction, rival_pawn)
        self.remove_pawn(self, pawn, rival_pawn.id > 0)
        self.update_board_pawn(new_x, new_y, pawn, pawn.id > 0)
    # This method is used when the move type is simple, move the pawn diagonally, change the state of board and coordinate of given pawn
    def simple_move(self, pawn, direction):
        """
        :param pawn Pawn object
        """
        new_x, new_y = self.get_new_coordinates(direction, pawn)
        self.update_board_pawn(new_x, new_y, pawn, pawn.id > 0)
    # This method is used to update the state of the board and pawn
    def update_board_pawn(self, new_x, new_y, pawn, p1 = True):
        self.board[new_x, new_y] = pawn.id
        self.board[pawn.coordinates] = 0
        if(p1):
            self.p1_pawns(pawn.id).coordinates = (new_x, new_y)
        else:
            self.p2_pawns(pawn.id).coordinates = (new_x, new_y)
    # This method is used to remove pawn from players' dictionary and updates the state of board
    def remove_pawn(self, pawn, p1 = True):
        pawn_id = pawn.id
        pawn_coordinates = pawn.coordinates
        if p1:
            self.p1_pawns.pop(pawn_id, None)
        else
            self.p2_pawns.pop(pawn_id, None)
        self.board[pawn_coordinates] = 0
    # This method checks if the game is over or not.
    def check_game_status(self):
        """
            This method checks the status of the game
            Returns true if the game is over and false if the game is still active in progress
        """
        if self.moves_since_last_capture > 50 or len(self.p1_pawns) == 0 or len(self.p2_pawns) == 0:
            return True
        return False
    # This method is used to declare winner
    def declare_winner(self):
        """
            This method declares the winner of the game
            Returns 1 | 0 | -1, 1 if player1 is the winner, -1 if player2 is the winner and 0 if its a tie
        """
        if len(self.p1_pawns) == 0:
            return 1
        elif len(self.p2_pawns) == 0:
            return -1
        else:
            return 0

    # String representation of the Board object
    def __str__(self):
        return f"Object details: \n{self.board}\n {self.p1_pawns} \n {self.p2_pawns}"


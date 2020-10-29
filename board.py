"""
This modules defines the board of the game based on the configuration the user has requested
"""
import numpy as np
import pawn

##DIRECTIONS##
NORTHWEST = "northwest"
NORTHEAST = "northeast"
SOUTHWEST = "southwest"
SOUTHEAST = "southeast"

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
                    self.p2_pawns[-pawn_id] = pawn.Pawn(-pawn_id, row, col, start_row)
                    pawn_id += 1
            if start_index == 0:
                start_index = 1
            else:
                start_index = 0

    def update_board_pawn(self, new_x, new_y, pawn, p1=True):
        old_x, old_y = pawn.coordinates
        temp = self.board[new_x][new_y]
        self.board[new_x][new_y] = pawn.id
        self.board[old_x][old_y] = temp
        if p1:
            self.p1_pawns[pawn.id].coordinates = (new_x,new_y)
        else:
            self.p2_pawns[pawn.id].coordinates = (new_x, new_y)

    def get_available_pawns(self,player_pawns_list,p2_list,dir):
        temp_dict = player_pawns_list
        player_available_pawns = []
        for p in temp_dict:
            #print(temp_dict[p])
            # print(type(temp_dict[p]))
            x, y = self.get_new_coordinates(dir[0], temp_dict[p]) # dir[0]
            a, b = self.get_new_coordinates(dir[1], temp_dict[p]) # dir[1]
            if (0 <= x < 8) and (0 <= y < 8) and self.board[x][y] == 0 and p not in player_available_pawns:
                player_available_pawns.append(p)
            elif (0 <= x < 8) and (0 <= y < 8) and self.board[x][y] in p2_list and p not in player_available_pawns:
                x1, y1 = self.get_new_coordinates(dir[0], p2_list[self.board[x][y]])
                if self.board[x1,y1] == 0 and p not in player_available_pawns:
                    player_available_pawns.append(p)
            if (0 <= a < 8) and (0 <= b < 8) and self.board[a][b] == 0 and p not in player_available_pawns:
                player_available_pawns.append(p)
            elif (0 <= a < 8) and (0 <= b < 8) and self.board[a][b] in p2_list and p not in player_available_pawns:
                a1, b1 = self.get_new_coordinates(dir[0], p2_list[self.board[a][b]])
                if self.board[a1,b1] == 0 and p not in player_available_pawns:
                    player_available_pawns.append(p)

        return player_available_pawns

    # This method is used to search for all the movable pawns of the players
    def check_available_pawns_to_move(self, p1=False):
        """
        :param p1 boolean 
        :return array array of pawns that can move forward/backward
        Available pawns to move
        """
        if p1 == True:
            self.board[2][1] = 0
            self.board[4][1] = 9
            self.board[2][3] = 0
            self.board[4][3] = 10
            return self.get_available_pawns(self.p1_pawns,self.p2_pawns,[SOUTHWEST,SOUTHEAST])
        else:
            return self.get_available_pawns(self.p2_pawns,self.p1_pawns,[NORTHWEST,NORTHEAST])


    def get_new_coordinates(self, dir, pawn):
        """
        Returns the coordinates one square in a different direction to (x,y).
        """
        x,y = (pawn.coordinates)
        if dir == NORTHWEST:
            return x - 1, y - 1
        elif dir == SOUTHWEST:
            return x + 1, y - 1
        elif dir == NORTHEAST:
            return x - 1, y + 1
        elif dir == SOUTHEAST:
            return x + 1, y + 1
        else:
            return 0

    # This method is used to check the possible coordinates that the pawn can move to
    def get_moves(self, pawn):
        """
        :param pawn Pawn object
        :return array array of coordinates the pawn can move to
        Returns a list of legal move locations from a set of coordinates (x,y) on the board.
        If that location is empty, then get_moves() return an empty list.
        """
        x, y = (pawn.coordinates)
        pawn_id = self.board[x][y]
        if pawn_id != 0:
            if pawn_id < 0 and pawn.is_king is False:
                get_pawn_moves = [self.get_new_coordinates(NORTHWEST, pawn), self.get_new_coordinates(NORTHEAST, pawn)]

            elif pawn_id > 0 and pawn.is_king is False:
                get_pawn_moves = [self.get_new_coordinates(SOUTHWEST, pawn), self.get_new_coordinates(SOUTHEAST, pawn)]

            else:
                get_pawn_moves = [self.get_new_coordinates(NORTHWEST, pawn), self.get_new_coordinates(NORTHEAST, pawn),
                                  self.get_new_coordinates(SOUTHWEST, pawn), self.get_new_coordinates(SOUTHEAST, pawn)]
        else:
            get_pawn_moves = []

        return get_pawn_moves

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


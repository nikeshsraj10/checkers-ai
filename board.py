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

# Obstacle
OBSTACLE = 13


class Board:
    # Initialize the board based on the config the user requested
    def __init__(self, numOfSquares=8):
        self.board = np.zeros((numOfSquares, numOfSquares))
        self.p1_pawns = {}
        self.p2_pawns = {}
        self.num_of_pawns = ((numOfSquares - 2) / 2) * (numOfSquares / 2)
        self.initialize_players(0, 1)
        if numOfSquares == 8:
            self.initialize_players(int(numOfSquares - ((numOfSquares - 2) / 2)), 0, False)
        elif numOfSquares == 10 or numOfSquares == 6:
            self.initialize_players(int(numOfSquares - ((numOfSquares - 2) / 2)), 1, False)
        self.total_moves = 0
        self.moves_since_last_capture = 0

    # Initialize player pawns and populate the board with their positions
    def initialize_players(self, start_row, start_index, p1=True):
        rows, cols = self.board.shape
        num_rows_to_fill = int((rows - 2) / 2)
        pawn_id = 1
        for row in range(start_row, start_row + num_rows_to_fill):
            for col in range(start_index, cols, 2):
                if (p1):
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
            self.p1_pawns[pawn.id].coordinates = (new_x, new_y)
        else:
            self.p2_pawns[pawn.id].coordinates = (new_x, new_y)

    def get_available_pawns(self, player_pawns_list, p2_list, dir):
        temp_dict = player_pawns_list
        player_available_pawns = []
        for p in temp_dict:
            if not temp_dict[int(p)].is_king:
                x, y = self.get_new_coordinates(dir[0], temp_dict[p])
                a, b = self.get_new_coordinates(dir[1], temp_dict[p])
                if self.check_boundry(x, y) and p not in player_available_pawns:
                    if self.board[x][y] == 0:
                        player_available_pawns.append(p)
                    elif self.board[x][y] in p2_list:
                        x1, y1 = self.get_new_coordinates(dir[0], p2_list[self.board[x][y]])
                        if self.check_boundry(x1, y1) and self.board[x1, y1] == 0:
                            player_available_pawns.append(p)
                if self.check_boundry(a, b) and p not in player_available_pawns:
                    if self.board[a][b] == 0:
                        player_available_pawns.append(p)
                    elif self.board[a][b] in p2_list:
                        a1, b1 = self.get_new_coordinates(dir[1], p2_list[self.board[a][b]])
                        if self.check_boundry(a1, b1) and self.board[a1, b1] == 0:
                            player_available_pawns.append(p)
            else:
                temp_list = self.get_kings_move(temp_dict[p])
                if len(temp_list) > 0:
                    player_available_pawns.append(p)

        return player_available_pawns

    def check_boundry(self, x, y):
        rows, cols = self.board.shape
        if (0 <= x < rows) and (0 <= y < cols):
            return True
        else:
            return False

    # This method is used to search for all the movable pawns of the players
    def check_available_pawns_to_move(self, p1=False):
        """
        :param p1 boolean 
        :return array array of pawns that can move forward/backward
        Available pawns to move
        """
        if p1 == True:
            return self.get_available_pawns(self.p1_pawns, self.p2_pawns, [SOUTHWEST, SOUTHEAST])
        else:
            return self.get_available_pawns(self.p2_pawns, self.p1_pawns, [NORTHWEST, NORTHEAST])

    def get_new_coordinates(self, dir, pawn):
        """
        Returns the coordinates one square in a different direction to (x,y).
        """
        x, y = (pawn.coordinates)
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

    def get_player1_moves(self, dir1, dir2, pawn):
        get_pawn_moves = []
        sw_x, sw_y = self.get_new_coordinates(dir1, pawn)
        se_x, se_y = self.get_new_coordinates(dir2, pawn)
        if self.check_boundry(sw_x, sw_y) and self.board[sw_x][sw_y] < 0 and self.board[sw_x][sw_y] != OBSTACLE:
            sw_sw_x, sw_sw_y = self.get_new_coordinates(dir1, self.p2_pawns[self.board[sw_x][sw_y]])
            if self.check_boundry(sw_sw_x, sw_sw_y) and self.board[sw_sw_x][sw_sw_y] == 0:
                get_pawn_moves.append((sw_sw_x, sw_sw_y))
        if self.check_boundry(se_x, se_y) and self.board[se_x][se_y] < 0 and self.board[sw_x][sw_y] != OBSTACLE:
            se_se_x, se_se_y = self.get_new_coordinates(dir2, self.p2_pawns[self.board[se_x][se_y]])
            if self.check_boundry(se_se_x, se_se_y) and self.board[se_se_x][se_se_y] == 0:
                get_pawn_moves.append((se_se_x, se_se_y))
        if self.check_boundry(sw_x, sw_y) and self.board[sw_x][sw_y] == 0:
            get_pawn_moves.append((sw_x, sw_y))
        if self.check_boundry(se_x, se_y) and self.board[se_x][se_y] == 0:
            get_pawn_moves.append((se_x, se_y))

        return get_pawn_moves

    def get_player2_moves(self, dir1, dir2, pawn):
        get_pawn_moves = []
        nw_x, nw_y = self.get_new_coordinates(dir1, pawn)
        ne_x, ne_y = self.get_new_coordinates(dir2, pawn)
        if self.check_boundry(nw_x, nw_y) and self.board[nw_x][nw_y] > 0 and self.board[nw_x][nw_y] != OBSTACLE:
            nw_nw_x, nw_nw_y = self.get_new_coordinates(dir1, self.p1_pawns[self.board[nw_x][nw_y]])
            if self.check_boundry(nw_nw_x, nw_nw_y) and self.board[nw_nw_x][nw_nw_y] == 0:
                get_pawn_moves.append((nw_nw_x, nw_nw_y))
        if self.check_boundry(ne_x, ne_y) and self.board[ne_x][ne_y] > 0 and self.board[ne_x][ne_y] != OBSTACLE:
            ne_ne_x, ne_ne_y = self.get_new_coordinates(dir2, self.p1_pawns[self.board[ne_x][ne_y]])
            if self.check_boundry(ne_ne_x, ne_ne_y) and self.board[ne_ne_x][ne_ne_y] == 0:
                get_pawn_moves.append((ne_ne_x, ne_ne_y))
        if self.check_boundry(nw_x, nw_y) and self.board[nw_x][nw_y] == 0:
            get_pawn_moves.append((nw_x, nw_y))
        if self.check_boundry(ne_x, ne_y) and self.board[ne_x][ne_y] == 0:
            get_pawn_moves.append((ne_x, ne_y))

        return get_pawn_moves

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
                get_pawn_moves = self.get_player2_moves(NORTHWEST, NORTHEAST, pawn)
            elif pawn_id > 0 and pawn.is_king is False:
                get_pawn_moves = self.get_player1_moves(SOUTHWEST, SOUTHEAST, pawn)
            else:
                get_pawn_moves = self.get_kings_move(pawn)
        else:
            get_pawn_moves = []

        return get_pawn_moves

    def get_kings_move(self, pawn):
        x, y = (pawn.coordinates)
        get_pawn_moves = []
        pawn_id = self.board[x][y]
        if pawn_id != 0:
            if pawn_id < 0:
                get_pawn_moves.extend(self.get_player2_moves(NORTHWEST, NORTHEAST, pawn))
                get_pawn_moves.extend(self.get_player2_moves(SOUTHWEST, SOUTHEAST, pawn))
            elif pawn_id > 0:
                get_pawn_moves.extend(self.get_player1_moves(NORTHWEST, NORTHEAST, pawn))
                get_pawn_moves.extend(self.get_player1_moves(SOUTHWEST, SOUTHEAST, pawn))
        return get_pawn_moves

    # This method is used to analyze the move when the pawn is selected
    def check_move_type(self, pawn, direction):
        """
        :param pawn Pawn object
        :return int  0 for simple move, 1 capturing move and -1 if the move cannot be made
        """
        new_x, new_y = self.get_new_coordinates(direction, pawn)
        new_id = self.board[new_x, new_y]
        if new_id == 0:
            return 0
        elif new_id > 0 and pawn.id > 0 or new_id < 0 and pawn.id < 0:
            return -1
        else:
            return 1

    # This method controls the pawn's movement
    def move_pawn(self, pawn, coordinate):
        """
            This method handle the pawn movement inside the board
            :param pawn_id int
            Changes the position of the pawn selected and state of board
            :return list if the move is of type capture and can be chained
        """
        direction = self.get_direction_from_coordinates(pawn, coordinate)
        self.total_moves += 1
        self.moves_since_last_capture += 1
        chain_capture_coordinates = []
        if self.check_move_type(pawn, direction) == 0:
            self.simple_move(pawn, direction)
        elif self.check_move_type(pawn, direction) == 1:
            self.move_capture_pawn(pawn, direction)
            #  Check if the move can be chained by another capture
            chain_capture_coordinates = self.get_chain_capture_coordinates(pawn)
        if (pawn.id > 0 and pawn.coordinates[0] == self.board.shape[0] - 1) or (
                pawn.id < 0 and pawn.coordinates[0] == 0):
            pawn.is_king = True
        return chain_capture_coordinates

    def get_chain_capture_coordinates(self, pawn):
        chain_capture_coordinates = []
        moves_list = self.get_moves(pawn)
        for coordinate in moves_list:
            move_type = self.check_move_type(pawn, self.get_direction_from_coordinates(pawn, coordinate))
            if move_type == 1:
                chain_capture_coordinates.append(coordinate)
        return chain_capture_coordinates

    # This method is used when the move type is a capturing move
    def move_capture_pawn(self, pawn, direction):
        """
        :param pawn Pawn object
        """
        pawn_id = pawn.id
        pawn_coordinates = pawn.coordinates
        rival_pawn_coordinates = self.get_new_coordinates(direction, pawn)
        rival_pawn = self.p1_pawns[self.board[rival_pawn_coordinates]] if self.board[rival_pawn_coordinates] > 0 else \
        self.p2_pawns[self.board[rival_pawn_coordinates]]
        new_x, new_y = self.get_new_coordinates(direction, rival_pawn)
        self.remove_pawn(rival_pawn, rival_pawn.id > 0)
        self.update_board_pawn(new_x, new_y, pawn, pawn.id > 0)

    # This method is used when the move type is simple, move the pawn diagonally, change the state of board and coordinate of given pawn
    def simple_move(self, pawn, direction):
        """
        :param pawn Pawn object
        """
        new_x, new_y = self.get_new_coordinates(direction, pawn)
        self.update_board_pawn(new_x, new_y, pawn, pawn.id > 0)

    # This method is used to update the state of the board and pawn
    def update_board_pawn(self, new_x, new_y, pawn, p1=True):
        self.board[new_x, new_y] = pawn.id
        self.board[pawn.coordinates] = 0
        if (p1):
            self.p1_pawns[pawn.id].coordinates = (new_x, new_y)
        else:
            self.p2_pawns[pawn.id].coordinates = (new_x, new_y)

    # This method is used to remove pawn from players' dictionary and updates the state of board
    def remove_pawn(self, pawn, p1=True):
        self.moves_since_last_capture = 0
        pawn_id = pawn.id
        pawn_coordinates = pawn.coordinates
        if p1:
            self.p1_pawns.pop(pawn_id, None)
        else:
            self.p2_pawns.pop(pawn_id, None)
        self.board[pawn_coordinates] = 0

    # This method checks if the game is over or not.
    def check_game_status(self):
        """
            This method checks the status of the game
            Returns true if the game is over and false if the game is still active in progress
        """
        if self.moves_since_last_capture > 40 or len(self.p1_pawns) == 0 or len(self.p2_pawns) == 0:
            return True
        return False

    # This method is used to declare winner
    def declare_winner(self):
        """
            This method declares the winner of the game
            Returns 1 | 0 | -1, 1 if player1 is the winner, -1 if player2 is the winner and 0 if its a tie
        """
        if len(self.p1_pawns) == 0:
            return -1
        elif len(self.p2_pawns) == 0:
            return 1
        else:
            return 1 if len(self.p1_pawns) > len(self.p2_pawns) else -1

    # This method gives the direction from the given pawn and new coordinate
    def get_direction_from_coordinates(self, pawn, new_coordinate):
        x, y = (pawn.coordinates)
        new_x, new_y = new_coordinate
        if x > new_x and y > new_y:
            return NORTHWEST
        elif x < new_x and y > new_y:
            return SOUTHWEST
        elif x > new_x and y < new_y:
            return NORTHEAST
        elif x < new_x and y < new_y:
            return SOUTHEAST

    def total_kings(self, pawns):
        count = 0
        for pawn in pawns.values():
            if pawn.is_king:
                count += 1
        return count

    def compute_score(self):
        return len(self.p1_pawns) - len(self.p2_pawns) + \
               (self.total_kings(self.p1_pawns) * 0.5 - self.total_kings(self.p2_pawns) * 0.5)

    def compute_score2(self):
        score = 0
        # if player1's turn
        if self.total_moves % 2 == 0:
            for i in range(self.board[0].size):
                for j in range(self.board[0].size):
                    pawn = self.board[i][j]
                    if pawn in self.p1_pawns.keys() or pawn in self.p2_pawns.keys():
                        if pawn in self.p1_pawns.keys() and self.p1_pawns[pawn].is_king:
                            score += 10
                        elif pawn in self.p2_pawns.keys() and self.p2_pawns[pawn].is_king:
                            score -= 10
                        elif pawn in self.p1_pawns.keys() and i < 4:
                            score += 5
                        elif pawn in self.p2_pawns.keys() and i < 4:
                            score -= 7
                        elif pawn in self.p1_pawns.keys() and i >= 4:
                            score += 7
                        elif pawn in self.p2_pawns.keys() and i >= 4:
                            score -= 5
        # if player2's turn
        else:
            for i in range(self.board[0].size):
                for j in range(self.board[0].size):
                    pawn = self.board[i][j]
                    if pawn in self.p1_pawns.keys() or pawn in self.p2_pawns.keys():
                        if pawn in self.p1_pawns.keys() and self.p1_pawns[pawn].is_king:
                            score += 10
                        elif pawn in self.p2_pawns.keys() and self.p2_pawns[pawn].is_king:
                            score -= 10
                        elif pawn in self.p1_pawns.keys() and i < 4:
                            score += 7
                        elif pawn in self.p2_pawns.keys() and i < 4:
                            score -= 5
                        elif pawn in self.p1_pawns.keys() and i >= 4:
                            score += 7
                        elif pawn in self.p2_pawns.keys() and i >= 4:
                            score -= 5
        #print(f"score: {score / (len(self.p1_pawns) + (len(self.p2_pawns)))}")
        return score / (len(self.p1_pawns) + (len(self.p2_pawns)))

    # This method adds obstacles to the board
    def set_obstacles(self, num_of_obstacles=0):
        obstacles = []
        rows = self.board.shape[0]
        while num_of_obstacles > 0:
            x = np.random.randint(rows)
            y = np.random.randint(rows)
            if self.board[x, y] == 0:
                self.board[x, y] = OBSTACLE
                obstacles.append((x, y))
                num_of_obstacles -= 1
        return obstacles

    # String representation of the Board object
    def __str__(self):
        return f"Board: \n{self.board}\n"


if __name__ == "__main__":
    board = Board()
    obs = board.set_obstacles(3)
    print(board)
    print(obs)

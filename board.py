import numpy as np
import pawn

class Board:

    def __init__(self, numOfSquares):
        self.board = np.zeros((numOfSquares, numOfSquares))
        self.p1_pawns = {}
        self.p2_pawns = {}
        self.num_of_pawns = ((numOfSquares - 2) / 2) * (numOfSquares / 2)
        self.initialize_players(0, 1)
        self.initialize_players(int(numOfSquares - ((numOfSquares - 2) / 2)), 0, False)

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



    def __str__(self):
        return f"Object details: \n{self.board}\n{self.num_of_pawns}\n {self.p1_pawns} \n {self.p2_pawns}"


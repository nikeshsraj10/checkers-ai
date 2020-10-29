"""
    This module handles logic to st
"""
import board as Board

class Game:
    def __init__(self):
        self.jump = False

    def start_game(self):
        print("Select the board configuration you want to play")
        try:
            board_created = False
            while(not board_created):
                numOfSquares = int(input("1. 6x6 \t2. 8x8 \t3.10x10 \n"))
                if(numOfSquares == 1):
                    board = Board.Board(6)
                    break
                elif(numOfSquares == 2):
                    board = Board.Board(8)
                    break
                elif(numOfSquares == 3):
                    board = Board.Board(10)
                    break
            print(board)
            board.update_board_pawn(4, 1, board.p1_pawns[9],True)
            board.update_board_pawn(4, 3, board.p1_pawns[10],True)
            print(board)
            print("Which pawn to be moved")
            lis = board.check_available_pawns_to_move(True)
            print(lis)

        except Exception as e:
            print(f"Error Occurred: {e}")
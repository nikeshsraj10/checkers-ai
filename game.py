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
            while not board.check_game_status():
                print(board)
                # Player1 Turn
                pawn_selected = False
                while not pawn_selected:
                    if board.total_moves % 2 == 0:
                        available_pawns = board.check_available_pawns_to_move(True)
                    else:
                        available_pawns = board.check_available_pawns_to_move(False)
                    print(available_pawns)
                    player_pawn_choice = int(input("Select Pawn to move\n"))
                    if(player_pawn_choice in available_pawns):
                        pawn_selected = True
                coordinate_selected = False
                while not coordinate_selected:
                    if board.total_moves % 2 == 0:
                        available_coordinates = board.get_moves(board.p1_pawns[player_pawn_choice])
                    else:
                        available_coordinates = board.get_moves(board.p2_pawns[player_pawn_choice])
                    print(available_coordinates)
                    player_coordinate_choice = int(input("Select the position of Coordinate to move, for eg: 1 or 2 or 3 or 4\n"))
                    if player_coordinate_choice <= len(available_coordinates) and player_coordinate_choice > 0:
                        coordinate_selected = True
                if board.total_moves % 2 == 0:
                    board.move_pawn(board.p1_pawns[player_pawn_choice], available_coordinates[player_coordinate_choice - 1])
                else:
                    board.move_pawn(board.p2_pawns[player_pawn_choice], available_coordinates[player_coordinate_choice - 1])




        except Exception as e:
            print(f"Error Occurred: {e}")
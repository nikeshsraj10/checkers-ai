"""
    This module handles the flow of game
"""
import board as Board
import sys
from bot import Node
from bot import Bot 

class Game:
    def __init__(self):
        self.jump = False

    def start_game(self):
        print("Select the board configuration you want to play")
        try:
            board_created = False
            while(not board_created):
                try:
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
                except (KeyboardInterrupt, SystemExit) as e:
                    sys.exit(0)
                except:
                    print("Enter Input in the proper format")   
            # Add 3 obstacles
            obstacles = board.set_obstacles(3)
            print(f"Obstacles added at {obstacles}")
            # Let player choose the AI to play against
            ai_selected = False
            while not ai_selected:
                try:
                    ai_select = int(input("Choose AI to play against: \n1: Baseline AI \t2: MCTS AI "))
                    if ai_select == 1 or ai_select == 2:
                        ai_selected = True
                except (KeyboardInterrupt, SystemExit) as e:
                    sys.exit(0)
                except:
                    print("Enter Input in the proper format")
            game_bot = Bot()
            nodes_processed = 0
            while not board.check_game_status():
                print(board)
                print(f"Move #: {board.total_moves}")
                if board.total_moves % 2 == 0:
                    print("AI Turn\n")
                else:
                    print("Player2, It's your turn to play\n")
                # Player1 Turn
                pawn_selected = False
                if board.total_moves % 2 == 0:
                    nodes_processed = game_bot.tree_node_processed
                    node = Node(board)
                    index, parent_state = game_bot.mcts(node, num_rollouts = 25)
                    node = parent_state.children()[index]
                    print(f"Nodes processed this turn {game_bot.tree_node_processed - nodes_processed}")
                else: 
                    while not pawn_selected:
                        try: 
                            available_pawns = board.check_available_pawns_to_move(False)
                            print(available_pawns)
                            player_pawn_choice = int(input("Select Pawn to move\n"))
                            if(player_pawn_choice in available_pawns):
                                pawn_selected = True
                        except (KeyboardInterrupt, SystemExit) as e:
                            sys.exit(0)
                        except:
                            print("Enter Input in the proper format")
                    coordinate_selected = False
                    while not coordinate_selected:
                        try:
                            available_coordinates = board.get_moves(board.p2_pawns[player_pawn_choice])
                            print(available_coordinates)
                            player_coordinate_choice = int(input("Select the position of Coordinate to move, for eg: 1 or 2 or 3 or 4\n"))
                            if player_coordinate_choice <= len(available_coordinates) and player_coordinate_choice > 0:
                                coordinate_selected = True
                        except (KeyboardInterrupt, SystemExit) as e:
                            sys.exit(0)
                        except:
                            print("Enter Input in the proper format")
                    pawn_chain_capture_coordinates = board.move_pawn(board.p2_pawns[player_pawn_choice], available_coordinates[player_coordinate_choice - 1])
                    if len(pawn_chain_capture_coordinates) > 0:
                        print(board)
                        proper_input =  False
                        # TODO: Add a while loop here to take care of wrong user input
                        curr_moves = board.total_moves
                        while not proper_input:
                            try:
                                board.total_moves = curr_moves
                                chain_capture = int(input("You captured a pawn and now the capture can be chained!!\nDo you want to proceed?\n Select 1.Yes 2.No\n"))
                                if chain_capture == 1:
                                    board.total_moves -= 1
                                    print(pawn_chain_capture_coordinates)
                                    chain_capture_coordinate_choice = int(input("Select the position of Coordinate to move, for eg: 1 or 2 or 3 or 4\n"))
                                    if chain_capture_coordinate_choice <= len(pawn_chain_capture_coordinates) and chain_capture_coordinate_choice > 0:
                                        proper_input = True
                                        board.move_pawn(board.p2_pawns[player_pawn_choice], pawn_chain_capture_coordinates[chain_capture_coordinate_choice - 1])
                            except (KeyboardInterrupt, SystemExit) as e:
                                sys.exit(0)
                            except:
                                print("Enter Input in the proper format")
                if node:
                    board = node.state
                else: 
                    break
            print("Game Over\n")
            winner = board.declare_winner()
            if winner == 1:
                print("Congratulations! Player1. You Won!!")
                print(f"Score = {board.compute_score()}")
            elif winner == -1:
                print("Congratulations! Player2. You Won!!")
                print(f"Score = {board.compute_score() * -1}")
            else:
                print("It's a Tie")
        except Exception as e:
            print(f"Error Occurred: {e}")
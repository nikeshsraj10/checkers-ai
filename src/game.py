"""
    This module handles the flow of game
"""
import board as Board
import sys
from bot import Node
from bot import Bot
from player import Player


class Game:
    def __init__(self):
        self.jump = False

    def start_game(self):
        global node
        print("Select the board configuration you want to play")
        try:
            board_created = False
            while (not board_created):
                try:
                    numOfSquares = int(input("1. 6x6 \t2. 8x8 \t3.10x10 \n"))
                    if (numOfSquares == 1):
                        board = Board.Board(6)
                        break
                    elif (numOfSquares == 2):
                        board = Board.Board(8)
                        break
                    elif (numOfSquares == 3):
                        board = Board.Board(10)
                        break
                except (KeyboardInterrupt, SystemExit) as e:
                    sys.exit(0)
                except:
                    print("Enter Input in the proper format")
                    # Add 3 obstacles
            obstacles = board.set_obstacles(3)
            print(f"Obstacles added at {obstacles}")
            # Let player1 choose his Control action
            player1_selected = False
            player1_select = 0
            while not player1_selected:
                try:
                    player1_select = int(input("Choose player 1 Control : \n1: Human \t2: BaseLine AI \t3: MCTS AI "
                                               "\t4: NN+MCTS AI"))
                    if player1_select == 1 or player1_select == 2 or player1_select == 3 or player1_select == 4:
                        player1_selected = True
                except (KeyboardInterrupt, SystemExit) as e:
                    sys.exit(0)
                except:
                    print("Enter Input in the proper format")
            # Let player2 choose his Control action
            player2_selected = False
            player2_select = 0
            while not player2_selected:
                try:
                    player2_select = int(
                        input("Choose player 2 Control: \n1: Human \t2: BaseLine AI \t3: MCTS AI "
                              "\t2: NN+MCTS AI"))
                    if player2_select == 1 or player2_select == 2 or player2_select == 3 or player2_select == 4:
                        player2_selected = True
                except (KeyboardInterrupt, SystemExit) as e:
                    sys.exit(0)
                except:
                    print("Enter Input in the proper format")
            game_bot = Bot()
            player_1 = Player(False)
            player_2 = Player(True)
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
                    if player1_select == 1:
                        player_1.player_human(board)
                    elif player1_select == 2:
                        node = player_1.player_BaseLine_AI(game_bot,board)
                    elif player1_select == 3:
                        node = player_1.player_MCTS_AI(game_bot,board)
                    elif player1_select == 4:
                        node = player_1.player_NN_MCTS_AI(game_bot,board)
                else:
                    if player2_select == 1:
                        player_2.player_human(board)
                    elif player2_select == 2:
                        node = player_2.player_BaseLine_AI(game_bot, board)
                    elif player2_select == 3:
                        node = player_2.player_MCTS_AI(game_bot, board)
                    elif player2_select == 4:
                        node = player_2.player_NN_MCTS_AI(game_bot, board)
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
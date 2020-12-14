import sys

from bot import Node, nn_puct, puct

class Player:
    def __init__(self,flag):
        #  False : player_1, True : Player_2
        self.player_num = flag

    # If selected player's Control is Human
    def player_human(self, board,player_pawn):
        player_pawn_choice = 0
        pawn_selected = False
        while not pawn_selected:
            try:
                available_pawns = board.check_available_pawns_to_move(self.player_num)
                print(available_pawns)
                player_pawn_choice = int(input("Select Pawn to move\n"))
                if player_pawn_choice in available_pawns:
                    pawn_selected = True
            except (KeyboardInterrupt, SystemExit) as e:
                sys.exit(0)
            except:
                print("Enter Input in the proper format")
            coordinate_selected = False
            while not coordinate_selected:
                try:
                    available_coordinates = board.get_moves(player_pawn[player_pawn_choice])
                    print(available_coordinates)
                    player_coordinate_choice = int(
                        input("Select the position of Coordinate to move, for eg: 1 or 2 or 3 or 4\n"))
                    if len(available_coordinates) >= player_coordinate_choice > 0:
                        coordinate_selected = True
                except (KeyboardInterrupt, SystemExit) as e:
                    sys.exit(0)
                except:
                    print("Enter Input in the proper format")
            pawn_chain_capture_coordinates = board.move_pawn(player_pawn[player_pawn_choice],
                                                             available_coordinates[player_coordinate_choice - 1])
            if len(pawn_chain_capture_coordinates) > 0:
                print(board)
                proper_input = False
                # TODO: Add a while loop here to take care of wrong user input
                curr_moves = board.total_moves
                while not proper_input:
                    try:
                        board.total_moves = curr_moves
                        chain_capture = int(input(
                            "You captured a pawn and now the capture can be chained!!\nDo you want to proceed?\n Select "
                            "1.Yes 2.No\n"))
                        if chain_capture == 1:
                            board.total_moves -= 1
                            print(pawn_chain_capture_coordinates)
                            chain_capture_coordinate_choice = int(
                                input("Select the position of Coordinate to move, for eg: 1 or 2 or 3 or 4\n"))
                            if len(pawn_chain_capture_coordinates) >= chain_capture_coordinate_choice > 0:
                                proper_input = True
                                board.move_pawn(player_pawn[player_pawn_choice],
                                                pawn_chain_capture_coordinates[chain_capture_coordinate_choice - 1])
                    except (KeyboardInterrupt, SystemExit) as e:
                        sys.exit(0)
                    except:
                        print("Enter Input in the proper format")

    # If selected player's Control is MCTS AI
    def player_MCTS_AI(self, game_bot, board):
        nodes_processed = game_bot.tree_node_processed
        node = Node(board, depth=0, choose_method=puct)
        res = game_bot.mcts(node, num_rollouts=100)
        if res is not None:
            index, parent_state = res
            node = parent_state.children()[index]
        print(f"Nodes processed this turn {game_bot.tree_node_processed - nodes_processed}")
        return node

    # If selected player's Control is BaseLine AI
    def player_BaseLine_AI(self, game_bot, board):
        nodes_processed = game_bot.tree_node_processed
        node = Node(board, depth=0)
        node = game_bot.base_line_AI(node)
        nodes_processed_this_turn = game_bot.tree_node_processed - nodes_processed
        print(f"nodes_processed_this_turn {nodes_processed_this_turn}")
        return node

    # If selected player's Control is NN+MCTS AI
    def player_NN_MCTS_AI(self, game_bot, board):
        nodes_processed = game_bot.tree_node_processed
        node = Node(board, depth=0, choose_method=nn_puct)
        res = game_bot.mcts(node, num_rollouts=100)
        if res is not None:
            index, parent_state = res
            node = parent_state.children()[index]
        print(f"Nodes processed this turn {game_bot.tree_node_processed - nodes_processed}")
        return node

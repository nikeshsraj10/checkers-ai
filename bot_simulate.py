'''
This module handles the code for the game bot
MCTS
'''
import argparse
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
from board import Board
import math
from bot import Node
from bot import Bot

def check_num_of_games(val):
    try:
        val = int(val)
        if(val < 0): 
            return 100
        return val
    except:
        return 100

def accept_board_config(val):
    try:
        val = int(val)
        if(val == 8 or val == 10 or val == 6): 
            return val
        return 8
    except:
        return 8
# type = lambda x : x if (x == 8 or x == 10) else 8
def main():
    parser = argparse.ArgumentParser(description="Enter the size of board and number of games you want to simulate")
    parser.add_argument('board_config', default = 8, type = accept_board_config)
    parser.add_argument('num_of_games', default = 100, type = check_num_of_games)
    args = parser.parse_args()
    board_config = args.board_config
    num_of_games = args.num_of_games
    print(f"Board config selected:{board_config}\nNumber of games to be played: {num_of_games}")
    state = Board(board_config)
    node = Node(state)
    moves = -1
    nodes_processed = 0
    games = 0
    moves_list = []
    scores = []
    nodes_processed_list_MCTS = []
    while games < num_of_games:
        state = Board(board_config)
        obstacles = state.set_obstacles(3)
        print(f"Obstacles added at {obstacles}")
        node = Node(state)
        games += 1
        moves = -1
        bot = Bot()
        bot2 = Bot()
        while not state.check_game_status():
            moves += 1
            print(f"Game #: {games}/{num_of_games}\nMove #: {moves}")
            if moves % 2 == 0:
                print(node.state)
                print(f"Moves since last capture: {state.moves_since_last_capture}")
                print("AI's turn")
                nodes_processed = bot.tree_node_processed
                node = bot.mcts(node)
                nodes_processed_this_turn = bot.tree_node_processed - nodes_processed
                print(f"nodes_processed_this_turn {nodes_processed_this_turn}")
                if node is None:
                    break
            else:
                print(node.state)
                print(f"Moves since last capture: {node.state.moves_since_last_capture}")
                print("Baseline AI turn")
                nodes_processed = bot2.tree_node_processed
                node = bot2.base_line_AI(node)
                nodes_processed_this_turn = bot.tree_node_processed - nodes_processed
                print(f"nodes_processed_this_turn {nodes_processed_this_turn}")
                if node is None:
                    break
            state = node.state
        print(f"Total moves: {moves}")
        score = state.compute_score()
        if(len(state.p1_pawns) > len(state.p2_pawns)):
            print("MCTS AI Won")
            print(f"Score = {score}")
        elif len(state.p1_pawns) < len(state.p2_pawns):
            print("BASELINE AI Won")
            print(f"Score = {score * -1}")
        else: 
            print("It's a draw")
            print(f"Score = {score}")
        print(f"total nodes processed = {bot.tree_node_processed + bot2.tree_node_processed}")
        moves_list.append(moves)
        scores.append(score)
        nodes_processed_list_MCTS.append(bot.tree_node_processed)
    with open(f"plots/Simulated_{board_config}x{board_config}_{num_of_games}.txt", 'w') as f:
        f.write(f"Moves List: {moves_list}\nScores List: {scores}\nNodes Processed List MCTS: {nodes_processed_list_MCTS}")
    print(moves_list)
    print(scores)
    print(nodes_processed_list_MCTS)
    generatePlots(nodes_processed_list_MCTS, "Range of Nodes processed", "Number of games", "Nodes processed for MCTS", f"plots/NodesprocessedMCTS_{board_config}_{num_of_games}")


def generatePlots(nodes_processed, x_label, y_label, title, file_name):
    n_bins = 10
    # Creating histogram
    fig, axs = plt.subplots(1, 1,
                            figsize=(10, 7),
                            tight_layout=True)

    # Remove axes splines
    for s in ['top', 'bottom', 'left', 'right']:
        axs.spines[s].set_visible(False)

    # Remove x, y ticks
    axs.xaxis.set_ticks_position('none')
    axs.yaxis.set_ticks_position('none')

    # Add padding between axes and labels
    axs.xaxis.set_tick_params(pad=5)
    axs.yaxis.set_tick_params(pad=10)

    # Add x, y gridlines
    axs.grid(b=True, color='grey',
            linestyle='-.', linewidth=0.5,
            alpha=0.6)

    # Creating histogram
    N, bins, patches = axs.hist(nodes_processed, bins=n_bins)

    # Setting color
    fracs = ((N ** (1 / 5)) / N.max())
    norm = colors.Normalize(fracs.min(), fracs.max())

    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)

    # Adding extra features

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)

    # Show plot
    plt.savefig(file_name)
    
if __name__ == "__main__":
    main()
    

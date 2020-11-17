'''
This module handles the code for the game bot
MCTS
'''
from copy import deepcopy
import numpy as np
from board import Board
import math


class Node():
    def __init__(self, state):
        self.state = state
        self.visit_count = 0
        self.score_total = 0
        self.score_estimate = 0
        self.nodes_processed = 0
        self.child_list = None  # lazy child generation

    def children(self):
        if self.child_list is None:
            self.child_list = self.get_actions()
        return self.child_list

    # This method returns the valid states of the board   
    def get_actions(self):
        states = []
        if self.state.total_moves % 2 == 0:
            for pawn in self.state.check_available_pawns_to_move(True):
                valid_moves = self.state.get_moves(self.state.p1_pawns[pawn])
                for move in valid_moves:
                    temp_board = deepcopy(self.state)
                    temp_board.move_pawn(temp_board.p1_pawns[pawn], move)
                    self.nodes_processed += 1
                    states.append(Node(temp_board))
        else:
            for pawn in self.state.check_available_pawns_to_move(False):
                valid_moves = self.state.get_moves(self.state.p2_pawns[pawn])
                for move in valid_moves:
                    temp_board = deepcopy(self.state)
                    temp_board.move_pawn(temp_board.p2_pawns[pawn], move)
                    self.nodes_processed += 1
                    states.append(Node(temp_board))

        return states

    def choose_child(self):
        children = self.children()
        try:
            c = np.random.randint(len(children))
        except Exception as e:
            return None
        return children[c]

    def compute_uct(self, Q, Np, Nc):
        return Q + math.sqrt((math.log(Np + 1)) / (Nc + 1))

    def __str__(self):
        return f"Node Details\n{self.state}\n {self.visit_count} \t {self.score_estimate}\n"

    def __repr__(self):
        return str(self)


class Bot:
    def __init__(self):
        self.tree_node_processed = 0

    def rollout(self, node, count):
        child = node.choose_child()
        if node.state.check_game_status() or count > 100 or child is None:
            # TODO: Consider King pawn for the score calculation
            result = node.state.compute_score()
        else:
            result = self.rollout(child, count + 1)
        node.visit_count += 1
        node.score_total += result
        node.score_estimate = node.score_total / node.visit_count
        return result

    def mcts(self, node):
        rollout_calls = 0
        tree_node_processed = 0
        for rollout_counter in range(25):
            self.rollout(node, rollout_calls + 1)
            rollout_calls = 0
        children = node.children()
        if len(children) == 0:
            return None
        max_index = 0
        if len(children) > 0:
            max_score = float('-inf')
            for counter in range(len(children)):
                score = node.compute_uct(children[counter].score_estimate, node.visit_count,
                                         children[counter].visit_count)
                tree_node_processed += children[counter].nodes_processed
                # print(score)
                if score > max_score:
                    max_score = score
                    max_index = counter
        self.tree_node_processed += tree_node_processed
        return children[max_index]

    def base_line_AI(self, node):
        rollout_calls = 0
        tree_node_processed = 0
        for rollout_counter in range(20):
            self.rollout(node, rollout_calls + 1)
            rollout_calls = 0
        children = node.children()
        for child in children:
            tree_node_processed += child.nodes_processed
        if len(children) == 0:
            return None
        a = np.random.randint(len(children))
        self.tree_node_processed += tree_node_processed
        return children[a]


if __name__ == "__main__":
    child = None
    state = Board(8)
    node = Node(state)
    moves = -1
    nodes_processed = 0
    games = 0
    moves_list = []
    scores = []
    nodes_processed_list_MCTS = []
    nodes_processed_list_baseline = []
    while games < 1:
        state = Board(8)
        node = Node(state)
        games += 1
        moves = -1
        bot = Bot()
        bot2 = Bot()
        while not state.check_game_status():
            moves += 1
            print(f"Game #: {games}\nMove #: {moves}")
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
        nodes_processed_list_baseline.append(bot2.tree_node_processed)
    with open('plots/SingleGameData.txt', 'w') as f:
        f.write(f"Moves List: {moves_list}\nScores List: {scores}\nNodes Processed List MCTS: {nodes_processed_list_MCTS}\nNodes Processed List Baseline: {nodes_processed_list_baseline}")
    print(moves_list)
    print(scores)
    print(nodes_processed_list_MCTS)
    print(nodes_processed_list_baseline)
    # print(child.state

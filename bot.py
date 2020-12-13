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

    def get_score_estimates(self):
        score_estimates = np.zeros(len(self.child_list))
        for index in range(len(self.child_list)):
            if self.child_list[index].visit_count != 0:
                score_estimates[index] = self.child_list[index].score_total / self.child_list[index].visit_count
            if self.state.total_moves % 2 != 0:
                score_estimates[index] *= -1
        return score_estimates

    def get_visit_counts(self):
        visit_counts = np.zeros(len(self.child_list))
        for index in range(len(self.child_list)):
            visit_counts[index] = self.child_list[index].visit_count
        return visit_counts
    
    def get_nodes_processed(self):
        nodes_processed = 0
        for index in range(len(self.child_list)):
            nodes_processed += self.child_list[index].nodes_processed
        return nodes_processed

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
        return puct(self)

    def __str__(self):
        return f"Node Details\n{self.state}\n {self.visit_count} \t {self.score_estimate}\n"

    def __repr__(self):
        return str(self)

def compute_uct(Q, Np, Nc):
        return Q + math.sqrt((math.log(Np + 1)) / (Nc + 1))

def puct(node):
    children = node.children()
    try:
        c = np.random.choice(len(children), p=puct_probs(node))
    except:
        return None
    return node.children()[c]

def puct_probs(node):
    uct_values = []
    n_p = node.visit_count
    visit_counts = node.get_visit_counts()
    score_estimates = node.get_score_estimates()
    for index in range(len(visit_counts)):
        nc = visit_counts[index]
        qc = score_estimates[index]
        uct = compute_uct(qc, n_p, nc)
        uct_values.append(uct)
    # Compute Softmax of all the uct values
    exp = np.exp(np.array(uct_values))
    probs = exp / exp.sum()
    return probs

class Bot:
    def __init__(self):
        self.tree_node_processed = 0

    def rollout(self, node, count, max_depth):
        child = node.choose_child()
        if node.state.check_game_status() or count > max_depth or child is None:
            # TODO: Consider King pawn for the score calculation
            result = node.state.compute_score()
        else:
            result = self.rollout(child, count + 1, max_depth)
        node.visit_count += 1
        node.score_total += result
        node.score_estimate = node.score_total / node.visit_count
        return result

    def mcts(self, node, num_rollouts = 25):
        rollout_calls = 0
        tree_node_processed = 0
        for rollout_counter in range(num_rollouts):
            self.rollout(node, rollout_calls + 1, max_depth = 100)
            rollout_calls = 0
        children = node.children()
        if len(children) == 0:
            return None
        max_index = 0
        self.tree_node_processed += node.get_nodes_processed()
        # self.tree_node_processed = node.get_nodes_processed()
        max = np.argmax(node.get_score_estimates())
        return children[max]

    def base_line_AI(self, node):
        children = node.children()
        c = np.random.choice(len(children))
        return children[c]


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

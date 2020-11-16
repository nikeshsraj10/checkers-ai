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
        self.child_list = None # lazy child generation
    
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
                # print(f"Valid Moves are {valid_moves}")
                for move in valid_moves:
                    temp_board =  deepcopy(self.state)
                    temp_board.move_pawn(self.state.p1_pawns[pawn], move)
                    # print(temp_board)
                    # print(temp_board.total_moves)
                    states.append(Node(temp_board))
        else:
            for pawn in self.state.check_available_pawns_to_move(False):
                valid_moves = self.state.get_moves(self.state.p2_pawns[pawn])
                # print(f"Valid Moves are {valid_moves}")
                for move in valid_moves:
                    temp_board =  deepcopy(self.state)
                    temp_board.move_pawn(self.state.p2_pawns[pawn], move)
                    # print(temp_board.total_moves)
                    # print(temp_board)
                    states.append(Node(temp_board))

        return states
    
    def choose_child(self):
        # c = neuralnet(encode(self.state))
        children = self.children()
        # if len(children) > 0:
        #     max_score = float('-inf')
        #     max_index = 0
        #     for counter in range(len(children)):
        #         print(f"children[counter].score_estimate, self.visit_count, children[counter].visit_count {children[counter].score_estimate}, {self.score_estimate}, {children[counter].visit_count}")
        #         score = self.compute_uct(children[counter].score_estimate, self.visit_count, children[counter].visit_count)
        #         print(score)
        #         if score > max_score:
        #             max_score = score
        #             max_index = counter
        #     return children[max_index]
        # else:
        #     return None
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

def rollout(node, count):
    child = node.choose_child()
    if node.state.check_game_status() or count > 15 or child is None:
        # TODO: Consider King pawn for the score calculation
        result = len(node.state.p1_pawns) - len(node.state.p2_pawns)
    else: result = rollout(child, count + 1)
    node.visit_count += 1
    node.score_total += result
    node.score_estimate = node.score_total / node.visit_count
    return result

def mcts(node):
    rollout_calls = 0
    for rollout_counter in range(10): 
        # print(f"MCTS LOOP {rollout_counter}")
        rollout(node, rollout_calls + 1)
        rollout_calls = 0
    children = node.children()
    if len(children) == 0:
        return None
    for child in children:
        print(child.visit_count)
    # a = np.argmax([
    #     child.score_estimate
    #     for child in children
    #     ])
    max_index = 0
    if len(children) > 0:
        max_score = float('-inf')
        for counter in range(len(children)):
            # print(f"children[counter].score_estimate, self.visit_count, children[counter].visit_count {children[counter].score_estimate}, {self.score_estimate}, {children[counter].visit_count}")
            score = node.compute_uct(children[counter].score_estimate, node.visit_count, children[counter].visit_count)
            print(score)
            if score > max_score:
                max_score = score
                max_index = counter
    return children[max_index]


if __name__ == "__main__":
    state = Board(8)
    child = None
    for _ in range(250):
        # print(f"outer loop {_}")
        if _ % 2 == 0:
            print(state)
            print(f"Moves since last capture: {state.moves_since_last_capture}")
            print("AI's turn")
            # if child is None:
            #     node = Node(state)
            # else:
            #     node = child
            node = Node(state)
            child = mcts(node)
            if child == None:
                break
        else:
            print(child.state)
            print("Players turn")
            state = child.state
            pawns = state.check_available_pawns_to_move(False)
            if len(pawns) == 0:
                break
            pawn = pawns[np.random.randint(len(pawns))]
            print(f"Pawn selected by player is {pawn}")
            moves = state.get_moves(state.p2_pawns[pawn])
            print(f"Moves available for player is {moves}")
            state.move_pawn(state.p2_pawns[pawn], moves[np.random.randint(len(moves))])
    print(len(state.p2_pawns))
    print(len(state.p1_pawns))
    # print(child.state)
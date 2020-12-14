import itertools as it
import board as bg
import bot
import torch as tr

def generate(board_size=8, num_games=2, num_rollouts=10, max_depth=4, num_of_pawns = 12):

    data = []    
    for game in range(num_games):
    
        state = bg.Board(numOfSquares = board_size, num_of_pawns = num_of_pawns)
        obstacles = state.set_obstacles(3)
        print(f"Obstacles added at {obstacles}")
        game_bot = bot.Bot()
        no_moves = 0
        for turn in it.count():
            print(f"Game:{game} of {num_games}, Turn:{turn}...")
            print(f"\n{state}\n")
            # Stop when game is over
            if state.check_game_status(): break            
            # Otherwise, use MCTS
            res = game_bot.mcts(bot.Node(state, choose_method = state.choose_method), num_rollouts = num_rollouts, max_depth = max_depth, choose_method = bot.puct)
            if res is not None:
                no_moves = 0
                a, node = res
                state = node.children()[a].state
            else:
                no_moves += 1
            if no_moves == 40:
                break
            # Add child states and their values to the data
            Q = node.get_score_estimates()
            for c,child in enumerate(node.children()):
                data.append((child.state, Q[c]))

    return data

def encode(state):
    encoded_state = tr.zeros(6, *state.board.shape)
    rows, cols = state.board.shape
    for row in range(rows):
        for col in range(cols):
            if state.board[row, col] == 0:
                encoded_state[0, row, col] = 1
            elif state.board[row, col] == bg.OBSTACLE:
                encoded_state[1, row, col] = 1
            elif state.board[row, col] in state.p1_pawns and not state.p1_pawns[state.board[row, col]].is_king:
                encoded_state[2, row, col] = 1
            elif state.board[row, col] in state.p1_pawns and state.p1_pawns[state.board[row, col]].is_king:
                encoded_state[3, row, col] = 1
            elif state.board[row, col] in state.p2_pawns and not state.p2_pawns[state.board[row, col]].is_king:
                encoded_state[4, row, col] = 1
            elif state.board[row, col] in state.p2_pawns and state.p2_pawns[state.board[row, col]].is_king:
                encoded_state[5, row, col] = 1
    return encoded_state

def get_batch(board_size=6, num_games=2, num_rollouts=100, max_depth=6, choose_method=None, num_of_pawns = 6):
    training_data = generate(board_size=board_size, num_games=num_games, num_rollouts=num_rollouts, max_depth=max_depth, num_of_pawns = num_of_pawns)
    inputs = None
    scores = []
    for state, score_estimate in training_data:
        encoded_state = encode(state)
        encoded_state = tr.reshape(encoded_state, (1, *tuple(encoded_state.shape)))
        scores.append(score_estimate)
        if inputs is not None:
            inputs = tr.cat([inputs, encoded_state])
        else:
            inputs = encoded_state
    outputs = tr.FloatTensor(scores).reshape(len(scores), 1)
    return (inputs, outputs)

if __name__ == "__main__":
    
    board_size, num_games = 8, 50
    if board_size == 8:
        num_of_pawns = 12
    elif board_size == 10:
        num_of_pawns = 20
    elif board_size == 6:
        num_of_pawns = 6

    try:
        inputs, outputs = get_batch(board_size, num_games=num_games, num_of_pawns = num_of_pawns)
    except Exception as e:
        print(e)
    print(inputs[-1])
    print(outputs[-1])

    import pickle as pk
    from pathlib import Path
    path = Path('~/../data/')
    with open(path/f"data{board_size}_{num_of_pawns}_{num_games}.pkl", "wb") as f: pk.dump((inputs, outputs), f)


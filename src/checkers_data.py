import itertools as it
import board as bg
import bot
import torch as tr

def generate(board_size=6, num_games=2, num_rollouts=10, max_depth=4):

    data = []    
    for game in range(num_games):
    
        state = bg.Board(numOfSquares = board_size)
        for turn in it.count():
            print("game %d, turn %d..." % (game, turn))
    
            # Stop when game is over
            if state.check_game_status(): break            
            # Otherwise, use MCTS
            a, node = bot.Bot().mcts(bot.Node(state), num_rollouts, max_depth)
            state = node.children()[a].state
            
            # Add child states and their values to the data
            Q = node.get_score_estimates()
            for c,child in enumerate(node.children()):
                data.append((child.state, Q[c]))

    return data

def encode(state):
    encoded_state = tr.zeros(5, *state.board.shape)
    rows, cols = state.board.shape
    for row in range(rows):
        for col in range(cols):
            if state.board[row, col] == 0:
                encoded_state[0, row, col] = 1
            elif state.board[row, col] in state.p1_pawns and not state.p1_pawns[state.board[row, col]].is_king:
                encoded_state[1, row, col] = 1
            elif state.board[row, col] in state.p1_pawns and state.p1_pawns[state.board[row, col]].is_king:
                encoded_state[2, row, col] = 1
            elif state.board[row, col] in state.p2_pawns and not state.p2_pawns[state.board[row, col]].is_king:
                encoded_state[3, row, col] = 1
            elif state.board[row, col] in state.p2_pawns and state.p2_pawns[state.board[row, col]].is_king:
                encoded_state[4, row, col] = 1
    return encoded_state

def get_batch(board_size=6, num_games=2, num_rollouts=50, max_depth=6, choose_method=None):
    training_data = generate(board_size=board_size, num_games=num_games, num_rollouts=num_rollouts, max_depth=max_depth)
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
        inputs, outputs = get_batch(board_size, num_games=num_games)
    except Exception as e:
        print(e)
    print(inputs[-1])
    print(outputs[-1])

    import pickle as pk
    from pathlib import Path
    path = Path('~/../data/')
    with open(path/f"data{board_size}_{num_of_pawns}_{num_games}.pkl", "wb") as f: pk.dump((inputs, outputs), f)


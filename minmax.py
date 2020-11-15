from copy import deepcopy

def minimax(board, depth, max_player):
    if depth == 0 or board.declare_winner() != 0:
        return board.evaluate(), board

    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(board, True):
            evaluation = minimax(move, depth - 1, False)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move

        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(board, False):
            evaluation = minimax(move, depth - 1, True)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move

        return minEval, best_move


def simulate_move(board, pawn,coordinate):
    board.move_pawn(pawn,coordinate)
    return board

#p1 turn when true
def get_all_moves(board, player_turn, game):
    moves = []

    for pawn in board.check_available_pawns_to_move(player_turn):
        valid_moves = board.get_moves(pawn)
        for move in valid_moves:
            temp_board = deepcopy(board)
            new_board = simulate_move(temp_board,pawn, move)
            moves.append(new_board)

    return moves

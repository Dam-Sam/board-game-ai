
import argparse
import copy
import sys
import time

cache = {} # you can use this to implement state caching
directions = {'r': [(-1, -1), (-1, 1)],
                  'b': [(1, 1), (1, -1)],
                  'R': [(1, -1), (1, 1), (-1, -1), (-1, 1)],
                  'B': [(1, -1), (1, 1), (-1, -1), (-1, 1)]}

class State:
    # This class is used to represent a state.
    # board : a list of lists that represents the 8*8 board
    def __init__(self, board):
        self.board = board
        self.width = 8
        self.height = 8

    def display(self):
        for i in self.board:
            for j in i:
                print(j, end="")
            print("")
        print("")

def get_opp_char(player):
    if player in ['b', 'B']:
        return ['r', 'R']
    else:
        return ['b', 'B']

def get_next_turn(curr_turn):
    if curr_turn == 'r':
        return 'b'
    else:
        return 'r'

def get_MinMax(player):
    if player =='b':
        return "MAX"
    else:
        return "MIN"
    
def is_within_bounds(x, y):
    """Check if the coordinates are within the board boundaries."""
    return 0 <= x < 8 and 0 <= y < 8

def generate_successors(state, player):
    """
    Generate all valid successors for the current player.
    Includes both simple moves and jumps.
    """
    successors = []

    opp_pieces = get_opp_char(player)

    def get_simple_moves(x, y, piece):
        """Generate all simple (non-capturing) moves for a given piece."""
        simple_moves = []
        for dx, dy in directions[piece]:
            nx, ny = x + dx, y + dy
            if is_within_bounds(nx, ny) and state.board[nx][ny] == '.':
                new_board = copy.deepcopy(state.board)
                new_board[nx][ny] = piece
                new_board[x][y] = '.'
                
                if piece == 'r' and nx == 0:
                    new_board[nx][ny] = 'R'
                elif piece == 'b' and nx == 7:
                    new_board[nx][ny] = 'B'
                
                simple_moves.append(State(new_board))

        return simple_moves

    def get_jump_moves(x, y, piece, board, jumps=[]):
        """Recursively generate all possible jump moves from a given piece."""
        jump_moves = []

        for dx, dy in directions[piece]:
            nx, ny = x + dx, y + dy
            jx, jy = x + 2*dx, y + 2*dy

            if (is_within_bounds(jx, jy) and 
                board[nx][ny] in opp_pieces and board[jx][jy] == '.'):

                new_board = copy.deepcopy(board)
                new_board[jx][jy] = piece
                new_board[x][y] = '.'
                new_board[nx][ny] = '.'

                if piece == 'r' and jx == 0:
                    new_board[jx][jy] = 'R'
                elif piece == 'b' and jx == 7:
                    new_board[jx][jy] = 'B'
                
                next_jumps = get_jump_moves(jx, jy, piece, new_board, jumps + [(jx, jy)])

                if next_jumps:
                    jump_moves.extend(next_jumps)

                else:
                    jump_moves.append(State(new_board))

        return jump_moves

    jump_moves = []
    for i in range(state.height):
        for j in range(state.width):
            piece = state.board[i][j]
            if piece.lower() == player:
                jump_moves.extend(get_jump_moves(i, j, piece, state.board))

    if jump_moves:
        return jump_moves

    for i in range(state.height):
        for j in range(state.width):
            piece = state.board[i][j]
            if piece.lower() == player:
                successors.extend(get_simple_moves(i, j, piece))

    return successors

def check_winner(state):
    """
    Determines if the game has reached a terminal state.
    
    Returns:
    'r' : if red wins
    'b' : if black wins
    '': if not terminal
    """
    red_pieces = 0
    black_pieces = 0
    
    for row in state.board:
        for piece in row:
            if piece == 'r' or piece == 'R':
                red_pieces += 1
            elif piece == 'b' or piece == 'B':
                black_pieces += 1

    if red_pieces == 0:
        return 'b'
    elif black_pieces == 0:
        return 'r'
    
    red_moves = any(generate_successors(state, 'r'))
    black_moves = any(generate_successors(state, 'b'))
    
    if not red_moves:
        return 'b'
    elif not black_moves:
        return 'r'
    
    return ''


def evaluate(state, depth, max_depth):
    """Evaluates Non-Terminal States"""
    red_score = 0
    black_score = 0

    piece_weight = 1
    king_weight = 2
    
    for row in state.board:
        for piece in row:
            if piece == 'r':
                red_score += piece_weight
            elif piece == 'R':
                red_score += king_weight
            elif piece == 'b':
                black_score += piece_weight
            elif piece == 'B':
                black_score += king_weight

    score = red_score - black_score
    
    return score

def utility(winner, depth):
    """Computes the utility value for a terminal state in the game."""
    
    WIN_VALUE = 1000000000000
    LOSS_VALUE = -1000000000000

    if winner == 'r':
        return WIN_VALUE - depth
    else:
        return LOSS_VALUE + depth


def minimax(state, depth, alpha, beta, maximizing_player, max_depth):
    """
    Minimax algorithm with alpha-beta pruning. Explores the game tree depth-first.
    """
    winner = check_winner(state)

    if winner:
        return utility(winner, depth)
    elif depth == max_depth:
        return evaluate(state, depth, max_depth)

    if maximizing_player:
        max_eval = float('-inf')
        for child in generate_successors(state, 'r'):
            eval = minimax(child, depth + 1, alpha, beta, False, max_depth)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for child in generate_successors(state, 'b'):
            eval = minimax(child, depth + 1, alpha, beta, True, max_depth)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def find_best_move(state, turn, max_depth):
    """
    Finds the best move for current player using the minimax algorithm with alpha-beta pruning.
    """
    best_move = None
    best_value = float('-inf')
    alpha = float('-inf')
    beta = float('inf')

    for move in generate_successors(state, turn):
        move_value = minimax(move, 1, alpha, beta, False, max_depth)
        
        if move_value > best_value:
            best_value = move_value
            best_move = move
        
        alpha = max(alpha, best_value)
    
    return best_move

def start_game(state, turn, max_depth):
    game = [state]
    winner = ''

    while not winner:
        state = find_best_move(state, turn, max_depth)

        game.append(state)
        winner = check_winner(state)
        turn = get_next_turn(turn)

    return game

def read_from_file(filename):

    f = open(filename)
    lines = f.readlines()
    board = [[str(x) for x in l.rstrip()] for l in lines]
    f.close()

    return board


def generate_output(game, outputfile):

    with open(outputfile, 'w') as sys.stdout:
        
        for state in game:
            state.display()

    return None

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzles."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that contains the solution."
    )
    args = parser.parse_args()

    initial_board = read_from_file(args.inputfile)
    state = State(initial_board)
    turn = 'r'

    max_depth = 10
    
    game = start_game(state, turn, max_depth)
    generate_output(game, args.outputfile)

    #sys.stdout = open(args.outputfile, 'w')
    # Example usage:
    # Write successors for the initial state
    #successors = generate_successors(state, turn)
    #for succ in successors:
    #    succ.display()

import heapq
import argparse
import sys

#====================================================================================

char_single = '2'

class Piece:
    """
    This represents a piece on the Hua Rong Dao puzzle.
    """

    def __init__(self, is_2_by_2, is_single, coord_x, coord_y, orientation):
        """
        :param is_2_by_2: True if the piece is a 2x2 piece and False otherwise.
        :type is_2_by_2: bool
        :param is_single: True if this piece is a 1x1 piece and False otherwise.
        :type is_single: bool
        :param coord_x: The x coordinate of the top left corner of the piece.
        :type coord_x: int
        :param coord_y: The y coordinate of the top left corner of the piece.
        :type coord_y: int
        :param orientation: The orientation of the piece (one of 'h' or 'v') 
            if the piece is a 1x2 piece. Otherwise, this is None
        :type orientation: str
        """

        self.is_2_by_2 = is_2_by_2
        self.is_single = is_single
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.orientation = orientation

    def set_coords(self, coord_x, coord_y):
        """
        Move the piece to the new coordinates. 

        :param coord: The new coordinates after moving.
        :type coord: int
        """

        self.coord_x = coord_x
        self.coord_y = coord_y

    def is_within_board(self, new_x, new_y, board_width, board_height):
        """
        Checks if the postion the piece wants to move is within the board
        """
        board_width = board_width - 1
        board_height = board_height - 1

        if board_width < new_x or 0 > new_x or 0 > new_y or board_height < new_y:
            return False
        
        if self.is_2_by_2:
            if 0 <= new_x + 1 <= board_width and 0 <= new_y + 1 <= board_height:
                return True
            
        elif self.is_single:
            return True
        
        elif self.orientation == 'h':
            if new_x + 1 <= board_width:
                return True
        elif self.orientation == 'v':
            if new_y + 1 <= board_height:
                return True

        return False
    
    def __repr__(self):
        return '{} {} {} {} {}'.format(self.is_2_by_2, self.is_single, \
            self.coord_x, self.coord_y, self.orientation)


class Board:
    """
    Board class for setting up the playing board.
    """

    def __init__(self, height, pieces):
        """
        :param pieces: The list of Pieces
        :type pieces: List[Piece]
        """

        self.width = 4
        self.height = height
        self.pieces = pieces

        # self.grid is a 2-d (size * size) array automatically generated
        # using the information on the pieces when a board is being created.
        # A grid contains the symbol for representing the pieces on the board.
        self.grid = []
        self.__construct_grid()

        self.blanks = []

    def is_occupied(self, new_x, new_y, moving_piece:Piece):
        """
        Check if the target position is occupied by any piece other than the one currently moving.
        """
        moving_piece_cords = create_set_of_coords(moving_piece, new_x, new_y)

        for piece in self.pieces:
            if piece == moving_piece:
                continue
            
            piece_cords = create_set_of_coords(piece, piece.coord_x, piece.coord_y)

            if not moving_piece_cords.isdisjoint(piece_cords):
                return True

        return False
    
    # customized eq for object comparison.
    def __eq__(self, other):
        if isinstance(other, Board):
            return self.grid == other.grid
        return False


    def __construct_grid(self):
        """
        Called in __init__ to set up a 2-d grid based on the piece location information.

        """

        for i in range(self.height):
            line = []
            for j in range(self.width):
                line.append('.')
            self.grid.append(line)

        for piece in self.pieces:
            if piece.is_2_by_2:
                self.grid[piece.coord_y][piece.coord_x] = '1'
                self.grid[piece.coord_y][piece.coord_x + 1] = '1'
                self.grid[piece.coord_y + 1][piece.coord_x] = '1'
                self.grid[piece.coord_y + 1][piece.coord_x + 1] = '1'
            elif piece.is_single:
                self.grid[piece.coord_y][piece.coord_x] = char_single
            else:
                if piece.orientation == 'h':
                    self.grid[piece.coord_y][piece.coord_x] = '<'
                    self.grid[piece.coord_y][piece.coord_x + 1] = '>'
                elif piece.orientation == 'v':
                    self.grid[piece.coord_y][piece.coord_x] = '^'
                    self.grid[piece.coord_y + 1][piece.coord_x] = 'v'
      
    def display(self):
        """
        Print out the current board.

        """
        for i, line in enumerate(self.grid):
            for ch in line:
                print(ch, end='')
            print()
    
    def to_string(self):
        """
        Returns the current board as one string.
        """
        str_board = ""
        for i, line in enumerate(self.grid):
            for ch in line:
                str_board = str_board + ch

        return str_board
        

class State:
    """
    State class wrapping a Board with some extra current state information.
    Note that State and Board are different. Board has the locations of the pieces. 
    State has a Board and some extra information that is relevant to the search: 
    heuristic function, f value, current depth and parent.
    """

    def __lt__(self, other):
        return self.f < other.f

    def __init__(self, board, hfn, f, depth, parent=None):
        """
        :param board: The board of the state.
        :type board: Board
        :param hfn: The heuristic function.
        :type hfn: Optional[Heuristic]
        :param f: The f value of current state.
        :type f: int
        :param depth: The depth of current state in the search tree.
        :type depth: int
        :param parent: The parent of current state.
        :type parent: Optional[State]
        """
        self.board = board
        self.hfn = hfn
        self.f = f
        self.depth = depth
        self.parent = parent


def read_from_file(filename):
    """
    Load initial board from a given file.

    :param filename: The name of the given file.
    :type filename: str
    :return: A loaded board
    :rtype: Board
    """

    puzzle_file = open(filename, "r")

    line_index = 0
    pieces = []
    final_pieces = []
    final = False
    found_2by2 = False
    finalfound_2by2 = False
    height_ = 0

    for line in puzzle_file:
        height_ += 1
        if line == '\n':
            if not final:
                height_ = 0
                final = True
                line_index = 0
            continue
        if not final: #initial board
            for x, ch in enumerate(line):
                if ch == '^': # found vertical piece
                    pieces.append(Piece(False, False, x, line_index, 'v'))
                elif ch == '<': # found horizontal piece
                    pieces.append(Piece(False, False, x, line_index, 'h'))
                elif ch == char_single:
                    pieces.append(Piece(False, True, x, line_index, None))
                elif ch == '1':
                    if found_2by2 == False:
                        pieces.append(Piece(True, False, x, line_index, None))
                        found_2by2 = True
        else: #goal board
            for x, ch in enumerate(line):
                if ch == '^': # found vertical piece
                    final_pieces.append(Piece(False, False, x, line_index, 'v'))
                elif ch == '<': # found horizontal piece
                    final_pieces.append(Piece(False, False, x, line_index, 'h'))
                elif ch == char_single:
                    final_pieces.append(Piece(False, True, x, line_index, None))
                elif ch == '1':
                    if finalfound_2by2 == False:
                        final_pieces.append(Piece(True, False, x, line_index, None))
                        finalfound_2by2 = True
        line_index += 1
        
    puzzle_file.close()
    board = Board(height_, pieces)
    goal_board = Board(height_, final_pieces)
    return board, goal_board


def create_set_of_coords(piece:Piece, coord_x, coord_y):
    piece_cords = set([(coord_x, coord_y)])
        
    if piece.is_2_by_2:
        piece_cords.update([(coord_x + 1, coord_y), (coord_x, coord_y + 1), (coord_x +  1, coord_y + 1)])
    
    elif piece.orientation == 'h':
        piece_cords.update([(coord_x + 1, coord_y)])
    elif piece.orientation == 'v':
        piece_cords.update([(coord_x, coord_y + 1)])

    return piece_cords


def grid_to_string(grid):
    string = ""
    for i, line in enumerate(grid):
        for ch in line:
            string += ch
        string += "\n"
    return string

def is_goal_state(current_board:Board, goal_board:Board):
    """
    Takes the current state of the board and returns TRUE if it matches the goal state of the baord.
    """
    if current_board.__eq__(goal_board):
        return True
    
    return False

def dfs_generate_successors(current_state:State):
    successor_states = []
    current_board = current_state.board

    width, height = current_board.width, current_board.height

    for piece in current_board.pieces:
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dx, dy in directions:
            new_x = piece.coord_x + dx
            new_y = piece.coord_y + dy

            if piece.is_within_board(new_x, new_y, width, height):

                if not current_board.is_occupied(new_x, new_y, piece):
                    new_pieces = [p for p in current_board.pieces]
                    new_piece = Piece(piece.is_2_by_2, piece.is_single, new_x, new_y, piece.orientation)
                    new_pieces[current_board.pieces.index(piece)] = new_piece

                    new_board = Board(current_board.height, new_pieces)
                    successor_states.append(State(new_board, None, None, 1, current_state))

    return successor_states


def DFSearch(initial_state, goal_state):
    frontier = [initial_state]
    explored = set()

    while frontier:
        curr_state = frontier.pop()
        
        str_board = curr_state.board.to_string()
        if str_board not in explored:
            explored.add(str_board)

            if curr_state.board.__eq__(goal_state.board):
                return curr_state
        
            frontier =  frontier + dfs_generate_successors(curr_state)

    return None


def generate_output(state:State, outputfile):
    results = []

    while state.parent != None:
        results.append(state.board)

        state = state.parent

        if state.parent == None:
            results.append(state.board)


    with open(outputfile, 'w') as sys.stdout:
        
        for board in results[::-1]:
            board.display()
            print("")

    return None

"""
/////A* Functions///// 
"""
def cost_function(parent_state:State):
    cost = 0

    return cost

def manhanttan_distance(current_board:Board, goal_board:Board):
    total_distance = 0

    for current_piece, goal_piece in zip(current_board.pieces, goal_board.pieces):
        current_x, current_y = current_piece.coord_x, current_piece.coord_y       
        goal_x, goal_y = goal_piece.coord_x, goal_piece.coord_y
        
        distance = abs(current_x - goal_x) + abs(current_y - goal_y)
        
        total_distance += distance

    return total_distance


def a_star_generate_successors(current_state:State, goal_state:State):
    successor_states = []
    current_board = current_state.board

    width, height = current_board.width, current_board.height

    for piece in current_board.pieces:
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dx, dy in directions:
            new_x = piece.coord_x + dx
            new_y = piece.coord_y + dy

            if piece.is_within_board(new_x, new_y, width, height):

                if not current_board.is_occupied(new_x, new_y, piece):
                    new_pieces = [p for p in current_board.pieces]
                    new_piece = Piece(piece.is_2_by_2, piece.is_single, new_x, new_y, piece.orientation)
                    new_pieces[current_board.pieces.index(piece)] = new_piece

                    #current_board.display()

                    new_board = Board(current_board.height, new_pieces)
                    #new_board.display()

                    h = manhanttan_distance(new_board, goal_state.board)
                    g = current_state.depth + 1

                    new_state = State(new_board, None, h + g, g, current_state)
                    successor_states.append(new_state)

    return successor_states


def AStarsearch(initial_state, goal_state):
    frontier = []
    heapq.heapify(frontier)
    heapq.heappush(frontier, initial_state)

    explored = set()

    while frontier:
        curr_state = heapq.heappop(frontier)
        
        if curr_state.board.__eq__(goal_state.board):
            return curr_state
        
        str_board = curr_state.board.to_string()
        
        if str_board not in explored:
            explored.add(str_board)
        
            for successor in a_star_generate_successors(curr_state, goal_state):
                heapq.heappush(frontier, successor)
                #print(successor.f)

    return None


if __name__ == "__main__":

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
    parser.add_argument(
        "--algo",
        type=str,
        required=True,
        choices=['astar', 'dfs'],
        help="The searching algorithm."
    )
    args = parser.parse_args()

    # read the board from the file
    board, goal_board = read_from_file(args.inputfile)

    newState = State(board, None, 0, 0, None)
    goalState = State(goal_board, None, 0, 0, None)

    if args.algo == 'astar':
        result_state = AStarsearch(newState, goalState)

    elif args.algo == 'dfs':
        result_state = DFSearch(newState, goalState)

    generate_output(result_state, args.outputfile)



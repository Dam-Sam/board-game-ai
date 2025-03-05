from csp import Constraint, Variable, CSP
from constraints import *
from backtracking import bt_search, soln_to_dict
import sys
import argparse

def print_solution(s, size):
  s_ = {}
  for (var, val) in s:
    s_[int(var.name())] = val
  for i in range(1, size-1):
    for j in range(1, size-1):
      print(s_[(i*size+j)],end="")
    print('')

def populate_ships(soln, size):
    board = soln_to_dict(soln, size)

    for i in range(1, size-1):
        for j in range(1, size-1):
            if (i < (size - 5) and board[i*size+j] == "S" and board[(i+1)*size+j] == "S" and board[(i+2)*size+j] == "S" and board[(i+3)*size+j] == "S" and board[(i+4)*size+j] == "S"):
                board[i*size+j] = "^"
                board[(i+1)*size+j] = "M"
                board[(i+2)*size+j] = "M"
                board[(i+3)*size+j] = "M"
                board[(i+4)*size+j] = "v"
            elif (i < (size - 4) and board[i*size+j] == "S" and board[(i+1)*size+j] == "S" and board[(i+2)*size+j] == "S" and board[(i+3)*size+j] == "S"):
                board[i*size+j] = "^"
                board[((i+1)*size+j)] = "M"
                board[((i+2)*size+j)] = "M"
                board[((i+3)*size+j)] = "v"
            elif (i < (size - 3) and board[i*size+j] == "S" and board[(i+1)*size+j] == "S" and board[(i+2)*size+j] == "S"):
                board[(i*size+j)] = "^"
                board[((i+1)*size+j)]= "M"
                board[((i+2)*size+j)] = "v"
            elif (i < (size - 2) and board[i*size+j] == "S" and board[(i+1)*size+j] == "S"):
                board[(i*size+j)] = "^"
                board[((i+1)*size+j)] = "v"

            if (j < (size - 5) and board[i*size+j] == "S" and board[i*size+j+1] == "S" and board[i*size+j+2] == "S" and board[i*size+j+3] == "S" and board[i*size+j+4] == "S"):
                board[i*size+j] = "<"
                board[i*size+j+1] ="M"
                board[i*size+j+2] ="M"
                board[i*size+j+3] ="M"
                board[i*size+j+4] =">"
            elif (j < (size - 4) and board[i*size+j] == "S" and board[i*size+j+1] == "S" and board[i*size+j+2] == "S" and board[i*size+j+3] == "S"):
                board[i*size+j] = "<"
                board[i*size+j+1] ="M"
                board[i*size+j+2] ="M"
                board[i*size+j+3] =">"
            elif (j < (size - 3) and board[i*size+j] == "S" and board[i*size+j+1] == "S" and board[i*size+j+2] == "S"):
                board[i*size+j] = "<"
                board[(i*size+j+1)] = "M"
                board[(i*size+j+2)] = ">"
            elif (j < (size - 2) and board[i*size+j] == "S" and board[i*size+j+1] == "S"):
                board[i*size+j] = "<"
                board[i*size+j+1] = ">"

    return board

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
file = open(args.inputfile, 'r')
b = file.read()
b2 = b.split()
size = len(b2[0])
size = size + 2
b3 = []
b3 += ['0' + b2[0] + '0']
b3 += ['0' + b2[1] + '0']
b3 += [b2[2] + ('0' if len(b2[2]) == 3 else '')]
b3 += ['0' * size]
for i in range(3, len(b2)):
  b3 += ['0' + b2[i] + '0']
b3 += ['0' * size]
board = "\n".join(b3)

varlist = []
varn = {}
conslist = []
ship_constraints = b2[2]
original_board = board.split()[3:]

#1/0 variables
for i in range(0,size):
  for j in range(0, size):
    v = None
    if i == 0 or i == size-1 or j == 0 or j == size-1:
      v = Variable(str(-1-(i*size+j)), [0])
    else:
      v = Variable(str(-1-(i*size+j)), [0,1])
    varlist.append(v)
    varn[str(-1-(i*size+j))] = v

#make 1/0 variables match board info
ii = 0
for i in board.split()[3:]:
  jj = 0
  for j in i:
    if j != '0' and j != '.':
      conslist.append(TableConstraint('boolean_match', [varn[str(-1-(ii*size+jj))]], [[1]]))
    elif j == '.':
      conslist.append(TableConstraint('boolean_match', [varn[str(-1-(ii*size+jj))]], [[0]]))
    jj += 1
  ii += 1

#row and column constraints on 1/0 variables
row_constraint = []
for i in board.split()[0]:
  row_constraint += [int(i)]

for row in range(0,size):
  conslist.append(NValuesConstraint('row', [varn[str(-1-(row*size+col))] for col in range(0,size)], [1], row_constraint[row], row_constraint[row]))

col_constraint = []
for i in board.split()[1]:
  col_constraint += [int(i)]

for col in range(0,size):
  conslist.append(NValuesConstraint('col', [varn[str(-1-(col+row*size))] for row in range(0,size)], [1], col_constraint[col], col_constraint[col]))

#diagonal constraints on 1/0 variables
for i in range(1, size-1):
    for j in range(1, size-1):
      for k in range(9):
        conslist.append(NValuesConstraint('diag', [varn[str(-1-(i*size+j))], varn[str(-1-((i-1)*size+(j-1)))]], [1], 0, 1))
        conslist.append(NValuesConstraint('diag', [varn[str(-1-(i*size+j))], varn[str(-1-((i-1)*size+(j+1)))]], [1], 0, 1))

#./S/</>/v/^/M variables
#these would be added to the csp as well, before searching,
#along with other constraints
for i in range(0, size):
 for j in range(0, size):
   v = Variable(str(i*size+j), ['.', 'S'])
   varlist.append(v)
   varn[str(str(i*size+j))] = v
    #connect 1/0 variables to W/S/L/R/B/T/M variables
   conslist.append(TableConstraint('connect', [varn[str(-1-(i*size+j))], varn[str(i*size+j)]], [[0,'.'],[1,'S']]))

#find all solutions and check which one has right ship #'s
csp = CSP('battleship', varlist, conslist)
solutions, num_nodes = bt_search('GAC', csp, 'mrv', False, False, ship_constraints, original_board, size)
board = populate_ships(solutions[0], size)

sys.stdout = open(args.outputfile, 'w')
for i in range(1, size-1):
    for j in range(1, size-1):
        print(board[(i*size+j)],end="")
    print('')


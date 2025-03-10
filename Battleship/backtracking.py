from csp import Constraint, Variable, CSP
from constraints import *
import random

class UnassignedVars:
    '''class for holding the unassigned variables of a CSP. We can extract
       from, re-initialize it, and return variables to it.  Object is
       initialized by passing a select_criteria (to determine the
       order variables are extracted) and the CSP object.

       select_criteria = ['random', 'fixed', 'mrv'] with
       'random' == select a random unassigned variable
       'fixed'  == follow the ordering of the CSP variables (i.e.,
                   csp.variables()[0] before csp.variables()[1]
       'mrv'    == select the variable with minimum values in its current domain
                   break ties by the ordering in the CSP variables.
    '''
    def __init__(self, select_criteria, csp):
        if select_criteria not in ['random', 'fixed', 'mrv']:
            pass #print "Error UnassignedVars given an illegal selection criteria {}. Must be one of 'random', 'stack', 'queue', or 'mrv'".format(select_criteria)
        self.unassigned = list(csp.variables())
        self.csp = csp
        self._select = select_criteria
        if select_criteria == 'fixed':
            #reverse unassigned list so that we can add and extract from the back
            self.unassigned.reverse()

    def extract(self):
        if not self.unassigned:
            pass #print "Warning, extracting from empty unassigned list"
            return None
        if self._select == 'random':
            i = random.randint(0,len(self.unassigned)-1)
            nxtvar = self.unassigned[i]
            self.unassigned[i] = self.unassigned[-1]
            self.unassigned.pop()
            return nxtvar
        if self._select == 'fixed':
            return self.unassigned.pop()
        if self._select == 'mrv':
            nxtvar = min(self.unassigned, key=lambda v: v.curDomainSize())
            self.unassigned.remove(nxtvar)
            return nxtvar

    def empty(self):
        return len(self.unassigned) == 0

    def insert(self, var):
        if not var in self.csp.variables():
            pass #print "Error, trying to insert variable {} in unassigned that is not in the CSP problem".format(var.name())
        else:
            self.unassigned.append(var)

def bt_search(algo, csp, variableHeuristic, allSolutions, trace, ship_constraints, original_board, size):
    '''Main interface routine for calling different forms of backtracking search
       algorithm is one of ['BT', 'FC', 'GAC']
       csp is a CSP object specifying the csp problem to solve
       variableHeuristic is one of ['random', 'fixed', 'mrv']
       allSolutions True or False. True means we want to find all solutions.
       trace True of False. True means turn on tracing of the algorithm

       bt_search returns a list of solutions. Each solution is itself a list
       of pairs (var, value). Where var is a Variable object, and value is
       a value from its domain.
    '''
    varHeuristics = ['random', 'fixed', 'mrv']
    algorithms = ['BT', 'FC', 'GAC']

    #statistics
    bt_search.nodesExplored = 0

    if variableHeuristic not in varHeuristics:
        pass #print "Error. Unknown variable heursitics {}. Must be one of {}.".format(
            #variableHeuristic, varHeuristics)
    if algo not in algorithms:
        pass #print "Error. Unknown algorithm heursitics {}. Must be one of {}.".format(
            #algo, algorithms)

    uv = UnassignedVars(variableHeuristic,csp)
    Variable.clearUndoDict()
    for v in csp.variables():
        v.reset()
    if algo == 'BT':
         solutions = BT(uv, csp, allSolutions, trace)
    elif algo == 'FC':
        for cnstr in csp.constraints():
            if cnstr.arity() == 1:
                FCCheck(cnstr, None, None)  #FC with unary constraints at the root
        solutions = FC(uv, csp, allSolutions, trace)
    elif algo == 'GAC':
        GacEnforce(csp.constraints(), csp, None, None) #GAC at the root
        solutions = GAC(uv, csp, allSolutions, trace, size, ship_constraints, original_board)

    return solutions, bt_search.nodesExplored

def BT(unAssignedVars, csp, allSolutions, trace):
    '''Backtracking Search. unAssignedVars is the current set of
       unassigned variables.  csp is the csp problem, allSolutions is
       True if you want all solutionss trace if you want some tracing
       of variable assignments tried and constraints failed. Returns
       the set of solutions found.

      To handle finding 'allSolutions', at every stage we collect
      up the solutions returned by the recursive  calls, and
      then return a list of all of them.

      If we are only looking for one solution we stop trying
      further values of the variable currently being tried as
      soon as one of the recursive calls returns some solutions.
    '''
    if unAssignedVars.empty():
        if trace: pass #print "{} Solution Found".format(csp.name())
        soln = []
        for v in csp.variables():
            soln.append((v, v.getValue()))
        return [soln]  #each call returns a list of solutions found
    bt_search.nodesExplored += 1
    solns = []         #so far we have no solutions recursive calls
    nxtvar = unAssignedVars.extract()
    if trace: pass #print "==>Trying {}".format(nxtvar.name())
    for val in nxtvar.domain():
        if trace: pass #print "==> {} = {}".format(nxtvar.name(), val)
        nxtvar.setValue(val)
        constraintsOK = True
        for cnstr in csp.constraintsOf(nxtvar):
            if cnstr.numUnassigned() == 0:
                if not cnstr.check():
                    constraintsOK = False
                    if trace: pass #print "<==falsified constraint\n"
                    break
        if constraintsOK:
            new_solns = BT(unAssignedVars, csp, allSolutions, trace)
            if new_solns:
                solns.extend(new_solns)
            if len(solns) > 0 and not allSolutions:
                break  #don't bother with other values of nxtvar
                       #as we found a soln.
    nxtvar.unAssign()
    unAssignedVars.insert(nxtvar)
    return solns

def GAC(unAssignedVars, csp, allSolutions, trace, size, ship_constraints, original_board):
    '''
    '''
    if unAssignedVars.empty():

        if trace: pass 

        soln = []

        for v in csp.variables():
            soln.append((v, v.getValue()))
        return [soln]

    bt_search.nodesExplored += 1
    solns = [] 
    nxtvar = unAssignedVars.extract()

    if trace: pass 

    for val in nxtvar.curDomain():
        if trace: pass 
        nxtvar.setValue(val)
        noDWO = True

        if GacEnforce(csp.constraintsOf(nxtvar), csp, nxtvar, val) == "DWO":
            noDWO = False

        if noDWO:
            new_solns = GAC(unAssignedVars, csp, allSolutions, trace, size, ship_constraints, original_board)
            if new_solns:
                board = soln_to_dict(new_solns[0], size)
                if(check_ship_constraints(board, size, ship_constraints)):
                    if valid_solution(original_board, board, size):
                        solns.extend(new_solns)
                        if len(solns) > 0:
                            break

        nxtvar.restoreValues(nxtvar,val)

    nxtvar.unAssign()
    unAssignedVars.insert(nxtvar)
    return solns

def GacEnforce(cnstrs, csp, assignedvar, assignedval):
    while len(cnstrs) != 0:
        cnstr = cnstrs.pop()

        for var in cnstr.scope():

            for val in var.curDomain():
                
                if not cnstr.hasSupport(var,val):
                    var.pruneValue(val,assignedvar,assignedval)

                    if var.curDomainSize() == 0:
                        return "DWO"

                    for recheck in csp.constraintsOf(var):

                        if recheck != cnstr and recheck not in cnstrs:
                            cnstrs.append(recheck)
    return "OK"

def soln_to_dict(soln, size):
    board = {}
    for (var, val) in soln:
        board[int(var.name())] = val
    
    return board

def check_ship_constraints(board, size, ship_constraints):
    five = 0
    four = 0
    three = 0
    two = 0
    one = 0

    for i in range(1, size-1):
        for j in range(1, size-1):
            if (i < (size - 5) and board[i*size+j] == "S" and board[(i+1)*size+j] == "S" and board[(i+2)*size+j] == "S" and board[(i+3)*size+j] == "S" and board[(i+4)*size+j] == "S"):
                board[i*size+j] = "^"
                board[(i+1)*size+j] = "M"
                board[(i+2)*size+j] = "M"
                board[(i+3)*size+j] = "M"
                board[(i+4)*size+j] = "v"
                five += 1
            elif (i < (size - 4) and board[i*size+j] == "S" and board[(i+1)*size+j] == "S" and board[(i+2)*size+j] == "S" and board[(i+3)*size+j] == "S"):
                board[i*size+j] = "^"
                board[((i+1)*size+j)] = "M"
                board[((i+2)*size+j)] = "M"
                board[((i+3)*size+j)] = "v"
                four += 1
            elif (i < (size - 3) and board[i*size+j] == "S" and board[(i+1)*size+j] == "S" and board[(i+2)*size+j] == "S"):
                board[(i*size+j)] = "^"
                board[((i+1)*size+j)]= "M"
                board[((i+2)*size+j)] = "v"
                three += 1
            elif (i < (size - 2) and board[i*size+j] == "S" and board[(i+1)*size+j] == "S"):
                board[(i*size+j)] = "^"
                board[((i+1)*size+j)] = "v"
                two += 1

            if (j < (size - 5) and board[i*size+j] == "S" and board[i*size+j+1] == "S" and board[i*size+j+2] == "S" and board[i*size+j+3] == "S" and board[i*size+j+4] == "S"):
                board[i*size+j] = "<"
                board[i*size+j+1] ="M"
                board[i*size+j+2] ="M"
                board[i*size+j+3] ="M"
                board[i*size+j+4] =">"
                five += 1
            elif (j < (size - 4) and board[i*size+j] == "S" and board[i*size+j+1] == "S" and board[i*size+j+2] == "S" and board[i*size+j+3] == "S"):
                board[i*size+j] = "<"
                board[i*size+j+1] ="M"
                board[i*size+j+2] ="M"
                board[i*size+j+3] =">"
                four += 1
            elif (j < (size - 3) and board[i*size+j] == "S" and board[i*size+j+1] == "S" and board[i*size+j+2] == "S"):
                board[i*size+j] = "<"
                board[(i*size+j+1)] = "M"
                board[(i*size+j+2)] = ">"
                three += 1
            elif (j < (size - 2) and board[i*size+j] == "S" and board[i*size+j+1] == "S"):
                board[i*size+j] = "<"
                board[i*size+j+1] = ">"
                two += 1
            
    for i in range(1, size-1):
        for j in range(1, size-1):
            if board[i*size+j] == "S":
                one += 1
    
    if one == int(ship_constraints[0]) and two == int(ship_constraints[1]) and three == int(ship_constraints[2]) and four == int(ship_constraints[3]) and five == int(ship_constraints[4]):
        return True

    return False


def valid_solution(original_board, board, size):

    for i in range(1, size-1):
        for j in range(1, size-1):
            soln_val = board[(i*size+j)]
            og_val = original_board[i][j]

            if og_val!= "0" and soln_val != og_val:
                return False
    return True
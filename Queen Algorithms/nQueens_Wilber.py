import random
import eel
import time

class Position: #class object used for the LCV implementation
    def __init__(self, qr, qc, value):
        self.column = qc
        self.row = qr 
        self.value = value
    def __str__(self):
        print(f"row = {self.row} \n column = {self.column} \n available spaces {self.value}")

#function to check whether two queens are attacking each other
def queenAttack(x_1, y_1, x_2, y_2):
    if x_1 == x_2:
        return True
    elif y_1 == y_2:
        return True
    elif abs(x_1 - x_2) == abs(y_1 - y_2):
        return True
    return False
#generates an initial state with one queen placement
def initial_state(n):
    row = random.randint(0, n-1)
    column = random.randint(0, n-1)
    board = [None] * n
    board[column] = row
    return board, column

@eel.expose
def numQueensAttack(arr):
    #finds the number of queens that are attacking each other
    h = 0
    for i in range(len(arr)): #uses the first queen in the order to compare with other queens
        if arr[i] == None: continue
        qR = arr[i]
        qC = i+1
        for j in range(len(arr)):
            if arr[j] == None: continue
            if i == j: continue
            oR, oC = arr[j], j+1
            if queenAttack(qR, qC, oR, oC):
               h = h + 1
    return h


def is_Complete(assignment):
    #check if every variable in assignment has a value
    assigned_columns = 0
    for i in assignment:
        if i != None:
            assigned_columns += 1
    if assigned_columns != len(assignment):
        return False

    if numQueensAttack(assignment) == 0:
        return True
    return False   

#MCV
def get_legal_moves(a, index, n):
    assignment = a.copy()
    num_of_legal = 0
    for i in range(n):
        assignment[index] = i
        if numQueensAttack(assignment) == 0:
            num_of_legal += 1
    return num_of_legal

#The following function assumes that the queen position it is receiving does not attack any other queen
#LCV Function, based on a given queen position -> checks the remaining columns for amount of legal queen placements
def get_legal_placements(assignment, row, column, vars): 
    n = len(assignment)
    assignment_copy = assignment.copy()
    assignment_copy[column] = row
    count = 0
    for c in vars:
        if c == column: continue #if the column being accessed is the one currently being indexed skip
        for i in range(n):
            assignment_copy[c] = i #assign a queen to the remaining columns
            if numQueensAttack(assignment_copy) == 0: count += 1 # if the assigned queen does not result in any queens attacking each other, it is a possible placement
            assignment_copy[c] = None

    return count

def most_contrained_value(assignment, vars, n):
    values = {}
    for i in vars:
        values.update({i: get_legal_moves(assignment, i, n)}) #vars[i] is the unassigned index we are trying to get the legal positions for
    
    max = float('inf')
    max_index = -1
    for key, value in values.items():
        if value <  max:
            max = value
            max_index = key
    
    return max_index

#heuristic function for least contrained values, will return the queen placement that leaves the most available queen spaces in the remaining column
def least_constrained_values(a, column, vars):
    assignment = a.copy()
    domain = [] #list to hold the LCV queen positions

    n = len(a)

    for row in range(n):
        assignment[column] = row
        #here we will check if the above queen position is violating any contraints (attacking any queen)
        if numQueensAttack(assignment) > 0: 
            assignment[column] = None
            continue
        legal_placements = get_legal_placements(assignment, row, column, vars)
        domain.append(Position(row, column, legal_placements))

    sorted_domain = sorted(domain, key=lambda placement: placement.value, reverse=True)


    return sorted_domain

@eel.expose
def backtracking_search(N):
    start = time.time()
    board, startingC = initial_state(N)
    unassigned = [startingC]
    for i in range(N):
        if i == startingC: continue 
        unassigned.append(i)
    return recursive_backtracking(board, unassigned, N), (time.time() - start)
@eel.expose
def recursive_backtracking(assignment, unassigned, N):
    if is_Complete(assignment):
        return assignment
    column = most_contrained_value(assignment, unassigned, N)
    for position in least_constrained_values(assignment, column, unassigned):
        assignment[column] = position.row
        unassigned.remove(column)
        result = recursive_backtracking(assignment, unassigned, N)
        if result != False:
            return result
        unassigned.append(column)
        assignment[column] = None
    return False

def get_num_attacking(c, column):
    current = c.copy()
    current[column] = None
    return numQueensAttack(c) - numQueensAttack(current)

def get_most_conflicted_column(current):
    n = len(current)
    most_conflicts = -1
    most_conflicted_column = -1
    for i in range(n):
        conflicts = get_num_attacking(current, i)
        if conflicts > most_conflicts:
            most_conflicts = conflicts
            most_conflicted_column = i
    return most_conflicted_column

def get_least_conflicting_queen(current, column):
    best = current.copy()
    c = current.copy()
    n = len(current)
    best[column] = None
    least = numQueensAttack(current)
    least_index = None
    for i in range(n):
        c[column] = i
        value = numQueensAttack(c) - numQueensAttack(best)
        if value < least:
            least = value
            least_index = i
    return least_index
    
def initial_state2(n):
    arr = []
    for i in range(n):
        arr.append(random.randint(0, n-1))
    return arr


def min_conflicts(N, max_restarts = 10):
    max_steps = 20000
    current = initial_state2(N)
    restarts = 0
    while restarts <= max_restarts:
        for i in range(max_steps):
            if numQueensAttack(current) == 0: return current
            conflicted_column = get_most_conflicted_column(current)
            var = get_least_conflicting_queen(current, conflicted_column)
            current[conflicted_column] = var
        restarts+= 1
    return False


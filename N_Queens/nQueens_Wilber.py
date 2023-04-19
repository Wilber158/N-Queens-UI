def queenAttack(x_1, y_1, x_2, y_2):
    if x_1 == x_2:
        return True
    elif y_1 == y_2:
        return True
    elif abs(x_1 - x_2) == abs(y_1 - y_2):
        return True
    return False

def numQueensAttack(arr):
    #finds the number of queens that are attacking each other
    h = 0
    for i in range(len(arr)): #uses the first queen in the order to compare with other queens
        qR = arr[i]
        qC = i+1
        for j in range(len(arr)):
            if i == j: continue
            oR, oC = arr[j], j+1
            if queenAttack(qR, qC, oR, oC):
               h = h + 1
    return h

def is_Complete(assignment):
    if numQueensAttack(assignment) == 0:
        return True
    return False   


def get_legal_column(assigment, index, n):
    num_of_legal = 0
    for i in range(n):
        assigment[index] = i
        if numQueensAttack(assigment) == 0:
            num_of_legal += 1
    return num_of_legal



def most_contrained_value(assignment):
    values = []
    for i in range(len(assignment)):
        






def backtracking_search(N):
    arr = [None] * N
    return recursive_backtracking(arr)

def recursive_backtracking(asssignment):
    if is_Complete(asssignment):
        return asssignment
    column = most_contrained_value(asssignment)


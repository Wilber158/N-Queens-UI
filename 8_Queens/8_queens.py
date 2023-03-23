import random
import math
import time

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


def initial_state(n):
    arr = []
    for i in range(n):
        arr.append(random.randint(0, n))
    return arr


def getNext(arr):
    #makes a random move on a certain column given a state
    nextArr = arr.copy()
    n = len(arr)
    nextC = random.randint(1, n)
    nextR = random.randint(0, n-1)
    nextArr[nextR] = nextC
    return nextArr

def decision(probability):
    return random.random() < probability

def debug_simulated_Annealing(initial):
    t0, k, alpha = 10000, 0, 0.85
    tk = t0
    current = initial
    for i in range(100000000):
        #simulating annealing (temperature change)
        tk = t0 * pow(alpha, k)
        print(f"Temp: {tk}")
        k = k + 1
        if(tk == 0):
            return current
        next = getNext(current)
        nextH = numQueensAttack(next)
        currentH = numQueensAttack(current)
        e = nextH - currentH
        print(f"change of E = {e}")
        if e < 0:
            current = next
        else:
            prob = math.exp(-(e/tk))
            print(f"Probability: {prob}")
            if(decision(prob)):
                current = next
        if currentH == 0: return current
        print(f"Current h: {currentH}")
    return current

def simulated_Annealing(initial):
    t0, k, alpha = 10000, 0, 0.85
    tk = t0
    current = initial
    for i in range(100000000):
        #simulating annealing (temperature change) using Exponential multiplicative cooling
        tk = t0 * pow(alpha, k)
        k = k + 1
    
        #checks if temperature is 0
        if(tk == 0):
            return current

        #gets the number of queens being attacked of current node and next node
        next = getNext(current)
        nextH = numQueensAttack(next)
        currentH = numQueensAttack(current)
        
        #gets the change in h for both nodes
        e = nextH - currentH
        #global minimum e < 0
        if e < 0:
            current = next
        else:
            #getting probabilty of exploring
            prob = math.exp(-(e/tk))
            if(decision(prob)):
                current = next
        #if true we have found the goal state
        if currentH == 0: return current

    return current


def main():
   start = time.monotonic()
   arr = initial_state(8)
   arr = simulated_Annealing(arr)
   end = time.monotonic()
   print(f"Elapsed time: {end - start}")
   print(arr)
   


main()
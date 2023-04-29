import random
import math
import time
import eel
import json


#function that checks whether two queens are attacking each other
def queenAttack(x_1, y_1, x_2, y_2):
    if x_1 == x_2:
        return True
    elif y_1 == y_2:
        return True
    elif abs(x_1 - x_2) == abs(y_1 - y_2):
        return True
    return False

#function that checks given a state represented by an array, the amount of queens who are attacking each other
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

@eel.expose
def isGoalState(arr):
    if numQueensAttack(arr) == 0:
        return True
    return False

#generates an initial random full state, given n 
def initial_state(n):
    arr = []
    for i in range(n):
        arr.append(random.randint(0, n))
    return arr


#
def getNext(arr):
    #makes a random move on a certain column given a state
    nextArr = arr.copy()
    n = len(arr)
    nextC = random.randint(0, n-1)
    nextR = random.randint(0, n-1)
    nextArr[nextR] = nextC
    return nextArr

#function to find the probabilities of exploring
def decision(probability):
    return random.random() < probability

#debug function used to visualize the process of the simulating annealing algorithm
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
        print(f"Current h: {currentH}")
    return current

#a simulating annealing algorithm that takes an initial state AND starting temperature
def simulated_Annealing2(initial, t0):
    k, alpha = 0, 0.85
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

#simulated annealing function that takes initial temperature
def simulated_Annealing(t0):
    k, alpha = 0, 0.85
    tk = t0
    current = initial_state(8)
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
        if currentH == 0: return current, 1

    return current, 0


#function that is used to display the board in the GUI used
@eel.expose()#exposing function to the javascript side
def animated_annealing(t0, initial=None):
    k, alpha = 0, 0.85
    tk = 0
    if initial:
        current = initial
    else:
        current = initial_state(8)

    for i in range(10000000000000):
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
        eel.display_Board(current)#calling 
        eel.sleep(.001)
        #if true we have found the goal state
        if currentH == 0: return current

    return current


def simulate(temp, runs):
    successful_runs = 0
    for i in range(runs):
        goalState, success = simulated_Annealing(temp)
        eel.display_Board(goalState)
        eel.sleep(.1)
        if success == 1:
            successful_runs += 1
    return successful_runs

#below we will use the class objects to calculate success rate based on certain temperatures
class success:
    def __init__(self, temp, success):
        self.temp = temp
        self.success = success


def get_success_rate():
    arr = []
    for i in range(100, 1000, 100):
        state, s = simulated_Annealing(i)
        print(state)
        if s == 0:
            obj = success(i, 0)
            arr.append(obj)
        else:
            obj = success(i, 1)
            arr.append(obj)

    for i in arr:
        print(f"Temp: {i.temp} Success: {i.success}")
    return arr


@eel.expose
def eight_queens(n, temp):
    state = initial_state(n)
    goal_state = simulated_Annealing(state, temp)
    return goal_state

def main():
    get_success_rate()

if __name__ == "__main___":
    main()
        


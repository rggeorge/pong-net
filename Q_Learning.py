import Maze
import threading
import time
import random as rand
import numpy as np
import matplotlib.pyplot as plt
import xlwt


discount = 0.4
actions = Maze.actions
book=xlwt.Workbook(encoding="utf-8")
sheet1=book.add_sheet("Sheet 1")
def Q_Reset():    
    states = []    
    Q = {}
    for i in range(Maze.x):
        for j in range(Maze.y):
            states.append((i, j))
    
    for state in states:
        temp = {}
        for action in actions:
            temp[action] = rand.random()
            #temp[action]=1
        Q[state] = temp
    
    for (i, j, c, w) in Maze.specials:
        for action in actions:
            Q[(i, j)][action] = w
    return Q
    
def do_action(action):
    s = Maze.Position
    r = -Maze.score
    if action == actions[0]:
        Maze.try_move(0, -1)
    elif action == actions[1]:
        Maze.try_move(0, 1)
    elif action == actions[2]:
        Maze.try_move(-1, 0)
    elif action == actions[3]:
        Maze.try_move(1, 0)
    else:
        return
    s2 = Maze.Position
    r += Maze.score
    return s, action, r, s2


def max_Q(s,Q):
    val = None
    act = None
    for a, q in Q[s].items():
        if val is None or (q > val):
            val = q
            act = a
    return act, val


def inc_Q(s, a, alpha, inc,Q):
    Q[s][a] *= 1 - alpha
    Q[s][a] += alpha * inc



def run():
    global discount
    time.sleep(1)
    alpha = 1
    t = 1
    MaxGames=130
    Iterations=10
    for i in range (Iterations):
        Q=Q_Reset()
        GameNum=0
        while GameNum<MaxGames:
            # Pick the right action
            
            s = Maze.Position
            max_act, max_val = max_Q(s,Q)
            (s, a, r, s2) = do_action(max_act)
    
            # Update Q
            max_act, max_val = max_Q(s2,Q)
            inc_Q(s, a, alpha, r + discount * max_val,Q)
    
            # Check if the game has restarted
            t += 1.0
    
            if Maze.has_restarted() or Maze.numMove>100000:
                GameNum+=1
                sheet1.write(GameNum,i,Maze.numMove,)
                Maze.restart_game()
                time.sleep(0.01)
                t = 1.0
    
            # Update the learning rate
            alpha = pow(t, -.05)
    
            # MODIFY THIS SLEEP IF THE GAME IS GOING TOO FAST.
            #time.sleep(0.1)
            
            if GameNum==MaxGames-1:
                book.save("MazeMoves.xls")
    
            
            
    
           
    
t = threading.Thread(target=run)
t.daemon = True
t.start()
Maze.start_game()
    

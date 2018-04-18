import Maze
import threading
import time
import random as rand
import numpy as np
import matplotlib.pyplot as plt
import xlwt
from keras.models import Sequential
from keras.layers import Dense


discount = 0.3
actions = Maze.actions
states = []

model=Sequential()
model.add(Dense(units=100,input_dim=3*Maze.Xgrid*Maze.Ygrid,activation='relu'))
model.add(Dense(units=50,activation='relu'))
model.add(Dense(units=4,activation='sigmoid'))
model.compile(loss='binary_crossentropy',optimizer='rmsprop')


        


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



def run():
    global discount 
    time.sleep(1)
    alpha = 1
    t = 1
    book=xlwt.Workbook(encoding="utf-8")
    sheet1=book.add_sheet("Sheet 1")
    GameNum=0
    MaxGames=100
    
    GridWall=np.zeros((Maze.Xgrid,Maze.Ygrid))
    for i in range(len(Maze.walls)):
        GridWall[Maze.walls[i][0],Maze.walls[i][1]]=1
    GridWall=np.reshape(GridWall,(Maze.Xgrid*Maze.Ygrid,1))
    
    GridGoal=np.zeros((Maze.Xgrid,Maze.Ygrid))
    for i in range(len(Maze.specials)):
        GridGoal[Maze.specials[i][0],Maze.specials[i][1]]=1
    GridGoal=np.reshape(GridGoal,(Maze.Xgrid*Maze.Ygrid,1)) 
    
    while GameNum<MaxGames:
        # Pick the right action
        GridPos=np.zeros((Maze.Xgrid,Maze.Ygrid))
        GridPos[Maze.Position[0],Maze.Position[1]]=1
        GridPos=np.reshape(GridPos,(Maze.Xgrid*Maze.Ygrid,1))
        State=[GridPos,GridGoal,GridWall]
        State=np.reshape(State,(3*Maze.Xgrid*Maze.Ygrid,1))
        s = Maze.Position
        Q=model.predict(x=State)
        max_act=np.argmax(Q)
        max_val =np.max(Q)
        (s, a, r, s2) = do_action(max_act)

        # Update Q
        GridPosNew=np.zeros((Maze.Xgrid,Maze.Ygrid))
        GridPosNew[s2[0],s2[1]]=1
        GridPosNew=np.reshape(GridPosNew,(Maze.Xgrid*Maze.Ygrid,1))
        StateNew=[GridPosNew,GridGoal,GridWall]
        StateNew=np.reshape(StateNew,(3*Maze.Xgrid*Maze.Ygrid,1))
        
        QNew=model.predict(x=StateNew)
        max_actNew=np.argmax(QNew)
        max_valNew =np.max(QNew)
        
        Target=Q
        Target[max_act]=Q[max_act]+alpha*(r + discount * max_valNew)
        model.fit(x=State,y=Target,batch_size=None,epochs=1)

        # Check if the game has restarted
        t += 1.0
        if Maze.has_restarted():
            GameNum+=1
            sheet1.write(GameNum,0,Maze.numMove,)
            Maze.restart_game()
            time.sleep(0.01)
            t = 1.0

        # Update the learning rate
        alpha = pow(t, -.1)

        # MODIFY THIS SLEEP IF THE GAME IS GOING TOO FAST.
        #time.sleep(0.1)
        
        if GameNum==MaxGames-1:
            book.save("MazeMoves.xls")
        
        
        

       

t = threading.Thread(target=run)
t.daemon = True
t.start()
Maze.start_game()



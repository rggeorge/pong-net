import Maze
import threading
import time
import numpy as np
import xlwt
import ReadImage


discount = 0.3
actions = Maze.actions
states = []
LR=.01
N1=50
N2=20
N3=4

W1=np.random.rand(3*ReadImage.m*ReadImage.n,N1)#//(3*ReadImage.m*ReadImage.n)
W2=np.random.rand(N1,N2)#//(3*ReadImage.m*ReadImage.n)
W3=np.random.rand(N2,N3)#//(3*ReadImage.m*ReadImage.n)

def sigmoid(x):
    return 1/(1+np.exp(-x))

def Network(X):
    global W1,W2, W3
    H1=np.matmul(np.transpose(W1),X)
    H1=sigmoid(H1)
    
    H2=np.matmul(np.transpose(W2),H1)
    H2=sigmoid(H2)
    
    Yhat=np.matmul(np.transpose(W3),H2)
    Yhat=sigmoid(Yhat)
    return Yhat
        
def NetworkFit(X,Y,epochs):
    global W1,W2,W3
    for i in range(epochs): 

        H1=np.matmul(np.transpose(W1),X)
        H1=sigmoid(H1)
        
        H2=np.matmul(np.transpose(W2),H1)
        H2=sigmoid(H2)
        
        Yhat=np.matmul(np.transpose(W3),H2)
        Yhat=sigmoid(Yhat)
        
        D3=Yhat-Y
        D2=np.multiply(np.matmul(W3,D3),np.multiply(H2,(1-H2)))
        D1=np.multiply(np.matmul(W2,D2),np.multiply(H1,(1-H1)))
        
        W3=W3-np.matmul(np.multiply(LR,H2),np.transpose(D3))
        W2=W2-np.matmul(np.multiply(LR,H1),np.transpose(D2))
        W1=W1-np.matmul(np.multiply(LR,X),np.transpose(D1))
        return W1,W2,W3,Yhat


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
        Q=Network(State)
        max_act=np.argmax(Q)
        max_val =np.max(Q)
        
        if max_act==0:
            GO='up'
        elif max_act==1:
            GO='down'
        elif max_act==2:
            GO='left'
        elif max_act==3:
            GO='right'
        (s, a, r, s2) = do_action(GO)

        # Update Q
        GridPosNew=np.zeros((Maze.Xgrid,Maze.Ygrid))
        GridPosNew[s2[0],s2[1]]=1
        GridPosNew=np.reshape(GridPosNew,(Maze.Xgrid*Maze.Ygrid,1))
        StateNew=[GridPosNew,GridGoal,GridWall]
        StateNew=np.reshape(StateNew,(3*Maze.Xgrid*Maze.Ygrid,1))
        
        QNew=Network(StateNew)
        max_actNew=np.argmax(QNew)
        max_valNew =np.max(QNew)
        
        Target=Q
        Target[max_act]=Q[max_act]*(1-alpha)
        Target[max_act]=Target[max_act]+alpha*(r + discount * max_valNew)
        NetworkFit(State,Target,1)

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




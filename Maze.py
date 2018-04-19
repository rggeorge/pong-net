from tkinter import *
import ReadImage
master = Tk()

cell_score_min = -0.2
cell_score_max = 0.2
Xgrid=ReadImage.n
Ygrid=ReadImage.m
Width=600/Ygrid

(x, y) = (Xgrid, Ygrid)
actions = ["up", "down", "left", "right"]

board = Canvas(master, width=x*Width, height=y*Width)
Position = (0, y-1)
score = 0
restart = False
walk_reward = -1
numMove=0

walls = ReadImage.walls
specials =ReadImage.goal

# =============================================================================
# walls=[(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(9,1),(10,1),(11,1),(12,1),(13,1),(14,1),(15,1),(16,1),(17,1),(18,1),(19,1),(20,1),(21,1),(22,1),(23,1),(24,1),(25,1),(26,1),(27,1),(28,1),(29,1),(30,1),(31,1),(32,1),(33,1),(34,1),(35,1),
#        (1,2),(8,2),(17,2),(23,2),(30,2),(35,2),
#        (1,3),(3,3),(4,3),(5,3),(6,3),(7,3),(8,3),(10,3),(11,3),(12,3),(13,3),(14,3),(15,3),(19,3),(20,3),(21,3),(23,3),(25,3),(26,3),(27,3),(28,3),(32,3),(33,3),(35,3),
#        (1,4),(3,4),(10,4),(17,4),(21,4),(28,4),(30,4),(33,4),(34,4),(35,4),
#        (1,5),(3,5),(5,5),(6,5),(7,5),(8,5),(9,5),(10,5),(11,5),(12,5),(13,5),(14,5),(15,5),(16,5),(17,5),(18,5),(19,5),(20,5),(21,5),(22,5),(23,5),(24,5),(25,5),(26,5),(27,5),(28,5),(29,5),(30,5),(31,5),(33,5),(35,5),
#        (1,6),(3,6),(5,6),(31,6),(33,6),(35,6),
#        (1,7),(3,7),(5,7),(7,7),(8,7),(9,7),(10,7),(11,7),(12,7),(13,7),(14,7),(15,7),(16,7),(17,7),(18,7),(19,7),(20,7),(21,7),(22,7),(23,7),(24,7),(25,7),(26,7),(27,7),(28,7),(29,7),(31,7),(32,7),(33,7),(35,7),
#        (1,8),(3,8),(5,8),(7,8),(19,8),(29,8),(31,8),(35,8),
#        (1,9),(3,9),(5,9),(7,9),(9,9),(10,9),(11,9),(12,9),(13,9),(14,9),(15,9),(16,9),(17,9),(19,9),(20,9),(21,9),(22,9),(23,9),(24,9),(25,9),(26,9),(27,9),(29,9),(31,9),(32,9),(33,9),(35,9),
#        (1,10),(3,10),(5,10),(7,10),(9,10),(27,10),(29,10),(31,10),(35,10),
#        (1,11),(3,11),(5,11),(7,11),(9,11),(11,11),(12,11),(13,11),(14,11),(15,11),(16,11),(20,11),(21,11),(22,11),(23,11),(24,11),(25,11),(27,11),(29,11),(31,11),(33,11),(34,11),(35,11),
#        (1,12),(3,12),(5,12),(7,12),(9,12),(11,12),(12,12),(13,12),(14,12),(15,12),(16,12),(20,12),(21,12),(22,12),(23,12),(24,12),(25,12),(27,12),(29,12),(31,12),(33,12),(35,12),
#        (1,13),(5,13),(7,13),(9,13),(11,13),(12,13),(13,13),(14,13),(15,13),(16,13),(20,13),(21,13),(22,13),(23,13),(24,13),(25,13),(27,13),(29,13),(31,13),(35,13),
#        (1,14),(3,14),(4,14),(5,14),(7,14),(9,14),(13,14),(14,14),(15,14),(21,14),(22,14),(23,14),(27,14),(29,14),(31,14),(32,14),(33,14),(35,14),
#        (1,15),(3,15),(5,15),(7,15),(9,15),(10,15),(11,15),(12,15),(14,15),(15,15),(16,15),(20,15),(21,15),(22,15),(24,15),(25,15),(16,15),(27,15),(29,15),(31,15),(35,15),
#        (1,16),(3,16),(5,16),(7,16),(13,16),(15,16),(16,16),(17,16),(19,16),(20,16),(21,16),(23,16),(24,16),(29,16),(31,16),(33,16),(35,16),
#        (1,17),(5,17),(7,17),(9,17),(10,17),(11,17),(13,17),(14,17),(16,17),(17,17),(18,17),(19,17),(20,17),(22,17),(23,17),(24,17),(25,17),(27,17),(28,17),(29,17),(31,17),(33,17),(35,17),
#        (1,18),(2,18),(3,18),(5,18),(7,18),(9,18),(11,18),(15,18),(17,18),(18,18),(19,18),(21,18),(29,18),(31,18),(33,18),(35,18),
#        (1,19),(5,19),(7,19),(9,19),(11,19),(12,19),(13,19),(15,19),(17,19),(18,19),(19,19),(21,19),(23,19),(24,19),(25,19),(26,19),(28,19),(29,19),(31,19),(32,19),(33,19),(35,19),
#        (1,20),(2,20),(3,20),(5,20),(7,20),(9,20),(15,20),(17,20),(18,20),(19,20),(21,20),(26,20),(28,20),(29,20),(35,20),
#        (1,21),(3,21),(5,21),(7,21),(9,21),(10,21),(11,21),(12,21),(13,21),(14,21),(15,21),(17,21),(18,21),(19,21),(21,21),(22,21),(23,21),(24,21),(25,21),(26,21),(28,21),(29,21),(31,21),(32,21),(33,21),(34,21),(35,21),
#        (1,22),(3,22),(5,22),(7,22),(12,22),(17,22),(18,22),(19,22),(24,22),(28,22),(29,22),(31,22),(35,22),
#        (1,23),(3,23),(5,23),(7,23),(9,23),(10,23),(12,23),(14,23),(15,23),(16,23),(17,23),(18,23),(19,23),(20,23),(21,23),(22,23),(24,23),(25,23),(26,23),(27,23),(28,23),(29,23),(31,23),(33,23),(35,23),
#        (1,24),(5,24),(7,24),(9,24),(12,24),(14,24),(15,24),(16,24),(17,24),(18,24),(19,24),(20,24),(21,24),(22,24),(24,24),(25,24),(31,24),(33,24),(35,24),
#        (1,25),(3,25),(4,25),(5,25),(7,25),(9,25),(10,25),(11,25),(12,25),(14,25),(15,25),(16,25),(17,25),(18,25),(19,25),(20,25),(21,25),(22,25),(24,25),(25,25),(27,25),(28,25),(29,25),(30,25),(31,25),(32,25),(33,25),(35,25),
#        (1,26),(7,26),(11,26),(12,26),(24,26),(25,26),(35,26),
#        (1,27),(3,27),(4,27),(5,27),(6,27),(7,27),(8,27),(9,27),(11,27),(12,27),(13,27),(14,27),(15,27),(16,27),(17,27),(18,27),(19,27),(20,27),(21,27),(22,27),(23,27),(24,27),(25,27),(27,27),(28,27),(29,27),(30,27),(31,27),(32,27),(33,27),(34,27),(35,27),
#        (1,28),(9,28),(11,28),(12,28),(13,28),(14,28),(15,28),(16,28),(17,28),(18,28),(19,28),(20,28),(21,28),(22,28),(23,28),(24,28),(25,28),(35,28),
#        (1,29),(3,29),(4,29),(5,29),(6,29),(7,29),(9,29),(26,29),(27,29),(28,29),(29,29),(30,29),(31,29),(32,29),(33,29),(35,29),
#        (1,30),(4,30),(9,30),(10,30),(11,30),(12,30),(13,30),(14,30),(15,30),(16,30),(17,30),(18,30),(19,30),(20,30),(22,30),(24,30),(32,30),(33,30),
#        (1,31),(3,31),(4,31),(6,31),(7,31),(8,31),(9,31),(10,31),(11,31),(12,31),(14,31),(20,31),(22,31),(24,31),(25,31),(26,31),(27,31),(28,31),(29,31),(30,31),(35,31),(36,31),
#        (1,32),(4,32),(6,32),(14,32),(16,32),(17,32),(18,32),(20,32),(22,32),(24,32),(30,32),(32,32),(33,32),(34,32),(36,32),
#        (1,33),(2,33),(3,33),(4,33),(6,33),(7,33),(8,33),(9,33),(10,33),(11,33),(12,33),(14,33),(16,33),(18,33),(20,33),(22,33),(23,33),(24,33),(26,33),(27,33),(28,33),(30,33),(34,33),(36,33),
#        (6,34),(8,34),(16,34),(20,34),(26,34),(28,34),(30,34),(31,34),(33,34),(34,34),(36,34),
#        (1,35),(2,35),(3,35),(4,35),(5,35),(6,35),(7,35),(8,35),(9,35),(10,35),(11,35),(12,35),(13,35),(14,35),(16,35),(17,35),(18,35),(19,35),(20,35),(22,35),(23,35),(24,35),(25,35),(26,35),(28,35),(30,35),(31,35),(33,35),(34,35),(36,35),
#        (28,36),(36,36)]
# 
# specials = [(17, 11, "green", 1),(18, 11, "green", 1),(19, 11, "green", 1),
#             (17, 12, "green", 1),(18, 12, "green", 1),(19, 12, "green", 1),
#             (17, 13, "green", 1),(18, 13, "green", 1),(19, 13, "green", 1),
#            (16, 14, "green", 1),(17, 14, "green", 1),(18, 14, "green", 1),(19, 14, "green", 1),(20, 14, "green", 1),
#             (17, 15, "green", 1),(18, 15, "green", 1),(19, 15, "green", 1),
#             (18, 16, "green", 1)]
# =============================================================================

cell_scores = {}


def create_GamePiece(i, j, action):
    if action == actions[0]:
        return board.create_polygon((i+0.5)*Width, j*Width,
                                    fill="white", width=1)
    elif action == actions[1]:
        return board.create_polygon((i+0.5)*Width, (j+1)*Width,
                                    fill="white", width=1)
    elif action == actions[2]:
        return board.create_polygon(i*Width, (j+0.5)*Width,
                                    fill="white", width=1)
    elif action == actions[3]:
        return board.create_polygon((i+1)*Width, (j+0.5)*Width,
                                    fill="white", width=1)


    
def make_maze():
    global specials, walls, Width, x, y, Position
    for i in range(x):
        for j in range(y):
            board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="white", width=1)
            temp = {}
            for action in actions:
                temp[action] = create_GamePiece(i, j, action)
            cell_scores[(i,j)] = temp
    for (i, j, c, w) in specials:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill=c, width=1)
    for (i, j) in walls:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="black", width=1)

make_maze()



def try_move(dx, dy):
    global Position, x, y, score, walk_reward, me, restart, numMove
    if restart == True:
        restart_game()
    x_new = Position[0] + dx
    y_new = Position[1] + dy
    numMove+=1
    score += walk_reward
    if (x_new >= 0) and (x_new < x) and (y_new >= 0) and (y_new < y) and not ((x_new, y_new) in walls):
        board.coords(me, x_new*Width+Width*2/10, y_new*Width+Width*2/10, x_new*Width+Width*8/10, y_new*Width+Width*8/10)
        Position = (x_new, y_new)
    for (i, j, c, w) in specials:
        if x_new == i and y_new == j:
            score += w-walk_reward
            
            #print ("score: ", score)
            print ("Moves: ", numMove)

            restart = True
            return



def call_up(event):
    try_move(0, -1)


def call_down(event):
    try_move(0, 1)


def call_left(event):
    try_move(-1, 0)


def call_right(event):
    try_move(1, 0)


def restart_game():
    global Position, score, me, restart, numMove
    Position = (0, y-1)
    score = 0
    numMove=0
    restart = False
    board.coords(me, Position[0]*Width+Width*2/10, Position[1]*Width+Width*2/10, Position[0]*Width+Width*8/10, Position[1]*Width+Width*8/10)

def has_restarted():
    return restart

master.bind("<Up>", call_up)
master.bind("<Down>", call_down)
master.bind("<Right>", call_right)
master.bind("<Left>", call_left)

me = board.create_rectangle(Position[0]*Width+Width*2/10, Position[1]*Width+Width*2/10,
                            Position[0]*Width+Width*8/10, Position[1]*Width+Width*8/10, fill="orange", width=1, tag="me")

board.grid(row=0, column=0)


def start_game():
    master.mainloop()

#start_game()
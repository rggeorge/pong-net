#PONG pygame
import numpy as np
import random
import pygame, sys
from pygame.locals import *

pygame.init()
fps = pygame.time.Clock()

#colors
WHITE = (255,255,255)
BLACK = (0,0,0)

#globals
WIDTH = 600
HEIGHT = 400       
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH // 2
HALF_PAD_HEIGHT = PAD_HEIGHT // 2
ball_pos = [0,0]
ball_vel = [0,0]
paddle1_vel = 0
Level=1
SpeedIncrease=1.2
Bounce=.2

#canvas declaration
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Single Player Pong')

# helper function that spawns a ball, returns a position vector and a velocity vector
# if right is True, spawn to the right, else spawn to the left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [.9*WIDTH,HEIGHT//2]
    horz = -1
    vert = random.randrange(-3,3)
    ball_vel = [horz,vert]

# define event handlers
def init():
    global paddle1_pos, paddle1_vel  # these are floats
    global score1, score2,Level  # these are ints
    paddle1_pos = [HALF_PAD_WIDTH - 1,HEIGHT//2]
    Level=1
    if random.randrange(0,2) == 0:
        ball_init(True)
    else:
        ball_init(False)


#draw function of canvas
def draw(canvas):
    global paddle1_pos, ball_pos, ball_vel,Level, Bounce
           
    canvas.fill(BLACK)
    pygame.draw.line(canvas, WHITE, [PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1)


    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos[1] > HALF_PAD_HEIGHT and paddle1_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HALF_PAD_HEIGHT and paddle1_vel > 0:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle1_vel < 0:
        paddle1_pos[1] += paddle1_vel


    #update ball
    ball_pos[0] += int(ball_vel[0])
    ball_pos[1] += int(ball_vel[1])

    #draw paddles and ball
    pygame.draw.rect(canvas,WHITE,(ball_pos[0],ball_pos[1],5,5))
    pygame.draw.polygon(canvas, WHITE, [[paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT], [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT]], 0)
   

    #ball collision check on top, bottom, or back walls
    if int(ball_pos[1]) <= 0:
        ball_vel[1] = - ball_vel[1]
    if int(ball_pos[1]) >= HEIGHT + 1:
        ball_vel[1] = -ball_vel[1]
    if int(ball_pos[0]) >= WIDTH + 1 - PAD_WIDTH:
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= SpeedIncrease
        Level+=1
    #ball collison check on gutters or paddles
    if int(ball_pos[0]) <=  PAD_WIDTH and int(ball_pos[1]) in range(paddle1_pos[1] - HALF_PAD_HEIGHT,paddle1_pos[1] + HALF_PAD_HEIGHT,1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[1] +=Bounce*paddle1_vel

    elif int(ball_pos[0]) <=  PAD_WIDTH:
        pygame.quit()
        sys.exit()

        


    #update scores
    myfont1 = pygame.font.SysFont("Stencil", 20)
    label1 = myfont1.render("Level "+str(Level), 1, WHITE)
    canvas.blit(label1, (WIDTH-100,20))


    
    
#keydown handler
def keydown(event):
    global paddle1_vel
    
    if event.key == K_UP:
        paddle1_vel = -8
    elif event.key == K_DOWN:
        paddle1_vel = 8


#keyup handler
def keyup(event):
    global paddle1_vel, paddle2_vel
    
    if event.key in (K_UP, K_DOWN):
        paddle1_vel = 0


init()


#game loop
while True:

    draw(window)

    for event in pygame.event.get():

        if event.type == KEYDOWN:
            keydown(event)
        elif event.type == KEYUP:
            keyup(event)
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    pygame.display.update()
    fps.tick(60)


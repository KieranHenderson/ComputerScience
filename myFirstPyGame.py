## Kieran Henderson, myFirstPyGame, This program is like a screen saver
##with three circles that change colour when thy bounce of the walls, they also bounce off each other.
## March 1st 2019

import pygame
import sys
import keyboard
import random
import math

pygame.init()

go = True
size = (800, 600)
screen = pygame.display.set_mode(size)
width = 800
height = 600

##getting three random colours 
randomColour = (random.randint(2,255), random.randint(2, 255), random.randint(2, 255))
colour = randomColour
colour1 = randomColour
colour2 = randomColour

WHITE = (255,255,255)

x = 100
y = 200
x1 = 575
y1 = 400
x2 = 400
y2 = 200
dx = 5
dy=random.randint(3,5)
dx1 = 5
dy1=random.randint(3,5)
dx2 = 5
dy2=random.randint(3,5)
r=25

clock = pygame.time.Clock()
FPS = 100

screen.fill(WHITE)

pygame.display.update()



while go:
##Using pythag to calculate distance between all the balls
    distance = math.sqrt (((x-x1)*(x-x1)) +((y-y1)*(y-y1)))
    distance1 = math.sqrt (((x1-x2)*(x1-x2)) +((y1-y2)*(y1-y2)))
    distance2 = math.sqrt (((x2-x)*(x2-x)) +((y2-y)*(y2-y)))
    
    randomColour = (random.randint(0,255), random.randint(0, 255), random.randint(0, 255))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            go = False


    clock.tick(FPS)
        
    screen.fill(WHITE)

##Using the distance from earlier to checking if the it is < r+r (they are colliding)
##and then checking if they are overlapping to the point that they get stuck and stopping that.
    
    if (distance < r+r and distance > r):
            if y-y1<20:
                dx=-dx
                dx1=-dx1
            if x-x1<15:
                dy=random.randint(3,5)
                dy1=random.randint(3,5)

    if (distance1 < r+r and distance1 > r):
            if y1-y2<20:
                dx1=-dx1
                dx2=-dx2
            if x1-x2<15:
                dy1=random.randint(3,5)
                dy2=random.randint(3,5)

    if (distance2 < r+r and distance2 > r):
            if y-y2<20:
                dx=-dx
                dx2=-dx2
            if x-x2<15:
                dy=random.randint(3,5)
                dy2 =random.randint(3,5)

##Circle one
    
    if (x>width-r): 
        dx = -dx
        colour = randomColour
    elif (x<r): 
        dx = -dx
        colour = randomColour
        
    if (y>height-r): 
        dy=-dy
        colour = randomColour
    elif (y<r):  
        dy=-dy
        colour = randomColour
##Circle two
            
    if (x1>width-r): 
        dx1 = -dx1
        colour1 = randomColour
    elif (x1<r): 
        dx1 = -dx1
        colour1 = randomColour
        
    if (y1>height-r): 
        dy1=-dy1
        colour1 = randomColour
    elif (y1<r):  
        dy1=-dy1
        colour1 = randomColour
##Circle three
            
    if (x2>width-r): 
        dx2 = -dx2
        colour2 = randomColour
    elif (x2<r): 
        dx2 = -dx2
        colour2 = randomColour
        
    if (y2>height-r): 
        dy2=-dy2
        colour2 = randomColour
    elif (y2<r):  
        dy2=-dy2
        colour2 = randomColour


##animating them        
    x=x+dx
    y=y+dy
    x1=x1+dx1
    y1=y1+dy1
    x2=x2+dx2
    y2=y2+dy2

##drawing the new circles         
    pygame.draw.circle (screen, colour, (x,y),25,0)
    pygame.draw.circle (screen, colour1, (x1, y1), 25, 0)
    pygame.draw.circle (screen, colour2, (x2, y2), 25, 0)
    pygame.display.update()
    
pygame.quit()
sys.exit()

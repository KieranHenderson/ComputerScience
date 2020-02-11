import pygame
import sys
import random
import math

pygame.init()

##pygame.mixer.music.load("music.wav")
    
width = 800
height = 600
screenSize = (width, height)
screen = pygame.display.set_mode((screenSize),0)
pygame.display.set_caption("U1A2 Test")


WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
BLACK = (0, 0, 0)
SILVER = (192, 192, 192)

Side = random.randint(1,2)

clock = pygame.time.Clock()
FPS = 100

font = pygame.font.SysFont(None, 25)
fontScore = pygame.font.SysFont(None, 78)   ##The different font sizes used
fontMP = pygame.font.SysFont(None, 50)

matchPoint = False
pause = False


def textObject(text,colour):
    textSurf = font.render(text, True, colour)  ##setting up an easy function for font and location
    return textSurf, textSurf.get_rect()

def textObjectBig(text,colour):
    textSurf = fontScore.render(text, True, colour) ##setting up larger font size for score
    return textSurf, textSurf.get_rect()

def textObjectMP(text,colour):
    textSurf = fontMP.render(text, True, colour) ##setting up larger font size for score
    return textSurf, textSurf.get_rect()

def messageDisplay(msg,colour):
    textSurf, textRect = textObject(msg,colour) ## easy function for displaying text on screen
    textRect.center = (width / 2), (height / 2)
    screen.blit(textSurf, textRect)

def button(msg,x,y,w,h,ic,ac,action=None):  ##making a function that I can later call which makes creating buttons easy
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x + w > mouse[0]  > x and y + h > mouse[1] > y:      ##takes location of mouse to see if you are hovering the correct area, aswell as if 
        pygame.draw.rect(screen, ac, (x, y, w, h))          ##the mouse is clicked while hovering then it will recive the action and execute the correct if statement
        if click [0] == 1 and action != None:
            if action == "play":
                game_loop()
            elif action == "quit":
                pygame.quit()
                quit()
            elif action == "unpause":
                unpaused()
            
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))      ##writing on buttons

    textSurf, textRect = textObject(msg,(0,0,0))
    textRect.center = ((x+w/2),(y+h/2))
    screen.blit(textSurf, textRect)

def game_intro():   ##function of the game intro
    matchPoint = False
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill(BLACK)
        textSurf, textRect = textObjectMP("Let's play some pong!", (255,255,255))     ##uses buttons to check the location of mouse and if it is hovering change the color to silver to add interactability 
        textRect.center = ((width/2), (height/2))                                   ##also returns the active value (play and quit) when the respecting area is clicked which allows the button function to work
        screen.blit(textSurf, textRect)

        button("Play",150,450,100,50,WHITE,SILVER,"play")
        button("Quit",550,450,100,50,WHITE,SILVER,"quit")

            
        

        
        pygame.display.update()
        clock.tick(15)

def victory(playerOneScore, playerTwoScore):        #game over function
    if playerOneScore > 10:
        winner = "Player One You Win!"
    elif playerTwoScore > 10:
        winner = "Player Two You Win"                ##firt player to reach 11 points scored
    while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            screen.fill(BLACK)
            textSurf, textRect = textObjectMP(str(winner), (255,255,255))
            textRect.center = ((width/2), (height/2))
            screen.blit(textSurf, textRect)

            button("Again?",150,450,100,50,WHITE,SILVER,"play")         ##asks them if they would like to quit or play again
            button("Quit",550,450,100,50,WHITE,SILVER,"quit")

            
            pygame.display.update()
            clock.tick(15)
    

def unpaused():     ##unpaused function 
    global pause
    ##pygame.mixer.music.unpause()    
    pause = False

def paused():   ##paused function

    ##pygame.mixer.music.pause()
    
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:       ##uses buttons asks to continue or quit
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    unpaused()
        screen.fill(BLACK)
        textSurf, textRect = textObjectMP("Paused", (255,255,255))
        textRect.center = ((width/2), (height/2))
        screen.blit(textSurf, textRect)

        button("Continue",150,450,100,50,WHITE,SILVER,"unpause")
        button("Quit",550,450,100,50,WHITE,SILVER,"quit")

        
        pygame.display.update()
        clock.tick(15)


def game_loop():        ##main game loop
    global pause
    global matchPoint
    matchPoint = False
    ##pygame.mixer.music.play(-1)
    
    screen.fill(BLACK)
    pygame.display.update()
                            ## main veriables for game
    RECTX1 = 25
    RECTX = 750
    xcircle = 400
    ycircle = 300
    PADDLEHEIGHT = 100
    y = 250
    y1 = 250
    dy1 = 0
    dy = 0
    dycircle = 0
    r = 15
    playerOneScore = 0
    playerTwoScore = 0



    if Side == 1:       ##takes a random int from earlier and decides which side the ball goes to at the beging of the game
        dxcircle = 3
    elif Side == 2:
        dxcircle = -3


    

    
    go = True
    
    while go:    
        if xcircle < r:
            ycircle = 300
            xcircle = 400
            dxcircle = -3
            dycircle = 0
            playerTwoScore = playerTwoScore + 1        ##goal stuff
            print("p2 : ", playerTwoScore)
        elif xcircle > width - r:
            xcircle = 400
            ycircle = 300
            dxcircle = 3
            dycircle = 0
            playerOneScore = playerOneScore + 1
            print("p1 : ", playerOneScore)

        if ycircle < r:             ##making the ball bounce off walls 
            dycircle = -dycircle
        elif ycircle > height - r:
            dycircle = -dycircle


        
        if y < r:       ##making paddles stay on screen
            dy = 0
            y = r 
        elif y > height - r - 100:
            dy = 0
            y = height - r - 100
        if y1 < r:
            dy1 = 0
            y1 = r 
        elif y1 > height - r - 100:
            dy1 = 0
            y1 = height - r - 100


        if playerOneScore > 10 or playerTwoScore > 10:      ##calling the victory function when somebody has more than 10 points 
            victory(playerOneScore, playerTwoScore)
            


        textSurfOne, textRectOne = textObjectBig(str(playerOneScore), WHITE)      #displaying score
        textRectOne.center = ((width/3), (height/8))
        
        textSurf, textRect = textObjectBig(str(playerTwoScore), WHITE)
        textRect.center = ((width-width/3), (height/8))
        
        if playerOneScore == 10 or playerTwoScore == 10:
            textSurfMP, textRectMP = textObjectMP("Match Point!", WHITE)
            textRectMP.center = ((width/2), (height/4))
            matchPoint = True
        

    ## bounce for right side
        realtiveIntY = (y+(PADDLEHEIGHT/2)) - ycircle
        normalIntY = (realtiveIntY/(PADDLEHEIGHT/2))
        bounceAngle = normalIntY * 73
        bounceAngle = round(bounceAngle/15)
        
        
    ## bounce for left side
        realtiveIntY1 = (y1+(PADDLEHEIGHT/2)) - ycircle
        normalIntY1 = (realtiveIntY1/(PADDLEHEIGHT/2))
        bounceAngle1 = normalIntY1 * 73
        bounceAngle1 = round(bounceAngle1/15)    

        
    ## collision check for paddle one (left)
        if y1 + PADDLEHEIGHT > ycircle > y1  and xcircle - r <= RECTX1 + 25:
            if dycircle==0:
                dxcircle=-dxcircle+1
            else:
                dxcircle=-dxcircle
            dycircle=dycircle-bounceAngle1

    ##Checking collision for second paddle (Right)    
        if y + PADDLEHEIGHT > ycircle > y  and xcircle - r >= RECTX - 25:
            if dycircle==0:
                dxcircle=-dxcircle-1
            else:
                dxcircle=-dxcircle
            dycircle=dycircle-bounceAngle
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                go = False
            elif event.type == pygame.KEYDOWN:
                #change colour here
                if event.key == pygame.K_DOWN:      ##all you can do on keyboard while in the main game area
                    dy = 6
                elif event.key == pygame.K_UP:
                    dy = -6
                elif event.key == pygame.K_w:
                    dy1 = -6
                elif event.key == pygame.K_s:
                    dy1 = 6
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_ESCAPE:
                    pause = True
                    paused()



            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:      ##making you stop when you aren't pressing buttons
                    dy = 0
                elif event.key == pygame.K_w or event.key == pygame.K_s:
                    dy1 = 0

        clock.tick(FPS)

        screen.fill (BLACK)             ##all drawing and screen updating
        y1 = y1 + dy1
        y = y + dy
        ycircle = ycircle + dycircle
        xcircle = xcircle + dxcircle
        pygame.draw.circle(screen, WHITE,(xcircle,ycircle), r,0)
        pygame.draw.rect(screen, WHITE, [RECTX, y, 25, PADDLEHEIGHT])
        pygame.draw.rect(screen, WHITE, [RECTX1, y1, 25, PADDLEHEIGHT])
        screen.blit(textSurf, textRect)
        screen.blit(textSurfOne, textRectOne)
        if matchPoint == True:
            screen.blit(textSurfMP, textRectMP)
        pygame.display.update()



game_intro()    ##starts game intro on start up
        
pygame.quit()
sys.exit()

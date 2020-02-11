import pygame
import sys
import time
import random
import os
import pygame_textinput

pygame.init()

pygame.mixer.music.load("assets/Mozart - Lacrimosa.mp3") ##Loading the mp3 file for music


##Stting up pygame, screen width and height as well as global veriables that I will need such as the paused, keyType and colour variables 
width = 1280
height = 720
size = (width, height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("hendersonFinalProject")

BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
SILVER = ( 192, 192, 192)
dy = 2
jumpHeight = 75
startY = 578
keyType = 'arrow'
pause = False

enemy=[]        ##Empty array to store all of my enemy objects in

##Two custom events that will be triggered later based off timers, Generate is for enemy spawn time and timer is to speed up the game every second
generate = pygame.USEREVENT+1
timer = pygame.USEREVENT+2

clock = pygame.time.Clock()


##For creating text objects for rendering on screen
def textObject(text, colour, size):
    font = pygame.font.SysFont(None, size)
    textSurf = font.render(text, True, colour)
    return textSurf, textSurf.get_rect()

##rendering a mesage on screen
def messageDisplay(msg, colour, size):
    textSurf, textRect = textObject(msg, colour, size)
    textRect.center = (width/2), (height/2)
    screen.blit(textSurf, textRect)

def button(msg,x,y,w,h,ic,ac,action=None):  ##making a function that I can later call which makes creating buttons easy
    ##get the position of the mouse and check when it is clicked
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    global keyType
    global musicPaused
    
    if x + w/2 > mouse[0]  > x - w/2 and y + h/2 > mouse[1] > y -h/2:      ##takes location of mouse to see if you are hovering the correct area, aswell as if 
        pygame.draw.rect(screen, ac, ((x-w/2), (y-h/2), w, h))          ##the mouse is clicked while hovering then it will recive the action and execute the correct if statement
        if click [0] == 1 and action != None:
            if action == "play":                ##call the difficulty select function to initiate the game starting
                diffSelect(keyType)
            elif action == "quit":              ##Quit the game
                pygame.quit()
                quit()
            elif action == "unpause":           ##will unpause the game
                unpaused()
            elif action == "easy":              ##Button is on the difficulty select screen and sets hp to 3 AKA Easy mode
                startGame(3, 'easy', keyType)
            elif action == "med":               ##Button is on the difficulty select screen and sets hp to 2 AKA Medium mode
                startGame(2, 'med', keyType)
            elif action == "hard":              ##Button is on the difficulty select screen and sets hp to 1 AKA Hard mode
                startGame(1, 'hard', keyType)
            elif action == "how to":            ##Will bring you from the home page to a page where you can see how to play the game
                howToPlay()
            elif action == "settings":          ##Bring you from the home page to settings page where you can change your controls 
                return settings()
            elif action == 'home':              ##Will bring you back to the main menu area from either he death screen or the paused screen
                gameIntro()
            elif action == 'hs':                ##Will bring you from the home page to the highscores page
                highScore()
            elif action == 'arrow':             ##Will set the value of keyType to arrow and then return that value
                keyType = 'arrow'
                return keyType
            elif action == 'ws':                ##Will set the value of keyType to ws and then return that value
                keyType = 'ws'
                return keyType
            elif action == 'music pause':
                pygame.mixer.music.pause()      ##pause the music
            elif action == 'music unpause':
                pygame.mixer.music.unpause()    ##unpause the music
            
    else:
        pygame.draw.rect(screen, ic, ((x-w/2), (y-h/2), w, h))  ##Drawing the actual button so that it is centered around the point you specified

    textSurf, textRect = textObject(msg,(BLACK), 25)            ##Displaying the correct text onto the button location
    textRect.center = ((x),(y))
    screen.blit(textSurf, textRect)                             ##Blit it all to the screen

def getUserText(message):       ##Taken from arrays project which we were given
    # Create TextInput-object
    textInput = pygame_textinput.TextInput()
    clock =pygame.time.Clock()
    go = True
    x=width
    y=height
    while go:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.draw.rect(screen, BLACK, (140, (height/4), 1000, (height/2)))    ##Draw black rectangle onto the screen
        clock.tick(30)
       
        inputSurf, inputRect = textObject(message, WHITE, 50)                   ##Writes your message to the user in white
        inputRect.center = ((x/2),250)                                          ##Center the message
        screen.blit(inputSurf, inputRect)

        # Blit its surface onto the screen
        screen.blit(textInput.get_surface(),(200,350))
        if textInput.update(events) == True:
            userInput =textInput.get_text()
            go = False
        pygame.display.update()                                                 ##Update everything

    return userInput

class RedEnemy(object):
    ##The images I need for animating the enemy in an array for easy access
    img = [pygame.image.load(os.path.join('assets', 'enemy1.png')),pygame.image.load(os.path.join('assets', 'enemy2.png'))]
    ##here I define all the variables that I will need to manipulate to control the enemy
    def __init__(self,x, y, width, height):
        self.x = x                      ##X position
        self.y = y                      ##Y position
        self.width = width              ##width
        self.height = height            ##height
        self.hitbox = (x,y,width,height)##creating a tuple with the name hitbox wit the charecteristics of my enemy 
        self.count = 0                  ##This is used to count how many times I have cycled through the enemy class and thus animate it accordingly

    def draw(self,screen):
        self.hitbox=(self.x + 5, self.y + 5, self.width-10, self.height)    ##Change the hit box so that it is a little less than the actual dimensions of the enemy(more forgiving for players)
        if self.count >= 32:                                                ##Animating the enemy
            self.count = 0
        screen.blit(self.img[self.count//16], (self.x,self.y))
        self.count += 1
##        pygame.draw.rect(screen,(255,0,0), self.hitbox, 2)        The actual hitbox as a box

    def collide(self, rect):
        if rect[0]+rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0]+self.hitbox[2]:        ##Checking if it collides with anything
            if rect[1] + rect[3] > self.hitbox[1] and rect[1] < self.hitbox[1]+self.hitbox[3]:
                return True
        return False


class Player(object):
    run = [pygame.image.load(os.path.join('assets', 'playerLeftFoot.png')),pygame.image.load(os.path.join('assets', 'playerRightFoot.png'))]
    jump = [pygame.image.load(os.path.join('assets', 'startJump.png')),pygame.image.load(os.path.join('assets', 'jumping.png')), pygame.image.load(os.path.join('assets', 'endJump.png'))]
    slide = pygame.image.load(os.path.join('assets', 'slide.png'))
    dead = pygame.image.load(os.path.join('assets', 'dead.png'))

    def __init__(self, x, y, width, height):
        self.x = x                      ##The first 5 here are the same as they were in the enemy class just for the player
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (x,y,width,height)
        self.running = False            ##The first of four possible states my player can be in, this is true while my player is running
        self.sliding = False            ##Second of the four possible states my player can be in, this one is true while he is sliding/ducking
        self.jumping = False            ##Third of the four possible states my player can be in, this one is true while he is jumoing
        self.death = False              ##Last of the four possible states my player can be in, this is true while my player is dead
        self.jumpCount = 0              ##counts the length of my jump and is used to determine how ong each frame of the animation lasts 
        self.runCount = 0               ##counts the length of my run and is used to determine how ong each frame of the animation lasts 
        self.slideCount = 0             ##counts the length of my slide and is used to determine how ong each frame of the animation lasts 

    def draw(self,screen):
        self.hitbox=(self.x + 5, self.y, self. width - 10, self.height)
        if self.death:
            ##if the player is dead, they are not jumping or sliding
            self.jumping = False
            self.sliding = False
            ##Blit player dead on screen
            screen.blit(self.dead, (self.x,self.y))
        elif self.jumping:
            ##Incrament jump count
            self.jumpCount +=1
            if self.jumpCount >= 60:
                self.jumpCount = 0
                ##When my jump count reaches the correct amount then the player is no longer jumping thus player.jumping is set to false
                self.jumping = False
            ##Change the hitbox so it is a little more forgiving to players
            self.hitbox=(self.x + 5, self.y, self. width - 10, self.height)
            ##Display correct jumping image on players location
            screen.blit(self.jump[self.jumpCount//20], (self.x,self.y))
        elif self.sliding:
            ##Change players hitbox so that it is actually posible to slide under obstacles 
            self.hitbox=(self.x + 5, self.y+16, self. width - 10, self.height-16)
            ##Incrament slide count
            self.slideCount +=1
            if self.slideCount >= 64 :
                self.slideCount = 0
            ##Display the slide image on my player
            screen.blit(self.slide, (self.x,self.y))
        ##If everything is false then running is true
        elif self.jumping == False and self.sliding == False and self.death == False:
            if self.runCount >= 32:
                self.runCount = 0
            ##Display correct running animation and
            screen.blit(self.run[self.runCount//16], (self.x,self.y))
            ##Incrament runcount
            self.runCount +=1
            ##Changing hit box a little
            self.hitbox=(self.x + 5, self.y, self. width - 10, self.height)

##        pygame.draw.rect(screen, RED, self.hitbox, 2)##Displaying hit box for my player

def makeImage(pic): ##Function to make a picture
    image = pygame.image.load(pic)
    ##image = pygame.transform.scale(image,(x,y))
    return image


def makeObj(image,x,y): ##Take a picture and make a rect object acording to the size so that you can blit the image to the rect object
    rectImage = image.get_rect()
    rectImage.x = x
    rectImage.y = y
    return rectImage

##---------------------------------------------------------------Start of Game Functions---------------------------------------------------------------##
def gameIntro():

    x=0     ##Simple var I used for screen scrolling on the main menu
    intro = True
    background = pygame.image.load("assets/Test3.png")  ##Load the background image
    player.death = False    ##Making sure the player is still not dead from a previous round by setting him to be alive
    
    while intro:
        for event in pygame.event.get():            ##Checking for quitting action
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        relX=x%background.get_rect().width
        screen.blit(background,(relX-background.get_rect().width,0))##Blit one background to the screen whos position always changes acording to the relative x value
        if relX<size[0]:
            screen.blit(background,(relX,0)) ##Rect that follows the first one esentially on an infinte loop
        x+=-2   ##incrament the counter value

        button("Play",(width/2),200,150,50,WHITE,SILVER,"play")         ##Allows player to play and is brought to the button function where the play action is executed
        button("How To Play",(width/2),300,150,50,WHITE,SILVER,"how to")##Allows player to enter the screen which teaches you how to play and is brought to the button function where the how to action is executed
        button("Settings",(width/2),400,150,50,WHITE,SILVER,"settings") ##Allows player to enter the settings page and is brought to the button function where the settings action is executed
        button("HighScores",(width/2),500,150,50,WHITE,SILVER,"hs")     ##Allows player to view the highscores and is brought to the button function where the hs action is executed
        button("Quit",(width/2),600,150,50,WHITE,SILVER,"quit")         ##Allows player to quit the game
                    
        pygame.display.update()
        clock.tick(30)


def howToPlay():
    how = True
    duck = makeImage('assets/howDuck.png')          ##Load my ducking instructions picture
    duck = pygame.transform.scale(duck,(640, 360))  ##change the dimensions so it will fit correctly 
    jump = makeImage('assets/howJump.png')          ##Load my jumping instructions picture
    jump = pygame.transform.scale(jump,(640, 360))  ##change the dimensions so it will fir correctly 

    while how:
        screen.fill((200,200,200))                  ##Fill screen with a gray colour and blit the pictures to the screen
        screen.blit(duck, (320,0))
        screen.blit(jump, (320,370))
        messageDisplay('Hit any button to return', (WHITE), 70) ##Tell the user they can hit any button they want to return to their previous screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:           ##Check for a quit event
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:        ##If a key is pushed then the current while loop condition becoms false and returns the player to their previous screen
                how = False
        pygame.display.update()

def highScore():
    high = True
    lineCount = 0   ##Count how many high scores are being displayed currently
    x=width/2       ##Center of screen
    y=128           ##Starting y height of the words
    file = open('HighScores.txt', 'r')  ##Open the highcores text file
    screen.fill(BLACK)                  ##Fill the screen with black
    textSurf, textRect = textObject('All Time Highscores!',(WHITE), 100)    ##Display 'All Time Highscores!' at the top of the screen
    textRect.center = ((width/2),(50))  ##center the text
    screen.blit(textSurf, textRect)
    for line in file:
        textSurf, textRect = textObject(line.strip('\n').strip('[').strip(']').replace("'",''),(WHITE), 60) ##For each line in the file get rid of all the string and array aspects 
        textRect.center = (x,y)
        if lineCount < 10:
            screen.blit(textSurf,textRect)      ##Display each line centered on the page as long as there are less than 10 currently being displayed
        y+=60
        lineCount +=1
    while high:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:       ##Check for quit event
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:    ##on key press current hile loop condition will become false and the player will return to their previous page
                high = False

                    

def settings():
    setting = True
    global keyType  ##load the global keyetype
    global musicPaused
    background=pygame.image.load('assets/test4.png')    ##load the background image

    while setting:
        for event in pygame.event.get():        ##Check for quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type ==pygame.KEYDOWN:     ##If a button is pressed go back to the previous screen
                setting = False
        screen.blit(background, (0,0))          ##blit the background
        if button("Arrow Keys",(width/2),225,150,50,WHITE,SILVER,"arrow"):  ##If the button pressed equals the arrow button then keyType = 'arrow'
            keyType = 'arrow'
        elif button("W and S",(width/2),325,150,50,WHITE,SILVER,"ws"):      ##If the button pressed equals the ws button then keyType = 'ws'
            keyType = 'ws'
            
        button("Unpause Music",(width/2),425,150,50,WHITE,SILVER,"music unpause")
        button("pause Music",(width/2),525,150,50,WHITE,SILVER,"music pause")

        pygame.display.update()
        clock.tick(30)
    return keyType      ##Return the keyType


def diffSelect(keyType):
    x=0
    intro = True
    background=pygame.image.load('assets/test4.png') ##Load the static background image 


    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:           ##Allows the player to exit the game whenever they would like
                pygame.quit()
                quit()
                
        screen.blit(background, (0,0))              ##Blit background onto the screen
        
        button("Easy",(width/2),300,100,50,WHITE,SILVER,"easy")     ##The easy difficulty is chosen and the easy action is exucuted in the button function
        button("Medium",(width/2),400,100,50,WHITE,SILVER,"med")    ##The medium difficulty is chosen and the medium action is exucuted in the button function
        button("Hard",(width/2),500,100,50,WHITE,SILVER,"hard")     ##The hard difficulty is chosen and the hard action is exucuted in the button function

                    
        pygame.display.update()
        clock.tick(30)

def startGame(hp, dif, keyType):
    countdown = 4       ##basic countdown is 4 and not three although 3 is displayed because there was an issue where the countdown would skip over the last second, now it only skips 0
    enemy.clear()       ##Clears the list which holds all of my enemy objects

    background=pygame.image.load('assets/test5.png')    ##Load background picture
    
    cImage = makeImage('assets/player3.png')            ##Generate the player but just an image not the actual object
    cObject = makeObj(cImage,200,startY)

    pygame.display.update()

    while countdown > 0:
        screen.blit(background,(0,0))                   ##displays the background
        messageDisplay(str(countdown-1), (WHITE), 120)  ##Displays the current countdown -1
        screen.blit(cImage,cObject)                     ##Display charecter
        countdown-=1                                    ##Incrament by -1 on the countdown timer
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   ##Check for quit game event
                pygame.quit()
                quit()
                
        if countdown != 0:                  ##If the countdown does not equal 0 then wait a second and loop again
            time.sleep(1)


    mainLoop(hp, dif, keyType)              ##Call the main game loop function

def unpaused():     ##unpaused function 
    global pause    ##When this is called all it deos is set the global variable paused equal to false    pygame.time.set_timer(generate,0)   ##create a timer object that ticks randomly between 2 econds and 3.5 second (used to determine when an enemy will come)
    pause = False

def paused():   ##paused function
    while pause:
        for event in pygame.event.get():            ##Checks for quiting event
            if event.type == pygame.QUIT:       
                quit()
            if event.type == pygame.KEYDOWN:        ##If you hit esc again then you unpause
                if event.key == pygame.K_ESCAPE:
                    unpaused()
        screen.fill(BLACK)              ##Fill the screen with black
        messageDisplay('Paused', (WHITE), 100)  ##Write paused on the screen
        
        textSurf, textRect = textObject('Escape To Continue', (WHITE), 25)  ##Reminding the player that they can also hit escape to continue the game
        textRect.center = (width/2), (height/4*3)
        screen.blit(textSurf, textRect)

        button("Continue",(width/4),450,100,50,WHITE,SILVER,"unpause")  ##You can unpause
        button("Home",(width/2),450,100,50,WHITE,SILVER,"home")         ##You can return to the home page/ main menu
        button("Quit",(width/4*3),450,100,50,WHITE,SILVER,"quit")       ##You can quit the game
        
        
        pygame.display.update()
        clock.tick(15)
        

def hit(hp, score, dif, lostHp):    
    hp-=1                       ##hp -=1 each time the player gets hit
    lostHp+=1                   ##Lost hp amount goes up each time you get hit 
    if hp == 0:                 ##If your hp is == 0 when you get hit then gameOver gets called
        gameOver(score, dif)
    return hp, lostHp           ##Return hp and losthp to game loop


def gameOver(score, dif):
    over = True
    player.death = True         ##Set the player state to death so he displays his death animation
    for i in range (len(enemy)):##Draw the current enemies on the screen
        enemy[i].draw(screen)
    player.draw(screen)         ##Draw he dead player on the screen
    pygame.display.update()


    if dif == 'hard':
        
        name=getUserText("Name: ")  ##Ask user for their name

        file = open('HighScores.txt', 'a')      ##Open the highscores text file for appending
        file.write(name + ',' + str(score)+'\n')##write the current name and score into the buttom of the file
        file.close()                            ##Close the file

        file = open('HighScores.txt', 'r')      ##Open the Highscores file for reading
        scores = []     ##array for each score and name combo
        bigFile = []    ##array for the final product
        for line in file:
            for word in line.split(','):
                scores.append(word.strip('\n').strip('[').strip(']').strip("'").strip('"')) ##strip all string and array charecters
        num = scores[1::2]  ##all the numbers in the scores array are asigned to an array
        names = scores[::2] ##all names are in scores array are asigned to an array
        for i in range (len(num)):  ##change all the numbers into an int
            num[i]=int(num[i])
            bigFile.append([names[i], num[i]])  ##Append the correct name with the correct score to the bigfile array
        bigFile.sort(key=lambda x: x[1], reverse = True)    ##sort the bigFile array ordered from highest scores first to the lowest score last
        file.close()    ##close the file

        file = open('HighScores.txt', 'w')      ##open the highscores fill to write over the current highscores file
        for i in range (len(bigFile)):          ##for each score/name tuple in the bigFile array, write it to the file with a new line after it
            file.write(str(bigFile[i]) + '\n')
        file.close()                            ##close the file
            

        
        

    while over:
        pygame.draw.rect(screen, BLACK, (140, (height/4), 1000, (height/2)))    ##draw a black rectangle on the screen in the middle
        messageDisplay('Better luck next time', WHITE, 120)                     ##display 'Better luck next time" in white on the black rectangle
        textSurf, textRect = textObject(str(score),(WHITE), 200)                ##display the score at the top of the screen
        textRect.center = ((width/2),(100))
        screen.blit(textSurf, textRect)
        player.draw(screen)                                                     ##display the player on the screen(who will be dead)
        
        for event in pygame.event.get():                                        ##check quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        button("Home",(width/4),450,100,50,WHITE,SILVER,"home")                 ##if the home button is click the player is brought back to the main menu
        button("Quit",(width/4*3),450,100,50,WHITE,SILVER,"quit")               ##if the quit button is pressed the player quits the game

        pygame.display.update()
        clock.tick(30)
    
def mainLoop(hp, dif, keyType):
    global pause    ##get paused global value
    screenX=0       ##screen x var for screen scrolling
    lostHp = 0      ##lost hp varriable
    jump = False    ##boolean that is used to control the jumping which tells the program when to come down
    down = False    ##boolean that tells the program when the player is coming down and when it has hit the ground
    running = True  ##boolean that is true by defaul because the player starts running
    go = True       ##while loop condition
    gameTime = 1    ##starting value which gets incramented by one everysecond which is used to control how fast the enemys approch
    score = 10      ##You start the game with 10 score
    player.y = startY   ##sets the players starting vertical position at the default start y
    background = pygame.image.load("assets/Test5.png")  ##load the scrolling background which has a floor



    pygame.time.set_timer(generate,random.randrange((2000*(gameTime)),(3500*(gameTime))))   ##create a timer object that ticks randomly between 2 econds and 3.5 second (used to determine when an enemy will come)
    pygame.time.set_timer(timer,1000)                                                       ##timer that ticks every second which is used to control how fast enemies approche you
    

    




    while go:

        for event in pygame.event.get():            ##Check for quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if keyType == 'arrow':                  ##if the key type equals the arrow keys then up and down arrows are used
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and player.y == startY and player.sliding == False and player.death == False:   ##if the player is on the ground, they aren't dead, they aren't sliding and the player presses the jump button then jump equals true
                        player.running = False  ##player class running becomes false
                        player.jumping = True   ##player jumping becomes true
                        jump = True
                    if event.key == pygame.K_DOWN and player.y == startY:   ##If the player is on the ground and the press the slide button then the player sliding equals true and player running becomes false
                        player.running = False
                        player.sliding = True
                    if event.key == pygame.K_ESCAPE:    ##if the player hits escape then the game becomes paused 
                        pause = True
                        paused()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN and player.y == startY:   ##if the player is on the ground and sliding and they release the slide button then running becomes true and sliding becomes false
                        player.sliding = False
                        player.running = True

                        
            if keyType == 'ws':                 ##Exactly the same logic as the previous checks just with different buttons
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w and player.y == startY and player.sliding == False and player.death == False:
                        player.running = False
                        player.jumping = True
                        jump = True
                    if event.key == pygame.K_s and player.y == startY:
                        player.running = False
                        player.sliding = True
                    if event.key == pygame.K_ESCAPE:
                        pause = True
                        paused()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_s and player.y == startY:
                        player.sliding = False
                        player.running = True


                        
                    
            if event.type == timer:##if the timer event happense (which is once every second) then gameTime goes up by one
                gameTime += 1
            if event.type == generate:      ##every 2 - 3.5 seconds the generate event triggers where a new enemy will be appended to the current list of enemies 
                r = random.randrange(0,3)   ##A random number is chosen (0,1,2,3) and based of that an enemy either spawns at the top of my (so player must duck) or at the bottom (so the player must jump)
                if r == 0 or r == 1:
                    enemy.append(RedEnemy(1290, startY+36 , 43, 36))
                else:
                    enemy.append(RedEnemy(1290, startY-36, 43, 36))


        
        if jump == True:    ##if jump is true
            if player.y >= startY-jumpHeight:   ##if the players y location is grater than  or equal to the start y - the jump height then players y location gets incramented by -dy
                player.y += -dy
            if player.y <= startY-jumpHeight:   ##hen the players y location becomes less than or equal to the start y - the jump height then down becomes true and jump becomes false
                down = True
                jump = False

        if down == True:    ##if down is true
            if player.y <=startY:       ##if players y location is greater than the start y then incrament the players y location by dy
                player.y += dy
            if player.y == startY:      ##when the player returns to the ground down becomes false and player running becomes true again
                down = False
                player.running = True






        ##screen rotation
        relX=screenX%background.get_rect().width    ##Blit one background to the screen whos position always changes acording to the relative x value
        screen.blit(background,(relX-background.get_rect().width,0))
        if relX<size[0]:
            screen.blit(background,(relX,0))    ##blit a second background after it and keep moving it to the side and then back to the begining again so it seems infinite 
        screenX+=-2 ##moves 2 pixles to the left every loop

        currentlyColliding = False  ##variable that tells game if the player is currently colliding with an enemy

        for enemies in enemy:                                   ##for each enemy
            if enemies.collide(player.hitbox):                  ##check to see if the enemies collide with the players hitbox
                currentlyColliding = True                       ##if they do this means currently colliding is true
                
                if currentlyColliding == True and hp != 1:      ##if currently colliding is true and hp is greater than 1 then the game displays the message ouch with a black screen
                    screen.fill(BLACK)
                    messageDisplay('Ouch', WHITE, 120)
                if collisionOccured == False:                   ##if collision occured is false then call the hit function 
                    hp, lostHp = hit(hp, score, dif, lostHp)
                    collisionOccured = True                     ##collsionoccured becoms true so that you dont take multiple hit from the same enemy

            enemies.x -= (2+(gameTime*.25))                     ##move the enemies to the left starts at 2 pixles then becomes mulitlied by the gameTime *.25 to scale as the game goes on longer
            if enemies.x < enemies.width * -1:                  ##if the enemies x position is less than the width of the screen + their width (far left side off screen) they are removed from the list of enemies
                enemy.pop(enemy.index(enemies))
            if score < 15:                                      ##fixing error where the first time there were two enemies (was impossible to pass)
                enemy.pop(0)
        if currentlyColliding == False:                         ##if currently colliding is false then no collision has occured (resetting the variables for the next time)
            collisionOccured = False

            

        dist = 40           ##distance between each heart
        for i in range (hp):
            screen.blit(pygame.image.load('assets/fullHeart.png'), ((1280 - dist),675)) ##loop as many times as you have hp and each time move them to the left by 40
            dist +=40

    
        deadDist = 40       ##distance between each dead heart
        if dif == 'easy':   ##need to check difficulty because the amount of total hp will change the where the first dead heart ill need to be placed
            for i in range (lostHp):
                screen.blit(pygame.image.load('assets/deadHeart.png'), ((1120 + deadDist),675)) ##loop through as many hearts that have died and each time move the x position to the right by 40
                deadDist +=40
        elif dif == 'med':
            for i in range (lostHp):
                screen.blit(pygame.image.load('assets/deadHeart.png'), ((1160 + deadDist),675)) ##loop through as many hearts that have died and each time move the x position to the right by 40
                deadDist +=40

            
        
        textSurf, textRect = textObject(str(score),(WHITE), 200)    ##display the score in white at the top of the screen
        textRect.center = ((width/2),(100))
        screen.blit(textSurf, textRect)

        
        for enemies in enemy:                                       ##draw each enemy in the array of enemies to the screen
            enemies.draw(screen)
            
        player.draw(screen)                                         ##draw the player to the screen

        pygame.display.update()

        clock.tick(60)
        score += 1                                                  ##score goes up by 1 for each loop
        
player = Player(200, startY, 43, 67)                                ##create the player at the very start of the game
pygame.mixer.music.play(-1)##playing the music

gameIntro()                                                         ##call the first window the player will see that acts as the main menu

pygame.quit()                                                       ##option to quit
sys.exit()

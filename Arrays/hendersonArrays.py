""" Strings and Files Template
    ** once you download this file - resave it as
    <yourname>StringsAndFiles.py
    This program has the menu completed for the assignments
    The menu works with both mouse or arrow key input
    Your task is to fill in the missing functions
"""

import pygame
import sys
import pygame_textinput  # need this for text input in pygame
import random
import math

# initialize pygame
pygame.init()

# set screen size
size = (800, 600)
screen = pygame.display.set_mode(size)
#------------------------methods--------------------------------------------
#menu function method
#prints menu selection and only exits after a choice has been made
def menu(titles):
    startY = 25
    spaceY = 33
    mainTitleFont = pygame.font.SysFont("arial", 72)
    buttonTitleFont = pygame.font.SysFont("arial", 24)
    selection = []
    rectWidth = 380
    rectHeight = 28
    x = int(screen.get_width()/2 - rectWidth/2)
    y = startY
    length = len(titles)
    num = 0
    hover = False
    # creates the Rects (containers) for the buttons
    for i in range (0,length,1):
        choiceRect = pygame.Rect(x,y,rectWidth,rectHeight)
        selection.append(choiceRect)
        y += spaceY


    #main loop in menu    
    go = True
    while go:    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                go = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    go = False
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_UP:
                    num -= 1                # if up arrow pressed move up one by changing num
                    if num < 0:             # make sure num doesn't go out of range
                        num = length-1
                elif event.key == pygame.K_DOWN:
                    num += 1                # if down arrow pressed move down by changing num
                    if num > length-1:      # make sure num doesn't go out of range
                        num = 0
                elif event.key == pygame.K_RETURN:
                    go = False              # if they hit Enter then exit the loop
            if event.type ==pygame.MOUSEMOTION:     # if mouse moved
                hover = False
                mx, my = pygame.mouse.get_pos()     # get the mouse position
                for i in range (length):            
                    if selection[i].collidepoint((mx,my)):  # check if x,y of mouse is in a button
                        num = i
                        hover = True
            if event.type == pygame.MOUSEBUTTONDOWN and hover == True:  #if mouse is in button
                go = False                                              # and has been clicked

        # draw all buttons                                                                
        for choice in selection:
            pygame.draw.rect(screen,RED,choice,0)
        
        # redraw selected button in another colour
        pygame.draw.rect(screen,GREEN,selection[num],0)
        
        # draw all the titles on the buttons
        x = int(screen.get_width()/2 - 150)
        y = startY
        for i in range(0,length,1):
            buttonTitle = buttonTitleFont.render(titles[i],True,WHITE)
            screen.blit(buttonTitle,(x,y))
            y += spaceY

        pygame.display.update()
    return num

# simply used anywhere in the program a pause is needed
def pause():
    go = True
    while go:    
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    go = False
       
        returnFont = pygame.font.SysFont('comicsansms',30)
        returnText = returnFont.render("Press Enter To Continue",True,RED)
        x = getHorizontalCentre(returnText)
        screen.blit(returnText, (x,400))
        pygame.display.update()

# to centre text horizontally
def getHorizontalCentre(textRendered):
    screenCentre = screen.get_width()/2
    textWidth = textRendered.get_width()/2
    x = int(screenCentre - textWidth)
    return x


# displays string to screen,  can add more choices if you like
# i.e. font size, colour, x position
def displayString(y,message):
    screen.fill(WHITE)        
    displayFont = pygame.font.SysFont("arial", 24)
    messageText = displayFont.render(message,True,BLACK)
    x = getHorizontalCentre(messageText)
    screen.blit(messageText,(x,y))
    pygame.display.update()
    pause()

def multiStringDisplay(y, dy, message):
    ## creat empty array
    array=[]
    ## set font, background colour and the message
    screen.fill(WHITE)        
    displayFont = pygame.font.SysFont("arial", 24)
    array.append(message.split('\n'))
    ##counting the amount of \n (newlines) there are and making a for loop to run that many times
    for i in range (message.count('\n')+1):
        ##setting the message to be equal to the array depending on which line it is on
        messageText = displayFont.render(str(array[0][i]),True,BLACK)
        x = getHorizontalCentre(messageText)
        ##putting it on screen
        screen.blit(messageText,(x,y))
        ##Moving it down so that it isn't all on one line
        y=y+dy
    pygame.display.update()
    pause()
    
def checkInt(number, message):

    while True:
        try:
            intNum = int(number)
            break
        except ValueError:
            number = getUserText(message)
    return intNum


# uses the pygame_textinput class to get user input (typed)
# after the user hits Enter it will return the string the user typed in
def getUserText(message):
    # Create TextInput-object
    textInput = pygame_textinput.TextInput()
    clock =pygame.time.Clock()
    go = True
    while go:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(WHITE)
        clock.tick(30)
       
        inputFont = pygame.font.SysFont('comicsansms',30)
        inputText = inputFont.render(message,True,RED)
        x = getHorizontalCentre(inputText)
        screen.blit(inputText, (x,300))

        # Blit its surface onto the screen
        screen.blit(textInput.get_surface(), (x,250))
        if textInput.update(events) == True:
            userInput =textInput.get_text()
            go = False
        pygame.display.update()

    return userInput

def openNewFile(fileName, readWrite):
    inputFont = pygame.font.SysFont('comicsansms',30)
    if readWrite == "read":
        io = "r"
    elif readWrite == "write":
        io = "w"

    while True:
        try:
            newFile = open(fileName, io)
            break
        except FileNotFoundError:
            screen.fill(WHITE)
            errorMessage = "Sorry, can't find: "+ fileName
            fileLine = inputFont.render(errorMessage,True,RED)
            screen.blit(fileLine, (100,200))
            pygame.display.update()
            pause()
            fileName = getUserText("Please input file name again")
    
    return newFile


# Array Functions----------------------------------------------------------
def enterInt():
    getInt = True
    array = []
    screen.fill(WHITE)
    displayString(100,"Enter positive integers, enter a negative one to end")
    while getInt == True:
        numStr = getUserText("Enter a positive integer (negative to end)")
        num = checkInt(numStr, "Sorry that's not an integer, try again")
        if num >= 0:
            array.append(num)
        else:
            getInt = False
    return array


def displayArray(array):
    message = ""
    length = len(array)
    if length != 0:
        for i in range(length):
            message = message + str(array[i]) + " "
    else: 
        message = "Please enter an array first"
    
    return message

def countIntegers(array):
    ##get length of array
    length = len(array)
    if length != 0:
        ##if the length does not equal 0 then display the length
        message = "There are " + str(length) + " integers in the array"
    ##else ask for them to enter an array first
    else: 
        message = "Please enter an array first"
    return message

def displayArrayReverse(array):
    ##get length
    length = len(array)
    ##check to make sure that the length is not 0
    if length != 0:
        ##reverses the list
        array.reverse()
        message = str(array)
    else: 
        message = "Please enter an array first"
    return message
    
def sumArray(array):
    ## get length
    length=len(array)
    ##empty variable for the sum
    sumA=0
    if length !=0:
        for i in range(length):
            ##add each number in array to sum verriable
            sumA=sumA+array[i]
        ##display sum
        message= 'The sum of the array is ' + str(sumA)
    else:
        message = 'Please entre an array first'
    return message

def averageArray(array):
    length=len(array)
    averageA=0
    if length !=0:
        for i in range(length):
            averageA=averageA+array[i]
        ##same as for sum just get it and divide by two and then use formating to only display 2 decimal places
        message= 'The sum of the array is ' + str("{:.2f}".format(averageA/len(array)))
    else:
        message = 'Please entre an array first'
    return message 

def findMaxMinArray(array):
    ##var for min(infinity)
    x=math.inf
    ##var for max(-infinity)
    y=-math.inf
    if len(array) != 0:
        for i in range (len(array)):
            ##run of all elemnts in array, if they are greater than the min var then it is new max
            if int(array[i])<x:
                x=array[i]
            elif int(array[i])>y:
                y=array[i]
        message = 'The max of your array is ' + str(y) + ', the min is ' + str(x)
    else:
        message = 'no array'
    return message

def searchArray(array):
    message=''
    ##answer is false by default
    answer = "False"
    ##get num from user
    numStr = getUserText("Enter a positive integer to search for")
    ##check if it is in it, if it is then answer becmes true
    if len(array) != 0:
        for i in range (len(array)):
            if array[i]==int(numStr):
                answer="True"
        message = answer
    else:
        return 'no array'
    return message

def writeArrayToFile(array):
    ##get file name
    numStr = getUserText("Enter the desired file name (include the extension) ")
    ##open file
    file=open(numStr, 'w+')
    ##write array to file
    for i in range(len(array)):
        file.write(str(array[i])+" ")
    file.close()
    
    ## don't forget to close the file after you are done

def readArrayFromFile():
    ##empty array
    array = []
    ##get file from user
    numStr = getUserText("Enter the desired file ")
    file=open(numStr, 'r')
    ##open file and split it into lines and words
    for line in file:
        line=line.split()
        for word in line:
            ##add each word to array
            array.append(int(word))
    return array
    file.close()
    # return the array when you are done

def searchAndReplace(array):
    message=''
    if len(array) != 0:
        try:
            ##ask for old and new int
            old = int(getUserText("Old num "))
            new = int(getUserText("New num "))
            ##run through and remoe old int
            ##replace new int in its spot
            for i in range(len(array)):
                if array[i]==old:
                    array.remove(old)
                    array.insert(i, new)
            message = str(array)

        except:
            message = 'unable to execute'
    else:
        message = 'no array'
    return message


def shuffleArray(array):
    ##run as many times as array is long
    if len(array) != 0:
        for i in range(len(array)):
            ##var = current array value
            x=int(array[i])
            ##get a random number between 0 and length of array
            loc=random.randint(0,len(array))
            ##remove x from its position
            array.remove(x)
            ##insert x at new random position
            array.insert(loc,x)
        message = str(array)
    else:
        message = 'no array'
    return message
    #remember don't use the built in shuffle command


def countWordsInFile():
    ##array for words
    words=[]
    ##array for num of words 
    count=[]
    ##array for end string 
    string=''
    ##get user file
    numStr = getUserText("Enter the desired file ")
    ##open it 
    file=open(numStr, 'r')
    ##go into file line by line and append the words to array
    for line in file:
        line=line.split()
        for word in line:
            ##counter object
            x=0
            ##string the words of punctuation
            word=word.strip(',').strip('.').strip('?').strip('!')
            ##if array is empty add the word 
            if words==[]:
                words.append(word)
                count.append(1)
            ##if it is greater than 1
            else:
                ##for the length of the array of words 
                for i in range (len(words)):
                    ##varriable that counts how many times each word appears
                    y=1
                    ##check if the word is already in the array if not then add it 
                    if word != words[i]:
                        x=x+1
                    ##counting how many times each word appeards and adding it to the count array
                    if word == words[i]:
                        y=y+1
                    if y > 1:
                        count.insert(i,y)
                ##add word to words array and add 1 to count array
                if x == len(words):
                    words.append(word)
                    count.append(1)
        ##puting it all together into a single string 
        for i in range (len(words)):
            string=string + words[i] + ':' + ' ' + str(count[i]) + '\n'
    ##using my custom display function to display on seperate lines 
    multiStringDisplay(150,25, string)            
    
    #you need to plan this one out before you code
    # create two arrays,  one for the words and one for the number of occurances of the word


def addToArray(array):
    ##get the number to add
    numStr = int(getUserText("Enter the number "))
    ##append the number
    array.append(numStr)
    return str(array)

def arrayInsert(array):
    ##get the number from user 
    numStr = int(getUserText("Enter the number "))
    ##get the position where they want to put it
    index = int(getUserText("Where would you like it to be (0 being the first position) "))
    try:
        ##insert what they want where they want it 
        array.insert(index, numStr)
    except:
        return 'unable to insert at that index'
    return str(array)

def remove(array):
    ##get the number they wish to remove
    numStr = int(getUserText("Enter the number "))
    ##count how many tims it appears and remove it that many times 
    count=array.count(numStr)
    if len(array) != 0:
        for i in range(count):
            array.remove(numStr)
    else:
        return 'no array'
    return str(array)



# main program -----------------------------------------------------------

# colours
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0,0,255)

# titles for  menu
menuMain = ["Enter Integers","Display Array","Count Integers In Array","Display Array In Reverse","Sum Integers in Array","Find Average of Array Integers","Find Max and Min","Search for Integer","Write Array to File","Fill Array from File","Search and Replace Integer","Shuffle the Array","Count Words in File","Add To Array", "Insert In Array", "Remove From Array","QUIT"]

screen.fill(WHITE)

mainMenu = True
newArray = []
newString = ""
# main loop
main = True
while main:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main = False

    screen.fill(WHITE)

    # for main menu, this menu selects the submenu or quits program
    # call string menu to display it and choose an option
    choose = menu(menuMain)
    # the last option returns to main menu
    if choose == len(menuMain)-1:
        main = False
        
    else:
        if choose == 0:  # option to get user input
            newArray = enterInt()
        elif choose == 1: # option for countCharacters funtion
            newString = displayArray(newArray)
        elif choose == 2:  # option for switchFirstAndLast function
            newString = countIntegers(newArray)
        elif choose == 3: # opton to reverse the list
            newString = displayArrayReverse(newArray)
        elif choose == 4: # option to find the sum of the array
            newString = sumArray(newArray)
        elif choose == 5: # option to get the average of the numbers in the array
            newString = averageArray(newArray)
        elif choose == 6: # option to find the max of the array
            newString = findMaxMinArray(newArray)
        elif choose == 7: # option to find out if a certain number is in the array
            newString = searchArray(newArray)
        elif choose == 8: # option to write your array to a file
            writeArrayToFile(newArray)
            newString = 'It has been done'
        elif choose == 9: # option to fill your array from a file 
            newArray = readArrayFromFile()
            newString = str(newArray)
        elif choose == 10: # option to search array for a number and replace it with another
            newString = searchAndReplace(newArray)
        elif choose == 11: # option to shuffle the array
            newString = shuffleArray(newArray)
        elif choose ==12: # option to count how many time the word apears in the file
            newString = countWordsInFile()
        elif choose ==13: # option to add to the end of the array
            newString = addToArray(newArray)
        elif choose ==14: # option to insert a number into the middle of the array
            newString = arrayInsert(newArray)
        elif choose ==15: # option to remove all occurances of a number from the array
            newString = remove(newArray)
        # choose cannot equal 12 because that function will already display it for me, this is so I dont have and empty screen
        if choose !=12:
        #display result of function
            displayString(150, newString)
            newString = ""
                         
    pygame.display.update()

pygame.QUIT
sys.exit()

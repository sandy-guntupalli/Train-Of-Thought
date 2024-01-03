from cmu_graphics import *
import math
import random
from PIL import Image
import os, pathlib 

###WELCOME TO TRAIN OF THOUGHT :)

def onAppStart(app):
###VARIABLES FOR THE BOARD
   app.width = 800
   app.height = 800
   app.rows = 20
   app.cols = 20
   app.margin = 5
   app.boardLeft = 0
   app.boardTop = 0
   app.boardWidth = app.width
   app.boardHeight = app.height
   app.cellBorderWidth = 1
   #paths for easy game
   app.board = [[0 for col in range(app.cols)] for row in range(app.rows)]  
###INITIALIZE RANDOM POSITIONS AND FIND VALID PATH
   randomHousePositions(app)
###VARIABLES FOR THE GAME
   #keep track of the score
   app.score = 0
   app.overallscore = 0
   app.maxScore = 5
   app.scoreG = 0
   app.scoreB = 0
   app.scorePi = 0
   app.scorePu = 0
   randomCounts(app)
   app.wrongTrains = 0
   app.wrongTrains1 = 0
   app.rightTrains = 0
   app.numTrains = 100
   #trains for easy game
   app.trains1 = [] 
   #trains for hard game
   app.trains2 = [] 
   app.trainIndex = 0
   #colors of the transition pieces for the game
   app.movePieceColor = None
   app.movePieceColor1 = None
   app.movePieceColor2 = None
   app.movePieceColor3 = None
   app.timeElapsed = 0
   #speeds for movement of trains
   app.speed = 0.175
   app.speed1 = 0.165
   app.speedBefore = 0
   app.delay1 = 70
   app.delay2 = 55
   #FEATURES VARIABLES
   app.slowSpeed = 0
   app.stepsPerSecond = 50
   app.playerAssist = False
   app.hardLevel = 1
   app.levelUp = False
   app.message = 'Level Up Level Up Level Up '
   app.charsPerLine = 27
   app.rainbow_colors = [
        'lightSalmon', 'darkSalmon', 'lightCoral', 'salmon', 'crimson', 'red',
        'fireBrick', 'darkRed', 'lightSalmon', 'coral', 'tomato', 'orange',
        'darkOrange', 'orangeRed', 'yellow', 'darkKhaki', 'gold', 'yellowGreen',
    'chartreuse', 'springGreen', 'green', 'darkGreen', 'lightSeaGreen',
    'deepSkyBlue', 'dodgerBlue', 'blue', 'mediumSlateBlue', 'darkSlateBlue',
    'purple', 'darkOrchid', 'darkMagenta', 'mediumVioletRed', 'hotPink',
    'deepPink', 'lightPink']
   app.cxStart = 800
   app.shift = 0
   app.snowflakePositions = generateRandomPositions(app, 100)
   # Snowflake feature variables
   app.snowflakeFeatureActive = False
   app.snowflakeCell = random.choice(findTrainPath(app.board, (2, 18), (app.randomRowM1, app.randomColM1)) + findTrainPath(app.board, (app.randomRowM1, app.randomColM1), (app.randomRowM2, app.randomColM2)) + findTrainPath(app.board, (app.randomRowM2, app.randomColM2), (app.randomRowM3, app.randomColM3)))
   app.snowflakeCell2 = random.choice(findTrainPath(app.board, (2, 18), (app.randomRowM, app.randomColM)))
   app.snowflakeButton = False
   app.angle = 0
   app.snowflakeButtonTimer = 0
   app.snowflakeFeatureDuration = 0
   app.celebration = False
   app.celebrationDuration = 0
###ALL OF THE IMAGES FOR THE GAMES
   #used the gif module from piazza 
   myGif = Image.open('images/cheering.gif')
   app.spriteList = []
   for frame in range(myGif.n_frames):
    #Set the current frame
    myGif.seek(frame)
    #Resize the image
    fr = myGif.resize((myGif.size[0]//2, myGif.size[1]//2))
    #Convert to CMUImage
    fr = CMUImage(fr)
    #Put in our sprite list
    app.spriteList.append(fr)
   app.spriteCounter = 0
   # Learned how to use images through PILS demo in Piazza
   #Source: https://www.google.com/url?sa=i&url=http%3A%2F%2Fwww.clker.com%2Fclipart-green-house-2.html&psig=AOvVaw3BNU4BsFGG_VXXbgjqXnHK&ust=1701469285841000&source=images&cd=vfe&ved=0CBQQjhxqFwoTCMC6spXh7IIDFQAAAAAdAAAAABAE
   app.greenimage = Image.open("images/green-house-hi2.png")
   app.greenimage = CMUImage(app.greenimage)
   #Source: https://www.google.com/url?sa=i&url=http%3A%2F%2Fwww.clker.com%2Fclipart-blue-house-3.html&psig=AOvVaw3aMTLPMSdVjs-UCE_f_722&ust=1701469303726000&source=images&cd=vfe&ved=0CBQQjhxqFwoTCOCjpp_h7IIDFQAAAAAdAAAAABAE
   app.blueimage = Image.open("images/blue-house-hi2.png")
   app.blueimage = CMUImage(app.blueimage)
   #drew this image myself in adobe app.random_rowM + 1, 15spark
   app.stationimage = Image.open("images/train-station.png")
   app.stationimage = CMUImage(app.stationimage)
   #Source: https://www.google.com/url?sa=i&url=http%3A%2F%2Fwww.clker.com%2Fclipart-purple-house-3.html&psig=AOvVaw2GZaVX6vVTP53nFUtnMUK5&ust=1701469177379000&source=images&cd=vfe&ved=0CBQQjhxqFwoTCJD27-Dg7IIDFQAAAAAdAAAAABAE
   app.purpleimage = Image.open("images/purple-house.png")
   app.purpleimage = CMUImage(app.purpleimage)
   #Source: https://www.google.com/url?sa=i&url=http%3A%2F%2Fwww.clker.com%2Fclipart-pink-house-5.html&psig=AOvVaw2l0F0bcXaDrJlNpbSoULR-&ust=1701469238316000&source=images&cd=vfe&ved=0CBQQjhxqFwoTCJDqmf7g7IIDFQAAAAAdAAAAABAE
   app.pinkimage = Image.open("images/pink-house.png")
   app.pinkimage = CMUImage(app.pinkimage)
   #made this image myself in adobe spark
   app.snowflakeimage = Image.open("images/snowflake.png")
   app.snowflakeimage = CMUImage(app.snowflakeimage)
   #made the instructions myself in adobe spark
   app.instructionsimage = Image.open("images/instructions.png")
   app.instructionsimage = CMUImage(app.instructionsimage)
   #made the instructions myself in adobe spark
   app.assistimage = Image.open("images/playerAssist.png")
   app.assistimage = CMUImage(app.assistimage)
#---------------------------------------------------------------------------------------------------------------------------------------------------------

#Learned how to use screens through screens demo in Piazza

#THIS IS THE WELCOME SCREEN
def welcome_redrawAll(app):
    drawLabel("Train of Thought", app.width/2, app.height/2 - 200, size = 90)
    drawRect(app.width//2 - 200, app.height//2, 400, 100, fill = 'orange')
    drawLabel("Play", app.width/2, app.height/2 + 50, size = 50)

def welcome_onMousePress(app, mouseX, mouseY):
    x0 = app.width//2 - 200
    y0 = app.height//2
    x1 = app.width
    y1 = app.height - 300
    if (x0 <= mouseX <= x1) and (y0 <= mouseY <= y1):
        setActiveScreen('instructions')

#---------------------------------------------------

#THIS IS THE INSTRUCTIONS SCREEN
def instructions_redrawAll(app):
    drawImage(app.instructionsimage, 0, 0, width=800, height=800)
    drawLabel("Press the enter key to Get Started", app.width/2, app.height/2 + 370, size = 30)

def instructions_onKeyPress(app, key):
    if key in 'enter':
        setActiveScreen('levels')

#---------------------------------------------------

#THIS IS THE LEVELS SCREEN
def levels_redrawAll(app):
    drawLabel("Choose Your Level", app.width/2, app.height/2 - 200, size=70)
    
    # Easy button
    drawRect(app.width//2 - 200, app.height//2, 200, 50, fill='orange')
    drawLabel("Easy", app.width/2 - 95, app.height/2 + 20, size=30)
    
    # Hard button
    drawRect(app.width//2 + 10, app.height//2, 200, 50, fill='orange')
    drawLabel("Hard", app.width/2 + 105, app.height/2 + 20, size=30)

def levels_onMousePress(app, mouseX, mouseY):
    easy_x0 = app.width//2 - 200
    easy_y0 = app.height//2
    easy_x1 = app.width//2 - 200 + 200
    easy_y1 = app.height//2 + 50
    
    hard_x0 = app.width//2 + 10
    hard_y0 = app.height//2
    hard_x1 = app.width//2 + 10 + 200
    hard_y1 = app.height//2 + 50

    if easy_x0 <= mouseX <= easy_x1 and easy_y0 <= mouseY <= easy_y1:
        generateTrains1(app, app.numTrains)
        setActiveScreen('game')

    elif hard_x0 <= mouseX <= hard_x1 and hard_y0 <= mouseY <= hard_y1:
        generateTrains2(app, app.numTrains)
        setActiveScreen('hardGame')

#---------------------------------------------------

#THIS IS THE GAME OVER SCREEN
def gameover_redrawAll(app):
    drawLabel("Game Over", app.width/2, app.height/2 - 200, size=70)

    # Display the score
    drawLabel(f"Your Score: {app.score}", app.width/2, app.height/2 - 100, size=30)

    drawLabel("Too many wrong answers!", app.width/2, app.height/2 - 50, size=30, fill='red')

    # Draw a button to go back to levels
    drawRect(app.width//2 - 100, app.height//2 + 50, 200, 50, fill='orange')
    drawLabel("Back to Levels", app.width/2, app.height//2 + 75, size=20)

def gameover_onMousePress(app, mouseX, mouseY):
    button_x0 = app.width//2 - 100
    button_y0 = app.height//2 + 50
    button_x1 = app.width//2 + 100
    button_y1 = app.height//2 + 100

    if button_x0 <= mouseX <= button_x1 and button_y0 <= mouseY <= button_y1:
        #RESET ALL OF THE VARIABLES
        app.trains1.clear()
        app.trains2.clear()
        app.wrongTrains = 0
        app.wrongTrains1 = 0
        app.speed = 0.175
        app.speed1 = 0.165
        app.speedBefore = 0
        app.delay1 = 70
        app.delay2 = 55
        app.rightTrains = 0
        app.score = 0
        app.overallscore = 0
        app.timeElapsed = 0 
        app.snowflakeFeatureActive = False
        app.levelUp = False
        app.playerAssist = False
        app.snowflakeFeatureTimer = 0
        randomHousePositions(app)
        app.maxScore = 7
        randomCounts(app)
        app.movePieceColor = None
        app.movePieceColor1 = None
        app.movePieceColor2 = None
        app.movePieceColor3 = None
        #Go back to the levels screen
        setActiveScreen('levels')

#---------------------------------------------------------------------------------------------------------------------------------------------------------

###FUNCTIONS FOR BOTH OF THE GAMES !!!!

###This generates all of the random house positions and finds a valid path to them, 
###It regenerates the values until everything is valid and true
###Learned about try and except when trying to learn about errors and how to prevent with randint
###https://www.w3schools.com/python/python_try_except.asp
Max = 1000
def randomHousePositions(app):
    attempts = 0
    while attempts < Max:
        try:
            app.randomRowM = random.randint(6, 16)
            app.randomColM = random.randint(7, 13)
            app.randomRowB = random.randint(app.randomRowM + 4, 17)
            app.randomColB = random.randint(1, app.randomColM - 3)
            app.randomRowG = random.randint(4, app.randomRowM - 2)
            app.randomColG = random.randint(2, app.randomColM - 3)
            app.randomRowM3 = random.randint(7, 10)
            app.randomColM3 = random.randint(5, 7)
            app.randomRowM2 = random.randint(7, 12)
            app.randomColM2 = random.randint(9, 12)
            app.randomRowM1 = random.randint(7, 13)
            app.randomColM1 = random.randint(14, 16)
            if app.randomRowM2 > app.randomRowM3:
                app.randomRowPink = random.randint(2, app.randomRowM3 - 3)
            else:
                app.randomRowPink = random.randint(2, app.randomRowM2 - 3)
            app.randomColPink = random.randint(app.randomColM3 + 2, app.randomColM2 - 2)
            app.randomRowG1 = random.randint(2, app.randomRowM3 - 4)
            app.randomColG1 = random.randint(app.rows - 19, app.cols - 17)
            app.randomRowB1 = random.randint(app.randomRowM3 + 3, 17)
            app.randomColB1 = random.randint(2, app.randomColM3 - 2)
            if app.randomRowM2 > app.randomRowM1:
                app.randomRowPurple = random.randint(app.randomRowM2 + 3, 17)
            else:
                app.randomRowPurple = random.randint(app.randomRowM1 + 5, 17)
            app.randomColPurple = random.randint(app.randomColM1 - 5, app.randomColM1 - 3)

            app.trainpath = [(2, 15)] + simplifyPath(findTrainPath(app.board, (2, 18), (app.randomRowM, app.randomColM)))
            app.bluepath = simplifyPath(findTrainPath(app.board, (app.randomRowM, app.randomColM), (app.randomRowB, app.randomColB)))
            app.greenpath = simplifyPath(findTrainPath(app.board, (app.randomRowM, app.randomColM), (app.randomRowG, app.randomColG)))
            app.bluepath2 = simplifyPath(findTrainPath(app.board, (app.randomRowM3, app.randomColM3), (app.randomRowB1, app.randomColB1)))
            app.greenpath2 = simplifyPath(findTrainPath(app.board, (app.randomRowM3, app.randomColM3), (app.randomRowG1, app.randomColG1)))
            app.purplepath = simplifyPath(findTrainPath(app.board, (app.randomRowM1, app.randomColM1), (app.randomRowPurple, app.randomColPurple)))
            app.pinkpath = simplifyPath(findTrainPath(app.board, (app.randomRowM2, app.randomColM2), (app.randomRowPink, app.randomColPink)))
            app.trainpath2 = [(2, 15)] + simplifyPath(findTrainPath(app.board, (2, 18), (app.randomRowM1, app.randomColM1)))
            app.trainpath3 = app.trainpath2 + simplifyPath(findTrainPath(app.board, (app.randomRowM1, app.randomColM1), (app.randomRowM2, app.randomColM2)))
            app.trainpath4 = app.trainpath3 + simplifyPath(findTrainPath(app.board, (app.randomRowM2, app.randomColM2), (app.randomRowM3, app.randomColM3)))

            if all(isinstance(value, int) for value in [app.randomRowM, app.randomColM, app.randomRowB, app.randomColB, app.randomRowG, app.randomColG, app.randomRowM3, app.randomColM3, app.randomRowM2, app.randomColM2, app.randomRowM1, app.randomColM1, app.randomRowPink, app.randomColPink, app.randomRowG1, app.randomColG1, app.randomRowB1, app.randomColB1, app.randomRowPurple, app.randomColPurple]):
                if all(isinstance(value, list) for value in [app.bluepath, app.greenpath, app.trainpath, app.bluepath2, app.greenpath2, app.purplepath, app.pinkpath, app.trainpath2, app.trainpath3, app.trainpath4]):
                    break  # Exit the loop if all conditions are met
        except (ValueError, TypeError):  # Catch specific exceptions that might occur
            pass
        attempts += 1

#---------------------------------------------------------------------------------------------------------------------------------------------------------
###This simplifies the path and finds just the main corner points
###This allows the train to move from one point to another with speed rather than moving step by step

def simplifyPath(path):
  if path == None:
    return None

  if len(path) < 3:
    return path

  for i in range(2, len(path)):
      first = path[i-2]
      middle = path[i-1]
      second = path[i]
    
      if (first[0] != middle[0] and first[1] == middle[1]) and (middle[0] == second[0] and middle[1] != second[1]) or (first[0] == middle[0] and first[1] != middle[1] and middle[0] != second[0] and middle[1] == second[1]):
        return [path[0]] + [middle] + [path[-1]]


  return [path[0]] + [path[-1]]
#---------------------------------------------------------------------------------------------------------------------------------------------------------

###This finds the shortest path from a start position to an end position
###Researched about BFS from this medium article and through the TP guide for pathfinding pdf document on website
#https://medium.com/omarelgabrys-blog/path-finding-algorithms-f65a8902eb40 researched about pathfinding strategies, BFS
def findTrainPath(board, startPosition, endPosition):
    #Initialize a queue containing the start position of the train
    queue = [(startPosition, [startPosition])]
    #Initialize a set marking which cells (nodes) are visited
    visited = set()
    while queue:
        #Get the current cell and the path taken so far from the front of the queue
        currentCell, path = queue.pop(0)
        #If the current cell is the target destination then we have a valid path
        if currentCell == endPosition:
            return path
        #Check if the current cell has been visited
        if currentCell in visited:
            continue
        #Otherwise mark the current cell as visited
        visited.add(currentCell)
        row, col = currentCell
        #All the moves to check each neighboring cell of the current cell
        moves = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
        for move in moves:
            newRow, newCol = move
            if 1 <= newRow <= 18 and 1 <= newCol <= 18:
                #Mark the neighboring cell as visited and update the path for the train
                #Now we move on to the neighboring cell
                newPath = path + [move]
                queue.append((move, newPath))
    return None

#---------------------------------------------------------------------------------------------------------------------------------------------------------  
###This allows us to put random counts on the train stiation which they have to fulfilll

def randomCounts(app):
    #random.randint(3, app.maxScore)
    app.scoreG = random.randint(4, app.maxScore)
    app.scoreB = random.randint(4, app.maxScore)
    app.scorePi = random.randint(4, app.maxScore)
    app.scorePu = random.randint(4, app.maxScore)

#---------------------------------------------------------------------------------------------------------------------------------------------------------  
###Drawing the Level UP
def levelUpDraw(app):
    char_width = 40  # Increase the width of each character
    letter_spacing = 60  # Adjust this value to control spacing between characters
    total_width = (len(app.message) * (char_width + letter_spacing) - letter_spacing)

    for i in range(len(app.message)):
        cx = (i + len(app.message) - app.shift) * (char_width + letter_spacing) % total_width
        charIndex = (i + app.shift) % len(app.message)
        rainbowColor = app.rainbow_colors[charIndex]
        drawLabel(app.message[charIndex], cx, app.height // 2, size=100, bold=True, fill=rainbowColor)

#---------------------------------------------------------------------------------------------------------------------------------------------------------  

###EASY GAME CODE

#---------------------------------------------------------------------------------------------------------------------------------------------------------

def game_redrawAll(app):
   drawRect(0, 0, app.width, app.height, fill='lightGreen')
   drawBoard(app)
   drawBoardBorder(app)
   drawTrainTracks(app)
   drawPiece(app)
   if app.snowflakeButton:
        snowflakeCell = app.snowflakeCell2
        if snowflakeCell is not None:
            cellRow, cellCol = snowflakeCell
            left, top = getCellLeftTop(app, cellRow, cellCol)
            width, height = getCellSize(app)
            drawImage(app.snowflakeimage, left-10, top-10, width=1.5*width, height=1.5*height)
   drawTrains1(app)
   drawImageCenteredOnCell2(app, 2,15, app.stationimage)
   drawScore(app)
   drawImageCenteredOnCell(app, app.randomRowB, app.randomColB, app.blueimage, app.scoreB)
   drawImageCenteredOnCell(app, app.randomRowG, app.randomColG, app.greenimage, app.scoreG)
   if app.playerAssist:
    drawSign(app)
   if app.levelUp:
    levelUpDraw(app)
    drawImage(app.spriteList[app.spriteCounter], 400, 280, align='center')
   if app.snowflakeFeatureActive:
    drawSnowflakes(app)
   pass

#---------------------------------------------------------------------------------------------------------------------------------------------------------

def game_onMousePress(app, mouseX, mouseY):
    clickedCell = getCell(app, mouseX, mouseY)

    #If the button is true make sure to initiate the feature
    if app.snowflakeButton:
        cellRow, cellCol = app.snowflakeCell2
        if clickedCell == (cellRow, cellCol):
            app.snowflakeFeatureActive = True
            app.snowflakeButton = False
            app.snowflakeDuration = 300
    #Don't let the trains change colors if train is on the click me piece
    if clickedCell != (app.randomRowM, app.randomColM):
        for train in app.trains1:
            if train.isGolden == False:
                train.changeColorOnClick(app, mouseX, mouseY)

    #Change the movePiece color if there is no player assist
    if not app.playerAssist:
        if clickedCell == (app.randomRowM, app.randomColM):
            app.movePieceColor = 'blue' if app.movePieceColor == 'green' else 'green'

#---------------------------------------------------------------------------------------------------------------------------------------------------------

def game_onStep(app):
    app.timeElapsed += 1
    num_trains = len(app.trains1)

    if app.rightTrains + app.wrongTrains != 0:
        app.overallscore = app.rightTrains / (app.rightTrains + app.wrongTrains)
    else:
        app.overallscore = 0 
    #Check if it's time to activate the snowflake feature
    if 0.7 < app.overallscore < 1 or app.score % 130 == 0 and app.score > 0 and app.playerAssist == False and app.levelUp == False:
        app.snowflakeButton = True
        app.snowflakeButtonTimer = 15
    
    #INITIATE THE SNOWFLAKE FEATURE
    if app.snowflakeFeatureActive:
        app.angle += 5
        app.speedBefore = app.speed
        app.speed = 0.095
    
    #INITIATE THE PLAYER ASSIST
    if 0 < app.overallscore < 0.6 or app.score % 150 == 0 and app.score > 0 and app.snowflakeFeatureActive == False and app.levelUp == False:
        app.playerAssist = True
        app.speedBefore = app.speed
        app.speed = 0.2
    
    #LEVEL UP
    if app.scoreG == 0 and app.scoreB == 0:
        app.levelUp = True
        app.speed = 0
        app.stepsPerSecond = 6
        app.spriteCounter = (app.spriteCounter + 1) % len(app.spriteList)
        app.shift = (app.shift + 1) % len(app.message)

    #MOVE THE TRAINS
    for i in range(num_trains):
        index = app.trainIndex + i
        if index < len(app.trains1) and app.timeElapsed > app.trains1[index].delay and app.timeElapsed % 0.5 == 0:
            train = app.trains1[index]
            moveTrain1(app, train)
    
    #DEACTIVATE THE SNOWFLAKE FEATURE
    if app.snowflakeFeatureActive:
        app.snowflakeButton = False
        app.snowflakeDuration -= 1
        if app.snowflakeDuration <= 0 or app.levelUp:
            # Deactivate the snowflake feature when the duration is over
            app.snowflakeFeatureActive = False
            app.snowflakeFeatureDuration = 0
            app.speed1 = app.speedBefore
    if app.snowflakeButton:
        app.snowflakeButtonTimer -= 1
        if app.snowflakeButtonTimer <= 0:
            app.snowflakeButton = False

    #DEACTIVATE PLAYER ASSIST
    if app.playerAssist and app.timeElapsed % (7 * app.stepsPerSecond) == 0 or app.levelUp:
        app.playerAssist = False
        app.speed = app.speedBefore

    #DEACTIVE LEVEL UP GIF
    if app.levelUp and app.timeElapsed % (10 * app.stepsPerSecond) == 0:
        app.levelUp = False
        app.maxScore += 5
        app.spriteCounter = 0
        randomCounts(app)
        app.hardLevel += 1
        app.speed = 0.165
        app.speed += 0.007 * app.hardLevel
        app.stepsPerSecond = 50

#---------------------------------------------------------------------------------------------------------------------------------------------------------
###This draws images centered on a cell so I don't have to position it 

def drawImageCenteredOnCell(app, row, col, image, score):
    left, top = getCellLeftTop(app, row, col)
    width, height = getCellSize(app)

    imageWidth = 220 
    imageHeight = 220 

    # Calculate the centered position
    imageCenterX = left + width / 2
    imageCenterY = top + height / 2

    # Adjust the position based on the size of the image
    image_left = imageCenterX - imageWidth / 2
    image_top = imageCenterY - height / 2 - imageHeight/2.2 

    drawImage(image, image_left, image_top, width=imageWidth, height=imageHeight)
    drawLabel(f"{score}", image_left + imageWidth/2, image_top + imageWidth/2, size = 30, fill = 'white', bold = True)

#---------------------------------------------------------------------------------------------------------------------------------------------------------
###These are all for OnStep and relate to the features

#sets custom delays for the trains, so that we can make things faster or slower generated
def setCustomDelays1(app, customDelay):
    for i in range(len(app.trains1)):
        app.trains1[i].delay = customDelay * i 


#Find the random positions for the snowflake feature
def generateRandomPositions(app, numPositions):
    positions = []
    for i in range(numPositions):
        row = random.randint(0, app.rows - 1)
        col = random.randint(0, app.cols - 1)
        positions.append((row, col))
    return positions

#Draw a Snowflake
def drawSnowflake(app, row, col, size):
    x, y = getCellLeftTop(app, row, col)

    #Draw a simple snowflake at the specified cell position with the given size
    drawLine(x - size, y, x + size, y, fill='white', rotateAngle=app.angle)
    drawLine(x, y - size, x, y + size, fill='white', rotateAngle=app.angle)
    drawLine(x - size / 1.4, y - size / 1.4, x + size / 1.4, y + size / 1.4, fill='white', rotateAngle=app.angle)
    drawLine(x - size / 1.4, y + size / 1.4, x + size / 1.4, y - size / 1.4, fill='white', rotateAngle=app.angle)

#Draw all of the snowflakes
def drawSnowflakes(app):
    if app.snowflakeFeatureActive:
        snowflakeSize = 15 
        for i in app.snowflakePositions:
            row, col = i
            drawSnowflake(app, row, col, snowflakeSize)


#---------------------------------------------------------------------------------------------------------------------------------------------------------
###ALL THINGS TRAINS

#Train Class
class Train1:
    def __init__(self, app, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.activePath = app.trainpath
        self.pathIndex = 0
        self.hasAssignedPath = False
        self.movedPastMovingPiece = False
        self.isGolden = False
    
    def changeColorOnClick(self, app, mouseX, mouseY):
        # Check if the mouse click is within the bounding box of the train
        left, top, right, bottom = self.getTrainBoundingBox(app)
        if left <= mouseX <= right and top <= mouseY <= bottom:
            # Change the color of the train
            self.color = random.choice(['blue', 'green'])

    def getTrainBoundingBox(self, app):
        # Helper method to get the bounding box of the train
        left, top = getCellLeftTop(app, self.row, self.col)
        width, height = getCellSize(app)
        return left, top, left + width, top + height

#Generate trains that come out of the station
def generateTrains1(app, num_trains):
    for i in range(num_trains):
        color = random.choice(['blue', 'green'])
        newTrain = Train1(app, 2, 15, color)
        app.trains1.append(newTrain)
        app.trains1[i].delay = i * app.delay1
        app.trains1[i].isGolden = random.random() < 0.2

#Code for Train Drawing
def drawTrain1(app, train):
    row, col = train.row, train.col
    left, top = getCellLeftTop(app, row, col)
    width, height = getCellSize(app)

    if train.isGolden:
        train.color = 'gold'
        # Draw the golden train with a different color or special appearance
        drawRect(left, top, width, height, fill='gold')

        # Draw windows on the train body, centered and spaced apart
        windowSize = width / 4
        windowSpacing = 10
        windowMargin = (width - 2 * windowSize - windowSpacing) / 2
        drawRect(left + windowMargin, top + height / 4, windowSize, windowSize, fill='white')
        drawRect(left + windowSize + 2 * windowSpacing, top + height / 4, windowSize, windowSize, fill='white')

        # Draw a topper (thin rectangle)
        drawRect(left, top, width, height/10, fill='black')

        # Draw the train wheels, bigger in size
        wheelRadius = width / 6
        drawCircle(left + width / 4, top + height, wheelRadius, fill='black')
        drawCircle(left + 3 * width / 4, top + height, wheelRadius, fill='black')

        # Draw an additional white circle inside each black wheel
        smallWheelRadius = wheelRadius / 2
        drawCircle(left + width / 4, top + height, smallWheelRadius, fill='white')
        drawCircle(left + 3 * width / 4, top + height, smallWheelRadius, fill='white')

        # drawImage(app.starimage, (left) + width/4 - 22, top + height/4 - 60, width = 70, height = 70)
        drawStar(left + width/2, top+height/2 - 40, 17, 5, fill='yellow', border='black')

    else:
        # Draw the train body
        drawRect(left, top, width, height, fill=train.color)

        # Draw windows on the train body, centered and spaced apart
        windowSize = width / 4
        windowSpacing = 10
        windowMargin = (width - 2 * windowSize - windowSpacing) / 2
        drawRect(left + windowMargin, top + height / 4, windowSize, windowSize, fill='white')
        drawRect(left + windowSize + 2 * windowSpacing, top + height / 4, windowSize, windowSize, fill='white')

        # Draw a topper (thin rectangle)
        drawRect(left, top, width, height/10, fill='black')

        # Draw the train wheels, bigger in size
        wheelRadius = width / 6
        drawCircle(left + width / 4, top + height, wheelRadius, fill='black')
        drawCircle(left + 3 * width / 4, top + height, wheelRadius, fill='black')

        # Draw an additional white circle inside each black wheel
        smallWheelRadius = wheelRadius / 2
        drawCircle(left + width / 4, top + height, smallWheelRadius, fill='white')
        drawCircle(left + 3 * width / 4, top + height, smallWheelRadius, fill='white')

#Draw all the trains in the app.trains1 list
def drawTrains1(app):
    for train in app.trains1:
        drawTrain1(app, train)

#Draw all of the tracks
def drawTrainTracks(app):
    path = [(2, 15), (2, 16), (2, 17)] + findTrainPath(app.board, (2, 18), (app.randomRowM, app.randomColM)) + findTrainPath(app.board, (app.randomRowM, app.randomColM), (app.randomRowB, app.randomColB)) + findTrainPath(app.board, (app.randomRowM, app.randomColM), (app.randomRowG, app.randomColG))
    for i in path:
        row, col = i
        drawCell(app, row, col, 'saddleBrown')
    
    path = findTrainPath(app.board, (app.randomRowM, app.randomColM), (app.randomRowB, app.randomColB)) + findTrainPath(app.board, (app.randomRowM, app.randomColM), (app.randomRowG, app.randomColG))
    for i in path:
        row, col = i
        drawCell(app, row, col, 'sienna')

#---------------------------------------------------------------------------------------------------------------------------------------------------------
###MOVING THE TRAINS AND CORRESPONDING FUNCTIONS

#Move the trains accordingly
def moveTrain1(app, train):
    if train.pathIndex < len(train.activePath):
        #get the next position
        nextPosition = train.activePath[train.pathIndex]
        nextRow, nextCol = nextPosition
        currentRow, currentCol = train.row, train.col

        #swift movement
        deltaRow = app.speed * (nextRow - currentRow)
        deltaCol = app.speed * (nextCol - currentCol)

        train.row += deltaRow
        train.col += deltaCol

        #Check if the train has reached the next point of the path
        if math.isclose(train.row, nextRow, abs_tol=0.01) and math.isclose(train.col, nextCol, abs_tol=0.01):
            train.pathIndex += 1

    #Check if we are on the move Piece
    targetRow, targetCol = app.randomRowM, app.randomColM
    if math.isclose(train.row, targetRow, abs_tol=0.01) and math.isclose(train.col, targetCol, abs_tol=0.01):
        train.movedPastMovingPiece = True
        if app.playerAssist:
            app.movePieceColor = train.color
        switchTrainPath(app, train)
    
    #if There is player assist, control their paths
    if app.playerAssist:
         controlTrainPath(app, train)
    else:
         app.playerAssist = False

    #Control all the scoring features and variables
    if train.pathIndex == len(train.activePath):
        app.wrongGreen = False
        app.wrongBlue = False
        app.trains1.remove(train)
        if train.color == 'green' and train.activePath[-1] == app.greenpath[-1]:
            if app.scoreG == 0:
                app.scoreG = 0
            else:
                app.scoreG -= 1
            app.score += 10
            app.rightTrains += 1
        elif train.color == 'blue' and train.activePath[-1] == app.bluepath[-1]:
            if app.scoreB == 0:
                app.scoreB = 0
            else:
                app.scoreB -= 1
            app.score += 10
            app.rightTrains += 1
        elif train.color == 'green' and train.activePath[-1] == app.bluepath[-1]:
            app.wrongTrains += 1
            app.score += 0
        elif train.color == 'blue' and train.activePath[-1] == app.greenpath[-1]:
            app.wrongTrains += 1
            app.score += 0
        elif train.isGolden and train.activePath[-1] == app.greenpath[-1]:
            if app.scoreG == 0:
                app.scoreG = 0
            else:
                app.scoreG -= 1
            app.score += 50
            app.rightTrains += 1
        elif train.isGolden and train.activePath[-1] == app.bluepath[-1]:
            if app.scoreB == 0:
                app.scoreB = 0
            else:
                app.scoreB -= 1
            app.score += 50
            app.rightTrains += 1
        else:
            app.score += 0
            app.wrongTrains += 0
    if app.wrongTrains > 10:
        setActiveScreen('gameover')

#SWITCHES THE PATH BASED ON THE MOVEPIECE COLOR
def switchTrainPath(app, train):
    if train.movedPastMovingPiece and not train.hasAssignedPath and not app.playerAssist:
        if app.movePieceColor == 'blue' and app.bluepath not in train.activePath and app.greenpath not in train.activePath:
            #Append the blue path
            train.activePath = app.trainpath + app.bluepath
            train.hasAssignedPath = True  #Set the flag to True once the train has been assigned a path
        elif app.movePieceColor == 'green' and app.greenpath not in train.activePath and app.bluepath not in train.activePath:
            #Append the greenpath
            train.activePath = app.trainpath + app.greenpath
            train.hasAssignedPath = True  #Set the flag to True once the train has been assigned a path

#PLAYER ASSIST FEATURE FOR CONTROLLING PATH
def controlTrainPath(app, train):
    targetRow, targetCol = app.randomRowM, app.randomColM
    if math.isclose(train.row, targetRow, abs_tol=0.01) and math.isclose(train.col, targetCol, abs_tol=0.01):
        app.movePieceColor = train.color
    if app.movePieceColor == 'blue' and app.bluepath not in train.activePath and app.greenpath not in train.activePath:
        #append the blue path
        train.activePath = app.trainpath + app.bluepath
    elif app.movePieceColor == 'green' and app.bluepath not in train.activePath and app.greenpath not in train.activePath:
        #append the green path
        train.activePath = app.trainpath + app.greenpath
    elif train.color == 'gold':
        #randomly choose green or blue path
        app.movePieceColor = random.choice(['blue', 'green'])
        if app.movePieceColor == 'blue' and app.bluepath not in train.activePath and app.greenpath not in train.activePath:
            train.activePath = app.trainpath + app.bluepath
        elif app.movePieceColor == 'green' and app.bluepath not in train.activePath and app.greenpath not in train.activePath:
            train.activePath = app.trainpath + app.greenpath

#---------------------------------------------------------------------------------------------------------------------------------------------------------

#Drawing the Moving Piece
def drawPiece(app):
    left, top = getCellLeftTop(app, app.randomRowM, app.randomColM)
    width, height = getCellSize(app) 
    if app.movePieceColor == 'blue':
        drawCell(app, app.randomRowM, app.randomColM, 'white')
        drawTrainTracks3(app,findTrainPath(app.board, (app.randomRowM, app.randomColM), (app.randomRowB, app.randomColB)))
        drawLine(left, top + height/2, left + width, top + height/2, arrowStart=False, arrowEnd=True)
    elif app.movePieceColor == 'green':
        drawCell(app, app.randomRowM, app.randomColM, 'white')
        drawTrainTracks3(app, findTrainPath(app.board, (app.randomRowM, app.randomColM), (app.randomRowG, app.randomColG)))
        drawLine(left + width, top + height/2, left, top + height/2, arrowStart=False, arrowEnd=True)
    elif app.movePieceColor == 'control':
        drawCell(app, app.randomRowM, app.randomColM, 'saddleBrown')
    else:
        drawCell(app, app.randomRowM, app.randomColM, "purple")
        drawLabel("Click Me", left + width/2, top + height/2, size=14, bold=True, fill="white")

#Drawing the Score Box
def drawScore(app):
    scoreBoxWidth = 150
    scoreBoxHeight = 60
    margin = 10
    scoreBoxLeft = app.width - scoreBoxWidth - margin
    scoreBoxTop = app.height - scoreBoxHeight - margin

    drawRect(scoreBoxLeft, scoreBoxTop, scoreBoxWidth, scoreBoxHeight, fill='white', borderWidth=2)

    drawLabel(f"Score: {app.score}", scoreBoxLeft + scoreBoxWidth/2, scoreBoxTop + scoreBoxHeight/2, size=18, bold=True)
    drawLabel(f"Level {app.hardLevel}", scoreBoxLeft + scoreBoxWidth/2, scoreBoxTop - 15, size=18, bold=True)

#---------------------------------------------------------------------------------------------------------------------------------------------------------

###CREATION OF THE BOARD 
def drawBoard(app):
   for row in range(app.rows):
       for col in range(app.cols):
           drawCell(app, row, col, None)
   pass

def drawBoardBorder(app):
   drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
            fill=None, border='black',
            borderWidth=2*app.cellBorderWidth)


def drawCell(app, row, col, color):
   cellLeft, cellTop =  getCellLeftTop(app, row, col)
   cellWidth, cellHeight = getCellSize(app)
   drawRect(cellLeft, cellTop, cellWidth, cellHeight,
            fill=color)

def getCellLeftTop(app, row, col):
   cellWidth, cellHeight = getCellSize(app)
   cellLeft = app.boardLeft + cellWidth*row
   cellTop = app.boardTop + cellHeight*col
   return (cellLeft, cellTop)

def getCellSize(app):
   cellWidth = app.boardWidth / app.rows
   cellHeight = app.boardHeight / app.cols
   return (cellWidth, cellHeight)

def getCell(app, x, y):
   dx = x - app.boardLeft
   dy = y - app.boardTop
   cellWidth, cellHeight = getCellSize(app)
   row = math.floor(dx/cellWidth)
   col = math.floor(dy/cellHeight)
   if (0 <= row < app.rows) and (0 <= col < app.cols):
     return (row, col)
   else:
     return None

#---------------------------------------------------------------------------------------------------------------------------------------------------------

###HARD GAME CODE

#---------------------------------------------------------------------------------------------------------------------------------------------------------

def hardGame_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill='lightGreen')
    drawTrainTracks2(app)
    drawMovePiece1(app)
    drawMovePiece2(app)
    drawMovePiece3(app)
    if app.snowflakeButton:
        snowflakeCell = app.snowflakeCell
        if snowflakeCell is not None:
            cellRow, cellCol = snowflakeCell
            left, top = getCellLeftTop(app, cellRow, cellCol)
            width, height = getCellSize(app)
            drawImage(app.snowflakeimage, left-10, top-10, width=1.5*width, height=1.5*height)
    drawTrains2(app)
    drawScore1(app)
    drawImageCenteredOnCell2(app, 2, 15, app.stationimage)
    drawImageCenteredOnCell1(app, app.randomRowG1, app.randomColG1, app.greenimage, app.scoreG)
    drawImageCenteredOnCell1(app, app.randomRowB1, app.randomColB1, app.blueimage, app.scoreB)
    drawImageCenteredOnCell1(app, app.randomRowPurple, app.randomColPurple, app.purpleimage, app.scorePu)
    drawImageCenteredOnCell1(app, app.randomRowPink, app.randomColPink, app.pinkimage, app.scorePi)
    if app.playerAssist:
        drawSign(app)
    if app.levelUp:
        levelUpDraw(app)
        drawImage(app.spriteList[app.spriteCounter], 400, 280, align='center')
    if app.snowflakeFeatureActive:
        drawSnowflakes(app)
    pass

#---------------------------------------------------------------------------------------------------------------------------------------------------------

def hardGame_onMousePress(app, mouseX, mouseY):
    clickedCell = getCell(app, mouseX, mouseY)
    if app.snowflakeButton:
        cellRow, cellCol = app.snowflakeCell
        if clickedCell == (cellRow, cellCol):
            app.snowflakeFeatureActive = True
            app.snowflakeButton = False
            app.snowflakeDuration = 300
    if clickedCell != (app.randomRowM1, app.randomColM1) and clickedCell != (app.randomRowM2, app.randomColM2) and clickedCell != (app.randomRowM3, app.randomColM3):
        for train in app.trains2:
            if train.isGolden == False:
                train.changeColorOnClick(app, mouseX, mouseY)
    if not app.playerAssist:
        if clickedCell == (app.randomRowM1, app.randomColM1):
            if app.movePieceColor1 == None:
                app.movePieceColor1 = 'purple'
            else:
                app.movePieceColor1 = None
        elif clickedCell == (app.randomRowM2, app.randomColM2):
            if app.movePieceColor2 == None:
                app.movePieceColor2 = 'pink'
            else:
                app.movePieceColor2 = None
        elif clickedCell == (app.randomRowM3, app.randomColM3):
            app.movePieceColor3 = 'blue' if app.movePieceColor3 == 'green' else 'green'

#---------------------------------------------------------------------------------------------------------------------------------------------------------

def hardGame_onStep(app):
    app.timeElapsed += 1
    num_trains = len(app.trains2)

    if app.rightTrains + app.wrongTrains != 0:
        app.overallscore = app.rightTrains / (app.rightTrains + app.wrongTrains)
    else:
        app.overallscore = 0

    #INITIATE THE SNOWFLAKE BUTTON
    if 0.3 < app.overallscore < 1 or app.score % 120 == 0 and app.score > 0 and app.playerAssist == False and app.levelUp == False:
        app.snowflakeButton = True
        app.snowflakeButtonTimer = 15
    
    #INITIATE THE SNOWFLAKE FEATURE
    if app.snowflakeFeatureActive:
        app.angle += 5
        app.speedBefore = app.speed1
        app.speed1 = 0.095

    #INITIATE THE PLAYER ASSIST
    if 0 < app.overallscore < 0.6 or app.score % 150 == 0 and app.score > 0 and app.snowflakeFeatureActive == False and app.levelUp == False:
        app.playerAssist = True
        app.speedBefore = app.speed1
        app.speed1 = 0.2
    
    #INITIATE THE LEVELUP
    if app.scoreG == 0 and app.scoreB == 0 and app.scorePi == 0 and app.scorePu == 0:
        app.levelUp = True
        app.speed1 = 0
        app.stepsPerSecond = 6
        app.spriteCounter = (app.spriteCounter + 1) % len(app.spriteList)
        app.shift = (app.shift + 1) % len(app.message)

    #Move trains
    for i in range(num_trains):
        index = app.trainIndex + i
        if index < len(app.trains2) and app.timeElapsed > app.trains2[index].delay and app.timeElapsed % 0.5 == 0:
            train = app.trains2[index]
            moveTrain2(app, train)
    #if the feature is active make the button dissapear
    if app.snowflakeFeatureActive:
        app.snowflakeButton = False
        app.snowflakeDuration -= 1
        if app.snowflakeDuration <= 0 or app.levelUp:
            # Deactivate the snowflake feature when the duration is over
            app.snowflakeFeatureActive = False
            app.snowflakeFeatureDuration = 0
            app.speed1 = app.speedBefore
    if app.snowflakeButton:
        app.snowflakeButtonTimer -= 1
        if app.snowflakeButtonTimer <= 0:
            app.snowflakeButton = False

    # Handle player assist
    if app.playerAssist and app.timeElapsed % (7 * app.stepsPerSecond) == 0 or app.levelUp:
        app.playerAssist = False
        app.speed1 = app.speedBefore

    # Handle level up timing
    if app.levelUp and app.timeElapsed % (10 * app.stepsPerSecond) == 0:
        app.levelUp = False
        app.maxScore += 5
        app.spriteCounter = 0
        randomCounts(app)
        app.hardLevel += 1
        app.speed1 = 0.165
        app.speed1 += 0.007 * app.hardLevel
        app.delay2 += 25
        app.stepsPerSecond = 50

#---------------------------------------------------------------------------------------------------------------------------------------------------------
###This draws images centered on a cell so I don't have to position it 

def drawImageCenteredOnCell1(app, row, col, image, score):
    left, top = getCellLeftTop(app, row, col)
    width, height = getCellSize(app)

    imageWidth = 220 
    imageHeight = 220

    # Calculate the centered position
    imageCenterX = left + width / 2
    imageCenterY = top + height / 2

    imageLeft = imageCenterX - imageWidth / 2
    imageTop = imageCenterY - height / 2 - imageHeight / 2.2
     
    drawImage(image, imageLeft, imageTop, width=imageWidth, height=imageHeight)
    drawLabel(f"{score}", imageLeft + imageWidth / 2, imageTop + imageWidth / 2, size=30, fill='white', bold=True)

def drawImageCenteredOnCell2(app, row, col, image):
    left, top = getCellLeftTop(app, row, col)
    width, height = getCellSize(app)

    imageWidth = 215
    imageHeight = 215

    # Calculate the centered position
    imageCenterX = left + width / 2
    imageCenterY = top + height / 2

    imageLeft = imageCenterX - imageWidth / 2.03
    imageTop = imageCenterY - height / 2 - imageHeight / 2.7

    drawImage(image, imageLeft, imageTop, width=imageWidth, height=imageHeight)

#---------------------------------------------------------------------------------------------------------------------------------------------------------
###These are all for OnStep and relate to the features


def drawSign(app):
    drawImage(app.assistimage, app.width//4-200, app.height//4-200, width = 800, height = 800)


def drawSnowflake(app, row, col, size):
    # Convert cell coordinates to pixel coordinates
    x, y = getCellLeftTop(app, row, col)

    # Draw a simple snowflake at the specified cell position with the given size
    drawLine(x - size, y, x + size, y, fill='white', rotateAngle=app.angle)
    drawLine(x, y - size, x, y + size, fill='white', rotateAngle=app.angle)
    drawLine(x - size / 1.4, y - size / 1.4, x + size / 1.4, y + size / 1.4, fill='white', rotateAngle=app.angle)
    drawLine(x - size / 1.4, y + size / 1.4, x + size / 1.4, y - size / 1.4, fill='white', rotateAngle=app.angle)

def drawSnowflakes(app):
    if app.snowflakeFeatureActive:
        snowflakeSize = 15 
        for i in app.snowflakePositions:
            row, col = i
            drawSnowflake(app, row, col, snowflakeSize)

# def scoringAlgorithm(app):
#     #percentage that you are getting things right
#     if app.rightTrains + app.wrongTrains > 0:
#         overallScore = app.rightTrains // (app.rightTrains + app.wrongTrains)
#     else:
#         overallScore = 1
#     return overallScore


def setCustomDelays(app, customDelay):
    for i in range(len(app.trains2)):
        app.trains2[i].delay = customDelay * i 

#---------------------------------------------------------------------------------------------------------------------------------------------------------
###Moving the Train and Corresponding Functions 

def moveTrain2(app, train):
    if train.pathIndex < len(train.activePath):
        #get the next position
        nextPosition = train.activePath[train.pathIndex]
        nextRow, nextCol = nextPosition
        currentRow, currentCol = train.row, train.col

        #swift movement
        deltaRow = app.speed1 * (nextRow - currentRow)
        deltaCol = app.speed1 * (nextCol - currentCol)

        train.row += deltaRow
        train.col += deltaCol

        # Check if the train has reached its destination
        if math.isclose(train.row, nextRow, abs_tol=0.01) and math.isclose(train.col, nextCol, abs_tol=0.01):
            train.pathIndex += 1
    
    if app.playerAssist:
         controlTrainPath1(app, train)
    else:
         app.playerAssist = False
    
    targetRow1, targetCol1 = app.randomRowM1, app.randomColM1 
    if math.isclose(train.row, targetRow1, abs_tol=0.01) and math.isclose(train.col, targetCol1, abs_tol=0.01):
        train.movedPastMovingPiece1 = True
        switchTrainPath1(app, train)
    
    targetRow2, targetCol2 = app.randomRowM2, app.randomColM2
    if math.isclose(train.row, targetRow2, abs_tol=0.01) and math.isclose(train.col, targetCol2, abs_tol=0.01):
        train.movedPastMovingPiece2 = True
        switchTrainPath2(app, train)
    
    targetRow3, targetCol3 = app.randomRowM3, app.randomColM3
    if math.isclose(train.row, targetRow3, abs_tol=0.01) and math.isclose(train.col, targetCol3, abs_tol=0.01):
        train.movedPastMovingPiece3 = True
        switchTrainPath3(app, train)
    
    if train.pathIndex == len(train.activePath):
        if train.color == 'purple' and train.activePath[-1] == app.purplepath[-1]:
            if app.scorePu == 0:
                app.scorePu = 0
            else:
                app.score += 10
                app.scorePu -= 1
            app.rightTrains += 1
        elif train.color == 'blue' and train.activePath[-1] == app.bluepath2[-1]:
            if app.scoreB == 0:
                app.scoreB = 0
            else:
                app.score += 10
                app.scoreB -= 1
            app.rightTrains += 1
        elif train.color == 'pink' and train.activePath[-1] == app.pinkpath[-1]:
            if app.scorePi == 0:
                app.scorePi = 0
            else:
                app.score += 10
                app.scorePi -= 1
            app.rightTrains += 1
        elif train.color == 'green' and train.activePath[-1] == app.greenpath2[-1]:
            if app.scoreG == 0:
                app.scoreG = 0
            else:
                app.score += 10
                app.scoreG -= 1
            app.rightTrains += 1
        elif train.isGolden and (train.activePath[-1] == app.bluepath2[-1]):
            if app.scoreB == 0:
                app.scoreB = 0
            else:
                app.scoreB -= 1
            app.score += 50
            app.rightTrains += 1
        elif train.isGolden and (train.activePath[-1] == app.greenpath2[-1]):
            if app.scoreG == 0:
                app.scoreG = 0
            else:
                app.scoreG -= 1
            app.score += 50
            app.rightTrains += 1
        elif train.isGolden and (train.activePath[-1] == app.pinkpath[-1]):
            if app.scorePi == 0:
                app.scorePi = 0
            else:
                app.scorePi -= 1
            app.score += 50
            app.rightTrains += 1
        elif train.isGolden and (train.activePath[-1] == app.purplepath[-1]):
            if app.scorePu == 0:
                app.scorePu = 0
            else:
                app.scorePu -= 1
            app.score += 50
            app.rightTrains += 1
        elif train.color == 'green' and (train.activePath[-1] == app.bluepath2[-1] or train.activePath[-1] == app.purplepath[-1] or train.activePath[-1] == app.pinkpath[-1]):
            app.wrongTrains1 += 1
            app.score += 0
        elif train.color == 'blue' and (train.activePath[-1] == app.greenpath2[-1] or train.activePath[-1] == app.purplepath[-1] or train.activePath[-1] == app.pinkpath[-1]):
            app.wrongTrains1 += 1
            app.score += 0
        elif train.color == 'pink' and (train.activePath[-1] == app.greenpath2[-1] or train.activePath[-1] == app.purplepath[-1] or train.activePath[-1] == app.bluepath2[-1]):
            app.wrongTrains1 += 1
            app.score += 0
        elif train.color == 'purple' and (train.activePath[-1] == app.greenpath2[-1] or train.activePath[-1] == app.pinkpath[-1] or train.activePath[-1] == app.bluepath2[-1]):
            app.wrongTrains1 += 1
            app.score += 0
        else:
            app.score += 0
            app.wrongTrains1 += 0
        app.trains2.remove(train)
    if app.wrongTrains1 > 30:
        setActiveScreen('gameover')
  
def controlTrainPath1(app, train):
    if train.color == 'purple':
        app.movePieceColor1 = 'purple'
        app.movePieceColor2 = None
        app.movePieceColor3 = None
        train.activePath = app.trainpath2 + app.purplepath
    if train.color == 'pink':
        train.activePath = app.trainpath3 + app.pinkpath
        app.movePieceColor1 = None
        app.movePieceColor2 = 'pink'
        app.movePieceColor3 = None
    if train.color == 'blue':
        train.activePath = app.trainpath4 + app.bluepath2
        app.movePieceColor1 = None
        app.movePieceColor2 = None
        app.movePieceColor3 = 'blue'
    if train.color == 'green':
        train.activePath = app.trainpath4 + app.greenpath2
        app.movePieceColor1 = None
        app.movePieceColor2 = None
        app.movePieceColor3 = 'green'
    if train.color == 'gold':
        app.trains2.remove(train)

def switchTrainPath1(app, train):
    if train.movedPastMovingPiece1 and not train.hasAssignedPath:
        if app.movePieceColor1 == 'purple' and app.purplepath not in train.activePath:
            #append the purple path
            train.activePath = app.trainpath2 + app.purplepath
            train.hasAssignedPath = True  # Set the flag to True once the train has been assigned a path
        elif app.movePieceColor1 == None and app.purplepath not in train.activePath:
            #keep it moving
            train.activePath = app.trainpath3
            train.hasAssignedPath = True  # Set the flag to True once the train has been assigned a path
    
def switchTrainPath2(app, train):
    train.hasAssignedPath = False
    if train.movedPastMovingPiece2 and not train.hasAssignedPath:
        if app.movePieceColor2 == 'pink' and app.pinkpath not in train.activePath:
            #append the pink path
            train.activePath = app.trainpath3 + app.pinkpath
            train.hasAssignedPath = True  #Set the flag to True once the train has been assigned a path
        elif app.movePieceColor2 == None and app.pinkpath not in train.activePath:
            #keep it moving
            train.activePath = app.trainpath4
            train.hasAssignedPath = True  #Set the flag to True once the train has been assigned a path

def switchTrainPath3(app, train):
    train.hasAssignedPath = False
    if train.movedPastMovingPiece3 and not train.hasAssignedPath:
        if app.movePieceColor3 == 'blue' and app.bluepath2 not in train.activePath and app.greenpath2 not in train.activePath:
            #append the blue path
            train.activePath = app.trainpath4 + app.bluepath2
            train.hasAssignedPath = True  #Set the flag to True once the train has been assigned a path
        elif app.movePieceColor3 == 'green' and app.greenpath2 not in train.activePath and app.bluepath2 not in train.activePath:
            #append the green path
            train.activePath = app.trainpath4 + app.greenpath2
            train.hasAssignedPath = True  #Set the flag to True once the train has been assigned a path
#---------------------------------------------------------------------------------------------------------------------------------------------------------
###CREATION OF THE BOARD

def drawBoard(app):
   for row in range(app.rows):
       for col in range(app.cols):
           drawCell(app, row, col, None)
   pass

def drawBoardBorder(app):
   drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
            fill=None, border='black',
            borderWidth=2*app.cellBorderWidth)


def drawCell(app, row, col, color):
   cellLeft, cellTop =  getCellLeftTop(app, row, col)
   cellWidth, cellHeight = getCellSize(app)
   drawRect(cellLeft, cellTop, cellWidth, cellHeight,
            fill=color)

def getCellLeftTop(app, row, col):
   cellWidth, cellHeight = getCellSize(app)
   cellLeft = app.boardLeft + cellWidth*row
   cellTop = app.boardTop + cellHeight*col
   return (cellLeft, cellTop)

def getCellSize(app):
   cellWidth = app.boardWidth / app.rows
   cellHeight = app.boardHeight / app.cols
   return (cellWidth, cellHeight)

def getCell(app, x, y):
   dx = x - app.boardLeft
   dy = y - app.boardTop
   cellWidth, cellHeight = getCellSize(app)
   row = math.floor(dx/cellWidth)
   col = math.floor(dy/cellHeight)
   if (0 <= row < app.rows) and (0 <= col < app.cols):
     return (row, col)
   else:
     return None

#---------------------------------------------------------------------------------------------------------------------------------------------------------
#ALL THINGS TRAIN

#Generate the Trains for the Hard Game
def generateTrains2(app, num_trains):
    for i in range(num_trains):
        color = random.choice(['blue', 'green', 'purple', 'pink'])
        newTrain = Train2(app, 2, 15, color)
        app.trains2.append(newTrain)
        app.trains2[i].delay = i * app.delay2
        app.trains2[i].isGolden = random.random() < 0.2

#Train Class
class Train2:
    def __init__(self, app, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.activePath = app.trainpath2
        self.pathIndex = 0 
        self.hasAssignedPath = False
        self.movedPastMovingPiece1 = False
        self.movedPastMovingPiece2 = False
        self.movedPastMovingPiece3 = False
        self.isGolden = False
        self.delay = 0
    
    def changeColorOnClick(self, app, mouseX, mouseY):
        #Check if the mouse click is within the bounding box of the train
        left, top, right, bottom = self.getTrainBoundingBox(app)
        if left <= mouseX <= right and top <= mouseY <= bottom:
            #Change the color of the train
            self.color = random.choice(['blue', 'green', 'purple', 'pink'])

    def getTrainBoundingBox(self, app):
        #Helper method to get the bounding box of the train
        left, top = getCellLeftTop(app, self.row, self.col)
        width, height = getCellSize(app)
        return left, top, left + width, top + height

#Code for what the trains will look like
def drawTrain2(app, train):
    row, col = train.row, train.col
    left, top = getCellLeftTop(app, row, col)
    width, height = getCellSize(app)
    if train.isGolden:
        train.color = 'gold'
        #Draw the golden train with a different color or special appearance
        drawRect(left, top, width, height, fill='gold')
        #Draw windows on the train body, centered and spaced apart
        windowSize = width / 4
        windowSpacing = 10
        windowMargin = (width - 2 * windowSize - windowSpacing) / 2
        drawRect(left + windowMargin, top + height / 4, windowSize, windowSize, fill='white')
        drawRect(left + windowSize + 2 * windowSpacing, top + height / 4, windowSize, windowSize, fill='white')

        #Draw a topper (thin rectangle)
        drawRect(left, top, width, height/10, fill='black')

        #Draw the train wheels, bigger in size
        wheelRadius = width / 6
        drawCircle(left + width / 4, top + height, wheelRadius, fill='black')
        drawCircle(left + 3 * width / 4, top + height, wheelRadius, fill='black')

        #Draw an additional white circle inside each black wheel
        smallWheelRadius = wheelRadius / 2
        drawCircle(left + width / 4, top + height, smallWheelRadius, fill='white')
        drawCircle(left + 3 * width / 4, top + height, smallWheelRadius, fill='white')

        drawStar(left + width/2, top+height/2 - 40, 17, 5, fill='yellow', border='black')

    else:
        #Draw the train body
        drawRect(left, top, width, height, fill=train.color)

        #Draw windows on the train body, centered and spaced apart
        windowSize = width / 4
        windowSpacing = 10
        windowMargin = (width - 2 * windowSize - windowSpacing) / 2
        drawRect(left + windowMargin, top + height / 4, windowSize, windowSize, fill='white')
        drawRect(left + windowSize + 2 * windowSpacing, top + height / 4, windowSize, windowSize, fill='white')

        #Draw a topper (thin rectangle)
        drawRect(left, top, width, height/10, fill='black')

        #Draw the train wheels, bigger in size
        wheelRadius = width / 6
        drawCircle(left + width / 4, top + height, wheelRadius, fill='black')
        drawCircle(left + 3 * width / 4, top + height, wheelRadius, fill='black')

        #Draw an additional white circle inside each black wheel
        smallWheelRadius = wheelRadius / 2
        drawCircle(left + width / 4, top + height, smallWheelRadius, fill='white')
        drawCircle(left + 3 * width / 4, top + height, smallWheelRadius, fill='white')

#Draw the Trains
def drawTrains2(app):
    for train in app.trains2:
        # Draw each train in the list
        drawTrain2(app, train)

#Draw the Train Tracks
def drawTrainTracks2(app):
    finalpath = [(2, 16), (2, 17), (2, 18)] + findTrainPath(app.board, (2, 18), (app.randomRowM1, app.randomColM1)) + findTrainPath(app.board, (app.randomRowM1, app.randomColM1), (app.randomRowM2, app.randomColM2)) + findTrainPath(app.board, (app.randomRowM2, app.randomColM2), (app.randomRowM3, app.randomColM3)) + findTrainPath(app.board, (app.randomRowM3, app.randomColM3), (app.randomRowB1, app.randomColB1)) + findTrainPath(app.board, (app.randomRowM3, app.randomColM3), (app.randomRowG1, app.randomColG1)) + findTrainPath(app.board, (app.randomRowM1, app.randomColM1), (app.randomRowPurple, app.randomColPurple)) + findTrainPath(app.board, (app.randomRowM2, app.randomColM2), (app.randomRowPink, app.randomColPink))
    for i in finalpath:
        row, col = i
        drawCell(app, row, col, 'sienna')
    
    finalpath2 = [(2, 16), (2, 17), (2, 18)] + findTrainPath(app.board, (2, 18), (app.randomRowM1, app.randomColM1)) + findTrainPath(app.board, (app.randomRowM1, app.randomColM1), (app.randomRowM2, app.randomColM2)) + findTrainPath(app.board, (app.randomRowM2, app.randomColM2), (app.randomRowM3, app.randomColM3))
    for i in finalpath2:
        row, col = i
        drawCell(app, row, col, 'saddleBrown')

#If they click the moving piece then we wil show a white path to that train station
def drawTrainTracks3(app, path):
    for i in path:
        row, col = i
        drawCell(app, row, col, 'white')

#---------------------------------------------------------------------------------------------------------------------------------------------------------

#Drawing the Moving Pieces
def drawMovePiece1(app):
    left, top = getCellLeftTop(app, app.randomRowM1, app.randomColM1)
    width, height = getCellSize(app) 
    if app.movePieceColor1 == 'purple':
        drawCell(app, app.randomRowM1, app.randomColM1, 'white')
        drawTrainTracks3(app, findTrainPath(app.board, (app.randomRowM1, app.randomColM1), (app.randomRowPurple, app.randomColPurple)))
        drawLine(left, top + height/2, left + width, top + height/2, arrowStart=False, arrowEnd=True)
    elif app.movePieceColor1 == None:
        drawCell(app, app.randomRowM1, app.randomColM1, "black")
        drawLabel("Click Me", left + width/2, top + height/2, size=14, bold=True, fill="white")

def drawMovePiece2(app):
    left, top = getCellLeftTop(app, app.randomRowM2, app.randomColM2)
    width, height = getCellSize(app) 
    if app.movePieceColor2 == 'pink':
        drawCell(app, app.randomRowM2, app.randomColM2, 'white')
        drawTrainTracks3(app, findTrainPath(app.board, (app.randomRowM2, app.randomColM2), (app.randomRowPink, app.randomColPink)))
        drawLine(left, top + height/2, left + width, top + height/2, arrowStart=True, arrowEnd=False)
    elif app.movePieceColor2 == None:
        drawCell(app, app.randomRowM2, app.randomColM2, "black")
        drawLabel("Click Me", left + width/2, top + height/2, size=14, bold=True, fill="white")

def drawMovePiece3(app):
    left, top = getCellLeftTop(app, app.randomRowM3, app.randomColM3)
    width, height = getCellSize(app) 
    if app.movePieceColor3 == 'green':
        drawCell(app, app.randomRowM3, app.randomColM3, 'white')
        drawTrainTracks3(app, findTrainPath(app.board, (app.randomRowM3, app.randomColM3), (app.randomRowG1, app.randomColG1)))
        drawLine(left, top + height/2, left + width, top + height/2, arrowStart=True, arrowEnd=False)
    elif app.movePieceColor3 == 'blue':
        drawCell(app, app.randomRowM3, app.randomColM3, "white")
        drawTrainTracks3(app, findTrainPath(app.board, (app.randomRowM3, app.randomColM3), (app.randomRowB1, app.randomColB1)))
        drawLine(left, top + height/2, left + width, top + height/2, arrowStart=False, arrowEnd=True)
    elif app.movePieceColor3 == None:
        drawCell(app, app.randomRowM3, app.randomColM3, "black")
        drawLabel("Click Me", left + width/2, top + height/2, size=14, bold=True, fill="white")

#Drawing the Score Box
def drawScore1(app):
    scoreBoxWidth = 150
    scoreBoxHeight = 60
    margin = 10
    scoreBoxLeft = app.width - scoreBoxWidth - margin
    scoreBoxTop = app.height - scoreBoxHeight - margin

    drawRect(scoreBoxLeft, scoreBoxTop, scoreBoxWidth, scoreBoxHeight, fill='white', borderWidth=2)

    drawLabel(f"Score: {app.score}", scoreBoxLeft + scoreBoxWidth/2, scoreBoxTop + scoreBoxHeight/2, size=19, bold=True)
    drawLabel(f"Level {app.hardLevel}", scoreBoxLeft + scoreBoxWidth/2, scoreBoxTop - 15, size=18, bold=True)

#---------------------------------------------------------------------------------------------------------------------------------------------------------


def main():
   runAppWithScreens(initialScreen='welcome')

main()
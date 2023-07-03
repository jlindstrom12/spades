import random
from cmu_112_graphics import *
import math
import time

#NOTES ABOUT CODE FOR GRADERS:
#Lots of variables are in list form
#In a list of 4 variables index 0 represents player, 1 is cpu1, 2 is cpu 2, and 3 is cpu3
#In a list of 2 variables index 0 represents team1(Player and cpu2) and 1 represents team2(cpu2 and cpu3)
#Functions organized in categories: Start Ups, Helper functions, Cpu Functions, Player functions, main game functions, keyboard/mouse interactions, and drawing functions

##########
#START UPS
##########
def appStarted(app):
    start(app)
    makeSuits(app)
    makeBigSpade(app)
    makeHomeBackground(app)
    app.helpScreen = 0 #place of help screen
    app.time = time.time() #time
    app.timerDelay = 1000 #Time delay

    #Settings
    app.team1Color = 'Blue' #team 1 color
    app.team2Color = 'Red' #team 2 color
    app.indicateLegals = True #For indicating which cards are legal in the players hand
    app.winningScore = 150 #Score to win the game

def start(app): #starts a game
    app.count = 0 #place holder
    app.startingPlayer = 0 #Number of player who starts the trick
    app.handWidth = 0 #used when clicking on cards to not throw out of bounds error
    app.cpu1 = "Shark"
    app.cpu2 = "Gamble" #Names are references to card Terms
    app.cpu3 = "Royalty"
    app.twoClubsCords = 0,0 #Hand and place of 2 of clubs
    app.cardsInPlay = [None]*4 #4 cards in play
    app.gameOver = False #boolean for game over
    app.scores = [0,0]#teams scores
    app.sandbags = [0,0]#teams sandbags
    newRound(app)
    app.state = "home" #state of visual, can be: home, help, settings, or game

def newRound(app): #Starts a newRound
    app.hands = [([0]*13) for i in range(4)]
    app.cardsInDeck = [] #Used for finding reamaing cards in deck
    createHands(app) #Create New Hands
    sortHandBySuit(app) #sorts players hand
    app.startingPlayer = None #sets starting player to whoever has the 2 of clubs
    while(app.startingPlayer == None):
        app.startingPlayer = find2Clubs(app)
    app.playersTricks = [0]*4 #number of tricks each player gets
    app.playersBids = [-1]*4 #number of tricks each player bids, -1 to not get confused with nill
    app.cardsInPlay = [None] * 4 #Resets cards in play to none
    app.combinedBids = [0,0] #List of combined bids of two teams
    app.turn = app.startingPlayer #starts with turn of starting player
    app.count = 0 #place holder
    app.suitPlayed = 'Clubs' #Starting suit is always clubs on first trick
    app.spadesBroken = False #reset breaking the spades
    app.vals = 0 #place holder   

#Image based on https://stock.adobe.com/search?k=card+suits
#Based on color changing code from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
def makeBigSpade(app):
    app.bigspade = app.loadImage('bigSpade.png')

    app.bigspade = app.scaleImage(app.bigspade,.75)
    app.bigspade = app.bigspade.crop((0,0,73.75*5,74.55*5-110))
    # now let's make a copy that only uses the red part of each rgb pixel:
    app.bigspade = app.bigspade.convert('RGB')
    app.image2 = Image.new(mode='RGB', size=app.bigspade.size)
    for x in range(app.image2.width):
        for y in range(app.image2.height):
            r,g,b = app.bigspade.getpixel((x,y))
            if(r<5 or g<5 or b<5):
                app.image2.putpixel((x,y),(0,100,0))
            else:
                app.image2.putpixel((x,y),(0,128,0))

#https://www.freepik.com/free-vector/playing-cards-background_898838.htm - Image URL
def makeHomeBackground(app):
    app.homeBackground = app.loadImage('Background2.jpeg')
    app.scaleImage(app.homeBackground, .75)

#Image based on https://stock.adobe.com/search?k=card+suits
#Based on sprite code from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
def makeSuits(app): #Create suit images
    spritestrip = app.loadImage('Suits.png')
    spritestrip = app.scaleImage(spritestrip,1/4)
    app.suits = [ ]
    for i in range(4):
        sprite = spritestrip.crop((73.75*.5*i, 0, 73.75*.5*(i+1), 74.55*.5))
        app.suits.append(sprite)
    
#################
#HELPER FUNCTIONS
#################

def voidInSuit(app,cpu): #Checks If Cpu/player is void in the suit played
    for i in range(len(app.hands[cpu])):
        if(app.hands[cpu][i][1] == app.suitPlayed):
            return False
    else:
        return True

def find2Clubs(app): #Finds player who has 2 of clubs. 2 of clubs starts each round
    if(len(app.hands) == 4 and len(app.hands[0])==13):
        for i in range(4):
            for j in range(12):
                
                if(app.hands[i]!=0 and app.hands[i][j] == [2,'Clubs']):
                    app.twoClubsCords = i,j
                    return i
    return None

def lastPlayer(app): #Checks who is the last player to play their card
    start = app.startingPlayer #Primarily for last Trick of the round
    if(start == 0): #So doesn't throw exception for None
        return 3
    else:
        return start-1

def getSuit(num): #Used to create the hands with suits
    if num == 0:
        return 'Spades'
    if num == 1:
        return 'Clubs'
    if num == 2:
        return 'Hearts'
    if num == 3:
        return 'Diamonds'

def partner(cpu): #Used to return the player or CPU's partner
    if(cpu==1): return 3
    if(cpu==2): return 0
    if(cpu==3): return 1

def createHands(app): #Randomly Creates 4 hands of 13 cards with 0 repeats
    count = 0
    
    for i in range(52):
        val = i%13 + 2
        suit = getSuit(i//13)

        app.cardsInDeck.append([val,suit])

    random.shuffle(app.cardsInDeck)

    for i in range (len(app.hands)):
        for j in range(len(app.hands[0])):
            app.hands[i][j] = app.cardsInDeck[count]
            count+=1        

def findCard(app,card): #Can find a card in the deck
    for i in range(len(app.cardsInDeck)):
        if(app.cardsInDeck[i]==card):
            return i
    else:
        return -1

def resume(app): #Used when starting up a game
    ans = None #Chooses to start a new game or resume the old game
    while ans==None:
        ans = app.getUserInput('Resume(R) or Restart(S)')
        if(ans!="R" and ans!="S" and ans!="r" and ans!="s"):
            ans = None
    return ans
        
def delay(app,val): #adds a time delay of time val seconds
    t = time.time()-app.time
    while(t<val):
        t = time.time()-app.time

#https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#ioMethods
def newWinningScore(app): #Can replace the winning score in settings
    score = 0
    while score==0:
        score = app.getUserInput('Input New Winning Score(x to cancel):')
        if(score == 'x'):
            return
        elif(score.isdigit()):
            score = int(score)
            if(score>0):
                app.winningScore = score
        else:
            score = 0

#https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#ioMethods            
def newColor(app): #Can change players colors in settings 
    color = ""
    while color=="":
        color = app.getUserInput('Input color(check spelling, x to cancel):')
        if(color == 'x'):
            return
        
    return color
    
################
#CPU FUNCTIONS
#################

def cpuBestLegalCard(app,cpu): #Chooses best card for the CPU
    card = minimax(app,cpu)
    app.cardsInPlay[cpu] = card
    if(app.startingPlayer==cpu): #If they started sets to starting suit
        app.suitPlayed = card[1]

def minimax(app,cpu): #Alogrithim for determining the best card
    legalCards = cpulistLegalCards(app,cpu)
    cardChoice = None
    maxVal = 0
    position = copy.deepcopy(app.cardsInPlay)
    for i in range(len(legalCards)): #Runs minimaxHelper for all legal cards
        card,place = legalCards[i] #Cpu could play
        if(card[0]==14 and card[1]==app.suitPlayed):
            app.hands[cpu].pop(place)
            return card
        else:
            position[app.turn] = card
            minimaxHelper(app,position,cpu+1,cpu)

        val = app.vals
        if(val>maxVal):
            maxVal = val
            cardChoice = i
        app.vals = 0
        
        
    if(app.startingPlayer == app.turn and len(app.hands[0])==13):
        card = [2,"Clubs"]
        _,place = app.twoClubsCords
    elif(cardChoice!=None):
        card,place = legalCards[cardChoice]
        
    app.hands[cpu].pop(place)
    
    return card
        
def minimaxHelper(app,position,turn, winner): #Recursive backtracking for alpha beta
    if( position[0]!=None and position[1]!=None and position[2]!=None and position[3]!=None):
        c = highestCard(app,position)
        if(c == winner or c == partner(winner)):
            app.vals+=winner
        else:
            app.vals+=0
    else:
        for i in app.cardsInDeck: #Will attempt all legal game positions and evaluate
            if(turn>3):
                turn = 0
            if(MoveLegal(app,turn,i)):
                if(i[1]==app.suitPlayed or i[1]=='Spades'): #Cuts off paths that are bad plays
                    position[turn] = i
                    solution = minimaxHelper(app,position,turn+1,winner)
                    if(solution != None):
                        return solution
                    else:
                        position[turn] = None
    return None            

def cpulistLegalCards(app,cpu): #returns a list of legal cards for CPU or player
    hand = app.hands[cpu]
    legalCards = []
    for i in range(len(hand)):
        if(MoveLegal(app,cpu,hand[i])):
            legalCards.append((hand[i],i))
    return legalCards

def cpuBidEstimate(app,cpu): #Used to estimate a CPU's Bid based on their hand
    hand = app.hands[cpu] #Fairly accurate according to large number testing
    bid = 0 #About .15 off what the average bid should be so maybe needs a little
    numSuits = [0,0,0,0] #work
    for card in hand:
        if(card[0]== 14 or card[0]==13): 
            if card[1]=='Spade':
                numSuits[0]-1
            bid+=1
        if(card[0]==12 and card[1]=='Spade'):
            bid+=1
        
        if(card[1]=='Diamond'):
            numSuits[3]+=1
        if(card[1]=='Spades'):
            numSuits[0]+=1
        if(card[1]=='Clubs'):
            numSuits[2]+=1
        if(card[1]=='Hearts'):
            numSuits[1]+=1

    if(numSuits[0]>4):
        bid+=numSuits[0]-3
    if(numSuits[1]<=2 or numSuits[2]<=2 or numSuits[3]<=2 ) and numSuits[0]>=3:
        bid+=1
    elif(numSuits[1]<=1 or numSuits[2]<=1 or numSuits[3]<=1 ) and numSuits[0]>=3:
        bid+=2
    if bid == 0:
        bid=1
    return bid

##################
#Player Functions
###################

#https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#ioMethods
def collectPlayerBid(app): #Gets Players bid 
    bid = None
    while bid==None:
        bid = app.getUserInput('What is your bid?(Type x for computer estimate)')
        if(bid == 'x'):
            bid = cpuBidEstimate(app,0)
        else:
            bid = int(bid)
        if(bid<-1 or bid>14):
            bid = None
    return bid
    
def sortHandBySuit(app): #Sorts player hand by suit and number
    diamonds = [] #makes it easier to visualize all cards
    hearts = []
    spades = []
    clubs = []
    for i in app.hands[0]:
        if(i[1]=="Diamonds"):
            diamonds.append(i)
        if(i[1]=="Hearts"):
            hearts.append(i)
        if(i[1]=="Clubs"):
            clubs.append(i)
        if(i[1]=="Spades"):
            spades.append(i)
    
    sortNumbers(diamonds)
    sortNumbers(spades)
    sortNumbers(hearts)
    sortNumbers(clubs)
    
    app.hands[0] = spades + diamonds + clubs + hearts

def sortNumbers(list): #Used to sort the numbers in the players hand
    count = 1
    while count < len(list):
        if(list[count-1][0]<list[count][0]):
            k = list[count]
            list[count] = list[count-1]
            list[count-1] = k
            count=1
        else:
            count+=1

####################################
#Main Functions for Game Performance
####################################
def MoveLegal(app,player,card): #Checks if the card the player clicks on or cpu chooses
    if(len(app.hands[player])==13 and find2Clubs(app) == player): #Is legal to play in that situation
        if card == [2, 'Clubs']:
            return True 
        else:
            return False
    elif(app.startingPlayer == player):
        if(card[1]=='Spades' and app.spadesBroken) or card[1]!='Spades':
            return True
        else:
            return False
    elif(app.startingPlayer != player):
        
        if(voidInSuit(app,player)):
           
            return True
        elif(card[1]!=app.suitPlayed):
            return False
   
    return True

def highestCard(app,list): #Returns the player 0-3 with the highest card in the Trick
    if(list[0]==None or list[1]==None or list[2]==None or list[3]==None):
        return
    highestCard = 0
    highestVal = 0
    highestSpade = 0
    spadesPlayed = False
    for i in range(len(list)):
        if(list[i][1]=='Spades'): #Spades are trump cards
            spadesPlayed = True #This section accounts for that
            if(highestSpade<list[i][0]):
                highestSpade = list[i][0]
                highestCard = i 

        if(not spadesPlayed):
            if(list[i][1] == app.suitPlayed):
                if(highestVal< list[i][0]):
                    highestVal = list[i][0]
                    highestCard = i


    return highestCard

def runTrick(app): #Main function. Runs The tricks
    if(app.playersBids[0]==None or app.playersBids[0]==-1): #Prompts player for bid
        collectBids(app)
    if(app.count<4 and len(app.hands[lastPlayer(app)])!=0):
        
        if(app.turn == 1 and app.cardsInPlay[1]==None):
            #CPU1 chooses card with alpha Beta Prunning
            cpuBestLegalCard(app,1)
            app.count+=1
            app.turn += 1
            return
        if(app.turn == 2 and app.cardsInPlay[2]==None):
            #CPU2 chooses card with alpha Beta Prunning
            cpuBestLegalCard(app,2)
            app.count+=1
            app.turn += 1
            return
        if(app.turn == 3 and app.cardsInPlay[3]==None):
            #CPU3 chooses card with alpha Beta Prunning
            cpuBestLegalCard(app,3)
            app.count+=1
            app.turn = 0  
            return #One card each timer fired

    elif(app.count>=4 and len(app.hands[lastPlayer(app)])!=0): #Resets after each trick
        if(app.cardsInPlay[0]!=None):
            winner = highestCard(app,app.cardsInPlay)
            app.playersTricks[winner]+=1
            app.startingPlayer = winner
            app.turn = app.startingPlayer
            if(app.cardsInPlay[0][1] == 'Spades' or app.cardsInPlay[1][1] == 'Spades' or app.cardsInPlay[2][1] == 'Spades' or app.cardsInPlay[3][1] == 'Spades'):
                app.spadesBroken = True
            app.cardsInPlay = [None] * 4
            app.count = 0

    if (len(app.hands[lastPlayer(app)]) == 0 and app.cardsInPlay[0] != None and #Resets after each round
    app.cardsInPlay[1] != None and 
    app.cardsInPlay[2] != None and 
    app.cardsInPlay[0] != None):
        winner = highestCard(app,app.cardsInPlay) #Restarts once round is over
        app.playersTricks[winner]+=1
        addScores(app)#AKA all 13 tricks are played that round
        app.count = 0
        newRound(app)

def addScores(app): #adds up the scores after each round
    nill = [None,None]
    made1 = app.playersTricks[0] + app.playersTricks[2]
    made2 = app.playersTricks[1] + app.playersTricks[3]
    if(app.playersBids[0]==0): #Finds if any players are nil
        nill[0] = 0
    if(app.playersBids[2]==0):
        nill[0] = 2

    if(app.playersBids[0]==0):
        nill[1] = 1
    if(app.playersBids[2]==0):
        nill[1] = 3

    #team1, Players team
    if(made1 == app.combinedBids[0]):
        app.scores[0]+=app.combinedBids[0]*10
    elif(made1<app.combinedBids[0]):
        app.scores[0]-=app.combinedBids[0]*10
    else: #Sandbags
        extra = made1 - app.combinedBids[0]
        app.scores[0]+=app.combinedBids[0]*10 + extra
        app.sandbags[0] +=extra
        if(app.sandbags[0]>=10):
            app.scores[0]-=100
            app.sandbags[0]=0
    if(nill[0]!=None):
        if app.playersTricks[nill[0]] !=0:
            app.scores[0]-=100
    #team2, CPUs
    if(made2 == app.combinedBids[1]):
        app.scores[1]+=app.combinedBids[1]*10
    elif(made2<app.combinedBids[1]):
        app.scores[1]-=app.combinedBids[1]*10
    else: #Sandbags
        extra = made2 - app.combinedBids[1]
        app.scores[1]+=app.combinedBids[1]*10 + extra
        app.sandbags[1]+=extra
        if(app.sandbags[1]>=10):
            app.scores[1]-=100
            app.sandbags[1]=0
    if(nill[1]!=None): #nill
        if app.playersTricks[nill[1]] !=0:
            app.scores[1]-=100

def collectBids(app): #Collects bids for the players. All 3 CPU bids and the players
    app.playersBids[1] = cpuBidEstimate(app,1) #In one place to add to a list
    app.playersBids[2] = cpuBidEstimate(app,2)
    app.playersBids[3] = cpuBidEstimate(app,3)
    app.playersBids[0] = collectPlayerBid(app)
    if(app.playersBids[0]!=None):
        app.combinedBids[0] += app.playersBids[0] + app.playersBids[2]
        app.combinedBids[1] += app.playersBids[1] + app.playersBids[3]

####################################
#Interactions with keyboard/mouse
####################################

def pressedHome(x,y): #Checks if home
    if(x<=100 and x>=25 and y<=50 and y>=25):
        return True
    return False
       
def mousePressed(app,event):
    x = event.x
    y = event.y
    if(app.gameOver):
        if(y>app.height/2-25 and y<app.height/2+25): #Find which button you pressed after game over
            if(x<app.width/2 and x>app.width/2-100):
                app.state = 'home'
            if(x>app.width/2 and x<app.width/2+100):
                start(app)
                app.state = 'game'

    if(app.state == "settings"): #Find which setting is pressed
        if(x>275 and x<475):
            if(y>100 and y<150):
                app.team1Color = newColor(app)
            if(y>150 and y<200):
                app.team2Color = newColor(app)
            if(y>200 and y<250):
               app.indicateLegals = not app.indicateLegals
            if(y>250 and y<300):
                 newWinningScore(app)
           
               

    if(app.state == "help"): #Find if you hit next or back in help screen
        if(x>25 and x<125 and y>425 and y<475 and app.helpScreen>0):
            app.helpScreen-=1
        if(x>625 and x<725 and y>425 and y<475 and app.helpScreen<3):
            app.helpScreen+=1
    if(app.state == "home"): #Find which button you press on home screen
        
        if(x>=535 and x<=750):
            if(y>=100 and y<=150):
                ans = resume(app)
                if(ans == 'S' or ans == 's'):
                    start(app)
                app.state = "game"
            if(y>=200 and y<=250):
                app.state = "help"
            if(y>=300 and y<=350):
                app.state = "settings"
    else:
        if pressedHome(event.x,event.y): #Finds if you pressed the home button on any screen
            app.state = "home"
    if(app.state == "game"): #For selecting the players card
        if(app.turn == 0):
            app.handwidth = len(app.hands[0])*54 + 50
            x = event.x
            y = event.y
            if(y>=400 and y<=470):
                if(x>=20 and x<=app.handwidth):
                    numCard = x//55
                    if(MoveLegal(app,0,app.hands[0][numCard])):
                        app.cardsInPlay[0] = app.hands[0].pop(numCard)
                        app.cardsInDeck.pop(findCard(app,app.cardsInPlay[0]))
                        app.turn+=1
                        app.count+=1
                        if(app.startingPlayer == 0):
                            app.suitPlayed = app.cardsInPlay[0][1]
                                
def keyPressed(app,event): #Another way of naviagating the help screen
    if(app.state == 'help'):
        if(event.key == 'Right' or event.key == 'Up') and app.helpScreen<3:
            app.helpScreen+=1
        if(event.key == 'Left' or event.key == 'Down') and app.helpScreen>0:
            app.helpScreen-=1
        
def timerFired(app):

    if(app.state == "game" and not app.gameOver): #runs tricks when in game and game isnt over
        app.time = time.time()
        runTrick(app)
        if(app.scores[0] >= app.winningScore or app.scores[1] >= app.winningScore):
            app.gameOver = True #Once somebody reaches the winning score
    

###################
#DRAWING FUNCTIONS
###################

#Draws an individual Card*
def drawCard(canvas,app,card,x1,y1,x2,y2):
    canvas.create_rectangle(x1,y1,x2,y2, fill = "White", outline = "black", 
    width = 3)
   
    if(card != 0):
        num = str(card[0])
        if(num =='13'):
            num = 'K'
        elif(num == '12'):
            num = 'Q'
        elif(num=='11'):
            num = 'J'
        elif(num=='14'): #Sets Ace as the highest card
            num = 'A' #Both for keeping track of who is winning and
                    #for sorting the cards numerically
           
        
        if(card[1] == 'Diamonds' or card[1] == 'Hearts'):
            
            canvas.create_text(x1+10,y1+10,text = num, 
            fill = 'Red',font = 'Ariel 12 bold')
            canvas.create_text(x2-10,y2-10,text = num, 
            fill = 'Red', font = 'Ariel 12 bold')

        else:
            canvas.create_text(x1+10,y1+10,text = num,
            font = 'Ariel 12 bold')
            canvas.create_text(x2-10,y2-10,text = num, 
            font = 'Ariel 12 bold')

        centerX = x1+(x2-x1)/2
        centerY = y1+(y2-y1)/2

        if(card[1] == 'Diamonds'):
            canvas.create_image(centerX, centerY, 
            image=ImageTk.PhotoImage(app.suits[3]))

        if(card[1]=='Hearts'):
            canvas.create_image(centerX, centerY, 
            image=ImageTk.PhotoImage(app.suits[1]))

        if(card[1]=='Clubs'):
            canvas.create_image(centerX, centerY, 
            image=ImageTk.PhotoImage(app.suits[2]))

        if(card[1]=='Spades'):
            canvas.create_image(centerX, centerY, 
            image=ImageTk.PhotoImage(app.suits[0]))
#Draws the players card played in the correct space*
def drawPlayersCard(app,canvas,card):
    if(app.cardsInPlay[0] != None):
        drawCard(canvas,app,card,350,225,400,295)
#Draws CPU1s card played in the correct space*
def drawCPU1Card(app,canvas,card):
     if(app.cardsInPlay[1] != None):
        drawCard(canvas,app,card,275,165,325,235)
#Draws CPU2s card played in the correct space*
def drawCPU2Card(app,canvas,card):
     if(app.cardsInPlay[2] != None):
        drawCard(canvas,app,card,350,105,400,175)
#Draws CPU3s card played in the correct space*
def drawCPU3Card(app,canvas,card):
     if(app.cardsInPlay[3] != None):
        drawCard(canvas,app,card,425,165,475,235)
#Draws all cards played in the center of the canvas symmetrically*
def drawCenterCards(app,canvas):
    drawPlayersCard(app,canvas,app.cardsInPlay[0])
    drawCPU1Card(app,canvas,app.cardsInPlay[1])
    drawCPU2Card(app,canvas,app.cardsInPlay[2])
    drawCPU3Card(app,canvas,app.cardsInPlay[3])
    
#Creates poker esk background, meant to represent green felt*
def drawBackground(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height, fill = 'Green')
    canvas.create_image(428, 190, image=ImageTk.PhotoImage(app.image2))
    #canvas.create_line(app.width/2,0,app.width/2,app.height, fill = 'pink', width = 10)
    drawPlayerIcons(app,canvas)
    drawScores(app,canvas)
    drawHomeButton(app,canvas)
#Draws player rectangles. After MVP add icons for aethetics*
def drawPlayerIcons(app,canvas):

    canvas.create_rectangle(300+25/2,325,425+25/2,375, outline = app.team1Color, width = 3) #Player
    canvas.create_text(375, 385, text = "Player", font = 'Aerial 15 bold')
    
    canvas.create_rectangle(300+25/2,20,425+25/2,70, outline = app.team1Color, width = 3) #CPU2
    canvas.create_text(375, 80, text = app.cpu2, font = 'Aerial 15 bold')

    canvas.create_rectangle(50,175,175,225, outline = app.team2Color, width = 3) #CPU1
    canvas.create_text(112.5, 235, text = app.cpu1, font = 'Aerial 15 bold')

    canvas.create_rectangle(575,175,700,225, outline = app.team2Color, width = 3) #CPU3
    canvas.create_text(112.5 + 525, 235, text = app.cpu3, font = 'Aerial 15 bold')
    displayBids(app,canvas)
#Display bids in player rectangles*
def displayBids(app,canvas):
    canvas.create_text(375, 350, text = str(app.playersTricks[0]) + " / " + str(app.playersBids[0]), font = 'Aerial 25 bold')
    canvas.create_text(375, 45, text = str(app.playersTricks[2]) + " / " + str(app.playersBids[2]), font = 'Aerial 25 bold')

    canvas.create_text(112.5, 200, text = str(app.playersTricks[1]) + " / " + str(app.playersBids[1]), font = 'Aerial 25 bold')
    canvas.create_text(112.5 + 525, 200, text = str(app.playersTricks[3]) + " / " + str(app.playersBids[3]), font = 'Aerial 25 bold')
#Draws players hand with all the cards remaining in their hand*
def drawHand(hand,canvas,app):

    if(len(hand)!=0):
        topY = 400
        bottomY = 470
        xwidth = 50
        if(hand[0]!=0):
            for i in range (len(hand)):
                drawCard(canvas,app,hand[i], 20+i*54, topY,70+i*54, bottomY)
        if(app.indicateLegals):
            drawLegals(app,canvas)
       
#Draws a home button on none homescreens    *    
def drawHomeButton(app,canvas):
    canvas.create_rectangle(25,25,100,50, fill = "dark green")
    canvas.create_text(75/2 + 25, 25/2 + 25,text = "Home", font = "Ariel 15 bold", fill = "Black")
#Draws the home screen*    
def drawHomeScreen(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height, fill = 'Black')
    canvas.create_image(app.width/2-150, app.height/2, image=ImageTk.PhotoImage(app.homeBackground))
    canvas.create_text(535 + (750-535)/2,50, text = "SPADES", font = "Ariel 40 bold", fill = "White")
    canvas.create_text(535 + (750-535)/2,125, text = "- PLAY", font = "Ariel 25 bold", fill = "White")
    canvas.create_text(535 + (750-535)/2,225, text = "- HOW TO PLAY", font = "Ariel 25 bold", fill = "White")
    canvas.create_text(535 + (750-535)/2,325, text = "- SETTINGS", font = "Ariel 25 bold", fill = "White")
    canvas.create_line(550,80,735,80,fill = 'White', width = "5")
#Draws the help/instructions screen*
def drawHelpScreen(app,canvas):
    terms = '''Important Terms: \n\nRound: A set of 13 tricks. Multiple Rounds are played each game \n \nTrick: a set of 4 cards, one played by each player.
    \nHand: Your set of 13 cards \n\nBid: The number of 13 tricks you think you will win with your hand\n\nVoid: Out of a suit\n\nNil: Your bid is 0\n\nStarting suit: Suit of the first card played in the trick'''
    
    rules = '''Rules: \n\n-In each trick the highest card played of the starting suit wins, Ace is highest\n\n-2 of Clubs starts the first trick of each round
    \n-Spades are trump cards. Highest spade always wins \n\n-You cannot play a spade until you are void in a suit or spades are broken by a CPU
    \n-Once you are void in a suit you can play anything.\nBut if you have a card of the starting suit you need to play it \n\n-After the first trick whoever wins the trick begins the next one.
    \n-If you are starting a trick you can play anything.\nHowever you can only play a spade if spades have been broken \n\n-Spades are broken by either the player or a cpu playing a spade when they are void in the starting'''

    bidding = '''Bidding: \n\n-Your bid is the number of tricks you think you will win \n\n-You and your partners bids are combined.\n EX: If you are for 4 and your partner is for 3 that means together you need to make 7
    \n-General Bidding Strategy: \n\n-An Ace or a King usually counts as one\n\n-If you have only one-two cards in a suit and more than 3 spades thats one-two \n\n-4+ spades usually counts as one for each spade above 3
    \n-If your hand is truly terrible you can bid nil. This means you will take 0 tricks \n\n-If unsure you can hit x for the computer estimate of your hand'''

    scoring = '''Scoring: \n\n-Your score is based on you and your partners combined tricks \n\n-If you make your combined bid you get your bid *10. \nEx: If your combined bid is 7 and you make your 7 tricks thats 70 points
    \n-For each trick over your combined bid you get a sandbag, 10 sandbags is -100 points \n\n-If you go under your combined bid you get negative your bid*10. \nEx: If your combined bid is 7 and you make your 7 tricks thats -70 points
    \n-If you go nil and individually take a trick your team gets -100 but if you make it you get +100. \nThis is regardless of your partner making thier tricks.'''
    canvas.create_rectangle(0,0,app.width,app.height, fill = 'Green')
    canvas.create_rectangle(25,425,125,475, fill = 'dark green')
    canvas.create_rectangle(625,425,725,475, fill = 'dark green')
    canvas.create_text(75,450,text = "Back", font = "Ariel 15 bold")
    canvas.create_text(675,450,text = "Next", font = "Ariel 15 bold")
    size = '15'
    drawHomeButton(app,canvas)
    if(app.helpScreen == 0):
        message = terms
    if(app.helpScreen == 1):
        message = rules
        size = '13'
    if(app.helpScreen == 2):
        message = bidding
    if(app.helpScreen == 3):
        message = scoring

    canvas.create_text(app.width/2,app.height/2, text = message, font = "Ariel " + size + " bold")
#Draws scores*
def drawScores(app,canvas):
    canvas.create_rectangle(575,25,700,100, fill = "dark green")
    canvas.create_text(575 + 125/2, 40, text = "Scores: ", font = "Ariel 15 bold")
    canvas.create_text(575 + 125/2, 60, text = app.team1Color+ " Team: " + str(app.scores[0]), font = "Ariel 15 bold")
    canvas.create_text(575 + 125/2, 80, text = app.team2Color+" Team: " + str(app.scores[1]), font = "Ariel 15 bold")
#Inidicates Legal Cards
def drawLegals(app,canvas): 
    list = cpulistLegalCards(app,0)
    r = 5
    for card,i in list:
        canvas.create_oval(45+i*54-r,470-r,45+i*54+r,470+r, fill = 'Light Green')
#Creates a settings screen
def drawSettings(app,canvas):

    canvas.create_rectangle(0,0,app.width,app.height, fill = 'Green')
    drawHomeButton(app,canvas)
    canvas.create_text(225 + (525-225)/2, 50, text = "SETTINGS:", font = "Ariel 25 bold underline")
    canvas.create_text(225 + (525-225)/2, 75, text = "Click on a setting to change it", font = "Ariel 15 bold")
    canvas.create_text(275 + (475-275)/2, 125, text ="-Team 1 Color: " + app.team1Color, font ="Ariel 18 bold")
    canvas.create_text(275 + (475-275)/2, 175, text ="-Team 2 Color: " + app.team2Color, font ="Ariel 18 bold")
    canvas.create_text(275 + (475-275)/2, 225, text ="-Indicate Legal Cards: " + str(app.indicateLegals), font ="Ariel 18 bold")
    canvas.create_text(275 + (475-275)/2, 275, text ="-Winning Score: " + str(app.winningScore), font ="Ariel 18 bold")
#Draws a game over message and two options, home and restart
def gameOver(app,canvas):
    winner = app.team1Color
    if(app.scores[1]>app.scores[0]):
        winner = app.team2Color
    canvas.create_text(app.width/2, app.height/2, text = "GAME OVER: " + winner + " Won!", font = "Ariel 22 bold")
    canvas.create_text(app.width/2, app.height/2+25, text = "Home     Restart", font = "Ariel 18 bold")

    
        
def redrawAll(app, canvas):
    if(app.state == "game"):
        drawBackground(app,canvas)
        if(not app.gameOver):
                drawHand(app.hands[0],canvas,app)
                drawCenterCards(app,canvas)
                
        else:
            gameOver(app,canvas)
    if(app.state == "home"):
        drawHomeScreen(app,canvas)
    if(app.state == "help"):
        drawHelpScreen(app,canvas)
    if(app.state == "settings"):
        drawSettings(app,canvas)

    

runApp(width=750, height=500)

    


   
            









        

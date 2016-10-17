import os, pygame
import Tkinter as Tk
import time
import UsernameData
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (200,50) # Centering screen as best as possible

"""

------------------------------------------------------------------------------------------------------------
 RESOURCES
------------------------------------------------------------------------------------------------------------

"""

# Define some colors
BLACK = (0, 0, 0)
GRAY = (25, 33, 36)
WHITE = (255, 255, 255)
GREEN = (60, 186, 84)
RED = (219, 50, 54)
BLUE = (72, 133, 237)
YELLOW = (244, 194, 13)


# X and O
cross = pygame.image.load("./images/x.png")# Player 1
circle = pygame.image.load("./images/o.png") #Player 2


"""
------------------------------------------------------------------------------------------------------------
  SETTING UP GRID
------------------------------------------------------------------------------------------------------------
"""
 
# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 150
HEIGHT = 150
 
# This sets the margin between each cell
MARGIN = 5
 
# Creating grid
grid = []
for row in range(3):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(3):
        grid[row].append(0)  # Append a cell


"""

------------------------------------------------------------------------------------------------------------

INITIALIZING PYGAME and SCREEN

------------------------------------------------------------------------------------------------------------

"""

# Initialize pygame
pygame.init()
pygame.font.init()

 
# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [900, 625]
screen = pygame.display.set_mode(WINDOW_SIZE)
 
# Set title of screen
pygame.display.set_caption("Tic-Tac-Toe")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

#In Current State: current_pos = [column][row]
#Setting starting position to (1,1)
current_pos = [1,1]
current_color = GREEN


# initialize font
myfont = pygame.font.Font(None, 24)

# render text
notification = myfont.render("Let's get started!", 1, (255,255,255))



"""
------------------------------------------------------------------------------------------------------------
  GLOBALS
------------------------------------------------------------------------------------------------------------
"""
#Player turn
player = 1

#Scores
player1_score = 0
player2_score = 0

#Winner
winner = 0

#Warning
warning = False

#Game State
game_state = 0
"""0 implies game in session"""
"""1 imples end of game, in limbo"""

usrTools = UsernameData.UsernameData()
usrTools.loadCurrentData()

"""

------------------------------------------------------------------------------------------------------------

      CLASSES

------------------------------------------------------------------------------------------------------------

    
"""            
user={}

def center(root): #to center our roots
    root.update_idletasks() # to ensure accuracy in height and width values
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    geo = root.geometry()
    size = tuple(geo.split('x'))
    size2 = tuple(size[1].split('+'))
    
    x = width/2 - int(size[0])/2
    y = height/2 - int(size2[0])/2
    root.geometry("%dx%d+%d+%d" % ((int(size[0]), int(size2[0])) + (x, y)))
    
class username():
    
    def __init__(self, playerNo):
        self.root = Tk.Tk()
        self.root.wm_title("Tic-Tac-Toe")
        self.label = Tk.Label(self.root, text=("Player " + str(playerNo) + ", enter your username: "))
        self.label.pack()
        self.name = Tk.StringVar()
        Tk.Entry(self.root, textvariable=self.name).pack()

        self.buttontext = Tk.StringVar()
        self.buttontext.set("Done")
        Tk.Button(self.root,
                  textvariable=self.buttontext,
                  command=self.btnclicked).pack()

        self.label = Tk.Label(self.root, text="")
        self.label.pack()
        center(self.root)

        self.root.mainloop()
        
    def btnclicked(self):
        
        user['name']=self.name.get()
        
        self.label.destroy()
        self.root.destroy()

    def button_click(self, e):
        pass 
    



"""

------------------------------------------------------------------------------------------------------------

  FUNCTIONS

------------------------------------------------------------------------------------------------------------


"""

def updateNotification(notification_object, text, screen):
    notification_object = myfont.render(text, 1, (255,255,255))
    screen.blit(notification_object, (225, 625-60))    


def moveSelector(key, grid, current_pos):
    global winner
    #Returns a 2-tuple (color, current_pos)
    if key == 'up':
        if (current_pos[1] - 1 >= 0):
            if (grid[current_pos[0]][current_pos[1] -1] == 0):
                current_pos[1] -= 1
                return(current_pos, GREEN) # Make Green
            else:
                current_pos[1] -= 1
                return(current_pos, RED) # Make Red              
   
    elif key == 'down':
        if (current_pos[1] + 1 <= 2):
            if (grid[current_pos[0]][current_pos[1] +1] == 0):
                current_pos[1] += 1
                return(current_pos, GREEN) # Make Green
            else:
                current_pos[1] += 1
                return(current_pos, RED) # Make Red  
   
    elif key == 'left':
        if (current_pos[0] - 1 >= 0):
            if (grid[current_pos[0] - 1][current_pos[1]] == 0):
                current_pos[0] -= 1
                return(current_pos, GREEN) # Make Green
            else:
                current_pos[0] -= 1
                return(current_pos, RED) # Make Red  
           
    elif key == 'right':
        if (current_pos[0] + 1 <= 2):
            if (grid[current_pos[0] + 1][current_pos[1]] == 0):
                current_pos[0] += 1
                return(current_pos, GREEN) # Make Green
            else:
                current_pos[0] += 1
                return(current_pos, RED) # Make Red 
            
    elif key == 'enter': #Switches player's turns and makes the current position red
        if (winner == 1):
            return(current_pos, BLUE) # Make Blue
        elif (winner == 2):
            return(current_pos, YELLOW) # Make Yellow
        else:
            return(current_pos, RED) # Make Red 
    
 
def checkGrid(grid):
    """ Returns (0/1/2, (i, 'r')/(i, 'c')/(i, 'd')/(i, 'id')"""
    #Check across rows
    for i in range(3):
        if(grid[i][0] != 0): #Making sure we don't check for equivalence of zeroes
            if (grid[i][0] == grid[i][1] and grid[i][0] == grid[i][2]):
                return [grid[i][0], (i, 'c')]
    #Check across columns
    for i in range(3):
        if(grid[0][i] != 0): #Making sure we don't check for equivalence of zeroes
            if (grid[0][i] == grid[1][i] and grid[0][i] == grid[2][i]):
                return [grid[0][i], (i, 'r')]
    #Check diagonals
    if (grid[1][1] == grid[2][2] and grid[2][2] == grid[0][0]):
        if (grid[1][1] != 0): #Making sure we don't have a zero diagonal
            return [grid[0][0], (i, 'd')]
    elif (grid[0][2] == grid[1][1] and grid[2][0] == grid[1][1]):
        if (grid[0][2] != 0): #Making sure we don't have a zero inverse diagonal
            return [grid[0][2], (i, 'id')]
    return [0, 'null'] #This only occurs if there isn't a winner

def gameFinished(grid):
    #Checks to see if there is a premature winner
    data = checkGrid(grid)
    result = data[0]
    if (result != 0): #This is only false if all zero's or a draw
            return True    #Returns True if there is a premature winner
    
    #Checks to see if every move has been played
    for i in range(3):
        for j in range(3):
            if (grid[i][j] == 0):
                return False
    #Returns true in the case of a draw and ever move played
    return True

def draw_winning_strikethrough(grid, screen):
    row_win = pygame.image.load("./images/row-win.png")
    column_win = pygame.image.load("./images/columns-win.png") 
    diagonal_win = pygame.image.load("./images/main-diagonal-win.png") 
    inverse_diagonal_win = pygame.image.load("./images/flipped-diagonal-win.png")
    data = checkGrid(grid)
    result = data[0]
    if (gameFinished(grid) == True and result != 0):
        data = checkGrid(grid)
        strikethrough = data[1]
        i = strikethrough[0]
        strikethrough_type = strikethrough[1]
        if (strikethrough_type == 'r'):
            if (i == 0):
                screen.blit(row_win, (55, 115))
            elif(i == 1):
                screen.blit(row_win, (55, 270))
            elif(i == 2):
                screen.blit(row_win, (55, 425))
            
        elif (strikethrough_type == 'c'):
            if (i == 0):
                screen.blit(column_win, (105, 85))
            elif(i == 1):
                screen.blit(column_win, (262, 85))
            elif(i == 2):
                screen.blit(column_win, (420, 85))
        elif (strikethrough_type == 'd'):
            screen.blit(diagonal_win, (45, 75))
        elif (strikethrough_type == 'id'):
            screen.blit(inverse_diagonal_win, (45, 75)) 


def gameStatus(grid):
    global screen
    global notification
    global game_state
    global player1_score
    global player2_score
    global usrTools
    if (gameFinished(grid) == True):
        data = checkGrid(grid)
        result = data[0]
        if (result == 1):
            notification = myfont.render(P1+' wins. Press "i" to play again', 1, (255,255,255))
            screen.blit(notification, (150, 40))
            if (game_state == 0):
                player1_score += 1
                usrTools.addNewResult(P1)
                usrTools.syncFile()
                winner = 1
            game_state = 1
        elif (result == 2):
            notification = myfont.render(P2+' wins. Press "i" to play again', 1, (255,255,255))
            screen.blit(notification, (150, 40))
            if (game_state == 0):
                player2_score += 1
                usrTools.addNewResult(P2)
                usrTools.syncFile()
                winner = 2
            game_state = 1
        elif (result == 0):
            notification = myfont.render('Match is drawn. Press "i" to play again', 1, (255,255,255))
            screen.blit(notification, (150, 40))
            game_state = 1
        
def reset(grid):
    for i in range(3):
        for j in range(3):
            grid[i][j] = 0
            

def drawBoard(screen):
    global player1_score
    global player2_score
    global player
    tictactoe_font = pygame.font.Font('./fonts/Mohave-Bold-Italics.ttf', 36)
    score_h1_font = pygame.font.Font('./fonts/Mohave-Bold-Italics.ttf', 24)
    score_text = score_h1_font.render('Scores:', 1, (255,255,255))
    score_font = pygame.font.Font('./fonts/Mohave-Bold-Italics.ttf', 16)
    player1_score_text = score_font.render(P1+' : {}'.format(player1_score), 1, (255,255,255))
    player2_score_text = score_font.render(P2+' : {}'.format(player2_score), 1, (255,255,255))
    current_player_font = pygame.font.Font('./fonts/Mohave-Bold-Italics.ttf', 20)
    current_player_text = current_player_font.render("Current Turn: Player {}".format(player), 1, (255,255,255))
    instruct_font = pygame.font.Font('./fonts/Mohave-Bold-Italics.ttf', 20)
    instruct_text = instruct_font.render("'L' for Leaderboard, 'C' for Controls".format(player), 1, (255,255,255))
    tictactoe = tictactoe_font.render("TIC-TAC-TOE", 1, (255,255,255)) 
    info_font = pygame.font.SysFont("monospace", 10)
    info_text_1 = info_font.render("It is player {}'s turn",1, (255,255,255))
    legend = pygame.image.load('./images/legend.png')
    screen.blit(tictactoe, (610, 50))
    screen.blit(legend, (580, 120))
    screen.blit(instruct_text, (610, 340))
    screen.blit(current_player_text, (610, 375))
    screen.blit(score_text, (610, 440))
    screen.blit(player1_score_text, (610, 485))
    screen.blit(player2_score_text, (610, 510)) 
            

    
"""

------------------------------------------------------------------------------------------------------------

      MAIN PROGRAM LOOP

------------------------------------------------------------------------------------------------------------

    
"""
                
p1=username(1)
P1=user['name']
p2=username(2)
P2=user['name']

while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  

            
        elif event.type == pygame.KEYDOWN:            
            
            """
            ------------------
            Player 1 Controls
            ------------------
            """
            
            if event.key == pygame.K_UP and game_state == 0:
                if (player == 1 and current_pos[1] != 0):
                    data = moveSelector('up', grid, current_pos)
                    current_pos = data[0]
                    current_color = data[1]
                    warning = False
                elif current_pos[1] == 0:
                    warning = True
                    notification = myfont.render('You cannot move further up', 1, (255,255,255))
                    screen.blit(notification, (225, 625-60))
                else:
                    warning = True
                    notification = myfont.render("It is "+P2+"'s turn", 1, (255,255,255))
                    screen.blit(notification, (225, 625-60))
                
            elif event.key == pygame.K_DOWN and game_state == 0:
                if (player == 1 and current_pos[1] != 2):
                    data = moveSelector('down', grid, current_pos)
                    current_pos = data[0]
                    current_color = data[1]
                    warning = False
                elif current_pos[1] == 2:
                    notification = myfont.render("You cannot move further down", 1, (255,255,255))
                    screen.blit(notification, (225, 625-60))
                    warning = True
                else:
                    notification = myfont.render("It is "+P2+"'s turn", 1, (255,255,255))
                    screen.blit(notification, (225, 625-60))
                    warning = True
            elif event.key == pygame.K_LEFT and game_state == 0:
                if (player == 1 and current_pos[0] != 0):
                    data = moveSelector('left', grid, current_pos)
                    current_pos = data[0]
                    current_color = data[1]
                    warning = False
                elif current_pos[0] == 0:
                    notification = myfont.render("You cannot move further left", 1, (255,255,255))
                    screen.blit(notification, (225, 625-60))
                    warning = True
                else:
                    notification = myfont.render("It is "+P2+"'s turn", 1, (255,255,255))
                    screen.blit(notification, (225, 625-60))
                    warning = True
            elif event.key == pygame.K_RIGHT and game_state == 0:
                if (player == 1 and current_pos[0] != 2):
                    data = moveSelector('right', grid, current_pos)
                    current_pos = data[0]
                    current_color = data[1]
                    warning = False
                elif current_pos[0] == 2:
                    notification = myfont.render("You cannot move further right", 1, (255,255,255))
                    screen.blit(notification, (225, 625-60))
                    warning = True
                else:
                    notification = myfont.render("It is "+P2+"'s turn", 1, (255,255,255))
                    screen.blit(notification, (225, 625-60))  
                    warning = True
                                    
                    
            """
            ------------------
            Player 2 Controls
            ------------------
            """
            
            if event.key == pygame.K_w and game_state == 0:
                if (player == 2 and current_pos[1] != 0):
                    data = moveSelector('up', grid, current_pos)
                    current_pos = data[0]
                    current_color = data[1]
                    warning = False
                elif current_pos[1] == 0:
                    notification = myfont.render("You cannot move further up", 1, (255,255,255))
                    screen.blit(notification, (225, 625-60))
                    warning = True
                else:
                    notification = myfont.render("It is "+P1+"'s turn", 1, (255,255,255))
                    screen.blit(notification, (225, 625-60))
                    warning = True
                
            elif event.key == pygame.K_s and game_state == 0:
                if (player == 2 and current_pos[1] != 2):
                    data = moveSelector('down', grid, current_pos)
                    current_pos = data[0]
                    current_color = data[1]
                    warning = False
                elif current_pos[1] == 2:
                    notification = myfont.render("You cannot mvoe further down", 1, (255,255,255))
                    screen.blit(notification, (225, 625-60)) 
                    warning = True
                else:
                    notification = myfont.render("It is "+P1+"'s turn", 1, (255,255,255))
                    screen.blit(notification, (225, 625-60))
                    warning = True
            elif event.key == pygame.K_a and game_state == 0:
                if (player == 2 and current_pos[0] != 0):
                    data = moveSelector('left', grid, current_pos)
                    current_pos = data[0]
                    current_color = data[1]
                    warning = False
                elif current_pos[0] == 0:
                    notification = myfont.render("You cannot move further left", 1, (255,255,255))
                    screen.blit(notification, (225, 625-60)) 
                    warning = True
                else:
                    notification = myfont.render("It is "+P1+"'s turn", 1, (255,255,255))
                    screen.blit(notification, (225, 625-60))
                    warning = True
            elif event.key == pygame.K_d and game_state == 0:
                if (player == 2 and current_pos[0] != 2):
                    data = moveSelector('right', grid, current_pos)
                    current_pos = data[0]
                    current_color = data[1]
                    warning = False
                    print(current_pos)
                elif current_pos[0] == 2:
                    notification = myfont.render("You cannot move further right", 1, (255,255,255))
                    screen.blit(notification, (225, 625-60))
                    warning = True
                else:
                    notification = myfont.render("It is "+P1+"'s turn", 1, (255,255,255))
                    screen.blit(notification, (225, 625-60))  
                    warning = True
                        
           
            if event.key == pygame.K_RETURN:
                if (player == 1 and grid[current_pos[0]][current_pos[1]] == 0):
                    grid[current_pos[0]][current_pos[1]] = 1
                    data = moveSelector('enter', grid, current_pos)
                    current_pos = data[0]
                    current_color = data[1]
                    player = 2
                elif(player == 2 and grid[current_pos[0]][current_pos[1]] == 0):
                    grid[current_pos[0]][current_pos[1]] = 2
                    data = moveSelector('enter', grid, current_pos)
                    current_pos = data[0]
                    current_color = data[1]                    
                    player = 1
                    
                    
            if (event.key == pygame.K_i and game_state == 1):
                reset(grid)
                current_pos = [1,1]
                player = 1
                winner = 0
                game_state = 0
            
            if event.key == pygame.K_l:
                root = Tk.Tk()
                root.title("Top 5 Most Wins")
                root.configure(bg = "black")
                label = Tk.Label(root, bg = "black", fg = "white", text= usrTools.getTop5Players())
                label.pack()
                center(root)
                label.after(8000, root.destroy)
                root.mainloop()
            
            if event.key == pygame.K_c:
                root = Tk.Tk()
                root.title("Controls")
                root.configure(bg = "black")
                label = Tk.Label(root, bg = "black", fg = "white", text= "Player 1 must use the UP, DOWN, LEFT and RIGHT arrows.\n Player 2 must use the keys W, S, A and D.\n Press ENTER to cement your choice of placement")
                label.pack()
                center(root)
                label.after(8000, root.destroy)
                root.mainloop()                
        
    
    # Set the screen background
    screen.fill(GRAY)
    # Updating notification
    screen.blit(notification, (225, 625-60))     
    
    #Checking game status
    gameStatus(grid)
    
    # Draw the grid
    for row in range(3):
        for column in range(3):
            color = WHITE
            if (row == current_pos[1] and column == current_pos[0]):
                color = current_color
                if (current_color == RED):
                    notification = myfont.render("You cannot use this spot", 1, (255,255,255))
                    screen.blit(notification, (225, 625-60))
                elif (current_color != RED and warning == False):
                    notification = myfont.render("This spot is available", 1, (255,255,255))
                    screen.blit(notification, (225, 625-60))                    
                    
            elif grid[column][row] == 1: #This convention is kind of backwards because of the way cartesian co-ordinates are switched with inex notation aij
                color = BLUE                 
            elif grid[column][row] == 2:
                color = YELLOW
                
                
            rect = pygame.draw.rect(screen,
                             color,
                             [50+(MARGIN + WIDTH) * column + MARGIN,
                              75+(MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
            
            #Draw x's and o's
            if grid[column][row] == 1:
                screen.blit(cross, (rect.centerx - 40, rect.centery - 40))
            elif grid[column][row] == 2:
                screen.blit(circle, (rect.centerx - 40, rect.centery - 40))
            
    
       
    #Drawing winning strikethrough
    draw_winning_strikethrough(grid, screen)
    
    #Drawing Board
    drawBoard(screen)
    
    # Limit to 60 frames per second
    clock.tick(60)
 
    
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
pygame.quit()

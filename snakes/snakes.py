import pygame, os
import Tkinter as Tk
import HighScores
from random import randint

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
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (51,104,255)

"""

------------------------------------------------------------------------------------------------------------
 GLOBALS
------------------------------------------------------------------------------------------------------------

"""

length = 0 #length of snake
current_direction = 'right'
score = 0
game_state = 0
difficulty = 1
message = ''
usrTools = HighScores.HighScores()
usrTools.loadData()

"""
------------------------------------------------------------------------------------------------------------
  SETTING UP GRID
------------------------------------------------------------------------------------------------------------
"""
 
# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 20
HEIGHT = 20
 
# This sets the margin between each cell
MARGIN = 2
 
# Creating grid
grid = []
for row in range(30):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(30):
        grid[row].append(0)  # Append a cell
 

"""

------------------------------------------------------------------------------------------------------------

INITIALIZING PYGAME and SCREEN

------------------------------------------------------------------------------------------------------------

"""


def randomStartingPosition():
    return [randint(2,29), randint(0, 29)]

#grid[y][x] = (x, y)

startingPosition = randomStartingPosition()
snakeCoords = [{'x': startingPosition[0],     'y': startingPosition[0]}, #Head
               {'x': startingPosition[0]- 1,  'y': startingPosition[0]},
               {'x': startingPosition[0]- 2,  'y': startingPosition[0]}] #Tail

# Initialize pygame
pygame.init()
 
# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [900, 660]
screen = pygame.display.set_mode(WINDOW_SIZE)
 
# Set title of screen
pygame.display.set_caption("Snakes")
 
# Loop until the user clicks the close button.
done = False
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
    
    def __init__(self):
        self.root = Tk.Tk()
        self.root.wm_title("Snake")
        self.label = Tk.Label(self.root, text=("Enter your username: "))
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

def updateGrid(x,y, grid):
    grid[y][x] = 0


def moveSnake(grid, direction, snakeCoords, screen):
    global game_state
    global message
    if (direction == 'right'  and game_state == 0):
        if (snakeCoords[0]['x'] < 29):
            snakeCoords.insert(0, {'x': snakeCoords[0]['x']+1, 'y':snakeCoords[0]['y']}) #Adding new head
            if (ateApple(grid, snakeCoords)):
                pass
            elif(ateSelf(grid, snakeCoords)):
                message = 'You bit yourself'
                gameOver(screen, message)                
                game_state = 1 
            elif(hitObstacle(grid, snakeCoords)):
                game_state = 1
                message = 'You hit an obstacle'
                gameOver(screen, message)                
                                  
            else:    
                updateGrid(snakeCoords[-1]['x'], snakeCoords[-1]['y'], grid)                
                del snakeCoords[-1]            
        else:
            message = ''
            gameOver(screen, message)
            game_state = 1
            
            
            
    elif(direction == 'left'  and game_state == 0):
        if (snakeCoords[0]['x'] >= 1):            
            snakeCoords.insert(0, {'x': snakeCoords[0]['x']-1, 'y':snakeCoords[0]['y']}) #Adding new head
            if (ateApple(grid, snakeCoords)):
                pass
            elif(hitObstacle(grid, snakeCoords)):
                message = 'You hit an obstacle'
                gameOver(screen, message)                
                game_state = 1      
            else:
                updateGrid(snakeCoords[-1]['x'], snakeCoords[-1]['y'], grid)
                del snakeCoords[-1]
        else:
            message = ''
            gameOver(screen, message)
            game_state = 1
    elif(direction == 'up'  and game_state == 0):
        if (snakeCoords[0]['y'] >= 1):            
            snakeCoords.insert(0, {'x': snakeCoords[0]['x'], 'y':snakeCoords[0]['y']-1}) #Adding new head
            if (ateApple(grid, snakeCoords)):
                pass
            elif(ateSelf(grid, snakeCoords)):
                message = 'You bit yourself'
                gameOver(screen, message)                
                game_state = 1 
            elif(hitObstacle(grid, snakeCoords)):
                message = 'You hit an obstacle'
                gameOver(screen, message)                
                game_state = 1    
            else:
                updateGrid(snakeCoords[-1]['x'], snakeCoords[-1]['y'], grid)
                del snakeCoords[-1]
        else:
            message = ''
            gameOver(screen, message)
            game_state = 1

    elif(direction == 'down'  and game_state == 0):
        if (snakeCoords[0]['y'] < 29):            
            snakeCoords.insert(0, {'x': snakeCoords[0]['x'], 'y':snakeCoords[0]['y']+1}) #Adding new head
            if (ateApple(grid, snakeCoords)):
                pass
            elif(ateSelf(grid, snakeCoords)):
                message = 'You bit yourself'
                gameOver(screen, message)                
                game_state = 1 
            elif(hitObstacle(grid, snakeCoords)):
                message = 'You hit an obstacle'
                gameOver(screen, message)                
                game_state = 1    
            else:
                updateGrid(snakeCoords[-1]['x'], snakeCoords[-1]['y'], grid)
                del snakeCoords[-1] 
        else:
            message = ''
            gameOver(screen, message)
            game_state = 1

def drawSnake(snakeCoords, grid):
    for i in range(len(snakeCoords)):
        x = snakeCoords[i]['x']
        y = snakeCoords[i]['y']
        grid[y][x] = 1
        


def gameOver(screen, message):
    h1 = pygame.font.SysFont("monospace", 36)
    h2 = pygame.font.SysFont("monospace", 22)
    h3 = pygame.font.SysFont("monospace", 15)
    # render text    
    game_over = h1.render("Game Over!", 1, (255,255,0))    
    if (message != ''):
        if (message == 'You bit yourself'):
            message_text = h2.render(message, 1, (255,255,0))
            screen.blit(message_text, (240, 200))            
        elif(message == 'You hit an obstacle'):
            message_text = h2.render(message, 1, (255,255,0))
            screen.blit(message_text, (225, 200))
    play_again = h3.render("Press 'r' to play again.", 1, (255,255,0))
    screen.blit(game_over, (240, 100))
    screen.blit(play_again, (240, 500)) 
        
        
def drawGrid(grid):
    global BLACK
    global RED
    global BLUE
    global MARGIN
    global WIDTH
    global HEIGHT
    for row in range(30):
        for column in range(30):
            color = BLACK
            if grid[row][column] == 1:
                color = GREEN
            elif grid[row][column] == 2:
                color = RED
            elif grid[row][column] == 3:
                color = BLUE
            pygame.draw.rect(screen, color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT]) 
def createObstacles():
    global grid
    obstacles = []
    num_obstacles = randint(2,6)
    for i in range(num_obstacles):
        seed_x = randint(0,24)
        seed_y = randint(0,24)
        #Size of obstaclebox
        for j in range(randint(2,5)):  #Width          
            for k in range(randint(2,5)): #Height
                prob = randint(0,4)
                if(prob !=4): #3 in 4 chance of occurring
                    obstacles.append({'x': seed_x + j, 'y': seed_y + k})
    for i in range(len(obstacles)):
        x = obstacles[i]['x']
        y = obstacles[i]['y']
        grid[y][x] = 3
    return obstacles           

#Creating Obstacles     
obstacles = createObstacles()

def createApple(grid):
    unique = False
    rand_x = 0
    rand_y = 0
    while (unique == False):        
        rand_x = randint(1,29)
        rand_y = randint(1,29)
        if (grid[rand_y][rand_x] == 0 and grid[rand_y - 1][rand_x - 1] == 0 and grid[rand_y - 1][rand_x] == 0 and grid[rand_y][rand_x - 1] == 0): #Making sure apple isn't around any near obstacles
            grid[rand_y][rand_x] = 2
            unique = True
    return [rand_x, rand_y]

#Creating Apple 
apple = createApple(grid)
            
def ateApple(grid, snakeCoords):
    global apple
    global score
    global current_direction
    if (snakeCoords[0]['x'] == apple[0] and snakeCoords[0]['y'] == apple[1]):
        grid[apple[1]][apple[0]] = 0
        score += 1
        apple = createApple(grid)
        return True
    else:
        return False

def ateSelf(grid, snakeCoords):
    global score
    head = snakeCoords[0]
    for i in range(1, len(snakeCoords)):
        if (head == snakeCoords[i]): #Snake bit itself
            return True  
    return False      
        
def reset():
    global score
    global grid
    global apple
    global snakeCoords
    global obstacles
    global message
    for i in range(30):
        for j in range(30):
            grid[i][j] = 0
    obstacles = createObstacles()
    apple = createApple(grid)
    score = 0
    difficulty = 1
    message = ''
    startingPosition = randomStartingPosition()
    snakeCoords = [{'x': startingPosition[0],     'y': startingPosition[0]}, #Head
                   {'x': startingPosition[0]- 1,  'y': startingPosition[0]},
               {'x': startingPosition[0]- 2,  'y': startingPosition[0]}] #Tail   
    


def hitObstacle(grid, snakeCoords):
    global obstacles
    for i in range(len(obstacles)):
        if (snakeCoords[0] == obstacles[i]):
            return True
    return False


def drawBoard(screen):
    global score
    global difficulty
    global P
    snakes_font = pygame.font.Font('./fonts/Mohave-Bold-Italics.ttf', 36)
    score_font = pygame.font.Font('./fonts/Mohave-Bold-Italics.ttf', 24)
    score_text = score_font.render((P + "'s Score: {}").format(score), 1, (255,255,255))
    difficulty_font = pygame.font.Font('./fonts/Mohave-Bold-Italics.ttf', 20)
    eight_bit_wonder_font = pygame.font.Font('./fonts/8-bit-wonder.ttf', 28)
    difficulty_text = difficulty_font.render('Difficulty: {}'.format(difficulty), 1, (255,255,255))
    snakes = eight_bit_wonder_font.render("SNAKES", 1, (255,255,255)) 
    info_font = pygame.font.SysFont("monospace", 10)
    info_text_1 = info_font.render('Avoid hitting the blue obstacles',1, (255,255,255))
    info_text_2 = info_font.render( 'Eat the apples to increase ',1,(255,255,255))
    info_text_3 = info_font.render( 'your score',1,(255,255,255))
    info_text_4 = info_font.render("Press 'l' to save progress, ",1,(255,255,255))
    info_text_5 = info_font.render("but not while game is active!",1,(255,255,255))
    legend = pygame.image.load('./images/legend.png')
    screen.blit(legend, (640, 120))
    screen.blit(snakes, (700, 50))
    screen.blit(info_text_1, (680, 315))
    screen.blit(info_text_2, (680, 345))
    screen.blit(info_text_3, (680, 355))
    screen.blit(info_text_4, (680, 385))
    screen.blit(info_text_5, (680, 395))
    screen.blit(difficulty_text, (680, 500))
    screen.blit(score_text, (680, 550)) 
    
    
    
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 

"""

-----------------------------------------------------

      MAIN PROGRAM LOOP

-----------------------------------------------------

    
"""

p = username()
P = user['name']

while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            usrTools.updateData()
            done = True  # Flag that we are done so we exit this loop
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and current_direction != 'down' and game_state == 0:
                current_direction = 'up'
                pass
            elif event.key == pygame.K_DOWN and current_direction != 'up' and game_state == 0:
                current_direction = 'down'
                pass
            elif event.key == pygame.K_LEFT and current_direction != 'right' and game_state == 0:
                current_direction = 'left'
                pass
            elif event.key == pygame.K_RIGHT and current_direction != 'left' and game_state == 0:
                current_direction = 'right'
                pass
            if event.key == pygame.K_r and game_state == 1:
                reset()
                game_state = 0
            if event.key == pygame.K_l and game_state == 1:
                usrTools.addNewResult(P, score)
                root = Tk.Tk()
                root.title("Best Scores")
                root.configure(bg = "black")
                label = Tk.Label(root, bg = "black", fg = "white", text = usrTools.getTop5())
                label.pack()
                center(root)
                label.after(8000, root.destroy)
                root.mainloop()            
            
    #Setting difficulty
    difficulty = (score // 3) + 1
    
    # Set the screen background
    screen.fill(GRAY)    
     
    # Draw the grid
    drawGrid(grid)
    
    #Move and draw the snake
    moveSnake(grid, current_direction, snakeCoords, screen)
    drawSnake(snakeCoords, grid)    
    
    #Drawing Board
    drawBoard(screen)
    
    #Displaying Game Over Screen
    if(game_state == 1):
            gameOver(screen, message)
 
    # Limit to 15 frames per second
    clock.tick(8 + difficulty)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
pygame.quit()

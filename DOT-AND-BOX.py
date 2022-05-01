import sys
import pygame
from pygame.locals import *
from easygui import *
from pygame import mixer

# initializing pygame and mixer
pygame.init()
mixer.init()

# setting background music
bg_music = pygame.mixer.Sound('./Tavern.ogg')
bg_music.set_volume(0.9)
bg_music.play(-1) # -1 for continuous playback

# creating golobal variables
clockobject = pygame.time.Clock()
fps = 60
screen_width = 1000
screen_height = 700
tile_size = 50
rectcoordls = []
scorels = []
firstrun = True
x, y = 0, 0
points_ = []
lp = len(points_)
px, py = 0, 0
plTurn = 1
run = True

# getting row and column size
def row_column(txt, val):
    text = f"Enter number of {txt}s\nnote's: {txt} value should not be more than {val}"
    title = f"{txt} window"
    return int(enterbox(text, title))

row = row_column("row", "13")
col = row_column("column", "19")

# setting box co-ordinates
boxls = []
for i in range(col): #19
    if i != col-1:
        for j in range(row): #13
            if j != row-1:
                f = (50+(i*50), 50+(j*50))
                ff, ss = f
                box = [f, (ff+50, ss), (ff+50, ss+50), (ff, ss+50)]
                boxls.append([(box[0], box[1]), (box[1], box[2]), (box[2], box[3]), (box[3], box[0])])

# creating dictionary
templist = []
for j in range(col+2): #21
    if j != 0 and j != col-1+2:
        for i in range(row+2): #15
            if i != 0 and i != row-1+2:
                templist.append(str(f'{j} {i}'))
dic = dict(zip(templist, [0 for i in range(1,248)]))

# drawing points
def draw_points():
    for j in range(col+2): #21
        if j != 0 and j != col-1+2:
            for i in range(row+2): #15
                if i != 0 and i != row-1+2:
                    pygame.draw.circle(screen, (255, 255, 255), (j * tile_size, i * tile_size), 5)

# define colours
BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PINK = (235, 65, 54)
BLUE = (66, 81, 245)
YELLOW = (245, 237, 12)

# define font
font = pygame.font.Font('freesansbold.ttf', 32)
font2 = pygame.font.Font('freesansbold.ttf', 60)

# creating player class
class Player():
    # initializtion
    def __init__(self, player, linecolor, boxcolor, opname, namecolour):
        self.begin = False
        self.linecolor = linecolor
        self.boxcolor = boxcolor
        self.player = player
        self.opname = opname
        self.namecolour = namecolour

    # function to indicate mouse position and draw circle in that position
    def IndicatePos(self, x, y):
        if x != '#':
            pygame.draw.circle(screen, self.linecolor, ((x+1)*50, (y+1)*50), 6)

    # function for checking mouse position is inside a point
    def checkpos(self, pos):
        mx, my = pos
        found = False
        
        x = 1
        for i in range(col+2): #21
            if i != 0 and i != col-1+2:
                y = 1
                for j in range(row+2): #15
                    if j != 0 and j != row-1+2:
                        if (mx <= (i*50)+5 and mx >= (i*50)-5) and (my <= (j*50)+5 and my >= (j*50)-5):
                            found = True
                            return (found, (i*50, j*50), str(f"{i} {j}"))
                    y += 1
                x += 1
                        
        return [found]

    # function for checking coordinates are not same and near
    def checkcoordAreNotSameAndNear(self):
        if (self.posStart[1] == self.posNow[1] and (self.posStart[0] == self.posNow[0]+50 or self.posStart[0] == self.posNow[0]-50)) \
        or (self.posStart[0] == self.posNow[0] and (self.posStart[1] == self.posNow[1]+50 or self.posStart[1] == self.posNow[1]-50)):
            return True
        return False

    # function for checking closed boxes
    def checkForClosedBox(self):
        global firstrun
        for i in boxls:
            count = 0
            for k in i:
                if any(k in sl for sl in points_) or any(k[::-1] in sl  for sl in points_):
                    count += 1
                    
            if count == 4:
                if not any(i[0][0] in l for l in rectcoordls) or firstrun:
                    firstrun = False
                    scorels.append(self.player)
                    rectcoordls.append((i[0][0], self.boxcolor, self.player[0].upper(), self.namecolour))
                
    # function for drawing rectangle and naming
    def drawRect(self):
        for i, j, k, l in rectcoordls:
            pygame.draw.rect(screen, j, (i[0], i[1], 50, 50), 0)

            box_name_show = font2.render(k, True, l)
            box_name_Rect = box_name_show.get_rect()
            box_name_Rect.center = (3+i[0]+box_name_Rect.width//2, i[1]+box_name_Rect.height//2)
            screen.blit(box_name_show, box_name_Rect)
            
    # function for getting line start and end coordinates
    def linecoord(self):
        if any(pygame.mouse.get_pressed()) and not self.begin:
            self.posStart = pygame.mouse.get_pos()
            value = self.checkpos(self.posStart)
            if value[0]:
                dic[value[2]] += 1
                if dic[value[2]] <= 4:
                    self.posStart = value[1]
                    self.begin = True

        if self.begin:
            self.posNow = pygame.mouse.get_pos()
            pygame.draw.line(screen, self.linecolor, (self.posStart[0], self.posStart[1]), (self.posNow[0], self.posNow[1]), 5)
                                                                                            

        if not any(pygame.mouse.get_pressed()) and self.begin:
            value = self.checkpos(self.posNow)
            if value[0]:
                self.posNow = value[1]
                if self.checkcoordAreNotSameAndNear():
                    dic[value[2]] += 1
                    if dic[value[2]] <= 4:
                        if not any((self.posStart, self.posNow) in sl for sl in points_) and not any((self.posNow, self.posStart) in sl for sl in points_):
                            points_.append(((self.posStart, self.posNow), self.linecolor))
                            self.begin = False

    # function for drawing line
    def linedraw(self):
        for i in range(len(points_)):
            pygame.draw.line(screen, points_[i][1], (points_[i][0][0][0], points_[i][0][0][1]), (points_[i][0][1][0], points_[i][0][1][1]), 5)

    # calling all self function
    def update(self, x, y):
        global lp
        self.linecoord()
        self.IndicatePos(x, y)
        self.checkForClosedBox()
        self.linedraw()
        self.drawRect()
        if len(points_) > lp:
            lp = len(points_)
            return True
        else:
            return False

# function for getting mouse position in pygame window
def getPos(mx, my):
    found = False
    px, py = '#', '#'

    x = 0
    for i in range(col+2): #21
        if i != 0 and i != col-1+2:
            y = 0
            for j in range(row+2): #15
                if j != 0 and j != row-1+2:
                    if (mx <= (i*50)+5 and mx >= (i*50)-5) and (my <= (j*50)+5 and my >= (j*50)-5):
                        px, py = x, y
                        found = True
                    if found:
                        break
                  
                    y += 1

            if found:
                break

            x += 1

    return (px, py)

# getting player info from user
choices = ["PINK", "GREEN", "BLUE", "BLACK", "YELLOW"]
def getRequiredData(p):
    text = f"Enter {p} name"
    title = "name window"
    username = str(enterbox(text, title))
    
    text = f"Select {p} line colour"
    title = "line colour"
    lineColour = str(choicebox(text, title, choices))
    
    choices.remove(lineColour)

    text = f"Select {p} name colour"
    title = "name colour"
    nameColour = str(choicebox(text, title, choices))

    choices.remove(nameColour)
    
    return [username, lineColour, lineColour, nameColour]

player1Data = getRequiredData("player1")
player2Data = getRequiredData("player2")

un1, lc1, bc1, nc1 = player1Data
un2, lc2, bc2, nc2 = player2Data
# creating player object
player1 = Player(un1, lc1, bc1, un2, nc1)
player2 = Player(un2, lc2, bc2, un1, nc2)

# creating font
player_name_show = font.render(player1.player, True, player1.linecolor)
turn_show = font.render("Turn: ", True, player1.linecolor)

# creating pygame display window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('DOT AND BOX')

while run:
    clockobject.tick(fps) # setting fps
    pygame.draw.rect(screen, RED, (0, 0, screen_width, screen_height)) # drawing background

    # checking for game end
    if len(scorels) != len(boxls): #216

        draw_points() # calling drawing points function

        # player turn
        if plTurn == 1:
            ls = len(scorels)
            if player1.update(px, py):
                if len(scorels) > ls and scorels[-1] == player1.player:
                    plTurn = 1
                    player_name_show = font.render(player1.player, True, player1.linecolor)
                    turn_show = font.render("Turn: ", True, player1.linecolor)
                else:
                    plTurn = 2
                    player_name_show = font.render(player2.player, True, player2.linecolor)
                    turn_show = font.render("Turn: ", True, player2.linecolor)
        else:
            ls = len(scorels)
            if player2.update(px, py):
                if len(scorels) > ls and scorels[-1] == player2.player:
                    plTurn = 2
                    player_name_show = font.render(player2.player, True, player2.linecolor)
                    turn_show = font.render("Turn: ", True, player2.linecolor)
                else:
                    plTurn = 1
                    player_name_show = font.render(player1.player, True, player1.linecolor)
                    turn_show = font.render("Turn: ", True, player1.linecolor)


        # display scores
        player_name_Rect = player_name_show.get_rect()
        screen.blit(player_name_show, (screen_width - player_name_Rect.width - 3, screen_height - player_name_Rect.height - 3))
    
        turn_Rect = turn_show.get_rect()
        screen.blit(turn_show, (screen_width - turn_Rect.width - 3 - player_name_Rect.width, screen_height - turn_Rect.height - 3))

        player1_show = font.render(f"{player1.player}'s Score: {scorels.count(un1)}", True, player1.linecolor)
        player1_Rect = player1_show.get_rect()
        screen.blit(player1_show, (10, screen_height - player1_Rect.height - 3))

        player2_show = font.render(f"{player2.player}'s Score: {scorels.count(un2)}", True, player2.linecolor)
        player2_Rect = player2_show.get_rect()
        screen.blit(player2_show, (player1_Rect.width + 25, screen_height - player2_Rect.height - 3))

    # if ends displaying result
    else:
        p1 = scorels.count(un1)
        p2 = scorels.count(un2)

        if p1 > p2:
            message = f"{un1} win"
        elif p1 < p2:
            message = f"{un2} win"
        else:
            message = "match draw"

        title = "match result"
        msg = msgbox(message, title)
        sys.exit()

    # getting mouse position inside a window
    mouse_presses = pygame.mouse.get_pressed()
    if mouse_presses[0]:
        mx, my = pygame.mouse.get_pos()
        px, py = getPos(mx, my)

    # evevts listener
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
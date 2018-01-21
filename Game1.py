"""
 This game is made by Octavio for fun :D



 ENJOY :D


TO DO:

Draw map screen

home screen

game over screen

pictures

fix turning bug










"""

import array
import pygame
import math
import sys

from pygame.locals import *
import random

# Define constants
# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# dimensions
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900
G_WIDTH = 15
# rate
SPEED = 60 * 60 * 24 * 12
# physics
G_CONST = 6.67408 * 10 ** -11
# player constants
PLAYER_RADIUS = 5
PlAYER_SPEED = 50
PLAYER_1_SCORE = 0
PLAYER_2_SCORE = 0
PLAYER_RELOAD = 200
# game_constants
MAX_POWERUPS = 15


class PowerUp:
    def _init_(self):
        self.x = 0
        self.y = 0
        self.width = G_WIDTH
        self.id = 0
        self.color = (0, 0, 0)

    def type(self, x):
        if x == 1:
            self.id = 1
            self.color = (255, 0, 0)
        if x == 2:
            self.id = 2
            self.color = (0, 255, 0)
        if x == 3:
            self.id = 3
            self.color = (0, 0, 255)
        if x == 4:
            self.id = 4
            self.color = (255, 255, 0)
        if x == 5:
            self.id = 5
            self.color = (255, 0, 255)
        if x==6:
            self.id=6
            self.color=(0,255,255)


class Block:
    def _init_(self):
        # block with location x y and size, Boolean if present or not, Boolean if contains player,
        self.x = 0
        self.y = 0
        self.width = G_WIDTH
        self.color = BLACK
        # block is true/false
        self.real = False
        # is there a player on me
        self.playerPresent = False

    def setTrue(self, boolean):
        if boolean == True:
            self.color = BLACK
            self.real = True
        else:
            self.color = WHITE
            self.real = False


class Bullet:
    def _init_(self):
        # velocity location (direction for later maybe)
        self.isAlive = True
        self.x = 0
        self.y = 0
        self.velocityX = 0
        self.velocityY = 0
        self.velocityBullet = 0
        self.angleFromNormal = 0
        self.length = 0
        self.bounce = 0
        self.id = 0

    def ammoType(self, x):
        # ammo type:1=pistol, 2=machine gun, 3=bazooka, 4=lazer
        if x == 1:
            self.velocityBullet = 100
            self.length = 3
            self.id = 1

        if x == 2:
            self.velocityBullet = 100
            self.length = 2
            self.id = 2
        if x == 3:
            self.velocityBullet = 50
            self.length = 6
            self.id = 3
        if x == 4:
            self.velocityBullet = 200
            self.length = 3
            self.id = 4
        if x==6:
            self.velocityBullet=400
            self.length=5
            self.id=6

class Button:
    def __init__(self):
        self.x=0
        self.y=0
        self.sizeX=0
        self.sizeY=0
        self.text=''
        self.color=(0,100,0)
        self.colorT=(100,0,100)
        self.fontSize=40
    def draw(self,screen):
        pygame.draw.rect(screen, self.color, (SCREEN_WIDTH / self.x, SCREEN_HEIGHT / self.y, self.sizeX, self.sizeY))
        font = pygame.font.Font(None, self.fontSize)
        text = font.render(self.text, 1, self.colorT)
        textpos = text.get_rect()
        textpos.centerx= SCREEN_WIDTH/self.x+self.sizeX/2
        textpos.centery = SCREEN_HEIGHT/self.y+self.sizeY/2
        screen.blit(text, textpos)
    def getMinX(self):
        return SCREEN_WIDTH/self.x
    def getMinY(self):
        return SCREEN_HEIGHT/self.y
    def getMaxX(self):
        return SCREEN_WIDTH/self.x+self.sizeX
    def getMaxY(self):
        return SCREEN_HEIGHT/self.y+self.sizeY


class Player:
    def __init__(self):
        # id
        self.id = 0
        self.initialX = 0
        self.initialY = 0
        self.score = 0
        self.color=(0,0,0)
        # location
        self.x = 0
        self.y = 0

        # velocity
        self.velocityX = 0.0
        self.velocityY = 0.0

        # direction
        self.angleFromNormal = 0.0

        # affected area
        self.radius = 0

        # attributes
        self.health = 100
        self.ammo = 20
        self.maxSpeed = 20
        self.fireRate = 1
        self.reload = 0

        # ammo type:1=pistol, 2=machine gun, 3=bazooka, 4=lazer
        self.ammoType = 1
        # power-ups :

        self.fastFire = False
        self.fastMove = False
        self.bounce = 0

    def isDead(self):
        self.x = self.initialX
        self.y = self.initialY
        self.bounce = 0
        self.changeAmmo(1)
        self.fastFire = False
        self.fastMove = False
        self.maxSpeed = PlAYER_SPEED
        self.score += 1

    def changeAmmo(self, id):

        if id == 1:
            self.fireRate = 400
            self.ammo = 20
            self.ammoType = id
        if id == 2:
            self.fireRate = 1000
            self.ammo = 50
            self.ammoType = id
        if id == 3:
            self.fireRate = 150
            self.ammo = 10
            self.ammoType = id
        if id == 4:
            self.fireRate = 2000
            self.ammo = 100
            self.ammoType = id
        if id == 5:
            self.bounce += 1
        if id==6:
            self.fireRate=5000
            self.ammo=20
            self.ammoType=id

class Picture:
    def __init__(self):
        self.picture_l = []
        self.picture_l.append(pygame.transform.scale(pygame.image.load("img/intro.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT)))
        self.index=0
    def update(self):
        if self.index>=len(self.picture_1):
            self.index=0
            return self.picture_1[self.index]
        else:
            self.index+=1
            return self.picture_1[self.index]



def main():
    """
    This is our main program.
    """
    pygame.init()

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("2d Shooter")

    #initialize button for keeping score and time
    bMain = Button()
    bMain.sizeX = 200
    bMain.sizeY = 20
    bMain.x = 1.2
    bMain.y = 1.05
    bMain.fontSize = 23
    bMain.color = (255, 0, 255)
    bMain.colorT = (0, 0, 0)

    # initialize required variables/lists
    bullet_set = set()
    bulletD_set = set()
    powerup_set = set()
    powerupD_set = set()

    enemy_list = []
    block_list = []
    player_list = []
    maxPowerUps = 0

    # grid to manage location and efficient collision detection
    # ---------------------------------------------------------------------------
    #    Grid is my attempt at broad phase collision detection for the whole game
    #    I attach objects that can collide to a 2d grid list
    #    if there are more than two objects of a certain type (bullet, wall),(player,wall)(bullet,Player)(bullet,bullet)
    #    then I switch to narrow phase collision detection between the objects of that list
    # ---------------------------------------------------------------------------
    grid = []

    # initialize grid with Blocks, so first two dimensions are static
    block = Block()
    for x in range(0, int(SCREEN_WIDTH / G_WIDTH)):
        grid.append([])
        for y in range(0, int(SCREEN_HEIGHT / G_WIDTH)):
            grid[x].append([])
            block = Block()
            block.x = x * G_WIDTH
            block.y = y * G_WIDTH
            block.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            rand = int(random.randint(0, 10))
###--------------make true for random map(first below)
            if rand == 1:
                block.setTrue(False)
            else:
                block.setTrue(False)
            if x == 0 or y == 0 or y == int(SCREEN_HEIGHT / G_WIDTH) - 1 or x == int(SCREEN_WIDTH / G_WIDTH) - 1:
                block.setTrue(True)

            grid[x][y].append(block)
   #random map true or false (also for clearing)
    def generateRandomMap(bool):
        for x in range(0, int(SCREEN_WIDTH / G_WIDTH)):
            for y in range(0, int(SCREEN_HEIGHT / G_WIDTH)):
                for block in grid[x][y]:

                    rand = int(random.randint(0, 10))
                    if rand == 1:
                        block.setTrue(bool)
                    else:
                        block.setTrue(False)
                    if x == 0 or y == 0 or y == int(SCREEN_HEIGHT / G_WIDTH) - 1 or x == int(SCREEN_WIDTH / G_WIDTH) - 1:
                        block.setTrue(True)

    # -----FIND---SPARE--SPOT-----
    def getSpareSpot():

        spareX = 0
        while spareX == 0:
            x = int(random.randint(100, SCREEN_WIDTH - 100) / G_WIDTH)
            y = int(random.randint(100, SCREEN_HEIGHT - 100) / G_WIDTH)

            spareX = 0
            spareY = 0
            for a in range(x, int(SCREEN_WIDTH / G_WIDTH)):
                if spareX == 0:
                    for b in range(y, int(SCREEN_HEIGHT / G_WIDTH)):
                        if spareY == 0:
                            for block in grid[x][y]:
                                if not block.real:
                                    spareX = a * G_WIDTH
                                    spareY = b * G_WIDTH

                                    return (spareX, spareY)

    # initialise player 1
    player = Player()
    x, y = getSpareSpot()
    player.x = x + PLAYER_RADIUS
    player.y = y + PLAYER_RADIUS
    player.radius = PLAYER_RADIUS
    player.maxSpeed = PlAYER_SPEED
    player.changeAmmo(1)
    player.fastFire = False
    player.id = 1
    player.color=(255,0,0)
    player.initialX = player.x
    player.initialY = player.y
    player_list.append(player)

    # player 2
    player = Player()
    player.x = random.randint(500, 800)
    player.y = (random.randint(500, 800))
    player.radius = PLAYER_RADIUS
    player.maxSpeed = PlAYER_SPEED
    player.initialX = player.x
    player.initialY = player.y
    player.color=(0,0,255)
    player.id = 2
    player.changeAmmo(1)
    player_list.append(player)

    clock = pygame.time.Clock()
    seconds = 0
    seconds2 = 0
    intro = True
    game=False
    outro=False

#----------------Immages:-------------------------




    while True:
#-----------------INTRO---------------------------



        while intro:
            screen.fill(BLACK)
            #draw intro immage:
            img_beginning = pygame.transform.scale(pygame.image.load("img/intro.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(img_beginning, (0, 0))

            #draw buttons:

            bDM = Button()
            bDM.sizeX = 150
            bDM.sizeY = 70
            bDM.x = 5
            bDM.y = 4
            bDM.color = (255, 255, 255)
            bDM.colorT = (0, 0, 0)
            bDM.text = 'Draw Map'
            bDM.draw(screen)

            bQ = Button()
            bQ.sizeX = 150
            bQ.sizeY = 70
            bQ.x = 1.6
            bQ.y = 4
            bQ.color = (255, 255, 255)
            bQ.colorT = (0, 0, 0)
            bQ.text = 'Quit'
            bQ.draw(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if click[0]==1:
                if mouse[0]>bDM.getMinX()and mouse[0]<bDM.getMaxX()and mouse[1]>bDM.getMinY()and mouse[1]<bDM.getMaxY():
                    intro = False
                    drawMap = True
                if mouse[0]>bQ.getMinX()and mouse[0]<bQ.getMaxX()and mouse[1]>bQ.getMinY()and mouse[1]<bQ.getMaxY():
                    sys.exit()




            clock.tick(15)
            pygame.display.flip()


#------------INTRO END-----------------
#--------------DRAW MAP SCREEN----------------
        player1=False
        player2=False
        while drawMap:
            screen.fill(BLACK)
            # wall
            for x in range(0, int(SCREEN_WIDTH / G_WIDTH)):
                for y in range(0, int(SCREEN_HEIGHT / G_WIDTH)):
                    for block in grid[x][y]:
                        pygame.draw.rect(screen, block.color, (block.x, block.y, G_WIDTH, G_WIDTH))
#-------------buttons------
           #spawns
            bP1S = Button()
            bP1S.sizeX = 50
            bP1S.sizeY = 20
            bP1S.x = 1.2
            bP1S.y = 1.25
            bP1S.fontSize = 23
            bP1S.color = (255, 0, 0)
            bP1S.colorT = (0, 255, 0)
            bP1S.text = 'Save Player 1'
            bP1S.draw(screen)
            bP1 = Button()
            bP1.sizeX = 50
            bP1.sizeY = 20
            bP1.x = 1.2
            bP1.y = 1.2
            bP1.fontSize = 23
            bP1.color = (255, 0, 0)
            bP1.colorT = (0, 255, 0)
            bP1.text = 'Spawn Player 1'
            bP1.draw(screen)
            #spawn 2
            bP2S = Button()
            bP2S.sizeX = 50
            bP2S.sizeY = 20
            bP2S.x = 1.2
            bP2S.y = 1.35
            bP2S.fontSize = 23
            bP2S.color = (0, 0, 255)
            bP2S.colorT = (0, 255, 0)
            bP2S.text = 'Save Player 2'
            bP2S.draw(screen)
            bP2 = Button()
            bP2.sizeX = 50
            bP2.sizeY = 20
            bP2.x = 1.2
            bP2.y = 1.3
            bP2.fontSize = 23
            bP2.color = (0, 0, 255)
            bP2.colorT = (0, 255, 0)
            bP2.text = 'Spawn Player 2'
            bP2.draw(screen)
            #random draw
            bR = Button()
            bR.sizeX = 50
            bR.sizeY = 20
            bR.x = 1.2
            bR.y = 1.05
            bR.fontSize=23
            bR.color = (255, 0, 255)
            bR.colorT = (0, 0, 0)
            bR.text = 'D r a w - R a n d o m'
            bR.draw(screen)
            # clear
            bC = Button()
            bC.sizeX = 50
            bC.sizeY = 20
            bC.x = 1.2
            bC.y = 1.15
            bC.fontSize = 23
            bC.color = (255, 0, 255)
            bC.colorT = (0, 0, 0)
            bC.text = 'C l e a r '
            bC.draw(screen)
            #play
            bP = Button()
            bP.sizeX = 50
            bP.sizeY = 20
            bP.x = 1.2
            bP.y = 1.1
            bP.fontSize = 23
            bP.color = (255, 0, 255)
            bP.colorT = (0, 0, 0)
            bP.text = 'P L A Y'
            bP.draw(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()


            if click[0] == 1 :

                x = int(mouse[0] / G_WIDTH)
                y = int(mouse[1] / G_WIDTH)
                if (not (player1 or player2)) and mouse[0]<SCREEN_WIDTH-10 and mouse[1]<SCREEN_HEIGHT-10:
                    for block in grid[x][y]:
                        block.setTrue(True)

                if mouse[0] > bP1S.getMinX() and mouse[0] < bP1S.getMaxX() and mouse[1] > bP1S.getMinY() and mouse[1] < bP1S.getMaxY():
                    player1=False
                if mouse[0] > bP1.getMinX() and mouse[0] < bP1.getMaxX() and mouse[1] > bP1.getMinY() and mouse[1] < bP1.getMaxY():
                    player1=True

                if mouse[0] > bP2S.getMinX() and mouse[0] < bP2S.getMaxX() and mouse[1] > bP2S.getMinY() and mouse[1] < bP2S.getMaxY():
                    player2=False
                if mouse[0] > bP2.getMinX() and mouse[0] < bP2.getMaxX() and mouse[1] > bP2.getMinY() and mouse[1] < bP2.getMaxY():
                    player2=True

                if mouse[0] > bC.getMinX() and mouse[0] < bC.getMaxX() and mouse[1] > bC.getMinY() and mouse[1] < bC.getMaxY():
                    generateRandomMap(False)
                if mouse[0] > bR.getMinX() and mouse[0] < bR.getMaxX() and mouse[1] > bR.getMinY() and mouse[1] < bR.getMaxY():
                    generateRandomMap(True)

                if mouse[0] > bP.getMinX() and mouse[0] < bP.getMaxX() and mouse[1] > bP.getMinY() and mouse[1] < bP.getMaxY():
                    drawMap = False
                    startTime = pygame.time.get_ticks()
                    game = True

                if player1 and not(mouse[0] > bP1S.getMinX() and mouse[0] < bP1S.getMaxX() and mouse[1] > bP1S.getMinY() and mouse[1] < bP1S.getMaxY()):
                    for player in player_list:
                        if player.id == 1:
                            player.initialX = mouse[0]
                            player.initialY = mouse[1]
                            player.x = player.initialX
                            player.y = player.initialY
                if player2 and not(mouse[0] > bP2S.getMinX() and mouse[0] < bP2S.getMaxX() and mouse[1] > bP2S.getMinY() and mouse[1] < bP2S.getMaxY()):
                    for player in player_list:
                        if player.id == 2:

                            player.initialX = mouse[0]
                            player.initialY = mouse[1]
                            player.x=player.initialX
                            player.y=player.initialY

            for player in player_list:
                pygame.draw.line(screen, BLACK, (player.x, player.y), (
                    player.x + player.radius * 2 * math.cos(player.angleFromNormal),
                    player.y + player.radius * 2 * math.sin(player.angleFromNormal)), 2)
                pygame.draw.circle(screen, player.color, (int(player.x), int(player.y)), int(player.radius))
            clock.tick(60)
            pygame.display.flip()


#---------MAIN LOOP-------------------
        while game:

            fps = clock.get_fps()
            ms = pygame.time.get_ticks()-startTime
            seconds = int(ms / 1000)

            if fps < 1:
                fps = 1

            # events:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

            # -----------PLAYER 1--------------------------
            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                for player in player_list:

                    if player.id == 1:
                        player.velocityX = PlAYER_SPEED * math.cos(player.angleFromNormal)
                        player.velocityY = PlAYER_SPEED * math.sin(player.angleFromNormal)

            if keys[pygame.K_DOWN]:
                for player in player_list:
                    if player.id == 1:
                        player.velocityX = -PlAYER_SPEED * math.cos(player.angleFromNormal)
                        player.velocityY = -PlAYER_SPEED * math.sin(player.angleFromNormal)

            if keys[pygame.K_DOWN]==False and keys[pygame.K_UP] == False:
                for player in player_list:
                    if player.id == 1:
                        player.velocityY = 0
                        player.velocityX = 0
            if keys[pygame.K_RIGHT]:
                for player in player_list:
                    if player.id == 1:
                        player.angleFromNormal += math.pi / 50

            if keys[pygame.K_LEFT]:
                for player in player_list:
                    if player.id == 1:
                        player.angleFromNormal -= math.pi / 50

                # ---------PLYER 1----------BULLET-------

            if keys[pygame.K_m]:

                for player in player_list:
                    if player.id == 1:

                        for powerup in powerup_set:
                            if (int(player.x / G_WIDTH) == int(powerup.x / G_WIDTH)) and (
                                    int(player.y / G_WIDTH) == int(powerup.y / G_WIDTH)):
                                player.changeAmmo(powerup.id)
                                maxPowerUps -= 1
                                powerupD_set.add(powerup)

                        player.reload += player.fireRate / fps
                        if player.ammo > 0 and player.reload >= PLAYER_RELOAD:
                            bullet = Bullet()
                            bullet.ammoType(player.ammoType)
                            bullet.angleFromNormal = player.angleFromNormal
                            bullet.x = player.x + player.radius * 2 * math.cos(player.angleFromNormal)
                            bullet.y = player.y + player.radius * 2 * math.sin(player.angleFromNormal)

                            bullet.velocityX = bullet.velocityBullet * math.cos(bullet.angleFromNormal)
                            bullet.velocityY = bullet.velocityBullet * math.sin(bullet.angleFromNormal)
                            player.ammo -= 1
                            bullet.bounce = player.bounce
                            player.reload = 0
                            bullet_set.add(bullet)
            if keys[pygame.K_m]==False:
                for player in player_list:
                    if player.id == 1:

                        if player.reload <= PLAYER_RELOAD:
                            player.reload += player.fireRate / fps
                            # ---------------------------infinit ammo for now----------------------

            # -----------PLAYER 2--------------------------
            if keys[pygame.K_e]:
                for player in player_list:
                    if player.id == 2:
                        player.velocityX = PlAYER_SPEED * math.cos(player.angleFromNormal)
                        player.velocityY = PlAYER_SPEED * math.sin(player.angleFromNormal)

            if keys[pygame.K_d]:
                for player in player_list:
                    if player.id == 2:
                        player.velocityX = -PlAYER_SPEED * math.cos(player.angleFromNormal)
                        player.velocityY = -PlAYER_SPEED * math.sin(player.angleFromNormal)

            if keys[pygame.K_d] == False and keys[pygame.K_e] == False:
                for player in player_list:
                    if player.id == 2:
                        player.velocityY = 0
                        player.velocityX = 0

            if keys[pygame.K_s]:
                for player in player_list:
                    if player.id == 2:
                        player.angleFromNormal -= math.pi / 50

            if keys[pygame.K_f]:
                for player in player_list:
                    if player.id == 2:
                        player.angleFromNormal += math.pi / 50

            # -------player 2 bullet
            if keys[pygame.K_q]:

                for player in player_list:
                    if player.id == 2:

                        for powerup in powerup_set:
                            if (int(player.x / G_WIDTH) == int(powerup.x / G_WIDTH)) and (
                                    int(player.y / G_WIDTH) == int(powerup.y / G_WIDTH)):
                                player.changeAmmo(powerup.id)
                                maxPowerUps -= 1
                                powerupD_set.add(powerup)

                        player.reload += player.fireRate / fps
                        if player.ammo > 0 and player.reload >= PLAYER_RELOAD:
                            bullet = Bullet()
                            bullet.isAlive = True
                            bullet.angleFromNormal = player.angleFromNormal
                            bullet.x = player.x + player.radius * 2 * math.cos(player.angleFromNormal)
                            bullet.y = player.y + player.radius * 2 * math.sin(player.angleFromNormal)
                            bullet.ammoType(player.ammoType)
                            bullet.velocityX = bullet.velocityBullet * math.cos(bullet.angleFromNormal)
                            bullet.velocityY = bullet.velocityBullet * math.sin(bullet.angleFromNormal)
                            player.ammo -= 1
                            bullet.bounce = player.bounce
                            player.reload = 0
                            bullet_set.add(bullet)

            if keys[pygame.K_q] == False:
                for player in player_list:
                    if player.id == 2:

                        if player.reload <= PLAYER_RELOAD:
                            player.reload += player.fireRate / fps

            # ----------------------------END OF EVENTS---------------------------------------------------------

            # -------------------------PHYSICS AND GAME LOGIC

            # bullet physics with blocks --------------for now same as player physics?---------------:

            for bullet in bullet_set:
                x = int(bullet.x / G_WIDTH)
                y = int(bullet.y / G_WIDTH)
                xPot = bullet.x + (1 / fps) * bullet.velocityX
                yPot = bullet.y + (1 / fps) * bullet.velocityY

                # for block on right (x+1) out of range
                for block in grid[x + 1][y]:
                    # if real and crossing(x velocity positive) make velocity x 0 in that direction
                    if block.real:
                        # if the potential location is greater than block.x
                        if (xPot + bullet.length) > block.x and bullet.velocityX > 0:
                            if bullet.id == 3:
                                if block.x == 0 or block.y == 0 or int(block.y / G_WIDTH) == int(
                                        SCREEN_HEIGHT / G_WIDTH) - 1 or (block.x / G_WIDTH) == int(
                                        SCREEN_WIDTH / G_WIDTH) - 1:
                                    bulletD_set.add(bullet)
                                else:
                                    block.real = False
                                    block.color = WHITE
                                    bulletD_set.add(bullet)

                                    break

                            if bullet.bounce > 0:
                                bullet.velocityX *= - 1
                                bullet.bounce -= 1
                                bullet.angleFromNormal = 3 * math.pi - bullet.angleFromNormal
                            else:
                                bulletD_set.add(bullet)

                # block on left
                for block in grid[x - 1][y]:
                    if block.real:
                        if xPot - bullet.length < (block.x + G_WIDTH) and bullet.velocityX < 0:

                            if bullet.id == 3:
                                if block.x == 0 or block.y == 0 or int(block.y / G_WIDTH) == int(
                                        SCREEN_HEIGHT / G_WIDTH) - 1 or (block.x / G_WIDTH) == int(
                                        SCREEN_WIDTH / G_WIDTH) - 1:
                                    bulletD_set.add(bullet)
                                else:
                                    block.real = False
                                    block.color = WHITE
                                    bulletD_set.add(bullet)

                                break

                            if bullet.bounce > 0:
                                bullet.velocityX *= -1
                                bullet.bounce -= 1
                                bullet.angleFromNormal = 3 * math.pi - bullet.angleFromNormal
                            else:
                                bulletD_set.add(bullet)
                # for block on top (y-1)
                for block in grid[x][y - 1]:
                    if block.real:
                        if yPot - bullet.length < (block.y + G_WIDTH) and bullet.velocityY < 0:
                            if bullet.id == 3:
                                if block.x == 0 or block.y == 0 or int(block.y / G_WIDTH) == int(
                                        SCREEN_HEIGHT / G_WIDTH) - 1 or (block.x / G_WIDTH) == int(
                                        SCREEN_WIDTH / G_WIDTH) - 1:
                                    bulletD_set.add(bullet)
                                else:
                                    block.real = False
                                    block.color = WHITE
                                    bulletD_set.add(bullet)

                                break

                            if bullet.bounce > 0:
                                bullet.velocityY *= -1
                                bullet.bounce -= 1
                                bullet.angleFromNormal = 2 * math.pi - bullet.angleFromNormal
                            else:
                                bulletD_set.add(bullet)
                # block under
                for block in grid[x][y + 1]:
                    if block.real:
                        if yPot + bullet.length > (block.y) and bullet.velocityY > 0:
                            if bullet.id == 3:
                                if block.x == 0 or block.y == 0 or int(block.y / G_WIDTH) == int(
                                        SCREEN_HEIGHT / G_WIDTH) - 1 or (block.x / G_WIDTH) == int(
                                        SCREEN_WIDTH / G_WIDTH) - 1:
                                    bulletD_set.add(bullet)
                                else:
                                    block.real = False
                                    block.color = WHITE
                                    bulletD_set.add(bullet)

                                break

                            if bullet.bounce > 0:
                                bullet.velocityY *= -1
                                bullet.bounce -= 1
                                bullet.angleFromNormal = 3 * math.pi - bullet.angleFromNormal
                            else:
                                bulletD_set.add(bullet)

            # ---------removing bullets and killing player-------

            for bullet in bullet_set:
                for player in player_list:
                    if ((player.x - bullet.x) ** 2) + ((player.y - bullet.y) ** 2) < PLAYER_RADIUS ** 2:
                        player.isDead()

                        bulletD_set.add(bullet)
            bullet_set = bullet_set - bulletD_set
            powerup_set = powerup_set - powerupD_set
            bulletD_set.clear()

            # --------------------Power Ups----------------------------

            if seconds2 % 5 == 0 and maxPowerUps < MAX_POWERUPS and seconds != seconds2:

                powerup = PowerUp()
                x, y = getSpareSpot()
                x, y = getSpareSpot()
                powerup.x = x
                powerup.y = y
                powerup.width = G_WIDTH
                powerup.type(random.randint(1, 6))
                maxPowerUps += 1
                powerup_set.add(powerup)

            # --update seconds



            # blocking player according to grid filled   (cannot access grid that responds as true.)

            for player in player_list:
                x = int(player.x / G_WIDTH)
                y = int(player.y / G_WIDTH)
                xPot = player.x + (1 / fps) * player.velocityX
                yPot = player.y + (1 / fps) * player.velocityY

                # for block on right (x+1
                for block in grid[x + 1][y]:
                    # if real and crossing(x velocity positive) make velocity x 0 in that direction
                    if block.real:
                        # if the potential location is greater than block.x
                        if (xPot + 2 * PLAYER_RADIUS) > block.x and player.velocityX > 0:
                            player.velocityX = -100
                # block on left
                for block in grid[x - 1][y]:
                    if block.real:
                        if xPot - 2 * PLAYER_RADIUS < (block.x + G_WIDTH) and player.velocityX < 0:
                            player.velocityX = 100

                # for block on top (y-1)
                for block in grid[x][y - 1]:
                    if block.real:
                        if yPot - 2 * PLAYER_RADIUS < (block.y + G_WIDTH) and player.velocityY < 0:
                            player.velocityY = 100
                # block under
                for block in grid[x][y + 1]:
                    if block.real:
                        if yPot + 2 * PLAYER_RADIUS > (block.y) and player.velocityY > 0:
                            player.velocityY = -100

            # updating player and bullet location Location (not logic)
            for player in player_list:
                player.x += (1 / fps) * player.velocityX
                player.y += (1 / fps) * player.velocityY

            for bullet in bullet_set:
                bullet.x += (1 / fps) * bullet.velocityX
                bullet.y += (1 / fps) * bullet.velocityY

            # ------------------END OF GAME LOGIC------------------------------------------

            # ------------------DRAWING------------------------------------------

            # Fill background
            background = pygame.Surface(screen.get_size())
            background = background.convert()
            background.fill((0, 0, 0))
            screen.blit(background, (0, 0))

            # drawing
            screen.fill(BLACK)

            # walls
            for x in range(0, int(SCREEN_WIDTH / G_WIDTH)):
                for y in range(0, int(SCREEN_HEIGHT / G_WIDTH)):
                    for block in grid[x][y]:
                        pygame.draw.rect(screen, block.color, (block.x, block.y, G_WIDTH, G_WIDTH))

            # players

            for player in player_list:
                x = int(player.x / G_WIDTH)
                y = int(player.y / G_WIDTH)

                # shows blocks (collision detection) for player
                #           for block in grid[x + 1][y]:
                #              pygame.draw.rect(screen, (random.randint(0, 255), 100, 100), (block.x, block.y, G_WIDTH, G_WIDTH))
                #         for block in grid[x - 1][y]:
                #            pygame.draw.rect(screen, (random.randint(0, 255), 100, 100), (block.x, block.y, G_WIDTH, G_WIDTH))
                #       for block in grid[x][y + 1]:
                #          pygame.draw.rect(screen, (random.randint(0, 255), 100, 100), (block.x, block.y, G_WIDTH, G_WIDTH))
                #     for block in grid[x][y - 1]:
                #        pygame.draw.rect(screen, (random.randint(0, 255), 100, 100), (block.x, block.y, G_WIDTH, G_WIDTH))

                # ------DRAW---PLAYER
                pygame.draw.line(screen, BLACK, (player.x, player.y), (
                    player.x + player.radius * 2 * math.cos(player.angleFromNormal),
                    player.y + player.radius * 2 * math.sin(player.angleFromNormal)), 2)
                pygame.draw.circle( screen ,player.color, (int(player.x), int(player.y)), int(player.radius))

                # -----------DRAW_POWERUPS
                for powerup in powerup_set:
                    pygame.draw.rect(screen, powerup.color, (powerup.x, powerup.y, G_WIDTH, G_WIDTH))
                # ------DRAW---BULLETS----
                for bullet in bullet_set:
                    x = int(bullet.x / G_WIDTH)
                    y = int(bullet.y / G_WIDTH)
                    pygame.draw.line(screen, BLACK, (bullet.x, bullet.y), (
                        bullet.x + bullet.length * math.cos(bullet.angleFromNormal),
                        bullet.y + bullet.length * math.sin(bullet.angleFromNormal)), 2)

                    # show collision detection:D
            #                for block in grid[x + 1][y]:
            #                    pygame.draw.rect(screen, (random.randint(0, 255), 100, 100), (block.x, block.y, G_WIDTH, G_WIDTH))
            #                for block in grid[x - 1][y]:
            #                    pygame.draw.rect(screen, (random.randint(0, 255), 100, 100), (block.x, block.y, G_WIDTH, G_WIDTH))
            #                for block in grid[x][y + 1]:
            #                    pygame.draw.rect(screen, (random.randint(0, 255), 100, 100), (block.x, block.y, G_WIDTH, G_WIDTH))
            #                for block in grid[x][y - 1]:
            #                    pygame.draw.rect(screen, (random.randint(0, 255), 100, 100), (block.x, block.y, G_WIDTH, G_WIDTH))

            # --- Wrap-up--draw score:

            for player in player_list:
                if player.id==1:
                    scorep2 = player.score
                if player.id==2:
                    scorep1 = player.score
            font = pygame.font.Font(None,50)
            text = font.render("score P red: "+str(scorep1)+"------"+str(seconds)+"------"+"score P blue: "+str(scorep2), 1,(100,0,255))
            textpos = text.get_rect()
            textpos.centerx = SCREEN_WIDTH / 2
            textpos.centery = SCREEN_HEIGHT /15
            screen.blit(text, textpos)

            #update time if needed
            if seconds != seconds2:
                if seconds>(3*60):
                    game=False
                    outro=True
                seconds2 = seconds
            # Limit to 60 frames per second

            clock.tick(60)

            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
    #---------OUTRO--------------
        while outro:
            screen.fill(BLACK)
            # draw intro immage:
            img_beginning = pygame.transform.scale(pygame.image.load("img/intro.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(img_beginning, (0, 0))

            # draw buttons:

            bDM = Button()
            bDM.sizeX = 150
            bDM.sizeY = 70
            bDM.x = 5
            bDM.y = 4
            bDM.color = (255, 255, 255)
            bDM.colorT = (0, 0, 0)
            bDM.text = 'Play Again:'
            bDM.draw(screen)

            bQ = Button()
            bQ.sizeX = 150
            bQ.sizeY = 70
            bQ.x = 1.6
            bQ.y = 4
            bQ.color = (255, 255, 255)
            bQ.colorT = (0, 0, 0)
            bQ.text = 'Quit'
            bQ.draw(screen)
            for player in player_list:
                if player.id==1:
                    scorep2 = player.score
                if player.id==2:
                    scorep1 = player.score
            #score:
            font = pygame.font.Font(None,50)
            text = font.render("score P red: "+str(scorep1)+"------"+str(seconds)+"------"+"score P blue: "+str(scorep2), 1,(100,0,255))
            textpos = text.get_rect()
            textpos.centerx = SCREEN_WIDTH / 2
            textpos.centery = SCREEN_HEIGHT /15
            screen.blit(text, textpos)
            # player win:
            font = pygame.font.Font(None, 50)
            if scorep2>scorep1:
                text = font.render("PLAYER BLUE WELL DONE!",1, (0, 0, 255))
            if scorep1>scorep2:
                text = font.render( "PLAYER RED WELL DONE!",1, (255, 0, 0))
            if scorep1==scorep2:
                text = font.render("IT'S A DRAW HOW SAD", 1, (255, 255, 255))
            textpos = text.get_rect()
            textpos.centerx = SCREEN_WIDTH / 2
            textpos.centery = SCREEN_HEIGHT / 2
            screen.blit(text, textpos)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if click[0] == 1:
                if mouse[0] > bDM.getMinX() and mouse[0] < bDM.getMaxX() and mouse[1] > bDM.getMinY() and mouse[
                    1] < bDM.getMaxY():
                    intro = True
                    outro=False
                if mouse[0] > bQ.getMinX() and mouse[0] < bQ.getMaxX() and mouse[1] > bQ.getMinY() and mouse[
                    1] < bQ.getMaxY():
                    sys.exit()

            clock.tick(15)
            pygame.display.flip()

if __name__ == "__main__":
    main()

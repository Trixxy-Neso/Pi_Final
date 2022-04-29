from smtpd import DebuggingServer
import sys
import random
import math
import os
import getopt
import pygame
from socket import *
from pygame.locals import *



# Health images
health_ani = [pygame.image.load("nohealthc.gif"), pygame.image.load("1healthc.gif"),
              pygame.image.load("2healthc.gif"), pygame.image.load("3healthc.gif"),
              pygame.image.load("4healthc.gif"), pygame.image.load("5healthc.gif")]

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("breadc.gif")
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.speed = 10
        self.state = "still"
        self.reinit()
        self.attacking = ""
        self.attack_frame = 0
        self.health = 5
        self.cooldown = False
        self.d_cooldown = False
        self.dashAbility = True
        

    def reinit(self):
        self.state = "still"
        self.movepos = [0,0]
        
        self.rect.midleft = self.area.midleft

    def update(self):
        newpos = self.rect.move(self.movepos)
        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()

    def moveup(self):
        self.movepos[1] += -5
        self.state = "moveup"

    def movedown(self):
        self.movepos[1] += 5
        self.state = "movedown"

    def moveright(self):
        self.movepos[0] += 5
        self.state = "moveright"

    def moveleft(self):
        self.movepos[0] += -5
        self.state = "moveleft"

    def stopmoveup(self):
        self.movepos[1] += 5
        self.state = "still"

    def stopmovedown(self):
        self.movepos[1] += -5
        self.state = "still"

    def stopmoveleft(self):
        self.movepos[0] += 5
        self.state = "still"

    def stopmoveright(self):
        self.movepos[0] += -5
        self.state = "still"

    def attack(self, direction):
        #print(self.attack_frame)

        # Check direction
        if direction == "RIGHT":
            self.image = pygame.image.load("attack_R.gif")
            #print("set sword")
        
        
        
        # if attack frame had reached the end, return
        if self.attack_frame > 10:
            self.attack_frame = 0
            self.image = pygame.image.load("breadc.gif")
            self.attacking = ""
            #print("stopping attack")

        
            

        self.attack_frame += 1

    def player_hit(self):
        if self.cooldown == False:      
            self.cooldown = True # Enable the cooldown
            pygame.time.set_timer(hit_cooldown, 1000) # Resets cooldown in 1 second
 
            self.health = self.health - 1
            health.image = health_ani[self.health]
             
            if self.health <= 0:
                self.kill()
                health.dead()
                pygame.display.update()

    def dash(self, direction):
        print("start dash")
        if self.d_cooldown == False:
            self.d_cooldown = True
            pygame.time.set_timer(dash_cooldown, 5000)

            if direction == "LEFT":
                newpos = self.rect.move(-70,0)
                if self.area.contains(newpos):
                    self.rect = newpos
                pygame.event.pump()
                self.image = pygame.image.load("dashLc.gif")

            if direction == "RIGHT":
                newpos = self.rect.move(70,0)
                if self.area.contains(newpos):
                    self.rect = newpos
                pygame.event.pump()

            if direction == "UP":
                newpos = self.rect.move(0,-70)
                if self.area.contains(newpos):
                    self.rect = newpos
                pygame.event.pump()

            if direction == "DOWN":
                newpos = self.rect.move(0,70)
                if self.area.contains(newpos):
                    self.rect = newpos
                pygame.event.pump()

            if direction == "LEFT_UP":
                newpos = self.rect.move(-50,-50)
                if self.area.contains(newpos):
                    self.rect = newpos
                pygame.event.pump()

            if direction == "RIGHT_UP":
                newpos = self.rect.move(50,-50)
                if self.area.contains(newpos):
                    self.rect = newpos
                pygame.event.pump()

            if direction == "LEFT_DOWN":
                newpos = self.rect.move(-50,50)
                if self.area.contains(newpos):
                    self.rect = newpos
                pygame.event.pump()

            if direction == "RIGHT_DOWN":
                newpos = self.rect.move(50,50)
                if self.area.contains(newpos):
                    self.rect = newpos
                pygame.event.pump()


    
class Sword(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sword.gif")
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.timer = 10

    
class HealthBar(pygame.sprite.Sprite):
      def __init__(self):
            super().__init__()
            self.image = pygame.image.load("5healthc.gif")
            self.rect = self.image.get_rect()
 
      # Game over is handeled in the health sprite because its easier
      def dead(self):
          self.image = pygame.image.load("gameoverc.gif")
          self.rect =  (200,200)   # self.image.get_rect()



def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('EEE')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 128, 0))

    # Initialise players
    global player1
    global health
    player1 = Player()
    health = HealthBar()

    # Initialise ball
   

    # Initialise sprites
    playersprites = pygame.sprite.RenderPlain((player1))
    healthsprites = pygame.sprite.RenderPlain((health))
    

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Initialise clock
    clock = pygame.time.Clock()

    # Others 
    global hit_cooldown
    hit_cooldown = pygame.USEREVENT + 1
    global dash_cooldown
    dash_cooldown = pygame.USEREVENT + 2
    global testing
    testing = True

    # Event loop
    while 1:
        # Make sure game doesn't run at more than 60 frames per second
        clock.tick(60)

        if player1.attacking == "RIGHT":
            player1.attack("RIGHT")

        # Setup key positions 
        moveUp = False
        moveDown = False
        moveRight = False
        moveLeft = False
        dashKey = False

        for event in pygame.event.get():
            if event.type == hit_cooldown:
                player1.cooldown = False
            if event.type == dash_cooldown:
                player1.d_cooldown = False
            if event.type == QUIT:
                return

            # Get key positions to be used later
            elif event.type == KEYDOWN:
                # Base Movement keys
                if event.key == K_w:
                    #player1.moveup()
                    moveUp = True
                if event.key == K_s:
                    #player1.movedown()
                    moveDown = True
                if event.key == K_a:
                    #player1.moveleft()
                    moveLeft = True
                if event.key == K_d:
                    #player1.moveright()
                    moveRight = True
                if event.key == K_RIGHT:
                    print('attack right keydown')
                    if player1.attacking == "":
                        print('triggering attack func')
                        player1.attack("RIGHT")
                        player1.attacking = "RIGHT"

                # Abilities
                if event.key == K_SPACE:
                    dashKey = True
                    print("Dash Key")
                
                # Testing
                if event.key == K_k and testing:
                    player1.player_hit()

                
            elif event.type == KEYUP:
                #if event.key == K_a or event.key == K_w or event.key == K_s or event.key == K_d:
                #    player1.movepos = [0,0]
                #    player1.state = "still"

                if event.key == K_a: 
                    player1.stopmoveleft()
                if event.key == K_d:
                    player1.stopmoveright()

                if event.key == K_w: 
                    player1.stopmoveup()
                if event.key == K_s:
                    player1.stopmovedown()

        ## Act on keypositions retrieved ##

        # Dash
        if dashKey:
            if player1.movepos[0] > 0 and player1.movepos[1] < 0:
                player1.dash("RIGHT_UP")
            if player1.movepos[0] < 0 and player1.movepos[1] < 0:
                player1.dash("LEFT_UP")
            if player1.movepos[0] > 0 and player1.movepos[1] > 0:
                player1.dash("RIGHT_DOWN")
            if player1.movepos[0] < 0 and player1.movepos[1] > 0:
                player1.dash("LEFT_DOWN")
            if player1.movepos[0] > 0:
                player1.dash("RIGHT")
            if player1.movepos[0] < 0:
                player1.dash("LEFT")
            if player1.movepos[1] > 0:
                player1.dash("DOWN")
            if player1.movepos[1] < 0:
                player1.dash("UP")

        if moveUp:
            player1.moveup()
        if moveDown:
            player1.movedown()
        if moveRight:
            player1.moveright()
        if moveLeft:
            player1.moveleft()


        
        screen.blit(background, player1.rect)
        screen.blit(background, health.rect)
        
        
        playersprites.update()
        playersprites.draw(screen)
        healthsprites.update()
        healthsprites.draw(screen)
        pygame.display.flip()


if __name__ == '__main__': main()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    #screen.fill(black)
    #screen.blit(ball, ballrect)

    pygame.display.flip()
from bdb import effective
from random import randint
import math
from tkinter import Frame
from wsgiref.handlers import format_date_time
import pygame
from socket import *
from pygame.locals import *



# Health images
health_ani = [pygame.image.load("nohealth.png"), pygame.image.load("1health.png"),
              pygame.image.load("2health.png"), pygame.image.load("3health.png"),
              pygame.image.load("4health.png"), pygame.image.load("5health.png")]

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("ffront.png")
        self.rect = self.image.get_rect()
        self.rect.update(self.rect.x, self.rect.y + 10, self.rect.width, self.rect.height - 10)
        self.rect.x = 300
        self.rect.y = 220
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
        self.invuln_cooldown = False
        self.dashAbility = True
        self.frame_switch = 1
        print("creating player")

    def reinit(self):
        self.state = "stopdown"
        self.movepos = [0,0]
        
        #self.rect.midleft = self.area.midleft

    def reset(self):
        self.rect.x = 300
        self.rect.y = 220
        self.state = "still"
        self.attack_frame = 0
        self.health = 5
        self.cooldown = False
        self.d_cooldown = False
        self.invuln_cooldown = False
        self.dashAbility = True
        self.frame_switch = 1
        print("reseting player")
        self.image = pygame.image.load("ffront.png")

    def update(self):
        newpos = self.rect.move(self.movepos)
        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()

        hit_player = pygame.sprite.spritecollide(self, Enemygroup, False)
        if hit_player:
            self.player_hit()

        if self.movepos[0] == 0 and self.movepos[1] == 0:
            
            if self.state == "stopup":
                self.image = pygame.image.load("fback.png")

            elif self.state == "stopdown":
                self.image = pygame.image.load("ffront.png")

            elif self.state == "stopright":
                self.image = pygame.image.load("fright.png")

            elif self.state == "stopleft":
                self.image = pygame.image.load("fleft.png")

        elif self.movepos[1] < 0:
            if self.frame_switch == 1:
                self.image = pygame.image.load("up1.png")
            else:
                self.image = pygame.image.load("up2.png")

        elif self.movepos[1] > 0:
            if self.frame_switch == 1:
                self.image = pygame.image.load("down1.png")
            else:
                self.image = pygame.image.load("down2.png")

        elif self.movepos[0] > 0:
            if self.frame_switch == 1:
                self.image = pygame.image.load("right1.png")
            else:
                self.image = pygame.image.load("right2.png")

        elif self.movepos[0] < 0:
            if self.frame_switch == 1:
                self.image = pygame.image.load("left1.png")
            else:
                self.image = pygame.image.load("left2.png")

        if self.cooldown == True:
            self.image.fill((190, 0, 0, 100), special_flags=pygame.BLEND_ADD)

        if self.invuln_cooldown == True:
            self.image.fill((60, 0, 0, 100), special_flags=pygame.BLEND_SUB)
        
        
    def frameUpdate(self):
        if self.frame_switch == 1:
            self.frame_switch = 2
        else:
            self.frame_switch = 1
        pygame.time.set_timer(frame_cooldown, 100)

            

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
        self.state = "stopup"

    def stopmovedown(self):
        self.movepos[1] += -5
        self.state = "stopdown"

    def stopmoveleft(self):
        self.movepos[0] += 5
        self.state = "stopleft"

    def stopmoveright(self):
        self.movepos[0] += -5
        self.state = "stopright"


    def player_hit(self):
        if self.cooldown == False and self.invuln_cooldown == False:      
            self.cooldown = True # Enable the cooldown
            pygame.time.set_timer(hit_cooldown, 1000) # Resets cooldown in 1 second
            self.image.fill((190, 0, 0, 100), special_flags=pygame.BLEND_ADD) # Red tint

            self.health = self.health - 1
            health.image = health_ani[self.health]
             
            if self.health <= 0:
                health.image = pygame.image.load("nohealth.png")
                #self.kill()
                self.rect.x = -100
                self.rect.y = -300
                health.dead()
                effect.player_death()
                global game_over 
                game_over = True
                pygame.display.update()
                

    def dash(self, direction):
        print("start dash")
        if self.d_cooldown == False:
            self.d_cooldown = True
            pygame.time.set_timer(dash_cooldown, 5000)

            self.invuln_cooldown = True # Hit cooldown
            pygame.time.set_timer(invuln_cooldown, 1000) 
            
            self.image.fill((60, 0, 0, 100), special_flags=pygame.BLEND_SUB)

            if direction == "LEFT":
                newpos = self.rect.move(-70,0)
                if self.area.contains(newpos):
                    self.rect = newpos
                pygame.event.pump()
                

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
        self.image = pygame.image.load("swordL.png")
        self.rect = self.image.get_rect()
        self.rect.x = -100
        self.rect.y = -100
        self.cooldown = False
        self.point = ""

    def attack(self, direction):
        if self.cooldown == False:
            self.cooldown = True
            pygame.time.set_timer(attack_cooldown, 200)
            self.point = direction 

    def neutral(self):
        self.point = ""
        self.cooldown = False



    def update(self, player): # has the enemy move with/to player

        if self.point != "":
            pcx = player.rect.x + (player.rect.width / 2)
            pcy = player.rect.y + (player.rect.height / 2)
            
            if self.point == "RIGHT":
                self.image = pygame.image.load("swordR.png")
                self.rect = self.image.get_rect()
                self.rect.x = pcx + 20
                self.rect.y = pcy - 10

            if self.point == "LEFT":
                self.image = pygame.image.load("swordL.png")
                self.rect = self.image.get_rect()
                self.rect.x = pcx - 80
                self.rect.y = pcy - 10

            if self.point == "UP":
                self.image = pygame.image.load("swordU.png")
                self.rect = self.image.get_rect()
                self.rect.x = pcx - 15
                self.rect.y = pcy - 80

            if self.point == "DOWN":
                self.image = pygame.image.load("swordD.png")
                self.rect = self.image.get_rect()
                self.rect.x = pcx - 15
                self.rect.y = pcy + 20

        else:
            self.image = pygame.image.load("swordL.png")
            self.rect = self.image.get_rect()
            self.rect.x = -100
            self.rect.y = -100

    

class Effect(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("shadow.png")
        self.rect = self.image.get_rect()

    def neutral(self):
        self.image = pygame.image.load("shadow.png")

    def dash(self):
        self.image = pygame.image.load("dash.png")

    def player_death(self):
        self.kill()
        
    def update(self, player): # has the enemy move with/to player
        pcx = player.rect.x #- (player.rect.width / 2)
        pcy = player.rect.y #- (player.rect.height / 2)

        self.rect.x = pcx - 13
        self.rect.y = pcy - 5



class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("breadc.png")
        self.rect = self.image.get_rect()
        self.rect.update(self.rect.x, self.rect.y + 10, self.rect.width, self.rect.height - 10)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

        #random spawn locations
        tryspawn = True
        while tryspawn:
            self.rect.x = randint(10, 750)
            self.rect.y = randint(10, 450)
            dx = (player1.rect.x + (player1.rect.width/2) ) - (self.rect.x + (self.rect.width/2))
            dy = (player1.rect.y + (player1.rect.height/2)) - (self.rect.y + (self.rect.height/2))
            dist = math.hypot(dx, dy)
            if dist < 200:
                tryspawn = True
            else: 
                tryspawn = False
        self.speed = 2
        
    def update(self, player): # has the enemy move with/to player
        dx = (player.rect.x + (player.rect.width/2) ) - (self.rect.x + (self.rect.width/2))
        dy = (player.rect.y + (player.rect.height/2)) - (self.rect.y + (self.rect.height/2))
        dist = math.hypot(dx, dy)
        if dist > 40:
            dx, dy = dx / dist, dy / dist
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

        # this handeles sword colision dectection, player colision is handeled in the player class
        hit_sword = pygame.sprite.spritecollide(self, Swordgroup, False)
        if hit_sword:
            self.kill()
            print("OH GOD IM DEAD")



    
class HealthBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("5health.png")
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

    # Game over is handeled in the health sprite because its easier, turns the health bar into the game over because the health bar is gone wanyway
    def dead(self):
        self.image = pygame.image.load("gameover.png")
        self.rect.center = self.area.center

    def reset(self):
        self.image = pygame.image.load("5health.png")
        self.rect = self.image.get_rect()




class NoticeBoard(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #self.image = pygame.image.load("nextwave.png")
        self.font = pygame.font.Font("font.ttf", 25)
        self.image = self.font.render("PRESS 'ENTER' TO START THE NEXT WAVE", True, (0,0,0))
        self.rect = self.image.get_rect()
        self.hide()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

    def nextWave(self):
        self.font = pygame.font.Font("font.ttf", 25)
        self.image = self.font.render("PRESS 'ENTER' TO START THE NEXT WAVE", True, (0,0,0))
        self.rect = self.image.get_rect()
        #print("set to next wave")
        self.rect.center = self.area.center #- (self.rect.width/2)
        self.rect.y = 80

    def restart(self):
        self.font = pygame.font.Font("font.ttf", 25)
        self.image = self.font.render("PRESS 'ENTER' TO RESTART", True, (0,0,0))
        self.rect = self.image.get_rect()
        #print("set to restart")
        self.rect.center = self.area.center #- (self.rect.width/2)
        self.rect.y = 80

    def show(self):
        self.rect.center = self.area.center #- (self.rect.width/2)
        self.rect.y = 80

    def hide(self):
        self.rect.x = -100
        self.rect.y = -300



class Backdrop(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("background.png")
        self.rect = self.image.get_rect()



class WaveCounter(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font("font.ttf", 20)
        self.image = self.font.render('YOU ARE ON WAVE 0', True, (0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 30

    def tick(self, wave_num):
        self.image = self.font.render(f'YOU ARE ON WAVE {wave_num}', True, (0,0,0))



def main():
    # Initialise screen
    pygame.init()
    
    screen = pygame.display.set_mode((750, 450))
    pygame.display.set_caption('Dough Gone Sour')


    # Fill background
    background = pygame.Surface(screen.get_size())
    #background = pygame.image.load("background.png")
    background = background.convert()
    background.fill((0, 128, 0))


    # Initialise players
    global effect
    effect = Effect()

    global player1
    player1 = Player()

    global sword
    sword = Sword()

    global Swordgroup
    Swordgroup = pygame.sprite.Group()
    Swordgroup.add(sword)

    global Playergroup
    Playergroup = pygame.sprite.Group()
    Playergroup.add(player1)


    # Initialise backgrounds
    global health
    health = HealthBar()

    global notice
    notice = NoticeBoard()

    global bgimage
    bgimage = Backdrop()

    global wave_counter
    wave_counter = WaveCounter()


    # Initialize enemies
    global Enemygroup
    Enemygroup = pygame.sprite.Group()
    def addEnemies(stage):
        thic_num = int(stage / 2)
        for i in range(0, stage):
            i = Enemy()
            Enemygroup.add(i)           
            enemysprites.add(i)
        
    

    # Initialise sprites
    playersprites = pygame.sprite.RenderPlain((player1))
    playereffectsprites = pygame.sprite.RenderPlain((effect))
    enemysprites = pygame.sprite.RenderPlain()   
    backgroundsprites = pygame.sprite.RenderPlain((health, notice, wave_counter))
    swordsprites = pygame.sprite.RenderPlain((sword))
    theverybackgroundsprites = pygame.sprite.RenderPlain((bgimage))

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
    global attack_cooldown
    attack_cooldown = pygame.USEREVENT + 3
    global invuln_cooldown
    invuln_cooldown = pygame.USEREVENT + 4
    global frame_cooldown 
    frame_cooldown = pygame.USEREVENT + 5
    global game_over
    game_over = False
    global testing
    testing = True
    wave_fin = True
    global wave_num
    wave_num = 1
    show_notice = False
    player1.frameUpdate()

    def restart():
        print("got here")
        global wave_fin
        wave_fin = True
        global wave_num
        wave_num = 1
        wave_counter.tick(wave_num)
        global show_notice
        show_notice = False
        global game_over
        game_over = False
        global notice
        notice.restart()
        player1.reset()
        health.reset()
        for enemy in Enemygroup:
            enemy.kill()


    # Event loop
    while 1:
        # Make sure game doesn't run at more than 60 frames per second
        clock.tick(60)
        
        if wave_fin == True and show_notice == False:
            notice.show()
            show_notice = True

        if len(enemysprites) == 0:
            wave_fin = True
            notice.nextWave()
            #notice.hide()

        # Setup key positions 
        moveUp = False
        moveDown = False
        moveRight = False
        moveLeft = False
        dashKey = False
        
        if game_over:
            notice.restart()
        

        for event in pygame.event.get():
            if event.type == hit_cooldown:
                player1.cooldown = False
                player1.image = pygame.image.load("ffront.png") # reset red tint
            if event.type == dash_cooldown:
                player1.d_cooldown = False
                effect.neutral()
            if event.type == attack_cooldown:
                sword.neutral()
            if event.type == invuln_cooldown:
                player1.invuln_cooldown = False
            if event.type == frame_cooldown:
                player1.frameUpdate()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            if event.type == QUIT:
                return
            if event.type == KEYDOWN and game_over == True:
                if event.key == K_RETURN:
                    restart()
                    print("restarting")

            # Get key positions to be used later
            elif event.type == KEYDOWN and game_over == False:
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
                    #print('attack RIGHT keydown')
                    sword.attack("RIGHT")
                if event.key == K_LEFT:
                    #print('attack LEFT keydown')
                    sword.attack("LEFT")
                if event.key == K_UP:
                    #print('attack UP keydown')
                    sword.attack("UP")
                if event.key == K_DOWN:
                    #print('attack DOWN keydown')
                    sword.attack("DOWN") 

                # Abilities
                if event.key == K_SPACE:
                    dashKey = True
                    print("Dash Key")
                
                # Testing
                if event.key == K_k and testing:
                    player1.player_hit()
                if event.key == K_l and testing:
                    player1.health = 1
                    player1.player_hit()

                # Waves
                if event.key == K_RETURN and wave_fin:
                    show_notice = False
                    wave_fin = False
                    addEnemies(wave_num)
                    wave_counter.tick(wave_num)
                    wave_num += 1
                    notice.hide()
                    print("starting next wave")

            

            elif event.type == KEYUP and game_over == False:
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
                effect.dash()
            if player1.movepos[0] < 0 and player1.movepos[1] < 0:
                player1.dash("LEFT_UP")
                effect.dash()
            if player1.movepos[0] > 0 and player1.movepos[1] > 0:
                player1.dash("RIGHT_DOWN")
                effect.dash()
            if player1.movepos[0] < 0 and player1.movepos[1] > 0:
                player1.dash("LEFT_DOWN")
                effect.dash()
            if player1.movepos[0] > 0:
                player1.dash("RIGHT")
                effect.dash()
            if player1.movepos[0] < 0:
                player1.dash("LEFT")
                effect.dash()
            if player1.movepos[1] > 0:
                player1.dash("DOWN")
                effect.dash()
            if player1.movepos[1] < 0:
                player1.dash("UP")
                effect.dash()

        if moveUp:
            player1.moveup()
        if moveDown:
            player1.movedown()
        if moveRight:
            player1.moveright()
        if moveLeft:
            player1.moveleft()


        # Update stuffs
        theverybackgroundsprites.update()
        if game_over == False:
            enemysprites.update(player1)
        playereffectsprites.update(player1)
        playersprites.update()
        backgroundsprites.update()
        backgroundsprites.update()
        swordsprites.update(player1)


        # Render Stuffs 

        for enemy in enemysprites:
            screen.blit(background, enemy.rect)
            
        screen.blit(background, player1.rect)
        screen.blit(background, health.rect)
        screen.blit(background, sword.rect)
        screen.blit(background, bgimage.rect)
        
        theverybackgroundsprites.draw(screen)
       
        #enemysprites.draw(screen)
     
        playereffectsprites.draw(screen)

        playersprites.draw(screen)

        backgroundsprites.draw(screen)
   
        swordsprites.draw(screen)
        
        pygame.display.flip()


if __name__ == '__main__': main()



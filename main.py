from random import randint
import math
from turtle import Screen, back
from wsgiref.handlers import format_date_time
import pygame
from socket import *
from pygame.locals import *

# Health images
health_ani = [pygame.image.load("nohealth.png"), pygame.image.load("1health.png"),
              pygame.image.load("2health.png"), pygame.image.load("3health.png"),
              pygame.image.load("4health.png"), pygame.image.load("5health.png")]

##### PLAYER CLASS #####

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("ffront.png")
        self.rect = self.image.get_rect()
        self.rect.update(self.rect.x, self.rect.y + 10, self.rect.width, self.rect.height - 10)
        self.rect.x = 280
        self.rect.y = 130
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
        self.wakeup_status = False
        self.return_start = False

    def reinit(self):
        self.state = "stopdown"
        self.movepos = [0,0]
        
        #self.rect.midleft = self.area.midleft

    def reset(self):
        #self.rect.x = 280
        #self.rect.y = 130
        self.state = "still"
        self.attack_frame = 0
        self.health = 5
        self.cooldown = False
        self.d_cooldown = False
        self.invuln_cooldown = False
        self.dashAbility = True
        self.frame_switch = 1
        self.reinit()
        #self.image = pygame.image.load("ffront.png")   

    def update(self):
        newpos = self.rect.move(self.movepos)
        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()

        hit_player = pygame.sprite.spritecollide(self, EnemyUppergroup, False)
        if hit_player:
            self.player_hit()

        if self.movepos[0] == 0 and self.movepos[1] == 0 and self.health > 0:
            
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

        if self.wakeup_status == True:
            if self.frame_switch == 1:
                self.image = pygame.image.load("ffront.png")
            else:
                self.image = pygame.image.load("dead.png")
        
        if self.cooldown == True:
            self.image.fill((190, 0, 0, 100), special_flags=pygame.BLEND_ADD)

        if self.invuln_cooldown == True:
            self.image.fill((60, 0, 0, 100), special_flags=pygame.BLEND_SUB)
            
        if self.return_start == True and game_over == True and self.wakeup_status == False:    
            dx = (300) - (self.rect.x + (self.rect.width/2))
            dy = (170) - (self.rect.y + (self.rect.height/2))
            dist = math.hypot(dx, dy)
            #print(f"Dist is :{dist}")
            #print(f"dy is :{dy}")
            if dx > 6 or dx < -6:
                #dx = dx / dist
                if dx > 0:
                    self.movepos[0] = 2
                if dx < 0:
                    self.movepos[0] = -2   
            else:
                self.movepos[0] = 0
                    
            if dy > 6 or dy < -6:
                #dy = dy / dist
                if dy > 0:
                    self.movepos[1] = 2
                if dy < 0:
                    self.movepos[1] = -2
            else:
                self.movepos[1] = 0
                    
            if dist < 10:
                self.return_start = False
                self.movepos[0] = 0
                self.movepos[1] = 0
                
    def frameUpdate(self):
        if self.frame_switch == 1:
            self.frame_switch = 2
        else:
            self.frame_switch = 1
        pygame.time.set_timer(frame_cooldown, 100)
        
    def wakeup(self, status):
        if status == "start":
            self.wakeup_status = True
            pygame.time.set_timer(wakeup_blink, 1000)
        else:
            self.wakeup_status = False       

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
                self.image = pygame.image.load("dead.png")
                self.image.fill((190, 0, 0, 100), special_flags=pygame.BLEND_ADD) # Red tint
                self.movepos[0] = 0
                self.movepos[1] = 0
                health.dead()
                for _ in range(0,purse_image.coins):
                    self.addCoin()
                #effect.player_death()
                global game_over 
                game_over = True
                pygame.display.update()
                
    def addCoin(self):
        print("Death Coins")
        i = Coin(self.rect.x, self.rect.y)
        #global coinsprites
        coinsprites.add(i)
            
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

##### SWORD CLASS #####
    
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

##### EFFECT CLASS #####

class Effect(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("shadow.png")
        self.rect = self.image.get_rect()

    def neutral(self):
        self.image = pygame.image.load("shadow.png")

    def dash(self):
        self.image = pygame.image.load("dash.png")

    #def player_death(self):
    #   self.kill()
        
    def update(self, player): # has the enemy move with/to player
        pcx = player.rect.x #- (player.rect.width / 2)
        pcy = player.rect.y #- (player.rect.height / 2)

        self.rect.x = pcx - 13
        self.rect.y = pcy - 10


##### ENEMY CLASS #####
##### IMPORTANT #####
# This is the only way to get the enemy/palyer behind-infront illusion to work as you can't render entities in the same group at diffrent layers.
# There are 2 classes of enemy so that enemies in the back render as behind and vise versa.
# There are 2 render groups, one where sprites are only visible above the player and one where sprites are only visible below.
# The 2 sprites are spawned on top of eachother and vanish/reappear in sync with eachother so it appears as one.
# The movement code is the same for both so they *should* stay in sync with eachother.
# This is a terrible and inneficient way of doing it but I think its the only way.

class UpperEnemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("breadc.png")
        #self.image.fill((190, 0, 0, 100), special_flags=pygame.BLEND_ADD)
        self.rect = self.image.get_rect()
        self.rect.update(self.rect.x, self.rect.y + 10, self.rect.width, self.rect.height - 10)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        global coinsprites
        
    def addCoin(self):
        chance = randint(0,5)
        if chance == 1:
            i = Coin(self.rect.x, self.rect.y)
            #global coinsprites
            coinsprites.add(i)
        if chance == 0:
            i = Coin(self.rect.x, self.rect.y)
            j = Coin(self.rect.x, self.rect.y)
            #global coinsprites
            coinsprites.add(i,j)
        
    def update(self, player): # has the enemy move with/to player
        dx = (player.rect.x + (player.rect.width/2) ) - (self.rect.x + (self.rect.width/2))
        dy = (player.rect.y + (player.rect.height/2)) - (self.rect.y + (self.rect.height/2))
        dist = math.hypot(dx, dy)
        if dist > 40:
            dx, dy = dx / dist, dy / dist
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

        # Change visibility to render behind or infront
        if self.rect.y <= player.rect.y:
            self.image.set_alpha(255)
        else:
            self.image.set_alpha(0)

        # this handeles sword colision dectection, player colision is handeled in the player class
        hit_sword = pygame.sprite.spritecollide(self, Swordgroup, False)
        if hit_sword:
            self.kill()
            #print("OH GOD IM DEAD")
            self.addCoin()
                     

class LowerEnemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("breadc.png")
        #self.image.fill((0, 0, 190, 100), special_flags=pygame.BLEND_ADD)
        self.rect = self.image.get_rect()
        self.rect.update(self.rect.x, self.rect.y + 10, self.rect.width, self.rect.height - 10)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.speed = 2
        
    def update(self, player): # has the enemy move with/to player
        dx = (player.rect.x + (player.rect.width/2) ) - (self.rect.x + (self.rect.width/2))
        dy = (player.rect.y + (player.rect.height/2)) - (self.rect.y + (self.rect.height/2))
        dist = math.hypot(dx, dy)
        if dist > 40:
            dx, dy = dx / dist, dy / dist
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed
        
        # Change visibility to render behind or infront
        if self.rect.y >= player.rect.y:
            self.image.set_alpha(255)
        else:
            self.image.set_alpha(0)

        # this handeles sword colision dectection, player colision is handeled in the player class
        hit_sword = pygame.sprite.spritecollide(self, Swordgroup, False)
        if hit_sword:
            self.kill()
            #print("OH GOD IM DEAD")

##### HEALTH CLASS #####
    
class HealthBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("5health.png")
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.hide()

    # Game over is handeled in the health sprite because its easier, turns the health bar into the game over because the health bar is gone wanyway
    def dead(self):
        self.image = pygame.image.load("gameover.png")
        self.rect.center = self.area.center

    def reset(self):
        self.image = pygame.image.load("5health.png")
        self.rect = self.image.get_rect()
        if veil_layer.location == "Title":
            self.hide()
        
    def show(self):
        self.rect = self.image.get_rect()

    def hide(self):
        self.rect.x = -100
        self.rect.y = -300

##### NOTICE CLASS #####

class NoticeBoard(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #self.image = pygame.image.load("nextwave.png")
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.font = pygame.font.Font("font.ttf", 25)
        self.image = self.font.render("PRESS 'ENTER' TO BEGIN", True, (0,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = self.area.center
        self.rect.y = 370
        #self.hide()
        
    def title(self):
        self.image = self.font.render("PRESS 'ENTER' TO BEGIN", True, (0,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = self.area.center
        self.rect.y = 370

    def nextWave(self):
        self.font = pygame.font.Font("font.ttf", 25)
        self.image = self.font.render("PRESS 'ENTER' TO START THE NEXT WAVE", True, (0,0,0))
        self.rect = self.image.get_rect()
        self.hide()
        #print("set to next wave")
        self.rect.center = self.area.center #- (self.rect.width/2)
        self.rect.y = 80

    def restart(self):
        self.font = pygame.font.Font("font.ttf", 25)
        self.image = self.font.render("PRESS 'ENTER' TO RESTART OR 'BACKSPACE' TO QUIT", True, (0,0,0))
        self.rect = self.image.get_rect()
        #print("set to restart")
        self.rect.center = self.area.center #- (self.rect.width/2)
        self.rect.y = 80

    def show(self):
        if veil_layer.location != "Title" and veil_layer.fading == None:
            self.rect.center = self.area.center #- (self.rect.width/2)
            self.rect.y = 80


    def hide(self):
        self.rect.x = -100
        self.rect.y = -300

##### BACKDROP CLASS #####

class Backdrop(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("title.png")
        self.rect = self.image.get_rect()
        self.rect.x += -8
        self.rect.y += -3
        self.fading = None
        
##### VEIL CLASS #####
        
class Veil(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((750,450))
        self.image = self.image.convert()
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.fading = None
        self.alpha = 0
        self.image.set_alpha(50)
        self.location = "Title"
        self.destination = None
        
    def next(self, location):
        if not self.fading:
            self.fading = 'IN'
            self.alpha = 50
            self.destination = location    
            print(f"sending to {location}")
        
    def update(self):
        self.image.set_alpha(self.alpha)
            
        if self.fading == 'IN':
            self.alpha += 4
            if self.alpha >= 255:
                self.location = self.destination
                self.fading = 'OUT'
                if self.destination == "Title":
                    bgimage.image = pygame.image.load("title.png")
                    bgimage.rect.x = -8
                    bgimage.rect.y = -3
                    health.hide()
                    wave_counter.hide()
                    purse_image.hide()
                    notice.title()
                    global game_over
                    game_over = True
                    clearScreen()
                elif self.destination == "Feild":
                    bgimage.image = pygame.image.load("background.png")
                    bgimage.rect.x = 0
                    bgimage.rect.y = 0
                    takedownShop()
                elif self.destination == "Store":
                    bgimage.image = pygame.image.load("store.png")
                    bgimage.rect.x = 0
                    bgimage.rect.y = 0
                    notice.hide()
                    setupShop()
                    
                if self.destination != "Title":
                    health.show()
                    wave_counter.show()
                    purse_image.show()
                global intro
                intro = False
        elif self.fading == 'OUT':
            self.alpha -= 4
            if self.alpha <= 0:
                self.fading = None 
                

##### COUNTER CLASS #####

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
        
    def show(self):
        self.rect.x = 500
        self.rect.y = 30

    def hide(self):
        self.rect.x = -100
        self.rect.y = -300

##### LEAF CLASS #####

class Leaf(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        type = randint(0,1)
        if type == 1:
            self.image = pygame.image.load("leaf.png")
            flipped = randint(0,1)
            if flipped == 1:
                self.image = pygame.transform.flip(self.image, True, True)
            else:
                self.image = pygame.transform.flip(self.image, False, True)
        else:
            self.image = pygame.image.load("leaf2.png")
        self.rect = self.image.get_rect()
        self.rect.x = randint(5,900)
        self.rect.y = -10
        self.scaleRandomness = randint(-5,5)
        self.image = pygame.transform.scale(self.image, (25 + self.scaleRandomness, 25 + self.scaleRandomness))
        self.moveSpeedX = 0
        self.moveSpeedY = 1

    def update(self):
        x = randint(-1,0)
        y = randint(0,1)
        self.rect.x += self.moveSpeedX + x
        self.rect.y += self.moveSpeedY + y

##### FIRE CLASS #####

class Fire(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        type = randint(0,1)
        self.image = pygame.image.load("fire.png")
        self.rect = self.image.get_rect()
        self.rect.x = randint(355,375)
        self.rect.y = randint(210,220)
        self.scaleRandomness = randint(-3,3)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() + self.scaleRandomness, self.image.get_height() + self.scaleRandomness))
        self.moveSpeedX = 0
        self.moveSpeedY = -1

    def update(self):
        x = randint(-2,0)/2
        y = randint(-2,0)
        self.rect.x += self.moveSpeedX + x
        self.rect.y += self.moveSpeedY + y
   
##### COIN CLASS #####
        
class Coin(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load("coin.png")
        self.rect = self.image.get_rect()
        # Hold coin pos as floats with decimal precision so it looks more natural
        self.rect.x = x + 30
        self.rect.y = y + 60
        self.floatPosX = float(self.rect.x)
        self.floatPosY = float(self.rect.y)
        self.startingy = self.rect.y
        self.xVelocity = float(randint(-30,30)/10)
        self.yVelocity = float(randint(100,150)/10)
        self.moveSpeedX = 0
        self.moveSpeedY = 1
        self.frame_switch = 0
        self.flying = False
        pygame.time.set_timer(coin_flip, 50)
        
    def frameUpdate(self):
        if self.flying:        
            if self.frame_switch == 1:
                self.frame_switch = 2
                self.image = pygame.image.load("coin.png")
                pygame.time.set_timer(coin_flip, 50)
            else:
                self.frame_switch = 1
                self.image = pygame.image.load("coin2.png")
                pygame.time.set_timer(coin_flip, 50)
        else:
            self.image = pygame.image.load("coin.png")

    def update(self):
        currenty = self.rect.y
        #yDist = self.startingy - currenty
        if currenty <= self.startingy:
            self.floatPosY -= self.yVelocity
            self.floatPosX += self.xVelocity
            # Turn float pos into actual pos without disturbing float pos, keeping decimal precision
            self.rect.y = int(self.floatPosY)
            self.rect.x = int(self.floatPosX)
            self.yVelocity -= 1
            self.flying = True
        else:
            self. flying = False
            
        if pygame.sprite.spritecollide(self, Playergroup, False) and player1.health >= 1:
            purse_image.tick()
            self.kill()
            
            
##### PURSE CLASS #####
            
class Purse(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font("font.ttf", 23)
        self.image = self.font.render('$0', True, (0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = 22
        self.rect.y = 55
        self.coins = 0

    def tick(self):
        self.coins += 1
        self.image = self.font.render(f'${self.coins}', True, (0,0,0))
        
    def show(self):
        self.rect.x = 22
        self.rect.y = 50

    def hide(self):
        self.rect.x = -100
        self.rect.y = -300
        
    def reset(self):
        self.coins = 0
        self.image = self.font.render(f'${self.coins}', True, (0,0,0))

##### BUYABLE CLASS #####
## Like the enemy class, the buyable is split into 2 and is rendered as an enemy to get around the rendering issue.
# Shorter dash cooldown
# Longer sword
# Shield - damage that resets each round
# Dodge chance
# Heal 

class UpperBuyable(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("breadc.png")
        #self.image.fill((190, 0, 0, 100), special_flags=pygame.BLEND_ADD)
        self.rect = self.image.get_rect()
        self.rect.update(self.rect.x, self.rect.y + 10, self.rect.width, self.rect.height - 10)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.bought = False
        
    def update(self, player): # has the enemy move with/to player
        # Change visibility to render behind or infront
        if self.rect.y <= player.rect.y:
            self.image.set_alpha(255)
        else:
            self.image.set_alpha(0)

        # this handeles sword colision dectection, player colision is handeled in the player class
        hit_sword = pygame.sprite.spritecollide(self, Swordgroup, False)
        if hit_sword and self.bought == False and purse_image.coins >= 5:
            #self.kill()
            purse_image.coins -= 5
            self.bought = True
            print("OH GOD IM BOUGHT")
            
    def clear(self):
        self.kill()
    
    # This line is to test if I broke git

class LowerBuyable(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("breadc.png")
        #self.image.fill((0, 0, 190, 100), special_flags=pygame.BLEND_ADD)
        self.rect = self.image.get_rect()
        self.rect.update(self.rect.x, self.rect.y + 10, self.rect.width, self.rect.height - 10)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def update(self, player): # has the enemy move with/to player
        # Change visibility to render behind or infront
        if self.rect.y >= player.rect.y:
            self.image.set_alpha(255)
        else:
            self.image.set_alpha(0)
            
    def clear(self):
        self.kill()

def setupShop():
    xPos = 200
    yPos = 200
    
    for i in range(0,2):
        i = UpperBuyable(xPos,yPos)
        j = LowerBuyable(xPos,yPos)
        ShopUppergroup.add(i)
        ShopLowergroup.add(j)
        shopuppersprites.add(i)
        shoplowersprites.add(j)
        xPos += 100
        
def takedownShop():
    for buyable in ShopUppergroup:
        buyable.kill()
    
    for buyable in ShopLowergroup:
        buyable.kill()
        
def clearScreen():
    for enemy in EnemyUppergroup:
            enemy.kill()

    for enemy in EnemyLowergroup:
        enemy.kill()
        
    for coin in coinsprites:
        coin.kill()
######################################################################
#                             MAIN                                   #
######################################################################   
       
def main():
    # Initialise screen
    pygame.init()
    
    global screen
    screen = pygame.display.set_mode((750, 450))
    pygame.display.set_caption('Dough Gone Sour')

    # Fill background
    background = pygame.Surface(screen.get_size())
    #background = pygame.image.load("background.png")
    background = background.convert()
    background.fill((0, 0, 0))    
    
    
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


    # Initialise foregrounds
    global health
    health = HealthBar()

    global notice
    notice = NoticeBoard()

    global bgimage
    bgimage = Backdrop()

    global wave_counter
    wave_counter = WaveCounter()
    
    global veil_layer
    veil_layer = Veil()
    
    global purse_image
    purse_image = Purse()

    def addLeaf():
        chance = randint(0,70)
        if chance == 70:
            i = Leaf()
            decosprites.add(i)
            
    def addFire():
        chance = randint(0,60)
        if chance == 60:
            i = Fire()
            decosprites.add(i)
            
    # Initialize shop sprites
    global ShopUppergroup
    ShopUppergroup = pygame.sprite.Group()
    global ShopLowergroup
    ShopLowergroup = pygame.sprite.Group()

    # Initialize enemies
    global EnemyUppergroup
    EnemyUppergroup = pygame.sprite.Group()
    global EnemyLowergroup
    EnemyLowergroup = pygame.sprite.Group()
    def addEnemies(stage):
        thic_num = int(stage / 2)
        for i in range(0, stage):
            tryspawn = True
            while tryspawn:
                x = randint(10, 750)
                y = randint(10, 450)
                dx = (player1.rect.x + (player1.rect.width/2) ) - (x + (player1.rect.width/2))
                dy = (player1.rect.y + (player1.rect.height/2)) - (y + (player1.rect.height/2))
                dist = math.hypot(dx, dy)
                if dist < 200:
                    tryspawn = True
                else: 
                    tryspawn = False
            i = UpperEnemy(x,y)
            j = LowerEnemy(x,y)
            EnemyUppergroup.add(i)
            EnemyLowergroup.add(j)             
            enemyuppersprites.add(i)
            enemylowersprites.add(j)
        
    

    # Initialise sprites
    playersprites = pygame.sprite.RenderPlain((player1))
    playereffectsprites = pygame.sprite.RenderPlain((effect))
    global enemyuppersprites
    enemyuppersprites = pygame.sprite.RenderPlain() 
    global enemylowersprites
    enemylowersprites = pygame.sprite.RenderPlain()
    global shopuppersprites
    shopuppersprites = pygame.sprite.RenderPlain()
    global shoplowersprites
    shoplowersprites = pygame.sprite.RenderPlain()    
    foregroundsprites = pygame.sprite.RenderPlain((health, notice, wave_counter, purse_image))
    swordsprites = pygame.sprite.RenderPlain((sword))
    theverybackgroundsprites = pygame.sprite.RenderPlain((bgimage))
    decosprites = pygame.sprite.RenderPlain()
    veilsprites = pygame.sprite.RenderPlain((veil_layer))
    global coinsprites
    coinsprites = pygame.sprite.RenderPlain()

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
    global wakeup_blink
    wakeup_blink = pygame.USEREVENT + 6
    global coin_flip
    coin_flip = pygame.USEREVENT + 7
    global game_over
    game_over = True
    global testing
    testing = True
    global intro 
    intro = True
    wave_fin = True
    global wave_num
    wave_num = 0
    show_notice = False
    player1.frameUpdate()
    global ignoreX
    ignoreX = 0
    global ignoreY
    ignoreY = 0

    def restart():
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
        #notice.restart()
        player1.reset()
        health.reset()
        purse_image.reset()
        '''
        for enemy in EnemyUppergroup:
            enemy.kill()

        for enemy in EnemyLowergroup:
            enemy.kill()
            
        for coin in coinsprites:
            coin.kill()
        
        '''
    health.hide()
    wave_counter.hide()
    purse_image.hide()

    # Event loop
    while 1:
        # Make sure game doesn't run at more than 60 frames per second
        clock.tick(60)
        
        if wave_fin == True and show_notice == False and veil_layer.location != "Title":
            notice.show()
            show_notice = True

        if len(enemyuppersprites) == 0 and intro == False:
            wave_fin = True
            if veil_layer.location == "Feild":
                notice.nextWave()
            #notice.hide()

        # Setup key positions 
        moveUp = False
        moveDown = False
        moveRight = False
        moveLeft = False
        dashKey = False
        
        
        if game_over and intro == False and veil_layer.location != "Title":
            notice.restart()
        

        for event in pygame.event.get():
            if event.type == hit_cooldown and player1.health > 0:
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
            if event.type == wakeup_blink:
                player1.wakeup("end")
            if event.type == coin_flip:
                for coin in coinsprites:    
                    coin.frameUpdate()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            if event.type == QUIT:
                return
            if event.type == KEYDOWN and event.key == K_x:
                print(ignoreX)
            if event.type == KEYDOWN and game_over == False and veil_layer.fading != None:  
                if event.key == K_w:
                    #player1.moveup()
                    ignoreY += 1
                if event.key == K_s:
                    #player1.movedown()
                    ignoreY -= 1
                if event.key == K_a:
                    #player1.moveleft()
                    ignoreX -= 1
                if event.key == K_d:
                    #player1.moveright()
                    ignoreX += 1
                    
            if event.type == KEYUP and game_over == False and veil_layer.fading != None:  
                if event.key == K_w:
                    #player1.moveup()
                    ignoreY -= 1
                if event.key == K_s:
                    #player1.movedown()
                    ignoreY += 1
                if event.key == K_a:
                    #player1.moveleft()
                    ignoreX += 1
                if event.key == K_d:
                    #player1.moveright()
                    ignoreX -= 1
                    print("keyup right")
                    print(ignoreX)
            
            if event.type == KEYDOWN and game_over == True and veil_layer.fading == None:
                if event.key == K_RETURN:
                    if not player1.health > 0:
                        player1.wakeup("start")
                    restart()
                    print("restarting")

                    if veil_layer.location == "Title":
                        #notice.hide()
                        veil_layer.next("Feild")
                    else:
                        clearScreen()
                    
                if event.key == K_BACKSPACE and intro == False:
                    if not player1.health > 0:
                        player1.wakeup("start")
                    veil_layer.next("Title")
                    restart()
                    print("moving to title")
                    player1.return_start = True
                    intro = True
                    
            # Get key positions to be used later
            elif event.type == KEYDOWN and game_over == False and veil_layer.fading == None:
                # Base Movement keys
                if event.key == K_w:
                    #player1.moveup()
                    moveUp = True
                    ignoreY = 0
                if event.key == K_s:
                    #player1.movedown()
                    moveDown = True
                    ignoreY = 0
                if event.key == K_a:
                    #player1.moveleft()
                    moveLeft = True
                    ignoreX = 0
                if event.key == K_d:
                    #player1.moveright()
                    moveRight = True
                    ignoreX = 0
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
                if event.key == K_p and testing:
                    i = Coin(200,200)
                    coinsprites.add(i)

                # Waves
                if event.key == K_RETURN and wave_fin and veil_layer.location == "Feild":
                    show_notice = False
                    wave_fin = False
                    addEnemies(wave_num)
                    wave_counter.tick(wave_num)
                    wave_num += 1
                    notice.hide()
                    print("starting next wave")
                    
                if event.key == K_b and wave_fin: 
                    if veil_layer.location == "Feild":
                        veil_layer.next("Store")
                        notice.hide()
                    if veil_layer.location == "Store":
                        veil_layer.next("Feild")
                        notice.show()

            

            elif event.type == KEYUP and game_over == False and veil_layer.fading == None:
                #if event.key == K_a or event.key == K_w or event.key == K_s or event.key == K_d:
                #    player1.movepos = [0,0]
                #    player1.state = "still"

                if event.key == K_a and ignoreX == 0: 
                    player1.stopmoveleft()
                    
                if event.key == K_d and ignoreX == 0:
                    player1.stopmoveright()

                if event.key == K_w and ignoreY == 0: 
                    player1.stopmoveup()
                if event.key == K_s and ignoreY == 0:
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

        if veil_layer.location == "Title":
            addFire()
        else:
            addLeaf()

        # Update stuffs
        theverybackgroundsprites.update()
        if game_over == False and veil_layer.fading == None:
            enemyuppersprites.update(player1)
            enemylowersprites.update(player1)
        shopuppersprites.update(player1)
        shoplowersprites.update(player1)
        playereffectsprites.update(player1)
        playersprites.update()
        foregroundsprites.update()
        swordsprites.update(player1)
        decosprites.update()
        veilsprites.update()
        coinsprites.update()


        # Render Stuffs 

        for enemy in enemyuppersprites:
            screen.blit(background, enemy.rect)

        for enemy in enemylowersprites:
            screen.blit(background, enemy.rect)
            
        for buyable in shopuppersprites:
            screen.blit(background, buyable.rect)
            
        for buyable in shoplowersprites:
            screen.blit(background, buyable.rect)
            
        for leaf in decosprites:
            screen.blit(background, leaf.rect)
            
        for coin in coinsprites:
            screen.blit(background, coin.rect)
            
        screen.blit(background, player1.rect)
        screen.blit(background, health.rect)
        screen.blit(background, sword.rect)     
        screen.blit(background, bgimage.rect)
        screen.blit(background, veil_layer.rect)
        
        theverybackgroundsprites.draw(screen)
       
        coinsprites.draw(screen)
       
        playereffectsprites.draw(screen)
        
        enemyuppersprites.draw(screen)
        
        shopuppersprites.draw(screen)

        if veil_layer.fading == None:
            playersprites.draw(screen)
        
        swordsprites.draw(screen)

        enemylowersprites.draw(screen)
        
        shoplowersprites.draw(screen)
        
        decosprites.draw(screen)
 
        foregroundsprites.draw(screen)
   
        veilsprites.draw(screen)
        
        if veil_layer.fading != None:
            playersprites.draw(screen)
        
        
        pygame.display.flip()


if __name__ == '__main__': main()



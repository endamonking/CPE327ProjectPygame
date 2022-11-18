from array import array
import imp
from pickle import FALSE
import pygame
import os
import random
from pygame import mixer

# Background music
pygame.mixer.init()
pygame.mixer.pre_init(44100,16,2,4096)
#load asset
BLACK = (0,0,0) 
animation_cooldown = 500
blackScreen = pygame.transform.scale(pygame.image.load(os.path.join('Asset', 'blackScreen.jpg')), (300, 75))

#enemy class
class enemy():
    def __init__(self, name, maxHp, defendPoint, attackPoint, xScale, yScale):
        self.name = name
        self.maxHp = maxHp
        self.currentHp = self.maxHp
        self.defendPoint = defendPoint
        self.currentDefPoint = self.defendPoint
        self.attackPoint = attackPoint
        self.currentAtkPoint = self.attackPoint
        self.lastUpdate = pygame.time.get_ticks()
        self.i = 0
        self.enemy_image = pygame.image.load(f'Asset/{self.name}/0.png')
        self.enemy_image = pygame.transform.scale(self.enemy_image, (xScale, yScale))
        self.turn = False
        self.death = False
        self.defendBuff = False
        self.attackBuff = False
        self.action = "idle"
        self.skillList = []

    def getAttackPower(self):
        return self.attackPoint

    def getTurn(self):
        return self.turn

    def draw_enemyIdle(self,WIN, currentTime, Xpose, Ypose, divide):
        if (currentTime - self.lastUpdate >= animation_cooldown):
            self.lastUpdate = currentTime
            if self.i < 1:
                self.i = self.i+1
            else:
                self.i = 0
        WIN.blit(self.enemy_image, (Xpose, Ypose), ((self.i * divide), 0, divide, 300)) #width come from total width / total frame

    #slime skill
    def attackSlime(self,enemy):
        rand = random.randint(1,10)
        damaged = 0
        if rand < 2:
            self.currentHp = self.maxHp
            print("enemy heal")
        elif rand >= 2:
            damaged = self.attackPoint - enemy.defendPoint
            if damaged <= 0:
                damaged = 0
            regen_sound = mixer.Sound(r'sound effect\Slime\regenerate.mp3')
            regen_sound.set_volume(1)
            regen_sound.play()
            enemy.currentHp = enemy.currentHp - damaged
            if enemy.currentHp < 0 :
                enemy.currentHp = 0
                enemy.death = True            
        return damaged, "monster"

    #Zombie skill
    def attackZombie(self,enemy):
        rand = random.randint(1,10)
        damaged = 0
        if rand < 3:
            damaged = self.attackPoint*2 - enemy.defendPoint
            print("enemy double attack")
            attack = mixer.Sound(r'sound effect\Zombie\attack.mp3')
            attack.set_volume(0.8)
            attack.play()
            if damaged <= 0:
                damaged = 0
        else:
            damaged = self.attackPoint - enemy.defendPoint
            attack = mixer.Sound(r'sound effect\Zombie\attack.mp3')
            attack.set_volume(0.8)
            attack.play()
            if damaged <= 0:
                damaged = 0

        enemy.currentHp = enemy.currentHp - damaged
        if enemy.currentHp < 0 :
            enemy.currentHp = 0
            enemy.death = True
        return damaged, "monster"
    #dragon skill  
    def attackDragon(self,enemy):
        rand = random.randint(1,100)
        damaged = 0
        if rand < 21:
            fire_ball = mixer.Sound(r'sound effect\Dragon\fire.mp3')
            fire_ball.set_volume(0.8)
            fire_ball.play()
            print("fire breathing")
            damaged = self.attackPoint
            if damaged <= 0:
                damaged = 0
        elif 20 < rand < 41:
            iron_skill = mixer.Sound(r'sound effect\Dragon\skin.mp3')
            iron_skill.set_volume(0.8)
            iron_skill.play()
            print("Iron skin")
            self.defendBuff = True
            Defi = 0
            self.currentDefPoint = self.defendPoint + 10
        else:
            damaged = self.attackPoint - enemy.defendPoint
            if damaged <= 0:
                damaged = 0
            attack = mixer.Sound(r'sound effect\Dragon\attack.mp3')
            attack.set_volume(0.8)
            attack.play()
        if self.defendBuff == True:
            Defi = Defi + 1
            if Defi >= 4:
                self.defendBuff = False
                self.currentDefPoint = self.defendPoint

        enemy.currentHp = enemy.currentHp - damaged
        if enemy.currentHp < 0 :
            enemy.currentHp = 0
            enemy.death = True
        return damaged, "monster"

    #werewolf1 skill  
    def attackWerewolf1(self,enemy):
        rand = random.randint(1,10)
        damaged = 0
        if rand < 4:
            damaged = self.attackPoint*2 - enemy.defendPoint
            print("enemy double slash")
            if damaged <= 0:
                damaged = 0
        elif 3 < rand < 6:
            print("Iron skin")
            self.defendBuff = True
            Defi = 0
            self.currentDefPoint = self.defendPoint + 10
        else:
            damaged = self.attackPoint - enemy.defendPoint
            if damaged <= 0:
                damaged = 0
        
        if self.defendBuff == True:
            Defi = Defi + 1
            if Defi >= 4:
                self.defendBuff = False
                self.currentDefPoint = self.defendPoint

        enemy.currentHp = enemy.currentHp - damaged
        if enemy.currentHp < 0 :
            enemy.currentHp = 0
            enemy.death = True
        return damaged, "monster"

        #werewolf2 skill  
    def attackWerewolf2(self,enemy):
        rand = random.randint(1,10)
        damaged = 0
        if rand < 4:
            damaged = self.currentAtkPoint*2 - enemy.defendPoint
            print("enemy double slash")
            if damaged <= 0:
                damaged = 0
        elif 3 < rand < 6:
            print("Iron skin")
            self.attackBuff = True
            atki = 0
            self.currentAtkPoint = self.attackPoint + 20
        else:
            damaged = self.currentAtkPoint - enemy.defendPoint
            if damaged <= 0:
                damaged = 0
        
        if self.attackBuff == True:
            atki = atki + 1
            if atki >= 4:
                self.attachBuff = False
                self.currentAtkPoint = self.attackPoint
                
        enemy.currentHp = enemy.currentHp - damaged
        if enemy.currentHp < 0 :
            enemy.currentHp = 0
            enemy.death = True
        return damaged, "monster"

    def showHealth(self, WIN):
        currentHP  = str(self.currentHp)
        my_font = pygame.font.SysFont("candara",40)

        #render text
        text_surface1 = my_font.render("HP : ", False, (255,255,255))
        WIN.blit(text_surface1, (780, 200))
        text_surface2 = my_font.render(currentHP, False, (255,255,255))
        WIN.blit(text_surface2, (880, 200))

    def isDead(self):
        gameStage = "Win"

        if self.currentHp <= 0 and self.name == "zombie":
            rand = random.randint(1,100)
            if rand < 1:
                regen = mixer.Sound(r'sound effect\Zombie\revive.mp3')
                regen.set_volume(0.8)
                regen.play()
                print("enemy revive with chance 50%")
                self.currentHp = self.maxHp
                gameStage = "Normal"
            self.death = False
        elif self.currentHp <= 0 and self.name == "werewolf1":
            print("knight become werewolf")
            gameStage = "Next"
            self.death = False
        elif self.currentHp <= 0:
            self.currentHp = 0
            self.death = True

        return gameStage

    def showMonsterStatus(self,win):
        if self.action == "stunned":
            blackScreen.set_alpha(128)
            win.blit(blackScreen, (780,170))

            text = "stunning"
            my_font = pygame.font.SysFont("candara",36)
            text_surface = my_font.render(text, False, (255,255,255))
            win.blit(text_surface, (780,180))



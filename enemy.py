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
boss_effect = pygame.transform.scale(pygame.image.load(os.path.join('Asset', 'boss_effect.png')), (200, 200))
Defi = 0
atki = 0
counter = 0

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
        self.casting = False
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

    def draw_effect(self,WIN, currentTime, Xpose, Ypose, divide):
        if (currentTime - self.lastUpdate >= animation_cooldown):
            self.lastUpdate = currentTime
            if self.i < 2:
                self.i = self.i+1
            else:
                self.i = 0
        WIN.blit(boss_effect, (Xpose, Ypose), ((self.i * divide), 0, divide, 300)) #width come from total width / total frame

    #slime skill
    def attackSlime(self,enemy):
        rand = random.randint(1,10)
        damaged = 0
        if rand < 2:
            self.currentHp = self.maxHp
            print("enemy heal")
        elif rand >= 2:
            damaged = self.attackPoint - enemy.currentDefendPoint
            if damaged <= 0:
                damaged = 0
            regen_sound = mixer.Sound(r'sound effect\Slime\regenerate.mp3')
            regen_sound.set_volume(1)
            regen_sound.play()
            enemy.currentHp = enemy.currentHp - damaged
            if enemy.currentHp <= 0 :
                enemy.currentHp = 0
                enemy.death = True            
        return damaged, "monster"

    #Zombie skill
    def attackZombie(self,enemy):
        rand = random.randint(1,10)
        damaged = 0
        if rand < 3:
            damaged = self.attackPoint*2 - enemy.currentDefendPoint
            print("enemy double attack")
            attack = mixer.Sound(r'sound effect\Zombie\attack.mp3')
            attack.set_volume(0.8)
            attack.play()
            if damaged <= 0:
                damaged = 0
        else:
            damaged = self.attackPoint - enemy.currentDefendPoint
            attack = mixer.Sound(r'sound effect\Zombie\attack.mp3')
            attack.set_volume(0.8)
            attack.play()
            if damaged <= 0:
                damaged = 0

        enemy.currentHp = enemy.currentHp - damaged
        if enemy.currentHp <= 0 :
            enemy.currentHp = 0
            enemy.death = True
        return damaged, "monster"
    #dragon skill  
    def attackDragon(self,enemy):
        global Defi
        print(Defi)
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
            damaged = self.attackPoint - enemy.currentDefendPoint
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
        if enemy.currentHp <= 0 :
            enemy.currentHp = 0
            enemy.death = True
        return damaged, "monster"

    #werewolf1 skill  
    def attackWerewolf1(self,enemy):
        global Defi

        rand = random.randint(1,10)
        damaged = 0
        if rand < 4:
            damaged = self.attackPoint*2 - enemy.currentDefendPoint
            print("enemy double slash")
            if damaged <= 0:
                damaged = 0
        elif 3 < rand < 6:
            print("Iron skin")
            self.defendBuff = True
            Defi = 0
            self.currentDefPoint = self.defendPoint + 10
        else:
            damaged = self.attackPoint - enemy.currentDefendPoint
            if damaged <= 0:
                damaged = 0
        
        if self.defendBuff == True:
            Defi = Defi + 1
            if Defi >= 4:
                self.defendBuff = False
                self.currentDefPoint = self.defendPoint

        enemy.currentHp = enemy.currentHp - damaged
        if enemy.currentHp <= 0 :
            enemy.currentHp = 0
            enemy.death = True
        return damaged, "monster"

        #werewolf2 skill  
    def attackWerewolf2(self,enemy):
        global atki

        rand = random.randint(1,10)
        damaged = 0
        if rand < 4:
            damaged = self.currentAtkPoint*2 - enemy.currentDefendPoint
            print("enemy double slash")
            if damaged <= 0:
                damaged = 0
        elif 3 < rand < 6:
            print("Hell hound")
            self.attackBuff = True
            atki = 0
            self.currentAtkPoint = self.attackPoint + 20
        else:
            damaged = self.currentAtkPoint - enemy.currentDefendPoint
            if damaged <= 0:
                damaged = 0
        
        if self.attackBuff == True:
            atki = atki + 1
            if atki >= 4:
                self.attachBuff = False
                self.currentAtkPoint = self.attackPoint
                
        enemy.currentHp = enemy.currentHp - damaged
        if enemy.currentHp <= 0 :
            enemy.currentHp = 0
            enemy.death = True
        return damaged, "monster"

    #witch skill  
    def attackWitch(self,enemy):
        rand = random.randint(1,20)
        damaged = 0
        if rand < 21:
            print("Death phantom")
            self.action = "casting"
        elif 20 < rand < 51:
            print("Demon bane")
            damaged = self.currentAtkPoint
        elif 50 < rand < 71:
            print("Draining")
            damaged = self.currentAtkPoint - enemy.currentDefendPoint
            if damaged < 0:
                damaged = 0
            enemy.currentMp = enemy.currentMp - damaged*0.2
            if enemy.currentMp < 0:
                enemy.currentMp = 0
            self.currentHp = self.currentHp + damaged*0.2
            if self.currentHp > self.maxHp:
                self.currenHp = self.maxHp
        else:
            damaged = self.attackPoint - enemy.currentDefendPoint
            if damaged <= 0:
                damaged = 0

        enemy.currentHp = enemy.currentHp - damaged
        if enemy.currentHp <= 0 :
            enemy.currentHp = 0
            enemy.death = True
        return damaged, "monster"

    #witchCasting
    def castWitch(self,enemy):
        self.action = "idle"
        damaged = self.currentAtkPoint*100000
        if damaged < 0:
            damaged = 0
        enemy.currentHp = enemy.currentHp - damaged
        if enemy.currentHp <= 0 :
            enemy.currentHp = 0
            enemy.death = True
        return damaged, "monster"

    #boss phase 1
    def attackBoss1(self,enemy):
        rand = random.randint(1,100)
        damaged = 0
        global Defi
        if rand < 21:
            print("True slash")
            damaged = self.currentAtkPoint
        elif 20 < rand < 41:
            print("Dimond skin")
            self.defendBuff = True
            Defi = 0
            self.currentDefPoint = self.defendPoint + 50
        elif 40 < rand < 66:
            print("Triple slash")
            damaged = self.currentAtkPoint*3 - enemy.currentDefendPoint
        else:
            print("Dark slash")
            damaged = self.attackPoint - enemy.currentDefendPoint
            if damaged <= 0:
                damaged = 0

        if self.defendBuff == True:
            Defi = Defi + 1
            if Defi >= 4:
                self.defendBuff = False
                self.currentDefPoint = self.defendPoint

        enemy.currentHp = enemy.currentHp - damaged
        if damaged > 0:
            self.currentHp = self.currentHp + damaged*0.25
            print("Drain Health")
        if enemy.currentHp <= 0 :
            enemy.currentHp = 0
            enemy.death = True
        return damaged, "monster"

    #boss phase 2
    def attackBoss2(self,enemy):
        rand = random.randint(1,100)
        damaged = 0
        global Defi
        if rand < 21:
            print("Death phantom")
            self.action = "casting"
        elif 20 < rand < 41:
            print("True slash")
            damaged = self.currentAtkPoint*1.5
        elif 40 < rand < 61:
            print("Dimond skin")
            self.defendBuff = True
            Defi = 0
            self.currentDefPoint = self.defendPoint + 50
        elif 60 < rand < 81:
            print("Triple slash")
            damaged = self.currentAtkPoint*3 - enemy.currentDefendPoint
        else:
            print("Phantom bane")
            print("Draining Mana")
            damaged = self.currentAtkPoint - enemy.currentDefendPoint
            if damaged < 0:
                damaged = 0
            enemy.currentMp = enemy.currentMp - damaged*0.2
            if enemy.currentMp < 0:
                enemy.currentMp = 0

        if self.defendBuff == True:
            Defi = Defi + 1
            if Defi >= 4:
                self.defendBuff = False
                self.currentDefPoint = self.defendPoint

        enemy.currentHp = enemy.currentHp - damaged
        if damaged > 0:
            self.currentHp = self.currentHp + damaged*0.4
            if self.currentHp > self.maxHp:
                self.currentHp = self.maxHp
            print("Drain Health")
        if enemy.currentHp <= 0 :
            enemy.currentHp = 0
            enemy.death = True
        return damaged, "monster"


        #witchCasting
    def castBoss(self,enemy):
        self.action = "idle"
        damaged = self.currentAtkPoint*10000000
        if damaged < 0:
            damaged = 0
        enemy.currentHp = enemy.currentHp - damaged
        if enemy.currentHp <= 0 :
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
        global counter
        if self.currentHp <= 0 and self.name == "zombie":
            if counter < 3:
                regen = mixer.Sound(r'sound effect\Zombie\revive.mp3')
                regen.set_volume(0.8)
                regen.play()
                self.currentHp = self.maxHp*(0.25*(3 - counter))
                gameStage = "Normal"
                self.death = False
                counter = counter + 1
            else:
                self.death = True
        elif self.currentHp <= 0 and self.name == "werewolf1":
            print("knight become werewolf")
            gameStage = "Next"
            self.death = False
        elif self.currentHp <= 0 and self.name == "boss1":
            print("The ture finale boss come")
            gameStage = "Next"
            self.death = False
        elif self.currentHp <= 0:
            self.currentHp = 0
            self.death = True

        return gameStage

    def showMonsterStatus(self,win):
        if self.action == "stunned":
            blackScreen.set_alpha(128)
            win.blit(blackScreen, (780,100))

            text = "stunning"
            my_font = pygame.font.SysFont("candara",36)
            text_surface = my_font.render(text, False, (255,255,255))
            win.blit(text_surface, (780,110))

        if self.action == "casting":
            blackScreen.set_alpha(128)
            win.blit(blackScreen, (780,100))

            text = "casting"
            my_font = pygame.font.SysFont("candara",36)
            text_surface = my_font.render(text, False, (255,255,255))
            win.blit(text_surface, (780,110))




from array import array
import imp
from pickle import FALSE
import pygame
import os
import random
import math
from pygame import mixer

# Background music
pygame.mixer.init()
pygame.mixer.pre_init(44100,16,2,4096)
#load asset
BLACK = (0,0,0) 
WIDTH = 1080
HEIGHT = 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
fireBallEF = pygame.transform.scale(pygame.image.load(
    os.path.join('Asset', 'Effect', 'fireBall.png')), (1800, 300))
fireBallEF = pygame.transform.rotate(fireBallEF,180)
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
        self.EfxLastUpdate = pygame.time.get_ticks() + 1
        self.i = 0
        self.enemy_image = pygame.image.load(f'Asset/{self.name}/0.png')
        self.enemy_image = pygame.transform.scale(self.enemy_image, (xScale, yScale))
        self.turn = False
        self.death = False
        self.defendBuff = False
        self.attackBuff = False
        self.action = "idle"
        self.showWhat = "nothing"
        self.casting = False
        self.skillList = []
        self.revi = 0
        self.efxI = 0

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

    def damageCal(self,attack,defense):
        return math.floor(10*attack/(defense+1))

    #slime skill
    def attackSlime(self,enemy):
        rand = random.randint(1,10)
        damaged = 0
        if rand < 2:
            self.currentHp = self.maxHp
            print("enemy heal")
        elif rand >= 2:
            damaged = self.damageCal(self.attackPoint,enemy.currentDefendPoint)
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
            damaged = 2*self.damageCal(self.attackPoint,enemy.currentDefendPoint)
            print("enemy double attack")
            attack = mixer.Sound(r'sound effect\Zombie\attack.mp3')
            attack.set_volume(0.5)
            attack.play()
            if damaged <= 0:
                damaged = 0
        else:
            damaged = self.damageCal(self.attackPoint,enemy.currentDefendPoint)
            attack = mixer.Sound(r'sound effect\Zombie\attack.mp3')
            attack.set_volume(0.5)
            attack.play()
            if damaged <= 0:
                damaged = 0

        enemy.currentHp = enemy.currentHp - damaged
        if enemy.currentHp <= 0 :
            enemy.currentHp = 0
            enemy.death = True
        return damaged, "monster"
    #dragon skill  
    def attackDragon(self,enemy,currentTime):
        global Defi
        print(Defi)
        rand = random.randint(1,100)
        damaged = 0
        if rand < 21:
            fire_ball = mixer.Sound(r'sound effect\Dragon\fire.mp3')
            fire_ball.set_volume(0.8)
            fire_ball.play()
            
            self.displayFireBallEffect(WIN,currentTime)
            print("fire breathing")
            damaged = self.attackPoint * 1.5
            
        elif 20 < rand < 41:
            iron_skill = mixer.Sound(r'sound effect\Dragon\skin.mp3')
            iron_skill.set_volume(0.8)
            iron_skill.play()
            print("Iron skin")
            self.defendBuff = True
            Defi = 0
            self.currentDefPoint = self.defendPoint + 10
        else:
            damaged = self.damageCal(self.attackPoint,enemy.currentDefendPoint)
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
    def displayFireBallEffect(self, WIN, currentTime):
        if (currentTime - self.EfxLastUpdate >= 100):
            self.EfxLastUpdate = currentTime
            if self.efxI < 12:
                self.efxI = self.efxI+1
            else:
                self.showWhat = "nothing"
                self.efxI = 0
                return
        # width come from total width / total frame
        WIN.blit(fireBallEF, (150 + ((12-self.efxI) * 50), 330), (((12-self.efxI) * 100), 0, 100, 300))
    #werewolf1 skill  
    def attackWerewolf1(self,enemy):
        global Defi

        rand = random.randint(1,10)
        damaged = 0
        if rand < 4:
            damaged = 2*self.damageCal(self.attackPoint,enemy.currentDefendPoint)
            double_slash = mixer.Sound(r'sound effect\Werewolf\double slash1.mp3')
            double_slash.set_volume(0.8)
            double_slash.play()
            print("enemy double slash")
            if damaged <= 0:
                damaged = 0
        elif 3 < rand < 6:
            iron_skin = mixer.Sound(r'sound effect\Werewolf\iron skin.mp3')
            iron_skin.set_volume(0.8)
            iron_skin.play()
            print("Iron skin")
            self.defendBuff = True
            Defi = 0
            self.currentDefPoint = self.defendPoint + 10
        else:
            attack = mixer.Sound(r'sound effect\Werewolf\attack1.mp3')
            attack.set_volume(0.8)
            attack.play()
            damaged = self.damageCal(self.attackPoint,enemy.currentDefendPoint)
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
            damaged = 2*self.damageCal(self.attackPoint,enemy.currentDefendPoint)
            double_slash = mixer.Sound(r'sound effect\Werewolf\double slash2.mp3')
            double_slash.set_volume(0.8)
            double_slash.play()
            print("enemy double slash")
            if damaged <= 0:
                damaged = 0
        elif 3 < rand < 6:
            print("Hell hound")
            hell_hound = mixer.Sound(r'sound effect\Werewolf\tansfrom.mp3')
            hell_hound.set_volume(0.8)
            hell_hound.play()
            self.attackBuff = True
            atki = 0
            self.currentAtkPoint = self.attackPoint + 20
        else:
            attack = mixer.Sound(r'sound effect\Werewolf\attack2.mp3')
            attack.set_volume(0.8)
            attack.play()
            damaged = self.damageCal(self.attackPoint,enemy.currentDefendPoint)
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
        rand = random.randint(1,100)
        damaged = 0
        if rand < 11:
            casting = mixer.Sound(r'sound effect\Witch\casting.mp3')
            casting.set_volume(0.8)
            casting.play()
            print("Death phantom")
            self.action = "casting"
        elif 10 < rand < 41:
            demon_bane = mixer.Sound(r'sound effect\Witch\attack.mp3')
            demon_bane.set_volume(0.8)
            demon_bane.play()
            print("Demon bane")
            damaged = self.currentAtkPoint
        elif 40 < rand < 61:
            draining = mixer.Sound(r'sound effect\Witch\drain mana.mp3')
            draining.set_volume(0.8)
            draining.play()
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
            attack = mixer.Sound(r'sound effect\Witch\attack.mp3')
            attack.set_volume(0.8)
            attack.play()
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
            true_slash = mixer.Sound(r'sound effect\Dark knight P1\true slash.mp3')
            true_slash.set_volume(0.8)
            true_slash.play()
            print("True slash")
            damaged = self.currentAtkPoint
        elif 20 < rand < 41:
            dimond_skin = mixer.Sound(r'sound effect\Dark knight P1\dimond skin.mp3')
            dimond_skin.set_volume(0.8)
            dimond_skin.play()
            print("Dimond skin")
            self.defendBuff = True
            Defi = 0
            self.currentDefPoint = self.defendPoint + 20
        elif 40 < rand < 66:
            triple_slash = mixer.Sound(r'sound effect\Dark knight P1\triple slash.mp3')
            triple_slash.set_volume(0.8)
            triple_slash.play()
            print("Triple slash")
            damaged = self.currentAtkPoint*3 - enemy.currentDefendPoint
        else:
            dark_slash = mixer.Sound(r'sound effect\Dark knight P1\dark slash.mp3')
            dark_slash.set_volume(0.8)
            dark_slash.play()
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
        if rand < 11:
            death_phantom = mixer.Sound(r'sound effect\Witch\attack.mp3')
            death_phantom.set_volume(0.8)
            death_phantom.play()
            print("Death phantom")
            self.action = "casting"
        elif 10 < rand < 31:
            true_slash = mixer.Sound(r'sound effect\Dark knight P2\true slash.mp3')
            true_slash.set_volume(0.8)
            true_slash.play()
            print("True slash")
            damaged = self.currentAtkPoint*1.5
        elif 30 < rand < 51:
            dimond_skin = mixer.Sound(r'sound effect\Dark knight P2\dimond skin.mp3')
            dimond_skin.set_volume(0.8)
            dimond_skin.play()
            print("Dimond skin")
            self.defendBuff = True
            Defi = 0
            self.currentDefPoint = self.defendPoint + 50
        elif 50 < rand < 71:
            triple_slash = mixer.Sound(r'sound effect\Dark knight P2\triple slash.mp3')
            triple_slash.set_volume(0.8)
            triple_slash.play()
            print("Triple slash")
            damaged = self.currentAtkPoint*3 - enemy.currentDefendPoint
        else:
            print("Phantom bane")
            print("Draining Mana")
            drain_mana = mixer.Sound(r'sound effect\Dark knight P2\dark ball.mp3')
            drain_mana.set_volume(0.8)
            drain_mana.play()
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
            if self.revi < 3:
                regen = mixer.Sound(r'sound effect\Zombie\revive.mp3')
                regen.set_volume(0.5)
                regen.play()
                self.currentHp = self.maxHp*(0.25*(3 - self.revi))
                gameStage = "Normal"
                self.death = False
                self.revi = self.revi + 1
            else:
                self.death = True
            return gameStage
        elif self.currentHp <= 0 and self.name == "werewolf1":
            print("knight become werewolf")
            gameStage = "Next"
            self.death = False
        elif self.currentHp <= 0 and self.name == "boss1":
            print("The ture finale boss come")
            gameStage = "Next"
            self.death = False
        elif self.currentHp <= 0 and self.name == "boss2":
            print("victory")
            gameStage = "victory"
            self.death = True
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




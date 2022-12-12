#
# This code use to create Enemy Object
# Each enemy have own unique skill and sprite animation to fight with player in each stage
# Each stage have different enemy
# Enemy include slime, zombie, dragon, werewolf(knight form), werewolf(werewolf form), witch, final boss phase1, final boss phase2
#  
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
#global variable
Defi = 0 # counter for defend point buff
atki = 0 # counter for attack point buff
counter = 0 # counter for count enemy's death
global_sound = 0.25 # sound volume at percent


#enemy class
class enemy():
    #Use to create enemy object
    #Arguments
    # maxHp - The maximum HP of enemy
    # maxMp - The maximum MP of enemy
    # defendPoint - The starter defend point of Player
    # attackPoint - The starter attackt point of Player  
    # argrument include of (monster'sname, DEFpoint,attackPoint, and scale for character which x and y coordinate)
    def __init__(self, name, maxHp, defendPoint, attackPoint, xScale, yScale):
        self.name = name
        self.maxHp = maxHp
        self.currentHp = self.maxHp # Current Hp of enemy. Start at max hp
        self.defendPoint = defendPoint
        self.currentDefPoint = self.defendPoint # Cureent DEF of enemy. Start at DEFpoint
        self.attackPoint = attackPoint
        self.currentAtkPoint = self.attackPoint #Current ATK of enemy. Start at ATKpoint
        self.lastUpdate = pygame.time.get_ticks() #To get the Time of enemy active 
        self.finalUpdate = pygame.time.get_ticks() #To get the Time of enemy active 
        self.EfxLastUpdate = pygame.time.get_ticks() + 1 #To get the Time of enemy effect
        self.i = 0 #Counter of idle animation
        self.j = 0 #Counter of idle animation
        self.enemy_image = pygame.image.load(f'Asset/{self.name}/0.png') # to get sprite asset for enemy from file according the input name
        self.enemy_image = pygame.transform.scale(self.enemy_image, (xScale, yScale)) # adjust size of enemy's sprite according xScale and yScale
        self.turn = False # Check the enemy turn
        self.death = False # Check The enemy is dead yet
        self.defendBuff = False # Check the duration for defend point buff
        self.attackBuff = False # Check the duration for attack point buff
        self.action = "idle" # The current action of enemy
        self.showWhat = "nothing" # specify enemy's action to display enemy's action on the screen
        self.casting = False # Check the duration for enemy casting's action
        self.revi = 0 # counter for enemy's resurrection
        self.efxI = 0 # counter for display enemy's skill
        self.dummyText = "nothing" # recieve input for display text on the screen
        
    # give enemy current ATK point
    # Return - current ATK point
    def getAttackPower(self):
        return self.attackPoint

    # give enemy current ATK point
    # Return - current ATK point
    def getTurn(self):
        return self.turn

    #Show status of enemy whatever enemy doing
    #Arguments
    # win - window screen
    # currentTime - The time the program is running
    def showMenu(self, win, currentTime):

        match self.showWhat:
            case "Attacking":
                    blackScreen.set_alpha(128)
                    win.blit(blackScreen, (400, 270))

                    text = self.dummyText
                    my_font = pygame.font.SysFont("candara", 36)
                    text_surface = my_font.render(text, False, (255, 255, 255))
                    win.blit(text_surface, (410, 280))
            case "usingSkill":
                    blackScreen.set_alpha(128)
                    win.blit(blackScreen, (400, 270))

                    text = self.dummyText
                    my_font = pygame.font.SysFont("candara", 36)
                    text_surface = my_font.render(text, False, (255, 255, 255))
                    win.blit(text_surface, (410, 280))                    

    #Display enemy's idle animation on screen
    #Arguments
    # WIN - window screen
    # currentTime - The time the program is running
    # Xpose - Display position of player in X axis
    # Ypose - Display position of player in Y axis
    def draw_enemyIdle(self,WIN, currentTime, Xpose, Ypose, divide):
        if (currentTime - self.lastUpdate >= animation_cooldown):
            self.lastUpdate = currentTime
            if self.i < 1:
                self.i = self.i+1
            else:
                self.i = 0
        WIN.blit(self.enemy_image, (Xpose, Ypose), ((self.i * divide), 0, divide, 300)) #width come from total width / total frame

    #Display enemy's skill animation or effect on screen
    #Arguments
    # WIN - window screen
    # currentTime - The time the program is running
    # Xpose - Display position of player in X axis
    # Ypose - Display position of player in Y axis
    def draw_effect(self,WIN, currentTime, Xpose, Ypose, divide):
        if (currentTime - self.finalUpdate >= animation_cooldown):
            self.finalUpdate = currentTime
            if self.j < 2:
                self.j = self.j+1
            else:
                self.j = 0
        WIN.blit(boss_effect, (Xpose, Ypose), ((self.j * divide), 0, divide, 300)) #width come from total width / total frame

    #Calculate damage that enemy do to the player
    #Return result which is damage
    #Arguments
    # attack - Current attack point of enemy
    # defend - Current defend point of enemy
    def damageCal(self,attack,defense):
        return math.floor(10*attack/(defense+1))
 
    #Set of slime behavior and skill
    #Return damage to display damaged done on screen
    #Argument
    #enemy - player character
    def attackSlime(self,enemy):
        rand = random.randint(1,10)
        damaged = 0
        #skill "Healing" with chance 20%
        #increase currentHp of the slime
        if rand < 3:
            self.currentHp = self.maxHp
            self.showWhat = "usingSkill"
            self.dummyText = "Healing"
        #Normal attack with chance 80%
        #Deal damage to the player
        elif rand >= 3:
            damaged = self.damageCal(self.currentAtkPoint,enemy.currentDefendPoint) 
            regen_sound = mixer.Sound(r'sound effect\Slime\regenerate.mp3')
            regen_sound.set_volume(global_sound)
            regen_sound.play()
            self.showWhat = "Attacking"
            self.dummyText = "Attack"
            enemy.currentHp = enemy.currentHp - damaged
            if enemy.currentHp <= 0 :
                enemy.currentHp = 0
                enemy.death = True            
        return damaged, "monster"

    #Set of zombie behavior and skill
    #Return damage to display damaged done on screen
    #Argument
    #enemy - player character
    def attackZombie(self,enemy):
        rand = random.randint(1,10)
        damaged = 0
        #skill "Double attack" with chance 20%
        #Deal damage to the player with 2 times attack power
        if rand < 3:
            damaged = 2*self.damageCal(self.currentAtkPoint,enemy.currentDefendPoint)
            self.showWhat = "usingSkill"
            self.dummyText = "Double attack"
            print("enemy double attack")
            attack = mixer.Sound(r'sound effect\Zombie\attack.mp3')
            attack.set_volume(global_sound)
            attack.play()
            if damaged <= 0:
                damaged = 0
        #Normal damage with chance 80%
        #Deal damage to the player
        else:
            damaged = self.damageCal(self.currentAtkPoint,enemy.currentDefendPoint)
            self.showWhat = "Attacking"
            self.dummyText = "Attack"
            attack = mixer.Sound(r'sound effect\Zombie\attack.mp3')
            attack.set_volume(global_sound)
            attack.play()
            if damaged <= 0:
                damaged = 0

        enemy.currentHp = enemy.currentHp - damaged
        if enemy.currentHp <= 0 :
            enemy.currentHp = 0
            enemy.death = True
        return damaged, "monster"

    #Set of dragon behavior and skill
    #Return damage to display damaged done on screen
    #Argument
    #enemy - player character 
    def attackDragon(self,enemy,currentTime):
        global Defi
        print(Defi)
        rand = random.randint(1,100)
        damaged = 0
        #skill "Double attack" with chance 20%
        #Deal damage to the player with 1.5 times attack power with ignore player's defendpoint
        if rand < 21:
            self.showWhat = "usingSkill"
            self.dummyText = "Fire breathing"
            fire_ball = mixer.Sound(r'sound effect\Dragon\fire.mp3')
            fire_ball.set_volume(global_sound)
            fire_ball.play()
            
            self.displayFireBallEffect(WIN,currentTime)
            print("fire breathing")
            damaged = math.floor(1.5*self.currentAtkPoint)
            if damaged <= 0:
                damaged = 0
        #skill "Iron skin" with chance 20%
        #Increase self defend point for 3 turn
        elif 20 < rand < 41:
            iron_skill = mixer.Sound(r'sound effect\Dragon\skin.mp3')
            iron_skill.set_volume(global_sound)
            iron_skill.play()
            self.showWhat = "usingSkill"
            self.dummyText = "Iron skin"
            print("Iron skin")
            self.defendBuff = True
            Defi = 0
            self.currentDefPoint = self.defendPoint + 10
        #Normal damage with chance 60%
        #Deal damage to the player
        else:
            damaged = self.damageCal(self.currentAtkPoint,enemy.currentDefendPoint)
            self.showWhat = "Attacking"
            self.dummyText = "Attack"
            if damaged <= 0:
                damaged = 0
            attack = mixer.Sound(r'sound effect\Dragon\attack.mp3')
            attack.set_volume(global_sound)
            attack.play()
        #count for defend buff duration
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

    #Show fireball effect
    #Arguments
    # win - window screen
    # currentTime - The time the program is running   
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

    #Set of werewolf phase 1 behavior and skill
    #This form is knight form before becomming werewolf
    #Return damage to display damaged done on screen
    #Argument
    #enemy - player character  
    def attackWerewolf1(self,enemy):
        global Defi

        rand = random.randint(1,10)
        damaged = 0
        #skill "Double slash" with chance 30%
        #Deal damage to the player with 2 times attack power
        if rand < 4:
            damaged = 2*self.damageCal(self.currentAtkPoint,enemy.currentDefendPoint)
            double_slash = mixer.Sound(r'sound effect\Werewolf\double slash1.mp3')
            double_slash.set_volume(global_sound)
            double_slash.play()
            self.showWhat = "usingSkill"
            self.dummyText = "Double slash"
            print("enemy double slash")
            if damaged <= 0:
                damaged = 0
        #skill "Iron skin" with chance 20%
        #Increase self defend point for 3 turn
        elif 3 < rand < 6:
            iron_skin = mixer.Sound(r'sound effect\Werewolf\iron skin.mp3')
            iron_skin.set_volume(global_sound)
            iron_skin.play()
            self.showWhat = "usingSkill"
            self.dummyText = "Iron skin"
            print("Iron skin")
            self.defendBuff = True
            Defi = 0
            self.currentDefPoint = self.defendPoint + 10
        #Normal damage with chance 50%
        #Deal damage to the player
        else:
            self.showWhat = "Attacking"
            self.dummyText = "Attack"
            attack = mixer.Sound(r'sound effect\Werewolf\attack1.mp3')
            attack.set_volume(global_sound)
            attack.play()
            damaged = self.damageCal(self.currentAtkPoint,enemy.currentDefendPoint)
            if damaged <= 0:
                damaged = 0
        #count for defend buff duration
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

     #Set of werewolf phase 2 behavior and skill
     #This form is Werewolf form after knight'form defeated
     #Return damage to display damaged done on screen
     #Argument
     #enemy - player character 
    def attackWerewolf2(self,enemy):
        global atki

        rand = random.randint(1,10)
        damaged = 0
        #skill "Double slash" with chance 30%
        #Deal damage to the player with 2 times attack power
        if rand < 4:
            damaged = 2*self.damageCal(self.currentAtkPoint,enemy.currentDefendPoint)
            double_slash = mixer.Sound(r'sound effect\Werewolf\double slash2.mp3')
            double_slash.set_volume(global_sound)
            double_slash.play()
            self.showWhat = "usingSkill"
            self.dummyText = "Double slash"
            print("enemy double slash")
            if damaged <= 0:
                damaged = 0
        #skill "Hell hound" with chance 20%
        #Increase self attack point for 3 turn
        elif 3 < rand < 6:
            print("Hell hound")
            self.showWhat = "usingSkill"
            self.dummyText = "Hell hound"
            hell_hound = mixer.Sound(r'sound effect\Werewolf\tansfrom.mp3')
            hell_hound.set_volume(global_sound)
            hell_hound.play()
            self.attackBuff = True
            atki = 0
            self.currentAtkPoint = self.attackPoint + 20
        #Normal attack with chance 50%
        #Deal damage to the player
        else:
            self.showWhat = "Attacking"
            self.dummyText = "Attack"
            attack = mixer.Sound(r'sound effect\Werewolf\attack2.mp3')
            attack.set_volume(global_sound)
            attack.play()
            damaged = self.damageCal(self.currentAtkPoint,enemy.currentDefendPoint)
            if damaged <= 0:
                damaged = 0
        #count for attack buff duration
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

    #Set of witch behavior and skill
    #Return damage to display damaged done on screen
    #Argument
    #enemy - player character  
    def attackWitch(self,enemy):
        rand = random.randint(1,100)
        damaged = 0
        #skill "Death phantom" with chance 10%
        #This unit will enter casting mode
        #after casting done the player instantly death
        if rand < 11:
            casting = mixer.Sound(r'sound effect\Witch\casting.mp3')
            casting.set_volume(global_sound)
            casting.play()
            self.showWhat = "usingSkill"
            self.dummyText = "Death phantom"
            print("Death phantom")
            self.action = "casting"
        #skill "Demon bane" with chance 30%
        #Deal damage to the player with ignore player's defend point
        elif 10 < rand < 41:
            demon_bane = mixer.Sound(r'sound effect\Witch\attack.mp3')
            demon_bane.set_volume(global_sound)
            demon_bane.play()
            self.showWhat = "usingSkill"
            self.dummyText = "Demon bane"
            print("Demon bane")
            damaged = self.currentAtkPoint
            if damaged <= 0 :
                damaged = 0
        #skill "Demon bane" with chance 20%
        #Deal damage to the player and drain Hp and Mp according to the self attack
        elif 40 < rand < 61:
            draining = mixer.Sound(r'sound effect\Witch\drain mana.mp3')
            draining.set_volume(global_sound)
            draining.play()
            self.showWhat = "usingSkill"
            self.dummyText = "Draining"
            print("Draining")
            damaged = self.damageCal(self.currentAtkPoint,enemy.currentDefendPoint)
            if damaged < 0:
                damaged = 0
            enemy.currentMp = enemy.currentMp - math.floor(damaged*0.2)
            if enemy.currentMp < 0:
                enemy.currentMp = 0
            self.currentHp = self.currentHp + math.floor(damaged*1)
            if self.currentHp > self.maxHp:
                self.currenHp = self.maxHp
        #Normal attack with chance 40%
        #Deal damage to the player
        else:
            self.showWhat = "Attacking"
            self.dummyText = "Attack"
            attack = mixer.Sound(r'sound effect\Witch\attack.mp3')
            attack.set_volume(global_sound)
            attack.play()
            damaged = self.damageCal(self.currentAtkPoint,enemy.currentDefendPoint)
            if damaged <= 0:
                damaged = 0

        enemy.currentHp = enemy.currentHp - damaged
        if enemy.currentHp <= 0 :
            enemy.currentHp = 0
            enemy.death = True
        return damaged, "monster"

    #Casting
    #skill action for casting skill
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

    #Set of boss phase 1 behavior and skill
    #Return damage to display damaged done on screen
    #Argument
    #enemy - player character
    def attackBoss1(self,enemy):
        rand = random.randint(1,100)
        damaged = 0
        global Defi
        #skill "True slash" with chance 20%
        #Deal damage to the player with ignore player's defendpoint
        if rand < 21:
            true_slash = mixer.Sound(r'sound effect\Dark knight P1\true slash.mp3')
            true_slash.set_volume(global_sound)
            true_slash.play()
            self.showWhat = "usingSkill"
            self.dummyText = "True slash"
            print("True slash")
            damaged = self.currentAtkPoint
            if damaged <= 0:
                damaged = 0
        #skill "Iron skin" with chance 20%
        #Increase self defend point for 4 turn
        elif 20 < rand < 41:
            dimond_skin = mixer.Sound(r'sound effect\Dark knight P1\dimond skin.mp3')
            dimond_skin.set_volume(global_sound)
            dimond_skin.play()
            self.showWhat = "usingSkill"
            self.dummyText = "Dimond skin"
            print("Dimond skin")
            self.defendBuff = True
            Defi = 0
            self.currentDefPoint = self.defendPoint + 20
        #skill "Triple slash" with chance 25%
        #Deal damage to the player with 3 times attack power
        elif 40 < rand < 66:
            triple_slash = mixer.Sound(r'sound effect\Dark knight P1\triple slash.mp3')
            triple_slash.set_volume(global_sound)
            triple_slash.play()
            self.showWhat = "usingSkill"
            self.dummyText = "Triple slash"
            print("Triple slash")
            damaged = self.damageCal(self.currentAtkPoint,enemy.currentDefendPoint)*3
            if damaged <= 0:
                damaged = 0
        #Normal attack with chance 35%
        #Deal damage to the player
        else:
            self.showWhat = "usingSkill"
            self.dummyText = "Dark slash"
            dark_slash = mixer.Sound(r'sound effect\Dark knight P1\dark slash.mp3')
            dark_slash.set_volume(global_sound)
            dark_slash.play()
            print("Dark slash")
            damaged = self.damageCal(self.currentAtkPoint,enemy.currentDefendPoint)
            if damaged <= 0:
                damaged = 0

        #count for defend buff duration
        if self.defendBuff == True:
            Defi = Defi + 1
            if Defi >= 4:
                self.defendBuff = False
                self.currentDefPoint = self.defendPoint

        if damaged < 0:
            damaged = 0
        enemy.currentHp = enemy.currentHp - damaged
        if damaged > 0:
            self.currentHp = self.currentHp + math.floor(damaged*0.25)
            if self.currentHp > self.maxHp:
                self.currentHp = self.maxHp
            print("Drain Health")
        if enemy.currentHp <= 0 :
            enemy.currentHp = 0
            enemy.death = True
        return damaged, "monster"

    #Set of boss phase 2 behavior and skill
    #Another form for the final boss
    #Return damage to display damaged done on screen
    #Argument
    #enemy - player character
    def attackBoss2(self,enemy):
        rand = random.randint(1,100)
        damaged = 0
        global Defi
        #skill "Death phantom" with chance 15%
        #This unit will enter casting mode
        #after casting done the player instantly death
        if rand < 16:
            death_phantom = mixer.Sound(r'sound effect\Witch\attack.mp3')
            death_phantom.set_volume(global_sound)
            death_phantom.play()
            self.showWhat = "usingSkill"
            self.dummyText = "Death phantom"
            print("Death phantom")
            self.action = "casting"
        #skill "True Slash" with chance 15%
        #Deal damage to the player with 1.5 times attack power with ignore player's defend point
        elif 15 < rand < 31:
            true_slash = mixer.Sound(r'sound effect\Dark knight P2\true slash.mp3')
            true_slash.set_volume(global_sound)
            true_slash.play()
            self.showWhat = "usingSkill"
            self.dummyText = "True slash"
            print("True slash")
            damaged = self.currentAtkPoint*1.5
            if damaged <= 0:
                damaged = 0
        #skill "Iron skin" with chance 15%
        #Increase self defend point for 3 turn
        elif 30 < rand < 46:
            dimond_skin = mixer.Sound(r'sound effect\Dark knight P2\dimond skin.mp3')
            dimond_skin.set_volume(global_sound)
            dimond_skin.play()
            self.showWhat = "usingSkill"
            self.dummyText = "Dimond skin"
            print("Dimond skin")
            self.defendBuff = True
            Defi = 0
            self.currentDefPoint = self.defendPoint + 30
        #skill "Triple slash" with chance 15%
        #Deal damage to the player with 3 times attack power
        elif 45 < rand < 61:
            triple_slash = mixer.Sound(r'sound effect\Dark knight P2\triple slash.mp3')
            triple_slash.set_volume(global_sound)
            triple_slash.play()
            self.showWhat = "usingSkill"
            self.dummyText = "Triple slash"
            print("Triple slash")
            damaged = self.damageCal(self.currentAtkPoint,enemy.currentDefendPoint)*3
            if damaged < 0:
                damaged = 0
        #skill "Phantom bane" with chance 40%
        #Deal damage to the player and drain Hp and Mp according to the self attack
        else:
            self.showWhat = "usingSkill"
            self.dummyText = "Phantom bane"
            print("Phantom bane")
            print("Draining Mana")
            drain_mana = mixer.Sound(r'sound effect\Dark knight P2\dark ball.mp3')
            drain_mana.set_volume(global_sound)
            drain_mana.play()
            damaged = self.damageCal(self.currentAtkPoint,enemy.currentDefendPoint) 
            if damaged < 0:
                damaged = 0
            enemy.currentMp = enemy.currentMp - math.floor(damaged*0.2)
            if enemy.currentMp < 0:
                enemy.currentMp = 0
        #count for defend buff duration
        if self.defendBuff == True:
            Defi = Defi + 1
            if Defi >= 4:
                self.defendBuff = False
                self.currentDefPoint = self.defendPoint

        if damaged < 0:
            damaged = 0
        enemy.currentHp = enemy.currentHp - damaged
        #Passive for boss
        #Healing itself after done damage
        if damaged > 0:
            self.currentHp = self.currentHp + math.floor(damaged*0.4)
            if self.currentHp > self.maxHp:
                self.currentHp = self.maxHp
            print("Drain Health")
        if enemy.currentHp <= 0 :
            enemy.currentHp = 0
            enemy.death = True
        return damaged, "monster"

    #Casting
    #skill action for casting skill
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

    # Display enemy health
    #Arguments
    # WIN - window screen
    def showHealth(self, WIN):
        currentHP  = str(self.currentHp)
        my_font = pygame.font.SysFont("candara",40)

        #render text
        text_surface1 = my_font.render("HP : ", False, (255,255,255))
        WIN.blit(text_surface1, (780, 200))
        text_surface2 = my_font.render(currentHP, False, (255,255,255))
        WIN.blit(text_surface2, (880, 200))

    #Check the enemy is already dead or not
    def isDead(self):
        gameStage = "Win"
        global counter
        #zombie wii resurrect itself for 3 time
        if self.currentHp <= 0 and self.name == "zombie":
            if self.revi < 3:
                self.showWhat = "usingSkill"
                self.dummyText = "Revived"
                regen = mixer.Sound(r'sound effect\Zombie\revive.mp3')
                regen.set_volume(global_sound)
                regen.play()
                self.currentHp = self.maxHp*(0.25*(3 - self.revi))
                gameStage = "Normal"
                self.death = False
                self.revi = self.revi + 1
            else:
                self.death = True
            return gameStage
        #When the werewolf phase 1 or knight die, Transform it to the werewolf(phase2)
        elif self.currentHp <= 0 and self.name == "werewolf1":
            self.showWhat = "usingSkill"
            self.dummyText = "Transform"
            print("knight become werewolf")
            gameStage = "Next"
            self.death = False
        #When the final boss phase 1, Transform it to the final boss phase 2
        elif self.currentHp <= 0 and self.name == "boss1":
            self.showWhat = "usingSkill"
            self.dummyText = "Bankai!!"
            print("The ture finale boss come")
            gameStage = "Next"
            self.death = False
        #When the final boss phase 2 die, change gamestate to win
        elif self.currentHp <= 0 and self.name == "boss2":
            print("victory")
            gameStage = "victory"
            self.death = True
        #Check Hp for current enemy, If <=0 the enemy confirm death
        elif self.currentHp <= 0:
            self.currentHp = 0
            self.death = True

        return gameStage

    # Display enemy status (Stun,cast) on the right top
    #Arguments
    # WIN - window screen
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




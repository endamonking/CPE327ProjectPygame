# This code use to create Player Object
# The player can Use normal attack or skill to deal DMG to target. Also Player have passive that will auto activated skill 
#
from array import array
import imp
from pickle import FALSE
import pygame
import os
import button
import math


# Background music
from pygame import mixer
pygame.mixer.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)

# load asset
BLACK = (0, 0, 0)
player_image = pygame.image.load(os.path.join('Asset', 'knight.png'))
player_image = pygame.transform.scale(player_image, (300, 300))
button_image = pygame.image.load(os.path.join('Asset', 'prBTN.png'))
blackScreen = pygame.transform.scale(pygame.image.load(
    os.path.join('Asset', 'blackScreen.jpg')), (300, 75))
attackEF = pygame.transform.scale(pygame.image.load(
    os.path.join('Asset', 'Effect', 'Pattack.png')), (700, 300))
fireBallEF = pygame.transform.scale(pygame.image.load(
    os.path.join('Asset', 'Effect', 'fireBall.png')), (1800, 300))

animation_cooldown = 500
efxCounter = 1

global_sound = 0.3

#Player Class
class player():
    #Use to create Player object
    #Arguments
    # maxHp - The maximum HP of Player 
    # maxMp - The maximum MP of Player
    # defendPoint - The starter defend point of Player
    # attackPoint - The starter attackt point of Player  
    def __init__(self, maxHp, maxMp, defendPoint, attackPoint):
        self.maxHp = maxHp
        self.maxMp = maxMp
        self.currentHp = self.maxHp # Current Hp of player. Start at max hp
        self.currentMp = self.maxMp # Current Mp of player. Start at max mp
        self.defendPoint = defendPoint
        self.attackPoint = attackPoint
        self.currentAttackPoint = self.attackPoint # Current ATK of player. Start at ATKpoint
        self.currentDefendPoint = self.defendPoint # Cureent DEF of player. Start at DEFpoint
        self.turnLeft = 0 # Counter of buff skill
        self.buffOrNot = False #Use to check player is Buffed or not
        self.lastUpdate = pygame.time.get_ticks() #To get the Time of player active 
        self.EfxLastUpdate = pygame.time.get_ticks() + 1 #To get the Time of Player effect
        self.i = 0  #Counter of idle animation
        self.efxI = 0 # Counter of effect animation
        self.turn = False # Check the player turn
        self.death = False # Check The player is dead yet
        self.action = "idle" # The current action of player
        self.skillList = [] # The skills that player has
        self.showWhat = "nothing" # Use to be dummy to display to screen
        self.buff = "none"
<<<<<<< HEAD
        self.passiveName = "No"
        self.passiveLevel = 0
        self.passiveCounter = 0
        #player sound effect
        self.player_attack = mixer.Sound(r'sound effect\Knight\normal attack.mp3')
        self.player_attack.set_volume(0.02)
        self.player_double_slash = mixer.Sound(r'sound effect\Knight\double slash.mp3')
        self.player_double_slash.set_volume(0.02)
        self.player_headbutt = mixer.Sound(r'sound effect\Knight\headbutt.mp3')
        self.player_headbutt.set_volume(0.02)
        self.player_paralyze = mixer.Sound(r'sound effect\Knight\paralyze.mp3')
        self.player_paralyze.set_volume(0.06)
        self.player_heal = mixer.Sound(r'sound effect\Knight\healing.mp3')
        self.player_heal.set_volume(0.02)
        self.player_restore_mana = mixer.Sound(r'sound effect\Knight\restore mana.mp3')
        self.player_restore_mana.set_volume(0.02)
        self.player_roar = mixer.Sound(r'sound effect\Knight\roaring.mp3')
        self.player_roar.set_volume(0.02)
        self.player_fire_ball = mixer.Sound(r'sound effect\Knight\fire ball.mp3')
        self.player_fire_ball.set_volume(0.04)
        self.player_lighting = mixer.Sound(r'sound effect\Knight\lighting.mp3')
        self.player_lighting.set_volume(0.03)
=======
        self.passiveName = "No" # The name of passive that player has
        self.passiveLevel = 0 # The passive level of player 
        self.passiveCounter = 0 # The counter of passive so it cannot do multiple time per action
>>>>>>> a2665691d9dc73dc4cf3b8eb074ab6a21f8923b0

    # give player current ATK point
    # Return - current ATK point
    def getAttackPower(self):
        return self.currentAttackPoint
    # give player turn status
    # retun - player's turn
    def getTurn(self):
        return self.turn

    #Show status of player such as No mana or show effect
    #Arguments
    # win - window screen
    # currentTime - The time the program is running
    def showMenu(self, win, currentTime):

        if self.showWhat == "noMana":
            blackScreen.set_alpha(128)
            win.blit(blackScreen, (400, 170))

            text = "Not enough mana"
            my_font = pygame.font.SysFont("candara", 36)
            text_surface = my_font.render(text, False, (255, 255, 255))
            win.blit(text_surface, (410, 180))
        elif self.showWhat == "Attacking":
            self.displayAttackEffect(win, currentTime)
        elif self.showWhat == "fireBall":
            self.displayFireBallEffect(win,currentTime)

    #Display player's idle animation on screen
    #Arguments
    # WIN - window screen
    # currentTime - The time the program is running
    # Xpose - Display position of player in X axis
    # Ypose - Display position of player in Y axis
    def draw_playerIdle(self, WIN, currentTime, Xpose, Ypose):
        if (currentTime - self.lastUpdate >= animation_cooldown):
            self.lastUpdate = currentTime
            if self.i < 2:
                self.i = self.i+1
            else:
                self.i = 0
        # width come from total width / total frame
        WIN.blit(player_image, (Xpose, Ypose), ((self.i * 100), 0, 100, 300))

    #Upgrade power of player
    # Arguments
    # option - Which option that player want to upgrade 
    def upgrade_stat(self, option):
        match option:
            case 0:  # increase maximum HP and MP and heal player
                self.maxHp = self.maxHp + 50
                self.maxMp = self.maxMp + 25

                self.currentHp = self.currentHp + (self.maxHp / 2)
                if self.currentHp >= self.maxHp:
                    self.currentHp = self.maxHp

                self.currentMp = self.currentMp + (self.maxMp / 2)
                if self.currentMp >= self.maxMp:
                    self.currentMp = self.maxMp

            case 1:  # increase attack power of player and slightly defend point
                self.attackPoint = self.attackPoint + 10
                self.currentAttackPoint = self.attackPoint
                self.defendPoint = self.defendPoint + 2
                self.currentDefendPoint = self.defendPoint

            case 2:  # increase defend pointof player and slightly maxmimum HP
                self.defendPoint = self.defendPoint + 10
                self.currentDefendPoint = self.defendPoint
                self.maxHp = self.maxHp + 20

    #Active the passive's ability
    #Arguments
    # action - Which category of passive that want to activated
    def passiveActivated(self, action):
        print(self.passiveLevel)
        if action == "Attack":
            match self.passiveName:
                case "Zeus blessing":  # while attacking HP
                    self.currentHp = self.currentHp + \
                        (self.currentAttackPoint * self.passiveLevel)
                    if self.currentHp >= self.maxHp:
                        self.currentHp = self.maxHp
                case "Poseidon grace":
                    self.currentMp = self.currentMp + \
                        (self.currentAttackPoint * self.passiveLevel)
                    if self.currentMp >= self.maxMp:
                        self.currentMp = self.maxMp
                case _:
                    pass
        elif action == "turn":
            match self.passiveName:
                case "Divine will":  # afterTurn
                    self.currentHp = self.currentHp + \
                        (self.maxHp * self.passiveLevel)*0.5
                    if self.currentHp >= self.maxHp:
                        self.currentHp = self.maxHp
                case "Odin absolution":
                    self.currentMp = self.currentMp + \
                        (self.maxMp * self.passiveLevel)*0.5
                    if self.currentMp >= self.maxMp:
                        self.currentMp = self.maxMp
                case _:
                    pass
    
    #Display the normal attack effect
    #Argument
    # WIN - window screen
    # currentTime - The time the program is running
    def displayAttackEffect(self, WIN, currentTime):

        if (currentTime - self.EfxLastUpdate >= 30):
            self.EfxLastUpdate = currentTime
            if self.efxI < 13:
                self.efxI = self.efxI+1
            else:
                self.showWhat = "nothing"
                self.efxI = 0
                return
        # width come from total width / total frame
        WIN.blit(attackEF, (810, 330), ((self.efxI * 50), 0, 50, 300))

    #Display the fire ball effect 
    #Arguments
    # WIN - window screen
    # currentTime - The time the program of running
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
        WIN.blit(fireBallEF, (150 + (self.efxI * 50), 330), ((self.efxI * 100), 0, 100, 300))

    #Deal normal DMG to ememy HP 
    #ARguments
    # enemy - Target of normal attack (Monster object)
    # Return 
    # damaged - The number of damage that player deal to target
    # "player" - Who made the damage (In here it's player)
    def attack(self, enemy):
        damaged = math.floor(10*self.currentAttackPoint/(enemy.currentDefPoint+1))
<<<<<<< HEAD
        self.player_attack.play()
=======
        attack_sound = mixer.Sound(r'sound effect\Knight\normal attack.mp3')
        attack_sound.set_volume(global_sound)
        attack_sound.play()
>>>>>>> a2665691d9dc73dc4cf3b8eb074ab6a21f8923b0
        self.showWhat = "Attacking"

        enemy.currentHp = enemy.currentHp - damaged
        if enemy.currentHp < 0:
            enemy.currentHp = 0
            enemy.death = True

        self.checkDuration()
        self.passiveActivated("Attack")
        return damaged, "player"

    #Add a skill to skill list of player
    # Arguments
    # skillName - Skill name that gonna added (string) 
    def getSkill(self, skillName):
        self.skillList.append(skillName)

    #Display skill button so player can click to choose action
    #Arguments
    # mp - The position of player mouse 
    # WIN - window screen
    # BLACK - Colour of text in button
    # enemy - Target of skill (Monster object)
    # return
    # action_cooldown - The cooldown number of Player action
    # dmg - The number of Damage that deal to enemy
    # side - Who deal damage (Player)
    def showSkill(self, mp,  WIN, BLACK, enemy):
        skillbuttonlist = []
        i = 0
        xButPose = 400
        yButPose = 600
        yNew = 0
        self.action = "usingSkill"
        action_cooldown = 0
        dmg = 0
        side = "player"

        # created back button
        backButton = button.button(xButPose, yButPose + yNew, button_image, 6)
        if backButton.draw(mp, WIN, BLACK, "Cancel", 28, 90, 37):
            self.action = "idle"
            action_cooldown = 90

        yNew = yNew - 100
        for x in self.skillList:
            skillbuttonlist.append(button.button(
                xButPose, yButPose + yNew, button_image, 6))
            yNew = yNew - 100

        for index, x in enumerate(skillbuttonlist):
            if x.draw(mp, WIN, BLACK, self.skillList[index], 28, 60, 37):
                action_cooldown = 0
                self.action = "idle"
                dmg, side = self.useSkill(self.skillList[index], enemy, WIN)

        return action_cooldown, dmg, side

    #Use the ability of active skill (The ability of skill depend on what player chooose to use)
    #Arguments
    # skillname - Name of skill that player want to use
    # enemy - Target of skill (Monster object)
    # win - window screen
    #Return
    # DMG - damage that deal to target
    # "player" - Side of who deal damage in here is Player
    def useSkill(self, skillName, enemy, win):
        dmg = 0
        match skillName:
            case "Double Slash": # deal *2 damage
                if self.currentMp >= 20:
                    #dmg = (self.currentAttackPoint * 2) - enemy.currentDefPoint 
                    dmg = math.floor((10*self.currentAttackPoint)*2/(enemy.currentDefPoint+1))
                    if dmg <= 0:
                        dmg = 0
<<<<<<< HEAD
                    self.player_double_slash.play()
=======
                    double_slash = mixer.Sound(
                        r'sound effect\Knight\double slash.mp3')
                    double_slash.set_volume(global_sound)
                    double_slash.play()
>>>>>>> a2665691d9dc73dc4cf3b8eb074ab6a21f8923b0

                    enemy.currentHp = enemy.currentHp - dmg
                    self.currentMp = self.currentMp - 20
                    self.turn = False
                    enemy.turn = True
                    self.checkDuration()
                    self.showWhat = "Attacking"
                    self.passiveCounter = 0
                else:
                    self.showWhat = "noMana"
                return dmg, "player"
            case "Headbutt": # Stunned enemy and deal 1x damage
                if self.currentMp >= 15:
                    dmg = math.floor(10*self.currentAttackPoint/(enemy.currentDefPoint+1))
                    if dmg <= 0:
                        dmg = 0
<<<<<<< HEAD
                    self.player_headbutt.play()
=======
                    headbutt = mixer.Sound(r'sound effect\Knight\headbutt.mp3')
                    headbutt.set_volume(global_sound)
                    headbutt.play()
>>>>>>> a2665691d9dc73dc4cf3b8eb074ab6a21f8923b0

                    enemy.action = "stunned"
                    enemy.currentHp = enemy.currentHp - dmg
                    self.currentMp = self.currentMp - 35
                    self.turn = False
                    enemy.turn = True
                    self.passiveCounter = 0
                    self.showWhat = "Attacking"
                    self.checkDuration()
                else:
                    self.showWhat = "noMana"
                return dmg, "player"
            case "Paralyze": # Stuned the enemy and deal 0.5x of damage
                if self.currentMp >= 5:
                    dmg = math.floor((10*self.currentAttackPoint)*0.5/(enemy.currentDefPoint+1))
                    if dmg <= 0:
                        dmg = 0
<<<<<<< HEAD
                    self.player_paralyze.play()

=======
                    paralyze = mixer.Sound(r'sound effect\Knight\paralyze.mp3')
                    paralyze.set_volume(global_sound)
                    paralyze.play()
>>>>>>> a2665691d9dc73dc4cf3b8eb074ab6a21f8923b0

                    enemy.action = "stunned"
                    self.currentMp = self.currentMp - 5
                    self.turn = False
                    enemy.turn = True
                    self.passiveCounter = 0
                    self.checkDuration()
                else:
                    self.showWhat = "noMana"
                return dmg, "player"
            case "Heal": # Heal player HP, 5x of base ATK point
                if self.currentMp >= 25:
                    heal = self.attackPoint * 5
                    self.currentHp = self.currentHp + heal
                    if self.currentHp >= self.maxHp:
                        self.currentHp = self.maxHp
<<<<<<< HEAD
                    self.player_heal.play()
=======
                    heal = mixer.Sound(r'sound effect\Knight\healing.mp3')
                    heal.set_volume(global_sound)
                    heal.play()
>>>>>>> a2665691d9dc73dc4cf3b8eb074ab6a21f8923b0
                    self.currentMp = self.currentMp - 25
                    self.turn = False
                    enemy.turn = True
                    self.passiveCounter = 0
                    self.checkDuration()
                else:
                    self.showWhat = "noMana"
                return 0, "player"
            case "Restore mana": # Restore the player MP , 3x of base ATK point
                reMana = self.attackPoint * 3
                self.currentMp = self.currentMp + reMana
                if self.currentMp >= self.maxMp:
                    self.currentMp = self.maxMp
<<<<<<< HEAD
                self.player_restore_mana.play()
=======
                restore_mana = mixer.Sound(
                    r'sound effect\Knight\restore mana.mp3')
                restore_mana.set_volume(global_sound)
                restore_mana.play()
>>>>>>> a2665691d9dc73dc4cf3b8eb074ab6a21f8923b0
                self.turn = False
                enemy.turn = True
                self.passiveCounter = 0
                self.checkDuration()
                return 0, "player"
            case "Roaring": # Buff the ATK and DEF of player 0.5x of base
                if self.currentMp >= 30:
                    self.turnLeft = 0
                    self.buffOrNot = True

                    self.currentAttackPoint = self.attackPoint + \
                        (self.attackPoint/2)
                    self.currentDefendPoint = self.defendPoint + \
                        (self.defendPoint/2)

<<<<<<< HEAD
                    self.player_roar.play()
=======
                    roar = mixer.Sound(r'sound effect\Knight\roaring.mp3')
                    roar.set_volume(global_sound)
                    roar.play()
>>>>>>> a2665691d9dc73dc4cf3b8eb074ab6a21f8923b0
                    self.currentMp = self.currentMp - 30
                    self.turn = False
                    enemy.turn = True
                    self.passiveCounter = 0
                return 0, "player"
            case "Fire ball": # Deal 3x damage 
                if self.currentMp >= 35:
                    dmg = math.floor((10*self.currentAttackPoint)*3/(enemy.currentDefPoint+1))
                    if dmg <= 0:
                        dmg = 0

<<<<<<< HEAD
                    self.player_fire_ball.play()
=======
                    fire_ball = mixer.Sound(
                        r'sound effect\Knight\fire ball.mp3')
                    fire_ball.set_volume(global_sound)
                    fire_ball.play()
>>>>>>> a2665691d9dc73dc4cf3b8eb074ab6a21f8923b0
                    enemy.currentHp = enemy.currentHp - dmg
                    self.currentMp = self.currentMp - 35
                    self.turn = False
                    enemy.turn = True
                    self.passiveCounter = 0
                    self.showWhat = "fireBall"
                    self.checkDuration()
                else:
                    self.showWhat = "noMana"
                return dmg, "player"
            case "Lighting bolt": # deal 2x damage also ignore enemy def
                if (self.currentMp >= 35):
                    dmg = math.floor(self.currentAttackPoint*2)
                    if dmg <= 0:
                        dmg = 0
<<<<<<< HEAD
                    self.player_lighting.play()
=======
                    lighting = mixer.Sound(r'sound effect\Knight\lighting.mp3')
                    lighting.set_volume(global_sound)
                    lighting.play()
>>>>>>> a2665691d9dc73dc4cf3b8eb074ab6a21f8923b0
                    enemy.currentHp = enemy.currentHp - dmg
                    self.currentMp = self.currentMp - 25
                    self.turn = False
                    enemy.turn = True
                    self.passiveCounter = 0
                    self.showWhat = "fireBall"
                    self.checkDuration()
                else:
                    self.showWhat = "noMana"
                return dmg, "player"

    # Display player health and MP
    #Arguments
    # WIN - window screen
    def showHealth(self, WIN):
        currentHP = str(self.currentHp)
        currentMP = str(self.currentMp)
        my_font = pygame.font.SysFont("candara", 40)

        # render text
        text_surface1 = my_font.render("HP : ", False, (255, 255, 255))
        WIN.blit(text_surface1, (100, 200))
        text_surface2 = my_font.render(currentHP, False, (255, 255, 255))
        WIN.blit(text_surface2, (200, 200))

        text_surface3 = my_font.render("MP : ", False, (255, 255, 255))
        WIN.blit(text_surface3, (100, 250))
        text_surface4 = my_font.render(currentMP, False, (255, 255, 255))
        WIN.blit(text_surface4, (200, 250))

    #Handle the duration of buff skill also deactivated when duration is run off 
    def checkDuration(self):
        if self.buffOrNot == True:
            if self.turnLeft >= 2:
                self.currentAttackPoint = self.attackPoint
                self.currentDefendPoint = self.defendPoint
                self.buffOrNot = False
            else:
                self.turnLeft = self.turnLeft + 1

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


class player():
    def __init__(self, maxHp, maxMp, defendPoint, attackPoint):
        self.maxHp = maxHp
        self.maxMp = maxMp
        self.currentHp = self.maxHp
        self.currentMp = self.maxMp
        self.defendPoint = defendPoint
        self.attackPoint = attackPoint
        self.currentAttackPoint = self.attackPoint
        self.currentDefendPoint = self.defendPoint
        self.turnLeft = 0
        self.buffOrNot = False
        self.lastUpdate = pygame.time.get_ticks()
        self.EfxLastUpdate = pygame.time.get_ticks() + 1
        self.i = 0
        self.efxI = 0
        self.turn = False
        self.death = False
        self.action = "idle"
        self.skillList = []
        self.showWhat = "nothing"
        self.buff = "none"
        self.passiveName = "No"
        self.passiveLevel = 0
        self.passiveCounter = 0

    def getAttackPower(self):
        return self.currentAttackPoint

    def getTurn(self):
        return self.turn

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

    def draw_playerIdle(self, WIN, currentTime, Xpose, Ypose):
        if (currentTime - self.lastUpdate >= animation_cooldown):
            self.lastUpdate = currentTime
            if self.i < 2:
                self.i = self.i+1
            else:
                self.i = 0
        # width come from total width / total frame
        WIN.blit(player_image, (Xpose, Ypose), ((self.i * 100), 0, 100, 300))

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
                self.currentAttackPoint = self.currentAttackPoint + 10
                self.defendPoint = self.defendPoint + 5

            case 2:  # increase defend pointof player and slightly maxmimum HP
                self.defendPoint = self.defendPoint + 10
                self.maxHp = self.maxHp + 20

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

    def attack(self, enemy):
        damaged = math.floor(10*self.currentAttackPoint/(enemy.currentDefPoint+1))
        attack_sound = mixer.Sound(r'sound effect\Knight\normal attack.mp3')
        attack_sound.set_volume(0.5)
        attack_sound.play()
        self.showWhat = "Attacking"

        enemy.currentHp = enemy.currentHp - damaged
        if enemy.currentHp < 0:
            enemy.currentHp = 0
            enemy.death = True

        self.checkDuration()
        self.passiveActivated("Attack")
        return damaged, "player"

    def getSkill(self, skillName):
        self.skillList.append(skillName)

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

    def useSkill(self, skillName, enemy, win):
        dmg = 0
        match skillName:
            case "Double Slash":
                if self.currentMp >= 20:
                    dmg = (self.currentAttackPoint * 2) - enemy.currentDefPoint
                    if dmg <= 0:
                        dmg = 0
                    double_slash = mixer.Sound(
                        r'sound effect\Knight\double slash.mp3')
                    double_slash.set_volume(0.5)
                    double_slash.play()

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
            case "Headbutt":
                if self.currentMp >= 15:
                    dmg = self.currentAttackPoint - enemy.currentDefPoint
                    if dmg <= 0:
                        dmg = 0
                    headbutt = mixer.Sound(r'sound effect\Knight\headbutt.mp3')
                    headbutt.set_volume(0.5)
                    headbutt.play()

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
            case "Paralyze":
                if self.currentMp >= 5:
                    dmg = (self.currentAttackPoint * 0.5) - \
                        enemy.currentDefPoint
                    if dmg <= 0:
                        dmg = 0
                    paralyze = mixer.Sound(r'sound effect\Knight\paralyze.mp3')
                    paralyze.set_volume(0.5)
                    paralyze.play()

                    enemy.action = "stunned"
                    self.currentMp = self.currentMp - 5
                    self.turn = False
                    enemy.turn = True
                    self.passiveCounter = 0
                    self.checkDuration()
                else:
                    self.showWhat = "noMana"
                return dmg, "player"
            case "Heal":
                if self.currentMp >= 25:
                    heal = self.attackPoint * 1.5
                    self.currentHp = self.currentHp + heal
                    if self.currentHp >= self.maxHp:
                        self.currentHp = self.maxHp
                    heal = mixer.Sound(r'sound effect\Knight\healing.mp3')
                    heal.set_volume(0.5)
                    heal.play()
                    self.currentMp = self.currentMp - 25
                    self.turn = False
                    enemy.turn = True
                    self.passiveCounter = 0
                    self.checkDuration()
                else:
                    self.showWhat = "noMana"
                return 0, "player"
            case "Restore mana":
                reMana = self.attackPoint * 1.1
                self.currentMp = self.currentMp + reMana
                if self.currentMp >= self.maxMp:
                    self.currentMp = self.maxMp
                restore_mana = mixer.Sound(
                    r'sound effect\Knight\restore mana.mp3')
                restore_mana.set_volume(0.5)
                restore_mana.play()
                self.turn = False
                enemy.turn = True
                self.passiveCounter = 0
                self.checkDuration()
                return 0, "player"
            case "Roaring":
                if self.currentMp >= 30:
                    self.turnLeft = 0
                    self.buffOrNot = True

                    self.currentAttackPoint = self.attackPoint + \
                        (self.attackPoint/2)
                    self.currentDefendPoint = self.defendPoint + \
                        (self.defendPoint/2)

                    roar = mixer.Sound(r'sound effect\Knight\roaring.mp3')
                    roar.set_volume(0.5)
                    roar.play()
                    self.currentMp = self.currentMp - 30
                    self.turn = False
                    enemy.turn = True
                    self.passiveCounter = 0
                return 0, "player"
            case "Fire ball":
                if self.currentMp >= 35:
                    dmg = (self.currentAttackPoint * 3) - enemy.currentDefPoint
                    if dmg <= 0:
                        dmg = 0

                    fire_ball = mixer.Sound(
                        r'sound effect\Knight\fire ball.mp3')
                    fire_ball.set_volume(0.5)
                    fire_ball.play()
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
            case "Lighting bolt":
                if (self.currentMp >= 25):
                    dmg = (self.currentAttackPoint * 2)
                    if dmg <= 0:
                        dmg = 0
                    lighting = mixer.Sound(r'sound effect\Knight\lighting.mp3')
                    lighting.set_volume(0.5)
                    lighting.play()
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

    def checkDuration(self):
        print(self.turnLeft)
        print(self.buffOrNot)
        if self.buffOrNot == True:
            if self.turnLeft >= 2:
                self.currentAttackPoint = self.attackPoint
                self.currentDefendPoint = self.defendPoint
                self.buffOrNot = False
            else:
                self.turnLeft = self.turnLeft + 1

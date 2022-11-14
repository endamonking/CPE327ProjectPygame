from array import array
import imp
from pickle import FALSE
import pygame
import os
import button

#load asset
BLACK = (0,0,0)
player_image = pygame.image.load(os.path.join('Asset', 'knight.png'))
player_image = pygame.transform.scale(player_image, (300, 300)) 
button_image = pygame.image.load(os.path.join('Asset', 'prBTN.png'))
blackScreen = pygame.transform.scale(pygame.image.load(os.path.join('Asset', 'blackScreen.jpg')), (300, 75))

animation_cooldown = 500

class player():
    def __init__(self, maxHp, maxMp, defendPoint, attackPoint):
        self.maxHp = maxHp
        self.maxMp = maxMp
        self.currentHp = self.maxHp
        self.currentMp = self.maxMp
        self.defendPoint = defendPoint
        self.attackPoint = attackPoint
        self.lastUpdate = pygame.time.get_ticks()
        self.i = 0
        self.turn = False
        self.death = False
        self.action = "idle"
        self.skillList = ["Double Slash", "Restore mana"]
        self.showWhat = "nothing"

    def getAttackPower(self):
        return self.attackPoint
    def getTurn(self):
        return self.turn

    def showMenu(self,win):
        if self.showWhat == "noMana":
            blackScreen.set_alpha(128)
            win.blit(blackScreen, (400,170))

            text = "Not enough mana"
            my_font = pygame.font.SysFont("candara",36)
            text_surface = my_font.render(text, False, (255,255,255))
            win.blit(text_surface, (410,180))

    def draw_playerIdle(self,WIN, currentTime, Xpose, Ypose):
        if (currentTime - self.lastUpdate >= animation_cooldown):
            self.lastUpdate = currentTime
            if self.i < 2:
                self.i = self.i+1
            else:
                self.i = 0
        WIN.blit(player_image, (Xpose, Ypose), ((self.i * 100), 0, 100, 300)) #width come from total width / total frame

    def upgrade_stat(self,option):
        match option:
            case 0: #increase maximum HP and MP and heal player
                print("option 1 increase maximum HP and MP and heal player")
            case 1: #increase attack power of player 
                print("option 2 increase attack power")
            case 2: #increase defend pointof player
                print("option 3 increase defend power")
                
    def attack(self,enemy):
        damaged = self.attackPoint - enemy.defendPoint
        if damaged <= 0:
            damaged = 0
        
        enemy.currentHp = enemy.currentHp - damaged
        if enemy.currentHp < 0 :
            enemy.currentHp = 0
            enemy.death = True

    def getSkill(self, skillName):
        self.skillList.append(skillName)

    def showSkill(self, mp,  WIN, WHITE, enemy):
        skillbuttonlist = []
        i = 0
        xButPose = 400
        yButPose = 600
        yNew = 0
        self.action = "usingSkill"
        action_cooldown = 0

        #created back button
        backButton = button.button(xButPose, yButPose + yNew, button_image, 6)
        if backButton.draw(mp, WIN, WHITE, "Cancel", 28, 90, 37):
            self.action = "idle"
            action_cooldown = 90

        yNew = yNew - 100
        for x in self.skillList:
            skillbuttonlist.append(button.button(xButPose, yButPose + yNew, button_image, 6))
            yNew = yNew - 100
        
        for index, x in enumerate(skillbuttonlist):
            if x.draw(mp, WIN, WHITE, self.skillList[index], 28, 60, 37):
                action_cooldown = 0
                self.action = "idle"
                self.useSkill(self.skillList[index], enemy, WIN)
    
        return action_cooldown

    def useSkill(self, skillName, enemy, win):
        match skillName:
            case "Double Slash":
                if self.currentMp >= 20:
                    dmg = (self.attackPoint * 2) - enemy.defendPoint
                    if dmg <= 0:
                        dmg = 0
                    
                    enemy.currentHp = enemy.currentHp - dmg
                    self.currentMp = self.currentMp - 20
                else:
                    self.showWhat = "noMana"
            case "Headbutt":
                print("Stun")
            case "Paralyze":
                print("stun")
            case "Heal":
                if self.currentMp >= 25:
                    heal = self.attackPoint * 1.5
                    self.currentHp = self.currentHp + heal
                    if self.currentHp >= self.maxHp:
                        self.currentHp = self.maxHp
                    self.currentMp = self.currentMp - 25
                    self.turn = False
                    enemy.turn = True   
                else:
                    self.showWhat = "noMana"
            case "Restore mana":
                reMana = self.attackPoint * 1.5
                self.currentMp = self.currentMp + reMana
                if self.currentMp >= self.maxMp:
                    self.currentMp = self.maxMp     
                self.turn = False
                enemy.turn = True       
            case "Roaring":
                print("buff")
            case "Fire ball":
                if self.currentMp >= 35:
                    dmg = (self.attackPoint * 3) - enemy.defendPoint
                    if dmg <= 0:
                        dmg = 0
                    
                    enemy.currentHp = enemy.currentHp - dmg
                    self.currentMp = self.currentMp - 35
                    self.turn = False
                    enemy.turn = True
                else:
                    self.showWhat = "noMana"
            case "Lighting bolt":
                if (self.currentMp >= 25):
                    dmg = (self.attackPoint * 2)
                    if dmg <= 0:
                        dmg = 0
                    
                    enemy.currentHp = enemy.currentHp - dmg
                    self.currentMp = self.currentMp - 25 
                    self.turn = False
                    enemy.turn = True
                else:
                    self.showWhat = "noMana"


    def showHealth(self, WIN):
        currentHP  = str(self.currentHp)
        currentMP = str(self.currentMp)
        my_font = pygame.font.SysFont("candara",40)


        #render text
        text_surface1 = my_font.render("HP : ", False, (255,255,255))
        WIN.blit(text_surface1, (100, 200))
        text_surface2 = my_font.render(currentHP, False, (255,255,255))
        WIN.blit(text_surface2, (200, 200))

        text_surface3 = my_font.render("MP : ", False, (255,255,255))
        WIN.blit(text_surface3, (100, 250))
        text_surface4 = my_font.render(currentMP, False, (255,255,255))
        WIN.blit(text_surface4, (200, 250))

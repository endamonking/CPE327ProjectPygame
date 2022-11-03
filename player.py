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
        self.skillList = ["test1" , "test2"]

    def getAttackPower(self):
        return self.attackPoint
    def getTurn(self):
        return self.turn

   # def get_image(sheet,frame, width, height, scale, WIN):
      #  image = pygame.Surface((width, height)).convert_alpha()
       # WIN.blit(player_image, (0, 0), ((frame * width), 0, width, height))
       # image = pygame.transform.scale(image, (width * scale, height * scale))
       # image.set_colorkey(BLACK)
       # return image
    
    def draw_playerIdle(self,WIN, currentTime, Xpose, Ypose):
        if (currentTime - self.lastUpdate >= animation_cooldown):
            self.lastUpdate = currentTime
            if self.i < 2:
                self.i = self.i+1
            else:
                self.i = 0
        WIN.blit(player_image, (Xpose, Ypose), ((self.i * 100), 0, 100, 300)) #width come from total width / total frame

    def upgrade_stat(option ):
        match option:
            case 0: #increase maximum HP and MP and heal player
                print("option 1 increase maximum HP and MP and heal player")
            case 1: #increase attack power of player 
                print("option 2 increase attack power")
            case 2: #increase defend pointof player
                print("option 3 increase defend power")
                
    def attack(self,enemy):
        enemy.currentHp = enemy.currentHp - self.attackPoint
        if enemy.currentHp < 0 :
            enemy.currentHp = 0
            enemy.death = True

    def getSkill(self):
        self.skillList.append("test")
        print(self.skillList)

    def showSkill(self, mp,  WIN, WHITE):
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
            if x.draw(mp, WIN, WHITE, self.skillList[index], 28, 90, 37):
                action_cooldown = 0
                self.action = "idle"
                print(self.skillList[index])
    
        return action_cooldown

    def useSkill(self, skillName):
        match skillName:
            case "test1":
                print("test1")
            case "test2":
                print("test2")




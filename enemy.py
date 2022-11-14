from array import array
import imp
from pickle import FALSE
import pygame
import os
import random

#load asset
BLACK = (0,0,0) 
animation_cooldown = 500

#enemy class
class enemy():
    def __init__(self, name, maxHp, defendPoint, attackPoint, xScale, yScale):
        self.name = name
        self.maxHp = maxHp
        self.currentHp = self.maxHp
        self.defendPoint = defendPoint
        self.attackPoint = attackPoint
        self.lastUpdate = pygame.time.get_ticks()
        self.i = 0
        self.enemy_image = pygame.image.load(f'Asset/{self.name}/0.png')
        self.enemy_image = pygame.transform.scale(self.enemy_image, (xScale, yScale))
        self.turn = False
        self.death = False
        self.action = "idle"
        self.skillList = []

    def getAttackPower(self):
        return self.attackPoint

    def getTurn(self):
        return self.turn

    def draw_enemyIdle(self,WIN, currentTime, Xpose, Ypose):
        if (currentTime - self.lastUpdate >= animation_cooldown):
            self.lastUpdate = currentTime
            if self.i < 1:
                self.i = self.i+1
            else:
                self.i = 0
        WIN.blit(self.enemy_image, (Xpose, Ypose), ((self.i * 100), 0, 100, 300)) #width come from total width / total frame

    #slime skill
    def attackSlime(self,enemy):
        rand = random.randint(1,10)
        if rand < 2:
            self.currentHp = self.maxHp
            print("enemy heal")

        elif rand >= 2:
            damaged = self.attackPoint - enemy.defendPoint
            if damaged <= 0:
                damaged = 0
        
            enemy.currentHp = enemy.currentHp - damaged
            if enemy.currentHp < 0 :
                enemy.currentHp = 0
                enemy.death = True

    #Zombie skill
    def attackZombie(self,enemy):
        rand = random.randint(1,10)
        if rand < 3:
            damaged = self.attackPoint*2 - enemy.defendPoint
            print("enemy double attack")
            if damaged <= 0:
                damaged = 0

        else:
            damaged = self.attackPoint - enemy.defendPoint
            if damaged <= 0:
                damaged = 0
        
        enemy.currentHp = enemy.currentHp - damaged
        if enemy.currentHp < 0 :
            enemy.currentHp = 0
            enemy.death = True

    #Werewolf skill 1 
    def attackZombie(self,enemy):
        rand = random.randint(1,10)
        if rand < 3:
            damaged = self.attackPoint*2 - enemy.defendPoint
            print("enemy double attack")
            if damaged <= 0:
                damaged = 0

        else:
            damaged = self.attackPoint - enemy.defendPoint
            if damaged <= 0:
                damaged = 0
        
        enemy.currentHp = enemy.currentHp - damaged
        if enemy.currentHp < 0 :
            enemy.currentHp = 0
            enemy.death = True

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

        if self.currentHp <= 0 and self.name == "slime":
            self.currentHp = 100
            gameStage = "Normal"
            self.death = False
        elif self.currentHp <= 0:
            self.currentHp = 0
            self.death = True

        return gameStage
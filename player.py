import imp
import pygame
import os

#load asset
BLACK = (0,0,0)
player_image = pygame.image.load(os.path.join('Asset', 'knight.png'))
player_image = pygame.transform.scale(player_image, (300, 300)) 

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
                print("option 2 increase attack player")
            case 2: #increase defend pointof player
                print("option 2 increase defend power")


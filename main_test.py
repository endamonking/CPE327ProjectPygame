import imp
from pickle import FALSE, TRUE
import string
from turtle import width
import pygame
import os
import test
import scene_manager

WHITE = (255,255,255)
KNIGHT_WIDTH = 200
KNIGHT_HEIGHT = 200
BLACK = (0,0,0)
#Window setting
WIDTH = 1080 
HEIGHT = 720 
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
FPS = 60
pygame.display.set_caption("Test") #name of program

#Load asset
knight_image = pygame.image.load(os.path.join('Asset', 'knight.png'))
knight = pygame.transform.scale(knight_image,(200,200))
prBTN_image = pygame.image.load(os.path.join('Asset', 'prBTN.png'))

COMMAND_BORDER = pygame.Rect(0, 432, WIDTH, 288)

#button class
class button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
    
    def draw(self, mPose):
        action = False
        if self.rect.collidepoint(mPose) and pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.clicked = True
            action = True
        
        if pygame.mouse.get_pressed()[0] == 0 and self.clicked == True: # reset
            self.clicked = False

        WIN.blit(self.image, (self.rect.x, self.rect.y))
        return action

        

#button init
prBTN = button(100, 532, prBTN_image, 0.5)
# The display need to manual update   
def draw_window(player,mPose):
    WIN.fill(WHITE)
    pygame.draw.rect(WIN, BLACK, COMMAND_BORDER)
    WIN.blit(knight, (player.x,player.y))
    if prBTN.draw(mPose):
        test.scene()
    pygame.display.update() 

def main():
    player = pygame.Rect(200,200,KNIGHT_WIDTH, KNIGHT_HEIGHT) # It close to create object in Unity
    clock = pygame.time.Clock()
    gameRunning = True
    while gameRunning:
        clock.tick(FPS)
        mousePos = pygame.mouse.get_pos() #mouse position
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameRunning = False
                
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_ESCAPE]: # exit game
            gameRunning = False
        draw_window(player,mousePos)
        
    pygame.quit()

if __name__ == "__main__":
    main()
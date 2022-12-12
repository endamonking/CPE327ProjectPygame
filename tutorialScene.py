#       This file use to create Tutorial scene.
#   This scene will tell how to play of game 
import pygame
import button
import os
import scene_manager
import sys

WHITE = (255,255,255)
BLACK = (0,0,0)
WIDTH = 1080 
HEIGHT = 720 
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
FPS = 60
pygame.display.set_caption("Demon's tower")

#asset
button_image = pygame.image.load(os.path.join('Asset', 'prBTN.png'))
background = pygame.transform.scale(pygame.image.load(os.path.join('Asset', 'title_background.png')), (1080, 720))
tuto1 = pygame.transform.scale(pygame.image.load(os.path.join('Asset', 'tutorial1.png')), (1080, 720))
tuto2 = pygame.transform.scale(pygame.image.load(os.path.join('Asset', 'tutorial2.png')), (1080, 720))
tuto3 = pygame.transform.scale(pygame.image.load(os.path.join('Asset', 'tutorial3.png')), (1080, 720))
tuto4 = pygame.transform.scale(pygame.image.load(os.path.join('Asset', 'tutorial4.png')), (1080, 720))
backBut = button.button(50,50,button_image, 5)
nextBut = button.button(800,50,button_image, 5)
toTitleBut = button.button(800,300,button_image, 5)
tutoNo = 0

#Display picture 1
def drawTuto1():
    WIN.fill(BLACK)
    WIN.blit(tuto1, (0,0))

#Display picture 2
def drawTuto2():
    WIN.fill(BLACK)
    WIN.blit(tuto2, (0,0))

#Display picture 3
def drawTuto3():
    WIN.fill(BLACK)
    WIN.blit(tuto3, (0,0))

#Display picture 4
def drawTuto4():
    WIN.fill(BLACK)
    WIN.blit(tuto4, (0,0))

#Display Next and back button also use to call other image
#Arguments
# mp - Player's mouse position
def draw_window(mp):
    global tutoNo

    if tutoNo != 3:
        word = "Next"
    else:
        word = "To title"

    WIN.fill(BLACK)
    current_Time = pygame.time.get_ticks()
    match tutoNo:
        case 0:
            drawTuto1()
        case 1:
            drawTuto2()
        case 2:
            drawTuto3()
        case 3:
            drawTuto4()
    print(tutoNo)
    if backBut.draw(mp,WIN,BLACK,"Back",26,70,28):
        tutoNo = tutoNo - 1
        if tutoNo < 0:
            tutoNo = 0
            scene_manager.loadStage(3,WIN,60)

    if nextBut.draw(mp,WIN,BLACK,word,26,70,28):
        tutoNo = tutoNo + 1
        if tutoNo > 3:
            tutoNo = 0
            scene_manager.loadStage(3,WIN,60)

    pygame.display.update()

#main loop of Tutorial Scene 
def main ():
    clock = pygame.time.Clock()
    gamRunning = True
    while gamRunning:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamRunning = False
                pygame.quit()
                sys.exit()

        mousePose = pygame.mouse.get_pos()
        draw_window(mousePose)
    
    

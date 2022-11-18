import pygame
import button
import os
import scene_manager

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

def createText():
    BigFont = "YOU DEAD" 

    my_font = pygame.font.SysFont("candara",128)
    text_surface1 = my_font.render(BigFont, False, (255,0,0))


    WIN.blit(text_surface1, (250,140))

def draw_window(mp):
    WIN.fill(BLACK)
    toTile = button.button(400,600,button_image, 7)
    current_Time = pygame.time.get_ticks()

    createText()
    if toTile.draw(mp,WIN,BLACK,"To title",28,95,45):
        scene_manager.loadStage(3,WIN,60)
    pygame.display.update()

def main ():
    clock = pygame.time.Clock()
    gamRunning = True
    while gamRunning:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamRunning = False

        mousePose = pygame.mouse.get_pos()
        draw_window(mousePose)
    
    pygame.quit()

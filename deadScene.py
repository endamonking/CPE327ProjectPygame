# Display Dead scene 
# Will have Text popup so Player can understand that They are dead
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


#Display text to screen
def createText():
    BigFont = "YOU DEAD" 
    info = "You have fail to reclaimed the throne of Thermidor Empire. Gameover!"

    my_font = pygame.font.SysFont("candara",128)
    smallFont = pygame.font.SysFont("candara",28)
    text_surface1 = my_font.render(BigFont, False, (255,0,0))
    text_surface2 = smallFont.render(info,False,WHITE)


    WIN.blit(text_surface1, (250,140))
    WIN.blit(text_surface2, (100,400))

#Display button and screen
#Arguments
# mp - Player's mouse position
def draw_window(mp):
    WIN.fill(BLACK)
    toTile = button.button(100,600,button_image, 6)
    current_Time = pygame.time.get_ticks()

    createText()
    if toTile.draw(mp,WIN,BLACK,"To title",28,85,35):
        scene_manager.loadStage(3,WIN,60)
    pygame.display.update()

#main loop of Dead scene
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

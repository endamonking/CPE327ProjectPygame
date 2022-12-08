import pygame
import os
import button
import scene_manager

BLACK = (0,0,0)
background = pygame.transform.scale(pygame.image.load(os.path.join('Asset', 'title_background.png')), (1080, 720))
button_image = pygame.image.load(os.path.join('Asset', 'prBTN.png'))

def draw_windowStage0(mousePose, WIN, text_surface1,text_surface2, button1,text_surface3):
    WIN.fill(BLACK)

    WIN.blit(text_surface3,(350,50))
    WIN.blit(text_surface1, (150,200))
    WIN.blit(text_surface2, (350,350))

    if (button1.draw(mousePose, WIN, (255,255,255), "To main menu",38, 50, 40)):
        scene_manager.loadStage(3,WIN,60)

    pygame.display.update()

def mainLoop(WIN, FPS):
    vicText = "Victory"
    text1 = "The Prince Successfully retakes the throne. He was able to gather an army and destroy the Germania Empire." 
    text2 = "They finally sign a Treaty and live happily afterward."
    my_font = pygame.font.SysFont("candara",18)
    bigfont = pygame.font.SysFont("candara", 120)
    text_surface1 = my_font.render(text1, False, (255,255,255))
    text_surface2 = my_font.render(text2, False, (255,255,255))
    text_surface3 = bigfont.render(vicText, False, (255,255,255))

    button1 = button.button(700,400,button_image, 7)

    clock = pygame.time.Clock()
    gamRunning = True
    while gamRunning:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamRunning = False

        mousePose = pygame.mouse.get_pos()
        draw_windowStage0(mousePose, WIN, text_surface1, text_surface2, button1, text_surface3)
        
    pygame.quit()
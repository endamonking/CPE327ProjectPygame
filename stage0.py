import pygame
import os
import button
import scene_manager

BLACK = (0,0,0)
background = pygame.transform.scale(pygame.image.load(os.path.join('Asset', 'title_background.png')), (1080, 720))
button_image = pygame.image.load(os.path.join('Asset', 'prBTN.png'))

def draw_windowStage0(mousePose, WIN, text_surface1,text_surface2,text_surface3, text_surface4, button1):
    WIN.fill(BLACK)
    WIN.blit(background,(0,0))
    WIN.blit(text_surface1, (100,100))
    WIN.blit(text_surface2, (200,250))
    WIN.blit(text_surface3, (300,350))
    WIN.blit(text_surface4, (400,450))
    if (button1.draw(mousePose, WIN, (255,255,255), "NEXT",38, 110, 40)):
        scene_manager.loadStage(1,0,0)

    pygame.display.update()

def stage0(WIN, FPS):
    intro1 = "The year is 1234, the Germania Empire has decided to attack the peaceful country Thermidor Empire." 
    intro2 = "The monster from Germania broke into the king's castle and assassinated him."
    intro3 = "Prince Louis had no choice but to flee the castle and fought for his life." 
    intro4 = "Until when the time came he would retake his throne."
    my_font = pygame.font.SysFont("candara",18)
    text_surface1 = my_font.render(intro1, False, (255,255,255))
    text_surface2 = my_font.render(intro2, False, (255,255,255))
    text_surface3= my_font.render(intro3, False, (255,255,255))
    text_surface4= my_font.render(intro4, False, (255,255,255))
    button1 = button.button(400,600,button_image, 7)

    clock = pygame.time.Clock()
    gamRunning = True
    while gamRunning:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamRunning = False

        mousePose = pygame.mouse.get_pos()
        draw_windowStage0(mousePose, WIN, text_surface1, text_surface2, text_surface3, text_surface4, button1)
        
    pygame.quit()
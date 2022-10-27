
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

#ASSET
button_image = pygame.image.load(os.path.join('Asset', 'prBTN.png'))
button1 = button.button(400, 352, button_image, 7)
button2 = button.button(400, 482, button_image, 7)
background = pygame.transform.scale(pygame.image.load(os.path.join('Asset', 'title_background.png')), (1080, 720))

def draw_window(mp):
    WIN.fill(BLACK)
    WIN.blit(background,(0,0))
    current_Time = pygame.time.get_ticks()
    if button1.draw(mp, WIN, WHITE, "button1", 38, 85, 40):
        #print("test")
        scene_manager.loadStage(0,WIN,60)
    if button2.draw(mp, WIN, WHITE, "Button2", 38, 85, 40):
        pygame.quit()

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


if __name__ == "__main__":
    main()
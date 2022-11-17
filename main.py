
import pygame
import button
import os
import scene_manager

# Background music
from pygame import mixer
pygame.mixer.init()
pygame.mixer.pre_init(44100,16,2,4096)
pygame.mixer.music.load(r'C:\Users\mayso\Downloads\CPE327\CPE327ProjectPygame-endamonking-patch-1\sound effect\background\background music.mp3')
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(-1)

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
    if button1.draw(mp, WIN, WHITE, "Start", 38, 85, 40):
        scene_manager.loadStage(0,WIN,60)
    if button2.draw(mp, WIN, WHITE, "Quit", 38, 85, 40):
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
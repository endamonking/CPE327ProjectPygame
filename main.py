import pygame
import button
import os


WHITE = (255,255,255)
BLACK = (0,0,0)
WIDTH = 1080 
HEIGHT = 720 
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
FPS = 60
pygame.display.set_caption("Demon's tower")

#ASSET
button_image = pygame.image.load(os.path.join('Asset', 'prBTN.png'))
button1 = button.button(450, 352, button_image, 0.5)
button2 = button.button(450, 482, button_image, 0.5)


def draw_window(mp):
    WIN.fill(WHITE)
    if button1.draw(mp, WIN):
        print("test")
    if button2.draw(mp, WIN):
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
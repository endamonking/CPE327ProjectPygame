import pygame


class button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
    
    def draw(self, mPose, WIN, color, word, size):
        action = False
        pygame.font.init()
        my_font = pygame.font.SysFont("candara",size)
        text_surface = my_font.render(word, False, color)
        if self.rect.collidepoint(mPose) and pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.clicked = True
            action = True
        
        if pygame.mouse.get_pressed()[0] == 0 and self.clicked == True: # reset
            self.clicked = False

        WIN.blit(self.image, (self.rect.x, self.rect.y))
        WIN.blit(text_surface, (self.rect.x, self.rect.y + 50) )
        return action

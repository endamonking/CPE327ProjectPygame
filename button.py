#  Created button to display Text and Player can click
#
import pygame
class button():
    #craete button object
    #Arguments
    # x - Position of button in X axis
    # y - Position of button in y axis
    # image - Image of button
    # scale - scale size of button
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
    
    #Display button and tet to screen
    #Arguments
    # mPose - The player's mouse position
    # WIN - window screen
    # color - colour of text
    # word - Text that you wanna print 
    # szie - Size of text
    # txPose - Text posiition in x axis
    # tyPose - Text posiition in y axis
    # Return 
    # Action - Action that want button gonna do (Like if else state mean in here = 1)
    def draw(self, mPose, WIN, color, word, size, txPose, tyPose):
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
        WIN.blit(text_surface, (self.rect.x + txPose, self.rect.y + tyPose) )
        return action

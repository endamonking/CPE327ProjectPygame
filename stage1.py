import pygame
import os
import button
import player


WHITE = (255,255,255)
BLACK = (0,0,0)
WIDTH = 1080 
HEIGHT = 720 
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
FPS = 60
pygame.display.set_caption("Demon's tower")

#ASSET
button_image = pygame.image.load(os.path.join('Asset', 'prBTN.png'))
<<<<<<< HEAD
button1 = button.button(450, 352, button_image, 0.5)
button2 = button.button(450, 482, button_image, 0.5)
background = pygame.transform.scale(pygame.image.load(os.path.join('Asset', 'title_background.png')), (1080, 720))
battlescreen = pygame.transform.scale(pygame.image.load(os.path.join('Asset', 'battlescreen.png')), (1080, 720))


player_image = pygame.image.load(os.path.join('Asset', 'knight.png'))
player_image = pygame.transform.scale(player_image, (300, 300))

counter = 0

def draw_window(mainplayer,enemy,mp):
    WIN.fill(BLACK)
    WIN.blit(background,(0,0))
    current_Time = pygame.time.get_ticks()
    #player.draw_playerIdle(WIN,current_Time, 100, 100)
=======
button1 = button.button(100, 600, button_image, 6)
button2 = button.button(600, 600, button_image, 6)
battlescreen = pygame.transform.scale(pygame.image.load(os.path.join('Asset', 'battlescreen.png')), (3240, 720))
counter = 0
i = 0
BackgroundLastUpdate = pygame.time.get_ticks()

def draw_backgroundaimation(currentTime):
    global i
    global BackgroundLastUpdate
    if (currentTime - BackgroundLastUpdate >= 750):
        BackgroundLastUpdate = currentTime
        if i < 2:
            i = i+1
        else:
            i = 0
    WIN.blit(battlescreen, (0,0), ((i * 1080), 0, 1080, 720)) #width come from total width / total frame

def draw_window(mainplayer,enemy,mp):
    WIN.fill(BLACK)
    current_Time = pygame.time.get_ticks()
    draw_backgroundaimation(current_Time)
    mainplayer.draw_playerIdle(WIN,current_Time, 100, 300)
>>>>>>> 533ea8d2fc34be608f316e9571c5ee9df3e4ea2d
    if mainplayer.currentHp == 0 :
        print("enemy win")
        exit()
    elif enemy.currentHp == 0 :
        print("player win")
        exit()
    else :
<<<<<<< HEAD
            turn(mainplayer,enemy,mp)
       
    button2.draw(mp, WIN, WHITE, "Button2", 38)
=======
        turn(mainplayer,enemy,mp)
       
    if (button2.draw(mp, WIN, WHITE, "Button2", 28, 90 ,37)):
        mainplayer.getSkill()
>>>>>>> 533ea8d2fc34be608f316e9571c5ee9df3e4ea2d
    pygame.display.update()

def turn(mainplayer,enemy,mp):
    if mainplayer.turn : 
<<<<<<< HEAD
             
        if button1.draw(mp, WIN, WHITE, "Attack", 38) :
=======
            
        if button1.draw(mp, WIN, WHITE, "Attack", 28, 90, 37) :
>>>>>>> 533ea8d2fc34be608f316e9571c5ee9df3e4ea2d
            print("player attack")
            mainplayer.attack(enemy)
            print(enemy.currentHp)
            
            mainplayer.turn = False
            enemy.turn = True
      
    elif enemy.turn :
        print("enemy attack")
        enemy.attack(mainplayer)
        print(mainplayer.currentHp)
        mainplayer.turn = True
        enemy.turn = False    
        
    
def main ():
    clock = pygame.time.Clock()
    gamRunning = True
    mainplayer = player.player(10,10,10,1)
    enemy = player.player(10,10,10,2)
    mainplayer.turn = True
<<<<<<< HEAD

=======
>>>>>>> 533ea8d2fc34be608f316e9571c5ee9df3e4ea2d
    while gamRunning:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamRunning = False
                
        mousePose = pygame.mouse.get_pos()
        draw_window(mainplayer,enemy,mousePose)

        
        
    pygame.quit()

<<<<<<< HEAD
if __name__ == "__main__":
    main()
    
=======

>>>>>>> 533ea8d2fc34be608f316e9571c5ee9df3e4ea2d
    
        


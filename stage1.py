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
button1 = button.button(100, 600, button_image, 6)
button2 = button.button(700, 600, button_image, 6)
battlescreen = pygame.transform.scale(pygame.image.load(os.path.join('Asset', 'battlescreen.png')), (3240, 720))
counter = 0
i = 0
BackgroundLastUpdate = pygame.time.get_ticks()
action_cooldown = 90
action_WaitTime = 90

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
    if mainplayer.currentHp == 0 :
        print("enemy win")
        exit()
    elif enemy.currentHp == 0 :
        print("player win")
        exit()
    else :
        turn(mainplayer,enemy,mp)
    pygame.display.update()

def turn(mainplayer,enemy,mp):
    global action_cooldown
    if mainplayer.turn : 
        action_cooldown = action_cooldown + 1
        if mainplayer.action == "usingSkill":
            action_cooldown = mainplayer.showSkill(mp, WIN, WHITE)
        if mainplayer.action == "idle" and action_cooldown >= action_WaitTime :
            if button1.draw(mp, WIN, WHITE, "Attack", 28, 90, 37) and action_cooldown >= action_WaitTime :
                print("player attack")
                mainplayer.attack(enemy)
                print(enemy.currentHp)
                action_cooldown = 0
                mainplayer.turn = False
                enemy.turn = True
                
            if (button2.draw(mp, WIN, WHITE, "Button2", 28, 90 ,37)) and action_cooldown >= action_WaitTime :
                mainplayer.action = "usingSkill"
        
    elif enemy.turn :
        action_cooldown = action_cooldown + 1
        if action_cooldown >= action_WaitTime:
            print("enemy attack")
            enemy.attack(mainplayer)
            print(mainplayer.currentHp)
            action_cooldown = 0
            mainplayer.turn = True
            enemy.turn = False    
        
    pygame.display.update()
def main ():
    clock = pygame.time.Clock()
    gamRunning = True
    mainplayer = player.player(10,10,10,1)
    enemy = player.player(10,10,10,2)
    mainplayer.turn = True
    while gamRunning:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamRunning = False
                
        mousePose = pygame.mouse.get_pos()
        draw_window(mainplayer,enemy,mousePose)
    pygame.quit()


    
        


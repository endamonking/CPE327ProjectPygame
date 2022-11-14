import pygame
import os
import button
import player
import path
import enemy

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
blackScreen = pygame.transform.scale(pygame.image.load(os.path.join('Asset', 'blackScreen.jpg')), (WIDTH, HEIGHT))

counter = 0
i = 0
BackgroundLastUpdate = pygame.time.get_ticks()
action_cooldown = 90
action_WaitTime = 90
gameState = "Normal"

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


def draw_window(mainplayer,slime,mp):
    global gameState

    WIN.fill(BLACK)
    current_Time = pygame.time.get_ticks()
    draw_backgroundaimation(current_Time)
    mainplayer.draw_playerIdle(WIN,current_Time, 100, 300)
    slime.draw_enemyIdle(WIN,current_Time, 780, 475)
    mainplayer.showHealth(WIN)
    slime.showHealth(WIN)
    if mainplayer.currentHp <= 0 :
        gameState = "Lose"
        exit()
    elif slime.currentHp <= 0 :
        gameState = slime.isDead()
    else :
        turn(mainplayer,slime,mp)

    if gameState == "Win":
        gameState = path.createPath(WIN,mainplayer,mp, gameState)
        
    pygame.display.update()

def turn(mainplayer,slime,mp):
    global action_cooldown
    mainplayer.showMenu(WIN)
    if action_cooldown == action_WaitTime:
        mainplayer.showWhat = "nothing" 

    if mainplayer.turn : 
        action_cooldown = action_cooldown + 1
        if mainplayer.action == "usingSkill":
            action_cooldown = mainplayer.showSkill(mp, WIN, WHITE, slime)
        if mainplayer.action == "idle" and action_cooldown >= action_WaitTime :
            if button1.draw(mp, WIN, WHITE, "Attack", 28, 90, 37) and action_cooldown >= action_WaitTime :
                print("player attack")
                mainplayer.attack(slime)
                print(slime.currentHp)
                action_cooldown = 0
                mainplayer.turn = False
                slime.turn = True
                
            if (button2.draw(mp, WIN, WHITE, "Button2", 28, 90 ,37)) and action_cooldown >= action_WaitTime :
                mainplayer.action = "usingSkill"
        
    elif slime.turn :
        action_cooldown = action_cooldown + 1
        if action_cooldown >= action_WaitTime:
            print("slime attack")
            slime.attackSlime(mainplayer)
            print(mainplayer.currentHp)
            action_cooldown = 0
            mainplayer.turn = True
            slime.turn = False    
        
    pygame.display.update()
def main ():
    #monster = []
    clock = pygame.time.Clock()
    gamRunning = True
    mainplayer = player.player(100,100,10,20)
    slime = enemy.enemy("slime",80,0,20,200,100)
    #สร้างมอนเพิ่ม
    #zombie = enemy.enmy
    #monster.append(slime)
    #monster.append(zombie)
    mainplayer.turn = True
    while gamRunning:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamRunning = False
                
        mousePose = pygame.mouse.get_pos()
        draw_window(mainplayer,slime,mousePose)
    pygame.quit()


    
        


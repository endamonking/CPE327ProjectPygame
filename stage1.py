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
blackScreen = pygame.transform.scale(pygame.image.load(os.path.join('Asset', 'blackScreen.jpg')), (300, 75))

#global var
counter = 0
i = 0
BackgroundLastUpdate = pygame.time.get_ticks()
action_cooldown = 90
action_WaitTime = 90
gameState = "Normal"
stunDuration = 0
dmg = 0
side = "Nothing"

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


def draw_window(mainplayer,monster,mp):
    global gameState
    global counter

    WIN.fill(BLACK)
    current_Time = pygame.time.get_ticks()
    draw_backgroundaimation(current_Time)
    mainplayer.draw_playerIdle(WIN,current_Time, 100, 300)
    if monster.name == "slime":
        monster.draw_enemyIdle(WIN,current_Time, 780, 475, 100)
    elif monster.name == "zombie":
        monster.draw_enemyIdle(WIN,current_Time, 780, 350, 100)
    elif monster.name == "dragon":
        monster.draw_enemyIdle(WIN,current_Time, 750, 300, 180)
    elif monster.name == "werewolf1" or "werewolf2":
        monster.draw_enemyIdle(WIN,current_Time, 750, 350, 100)

    mainplayer.showHealth(WIN)
    monster.showHealth(WIN)
    if mainplayer.currentHp <= 0 :
        gameState = "Lose"
        exit()
    elif monster.currentHp <= 0 :
        gameState = monster.isDead()
    else :
        turn(mainplayer,monster,mp)

    if gameState == "Win":
        gameState , counter = path.createPath(WIN,mainplayer,mp, gameState, counter)
        mainplayer.turn = True
        monster.turn = False
    elif gameState == "Next":
        counter = counter + 1
        gameState = "Normal"
        mainplayer.turn = True
        monster.turn = False

    pygame.display.update()

def turn(mainplayer,monster,mp):
    global action_cooldown
    global counter
    global stunDuration
    global dmg
    global side

    if stunDuration == 1:
        stunDuration = 0
        monster.action = "idle"
    mainplayer.showMenu(WIN)
    monster.showMonsterStatus(WIN)
    showDamage(dmg, side, mainplayer)
    if action_cooldown == action_WaitTime:
        mainplayer.showWhat = "nothing" 
        side = "Nothing"

    if mainplayer.turn : 
        action_cooldown = action_cooldown + 1
        if mainplayer.action == "usingSkill":
            action_cooldown, dmg, side = mainplayer.showSkill(mp, WIN, WHITE, monster)
        if mainplayer.action == "idle" and action_cooldown >= action_WaitTime :
            if button1.draw(mp, WIN, WHITE, "Attack", 28, 90, 37) and action_cooldown >= action_WaitTime :
                print("player attack")
                dmg, side = mainplayer.attack(monster)
                print(monster.currentHp)
                action_cooldown = 0
                mainplayer.turn = False
                monster.turn = True
                
            if (button2.draw(mp, WIN, WHITE, "Skills", 28, 90 ,37)) and action_cooldown >= action_WaitTime :
                mainplayer.action = "usingSkill"
        
    elif monster.turn :
        action_cooldown = action_cooldown + 1
        if action_cooldown >= action_WaitTime:
            if monster.action == "idle":
                print("monster attack")
                if monster.name == "slime":
                    dmg, side = monster.attackSlime(mainplayer)
                elif monster.name == "zombie":
                    dmg, side = monster.attackZombie(mainplayer)
                elif monster.name =="dragon":
                    dmg, side = monster.attackDragon(mainplayer)
                elif monster.name =="werewolf1":
                    dmg, side = monster.attackWerewolf1(mainplayer)
                elif monster.name =="werewolf2":
                    dmg, side = monster.attackWerewolf2(mainplayer)
                print(mainplayer.currentHp)
                action_cooldown = 0
                mainplayer.turn = True
                monster.turn = False    
            elif monster.action == "stunned":
                print(stunDuration)
                stunDuration = stunDuration + 1
                action_cooldown = 0
                mainplayer.turn = True
                monster.turn = False    
            elif monster.action == "casting":
                pass

    pygame.display.update()

def showDamage(DMG, side, player):

    if side == "player" and player.showWhat == "nothing":
        sDMG = str(DMG)
        blackScreen.set_alpha(128)
        WIN.blit(blackScreen, (400,170))
        finalText = "player dealt : " + sDMG
        my_font = pygame.font.SysFont("candara",36)
        text_surface = my_font.render(finalText, False, (255,255,255))
        WIN.blit(text_surface, (410,180))
    elif side == "monster":
        sDMG = str(DMG)
        blackScreen.set_alpha(128)
        WIN.blit(blackScreen, (400,170))
        finalText = "Monster dealt : " + sDMG
        my_font = pygame.font.SysFont("candara",36)
        text_surface = my_font.render(finalText, False, (255,255,255))
        WIN.blit(text_surface, (410,180))

def createMonster(monster):

    slime = enemy.enemy("slime",80,0,20,200,100)
    zombie = enemy.enemy("zombie",50,10,30,200,200)
    slime = enemy.enemy("slime",50,0,20,200,100)
    zombie = enemy.enemy("zombie",100,10,30,200,200)
    dragon = enemy.enemy("dragon",200,25,40,360,300)
    werewolf1 = enemy.enemy("werewolf1",200, 40,30, 200, 200)
    werewolf2 = enemy.enemy("werewolf2",300, 10,50, 200, 200)
    #monster.append = enemy.enemy("zombie",80,0,20,200,100)
    #สร้างมอนเพิ่ม
    #zombie = enemy.enmy
    monster.append(slime)
    monster.append(zombie)
    monster.append(dragon)
    monster.append(werewolf1)
    monster.append(werewolf2)

def main ():
    global counter
    monster = []
    clock = pygame.time.Clock()
    gamRunning = True
    #order list name hp defend attack xpose ypose 
    mainplayer = player.player(10000,10000,10,40)
    createMonster(monster)
    mainplayer.turn = True
    while gamRunning:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamRunning = False
                
        mousePose = pygame.mouse.get_pos()
        draw_window(mainplayer,monster[counter],mousePose)
    pygame.quit()


    
        


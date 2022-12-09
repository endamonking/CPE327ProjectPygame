import pygame
import os
import button
import player
import path
import enemy
import scene_manager


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH = 1080
HEIGHT = 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
pygame.display.set_caption("Demon's tower")

# ASSET
button_image = pygame.image.load(os.path.join('Asset', 'prBTN.png'))
button1 = button.button(100, 600, button_image, 6)
button2 = button.button(700, 600, button_image, 6)
battlescreen = pygame.transform.scale(pygame.image.load(
    os.path.join('Asset', 'battlescreen.png')), (3240, 720))
blackScreen = pygame.transform.scale(pygame.image.load(
    os.path.join('Asset', 'blackScreen.jpg')), (300, 75))
bossScreen = pygame.transform.scale(pygame.image.load(
    os.path.join('Asset', 'boss_background.png')), (4320, 720))

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
bossYet = False


def draw_backgroundaimation(currentTime):
    global i
    global BackgroundLastUpdate
    if (currentTime - BackgroundLastUpdate >= 750):
        BackgroundLastUpdate = currentTime
        if i < 2:
            i = i+1
        else:
            i = 0
    # width come from total width / total frame
    WIN.blit(battlescreen, (0, 0), ((i * 1080), 0, 1080, 720))


def draw_bossBackgroundAnimation(currentTime):
    global i
    global BackgroundLastUpdate

    if (currentTime - BackgroundLastUpdate >= 750):
        BackgroundLastUpdate = currentTime
        if i < 3:
            i = i+1
        else:
            i = 0

    # width come from total width / total frame
    WIN.blit(bossScreen, (0, 0), ((i * 1080), 0, 1080, 720))


def draw_window(mainplayer, monster, mp):
    global gameState
    global counter

    WIN.fill(BLACK)
    current_Time = pygame.time.get_ticks()

    if counter < 6:
        draw_backgroundaimation(current_Time)
    elif counter >= 6:
        draw_bossBackgroundAnimation(current_Time)

    mainplayer.draw_playerIdle(WIN, current_Time, 100, 300)
    if monster.name == "slime":
        monster.draw_enemyIdle(WIN, current_Time, 780, 475, 100)
    elif monster.name == "zombie":
        monster.draw_enemyIdle(WIN, current_Time, 780, 350, 100)
    elif monster.name == "dragon":
        monster.draw_enemyIdle(WIN, current_Time, 750, 300, 180)
    elif monster.name == "werewolf1" or "werewolf2":
        monster.draw_enemyIdle(WIN, current_Time, 750, 350, 100)
    elif monster.name == "witch":
        monster.draw_enemyIdle(WIN, current_Time, 750, 350, 100)
    elif monster.name == "boss1":
        monster.draw_enemyIdle(WIN, current_Time, 750, 350, 100)
    elif monster.name == "boss2":
        monster.draw_enemyIdle(WIN, current_Time, 750, 350, 100)
        monster.draw_effect(WIN, current_Time, 750, 350, 100)

    mainplayer.showHealth(WIN)
    monster.showHealth(WIN)
    if mainplayer.currentHp <= 0:
        gameState = "Lose"
        counter = 0
        path.reset()
        scene_manager.loadStage(2, WIN, 60)
    elif monster.currentHp <= 0:
        gameState = monster.isDead()
    else:
        turn(mainplayer, monster, mp,current_Time)

    if gameState == "Win":
        mainplayer.showWhat = "nothing"
        gameState, counter = path.createPath(
            WIN, mainplayer, mp, gameState, counter)
        mainplayer.turn = True
        monster.turn = False
    elif gameState == "Next":
        counter = counter + 1
        gameState = "Normal"
        mainplayer.turn = True
        monster.turn = False
    elif gameState == "victory":
        counter = 0
        path.reset()
        gameState = "Normal"
        scene_manager.loadStage(5, WIN, 60)

    pygame.display.update()


def turn(mainplayer, monster, mp, current_Time):
    global action_cooldown
    global counter
    global stunDuration
    global dmg
    global side

    if stunDuration == 1:
        stunDuration = 0
        monster.action = "idle"
    mainplayer.showMenu(WIN, current_Time)
    monster.showMonsterStatus(WIN)
    showDamage(dmg, side, mainplayer)

    if action_cooldown == action_WaitTime:
        mainplayer.showWhat = "nothing"
        side = "Nothing"

    if mainplayer.turn:
        if mainplayer.passiveCounter == 0:
            mainplayer.passiveActivated("turn")
            mainplayer.passiveCounter = mainplayer.passiveCounter + 1

        action_cooldown = action_cooldown + 1
        if mainplayer.action == "usingSkill":
            action_cooldown, dmg, side = mainplayer.showSkill(
                mp, WIN, BLACK, monster)
        if mainplayer.action == "idle" and action_cooldown >= action_WaitTime:
            if button1.draw(mp, WIN, BLACK, "Attack", 28, 90, 37) and action_cooldown >= action_WaitTime:
                print("player attack")
                dmg, side = mainplayer.attack(monster)
                print(monster.currentHp)
                action_cooldown = 0
                mainplayer.turn = False
                monster.turn = True
                mainplayer.passiveCounter = 0

            if (button2.draw(mp, WIN, BLACK, "Skills", 28, 90, 37)) and action_cooldown >= action_WaitTime:
                mainplayer.action = "usingSkill"

    elif monster.turn:
        action_cooldown = action_cooldown + 1
        if action_cooldown >= action_WaitTime:
            if monster.action == "idle":
                print("monster attack")
                if monster.name == "slime":
                    dmg, side = monster.attackSlime(mainplayer)
                elif monster.name == "zombie":
                    dmg, side = monster.attackZombie(mainplayer)
                elif monster.name == "dragon":
                    dmg, side = monster.attackDragon(mainplayer)
                elif monster.name == "werewolf1":
                    dmg, side = monster.attackWerewolf1(mainplayer)
                elif monster.name == "werewolf2":
                    dmg, side = monster.attackWerewolf2(mainplayer)
                elif monster.name == "witch":
                    dmg, side = monster.attackWitch(mainplayer)
                elif monster.name == "boss1":
                    dmg, side = monster.attackBoss1(mainplayer)
                elif monster.name == "boss2":
                    dmg, side = monster.attackBoss2(mainplayer)
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
                if monster.name == "witch":
                    dmg, side = monster.castWitch(mainplayer)
                if monster.name == "boss2":
                    dmg, side = monster.castBoss(mainplayer)

    pygame.display.update()


def showDamage(DMG, side, player):

    if side == "player" and player.showWhat == "nothing" and DMG != 0:
        sDMG = str(DMG)
        blackScreen.set_alpha(128)
        WIN.blit(blackScreen, (400, 170))
        finalText = "Player dealt : " + sDMG
        my_font = pygame.font.SysFont("candara", 26)
        text_surface = my_font.render(finalText, False, (255, 255, 255))
        WIN.blit(text_surface, (410, 180))
    elif side == "monster" and DMG != 0:
        sDMG = str(DMG)
        blackScreen.set_alpha(128)
        WIN.blit(blackScreen, (400, 170))
        finalText = "Monster dealt : " + sDMG
        my_font = pygame.font.SysFont("candara", 26)
        text_surface = my_font.render(finalText, False, (255, 255, 255))
        WIN.blit(text_surface, (410, 180))


def createMonster(monster):
    # NAME,hp,Def,Atk,Xpose,Ypose
    slime = enemy.enemy("slime",15,10,5,200,100)
    zombie = enemy.enemy("zombie",20,5,5,200,200)
    dragon = enemy.enemy("dragon",80,10,15,360,300)
    werewolf1 = enemy.enemy("werewolf1",50,10,10, 200, 200)
    werewolf2 = enemy.enemy("werewolf2",80,15,12, 200, 200)
    witch = enemy.enemy("witch",100,10,30,200,200)
    boss1 =enemy.enemy("boss1",150,15,40,200,200)
    boss2 =enemy.enemy("boss2",200,15,50,200,200)

    #monster.append = enemy.enemy("zombie",80,0,20,200,100)
    # สร้างมอนเพิ่ม
    #zombie = enemy.enmy
    monster.append(slime)
    monster.append(zombie)
    monster.append(dragon)
    monster.append(werewolf1)
    monster.append(werewolf2)
    monster.append(witch)
    monster.append(boss1)
    monster.append(boss2)


def main():
    global counter
    monster = []
    clock = pygame.time.Clock()
    gamRunning = True
    # order list name hp defend attack xpose ypose
    mainplayer = player.player(100,100, 10, 10)
    createMonster(monster)
    mainplayer.turn = True
    while gamRunning:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamRunning = False

        mousePose = pygame.mouse.get_pos()
        draw_window(mainplayer, monster[counter], mousePose)
    pygame.quit()

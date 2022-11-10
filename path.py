import pygame
import os
import button
import random

WHITE = (255,255,255)
button_image = pygame.image.load(os.path.join('Asset', 'prBTN.png'))
blackScreen = pygame.transform.scale(pygame.image.load(os.path.join('Asset', 'blackScreen.jpg')), (1000, 600))

state = 0
i = 0
activeSkillAlready = False
activeSkillList = []
upgradeStatusAlready = False

def randomActiveSkill_AndCheck(player):
    randoming = True
    while randoming:
        dupe = True
        skillList = []
        number = random.sample(range(8), 3)
        for a in number:
            match a:
                case 0:
                    skillList.append("Double_Slash")
                case 1:
                    skillList.append("Headbutt")
                case 2:
                    skillList.append("Paralyze")
                case 3:
                    skillList.append("Heal")
                case 4:
                    skillList.append("Restore_mana")
                case 5:
                    skillList.append("Roaring ")
                case 6:
                    skillList.append("Fire_ball")
                case 7:
                    skillList.append("Lighting_bolt")

        for b in skillList:
            for c in player.skillList:
                if b == c:
                    dupe = False

        if dupe == True:
            randoming = False

    return skillList

def createPath(win,player,mp, gameState):
    newGS = "Win"

    blackScreen.set_alpha(128)
    win.blit(blackScreen, (50,50))
    match state:
        case 0:
            getPassiveskil(win,player,mp)
        case 1:
            getActiveSkill(win,player,mp)
        case 2:
            newGS = upgradeStatus(win,player,mp)

    return newGS


def getPassiveskil(win, player, mp):
    global state
    event1 = button.button(600, 100, button_image, 6)
    event2 = button.button(600, 200, button_image, 6)
    event3 = button.button(600, 300, button_image, 6)
    
    print("ehe")
    state = 1

def getActiveSkill(win,player,mp):
    global state
    global i 
    global activeSkillAlready
    global activeSkillList

    i = i + 1
    Aevent1 = button.button(700, 100, button_image, 6)
    Aevent2 = button.button(700, 300, button_image, 6)
    Aevent3 = button.button(700, 500, button_image, 6)

    if activeSkillAlready == False:
        activeSkillList = randomActiveSkill_AndCheck(player)
        activeSkillAlready = True

    if i >= 60: 
        if Aevent1.draw(mp, win, WHITE, activeSkillList[0], 28, 50, 37):
            state = 2
            i = 0
            activeSkillAlready = False
            player.getSkill(activeSkillList[0])
        if Aevent2.draw(mp, win, WHITE, activeSkillList[1], 28, 50, 37):
            state = 2
            i = 0   
            activeSkillAlready = False
            player.getSkill(activeSkillList[1])     
        if Aevent3.draw(mp, win, WHITE, activeSkillList[2], 28, 50, 37):
            state = 2
            i = 0
            activeSkillAlready = False
            player.getSkill(activeSkillList[2])

def upgradeStatus(win,player,mp):
    global state
    global i
    global upgradeStatusAlready

    Sevent1 = button.button(700, 100, button_image, 8)
    Sevent2 = button.button(700, 300, button_image, 8)
    Sevent3 = button.button(700, 500, button_image, 8)

    i = i + 1
    if i >= 60:
        if Sevent1.draw(mp, win, WHITE, "Increase HP and MP", 28, 50, 50):
            player.upgrade_stat(0)
            state = 0
            i = 0  
        if Sevent2.draw(mp, win, WHITE, "Increase attack power", 28, 50, 50):
            player.upgrade_stat(1)
            state = 0  
            i = 0  
        if Sevent3.draw(mp, win, WHITE, "Increase defend power", 28, 50, 50):
            player.upgrade_stat(2)
            state = 0 
            i = 0   

    return "Normal"
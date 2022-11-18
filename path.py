import pygame
import os
import button
import random

WHITE = (255,255,255)
button_image = pygame.image.load(os.path.join('Asset', 'prBTN.png'))
blackScreen = pygame.transform.scale(pygame.image.load(os.path.join('Asset', 'blackScreen.jpg')), (1000, 700))

state = 0
i = 0
activeSkillAlready = False
activeSkillList = []
upgradeStatusAlready = False
skillStory = ""


def createStory(win, skillName, mp):
    global state
    global i

    but1 = button.button(410, 600, button_image, 6)
    i = i +1

    if i >= 60:
        if but1.draw(mp, win, WHITE, "Next", 30, 100, 37):
            state = 3
            i = 0

    match skillName:
        case "Double Slash":
            text = "Meet with a Samurai swordsmith that is under attack by slime, we help him defeat the slime, In return get trained by him."
        case "Headbutt":
            text = "Meet with a Viking explorer, we gave him our country map. In return we get trained by him."
        case "Paralyze":
            text = "Meet with an alchemist, we gave him some money. In return he gave us a Paralyze skill."
        case "Heal":
            text = "Meet with a Healing fountain. We keep it in a bottle."
        case "Restore mana":
            text = "Meet with a random traveler that is under attack by a thief. You help the random traveler, he gives you a Restore mana skill."
        case "Roaring":
            text = "Meet with a stray wherewolf, we gave him food. In return we gave us Roaring skill."
        case "Fire ball":
            text = "Meet with a Dungeon warden, we help him fix the Dungeon entrance. He gave us a Fireball skill in return."
        case "Lighting bolt":
            text = "Worship Zeus, he appeared before us and gave us Lighting bolt skill"
    
    my_font = pygame.font.SysFont("candara",18)
    text_surface = my_font.render(text, False, (255,255,255))
    win.blit(text_surface, (100, 200))

def displaySkillDescription(skillName, xPose, Ypose, win):

    match skillName:
        case "Double Slash":
            text = "Deal double damage of attackpower"
        case "Headbutt":
            text = "Deal damage and stun the enemy"
        case "Paralyze":
            text = "Stune the enemy"
        case "Heal":
            text = "Recovery some HP"
        case "Restore mana":
            text = "Recovery some MP"
        case "Roaring":
            text = "increase defend and attack power"
        case "Fire ball":
            text = "Deal massive damage"
        case "Lighting bolt":
            text = "Deal damage to the enemy"
    
    my_font = pygame.font.SysFont("candara",36)
    text_surface = my_font.render(text, False, (255,255,255))
    win.blit(text_surface, (xPose, Ypose))


def randomActiveSkill_AndCheck(player):
    randoming = True
    while randoming:
        dupe = True
        skillList = []
        number = random.sample(range(8), 3)
        if len(player.skillList) >=4:
            print("you cannot have skill more than 4")
            randoming = False
            return skillList

        number = random.sample(range(8), 3)
        for a in number:
            match a:
                case 0:
                    skillList.append("Double Slash")
                case 1:
                    skillList.append("Headbutt")
                case 2:
                    skillList.append("Paralyze")
                case 3:
                    skillList.append("Heal")
                case 4:
                    skillList.append("Restore mana")
                case 5:
                    skillList.append("Roaring")
                case 6:
                    skillList.append("Fire ball")
                case 7:
                    skillList.append("Lighting bolt")

        for b in skillList:
            for c in player.skillList:
                if b == c:
                    print("0")
                    dupe = False

        if dupe == True:
            randoming = False

    return skillList

def createPath(win,player,mp, gameState, counter):
    newGS = "Win"
    newCounter = counter

    text1 = "Choose the upgrade"
    my_font = pygame.font.SysFont("candara",36)
    text_surface1 = my_font.render(text1, False, (255,255,255))

    blackScreen.set_alpha(128)
    win.blit(blackScreen, (50,50))
    win.blit(text_surface1, (400,100))
    match state:
        case 0:
            getPassiveskil(win,player,mp)
        case 1:
            getActiveSkill(win,player,mp)
        case 2:
            createStory(win, skillStory,mp)
        case 3:
            newGS, newCounter = upgradeStatus(win,player,mp, counter)

    return newGS, newCounter


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
    global skillStory

    i = i + 1
    Aevent1 = button.button(700, 150, button_image, 6)
    Aevent2 = button.button(700, 350, button_image, 6)
    Aevent3 = button.button(700, 550, button_image, 6)

    if activeSkillAlready == False:
        activeSkillList = randomActiveSkill_AndCheck(player)
        activeSkillAlready = True

    if len(activeSkillList) == 0:
        state = 3
        i = 0
        activeSkillAlready = False
        print("empty list")
        pass

    if i >= 60: 
        displaySkillDescription(activeSkillList[0], 100,180,win)
        if Aevent1.draw(mp, win, WHITE, activeSkillList[0], 28, 50, 37):
            state = 2
            i = 0
            activeSkillAlready = False
            player.getSkill(activeSkillList[0])
            skillStory = activeSkillList[0]

        displaySkillDescription(activeSkillList[1], 100,380,win)
        if Aevent2.draw(mp, win, WHITE, activeSkillList[1], 28, 50, 37):
            state = 2
            i = 0   
            activeSkillAlready = False
            player.getSkill(activeSkillList[1])     
            skillStory = activeSkillList[1]

        displaySkillDescription(activeSkillList[2], 100,580,win)
        if Aevent3.draw(mp, win, WHITE, activeSkillList[2], 28, 50, 37):
            state = 2
            i = 0
            activeSkillAlready = False
            player.getSkill(activeSkillList[2])
            skillStory = activeSkillList[2]

def upgradeStatus(win,player,mp,counter):
    global state
    global i
    global upgradeStatusAlready

    Sevent1 = button.button(700, 150, button_image, 8)
    Sevent2 = button.button(700, 350, button_image, 8)
    Sevent3 = button.button(700, 550, button_image, 8)

    i = i + 1
    if i >= 60:
        if Sevent1.draw(mp, win, WHITE, "Increase HP and MP", 28, 50, 50):
            player.upgrade_stat(0)
            state = 0
            i = 0  
            counter = counter+1
        if Sevent2.draw(mp, win, WHITE, "Increase attack power", 28, 50, 50):
            player.upgrade_stat(1)
            state = 0  
            i = 0  
            counter = counter+1
        if Sevent3.draw(mp, win, WHITE, "Increase defend power", 28, 50, 50):
            player.upgrade_stat(2)
            state = 0 
            i = 0   
            counter = counter+1
    
    return "Normal", counter 

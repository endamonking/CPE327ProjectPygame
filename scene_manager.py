# Use to change between scene So another scene that want to go to other scene dont need to import all file.
# They need only once
import pygame
import button
import os
import stage0
import stage1
import deadScene
import main
import tutorialScene
import victoryScreen


#Change scene to other scene 
#Arguments
# stage - scene that you want to go
# WIN - window screen
# FPS - FPS of game
def loadStage(stage, WIN, FPS):
    match stage:
        case 0:
            stage0.stage0(WIN,FPS)
        case 1:
            stage1.main()
        case 2:
            deadScene.main()
        case 3:
            main.main()
        case 4:
            tutorialScene.main()
        case 5:
            victoryScreen.mainLoop(WIN,FPS)

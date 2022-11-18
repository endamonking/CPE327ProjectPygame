import pygame
import button
import os
import stage0
import stage1
import deadScene
import main

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

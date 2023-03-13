import pygame

from game import Game

windowWidth = 1024
windowHeight = 768
windowBorder = 0
scaler = 2.5
game = Game(pygame, scaler, windowWidth, windowHeight, False)
game.start()

import pygame, sys # this imports pygame
import random # this imports random - randomness is key in a game like this
import time # this imports time - for time between attacks and stuff
import math # this imports math

pygame.init()

# the game window
screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("FIGHT!")

# defining colours

black = (0, 0, 0)
gold = (218, 165, 32)
grey = (200, 200, 200)
green = (0, 200, 0)
red = (200, 0, 0)
white = (255, 255, 255)
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

# move as in taking turns

class Move():

    def __init__(self, name, power, type):
        self.name = name # name of the move
        self.power = power # power of move -- the amount of damage dealt
        self.type = type # type as in like water, fire and grass

class Dynamon(pygame.sprite.Sprite):

    def __init__(self, name, level, x, y):
        
        pygame.sprite.Sprite.__init__(self)

        # set name and level of Dynamon
        self.name = name
        self.level = level

        # sprite position
        self.x = x
        self.y = y

        # start number of healing spray
        self.num_healspray = 3

        # set predefined stats of the dynamon
        self.current_hp = 100 + self.level
        self.max_hp = 100 + self.level
        self.attack = 50
        self.defence = 30
        self.speed = 40

        # set dynamon types
        self.types = ["normal"]

        # set sprite width
        self.size = 150

        # set sprite to thefront facing sprite
        self.set_sprite("front_default")
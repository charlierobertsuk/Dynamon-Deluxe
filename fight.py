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

    def perform_attack(self, other, move):

        print(f'{self.name} used {move.name}') # NOTE: Pls print onscreen!!

        # pause for 2 seconds
        time.sleep(2) # using time import

        # calculate the damage
        damage = (2 * self.level + 10) / 250 * self.attack / other.defense * move.power

        # same type attack bonus (STAB)
        if move.type in self.types:
            damage *= 1.5 # damage multiplier by 1.5 times the damage

        # critical hit (6.25% chance)
        random_num = random.randint(1, 10000)
        if random_num <= 625:
            damage *= 1.5 # damage multiplier by 1.5 times the damage again if crit

        # round down the damage
        damage = math.floor(damage) # math.floor rounds the number down to the nearest intager

        other.take_damage(damage) # other character take damage

    def take_damage(self, damage):

        self.current_hp -= damage # quite clearly takes damage

        # hp should not go below 0 cos thats not meant to be possible
        if self.current_hp < 0:
            self.current_hp = 0

    def use_potion(self):

        # check if there are potions left
        if self.num_potions > 0:

            # add 30 hp (but don't go over the max hp)
            self.current_hp += 30
            if self.current_hp > self.max_hp:
                self.current_hp = self.max_hp

            # decrease the number of potions left
            self.num_potions -= 1

    def set_sprite(self, side):

        # set the sprite to a predefined image
        self.image = pygame.image.load("graphics/dynadex/real-dynamon/kickflik.png").convert_alpha() # add sprite NOTE: change to not only be kickflick - fix pls
        self.image.fill(grey)
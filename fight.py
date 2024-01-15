import pygame, sys # this imports pygame
from pygame.locals import * # imports pygame Rect which basicaly stores rectangular coordinates
import random # this imports random - randomness is key in a game like this
import time # this imports time - for time between attacks and stuff
import math # this imports math

pygame.init()

# the game window
game_width = 1280
game_height = 720
size = (game_width, game_height)
game = pygame.display.set_mode(size)
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

    def set_sprite(self, size):

        # set the sprite to a predefined image

        #self.image = pygame.image.load("graphics/dynadex/real-dynamon/kickflik.png").convert_alpha() # add sprite NOTE: change to not only be kickflick - fix pls
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(grey)
    
    def set_moves(self):

        self.moves = []

        # defines some simple moves
        move1 = Move(name='Sonic Shock', power=40, type='normal')
        move2 = Move(name='Scratch', power=35, type='normal')
        move3 = Move(name='Fire Storm', power=50, type='fire')
        move4 = Move(name='Bubble Burst', power=45, type='water')
        move5 = Move(name='Leaf Strike', power=45, type='Grass')

        self.moves = [move1, move2, move3, move4, move5]

    def draw(self, alpha=255):

        sprite = self.image.copy()
        transparency = (255, 255, 255, alpha)
        sprite.fill(transparency, None, pygame.BLEND_RGBA_MULT)
        game.blit(sprite, (self.x, self.y))

    
    def draw_hp(self):

        # display the health bar
        bar_scale = 200 // self.max_hp
        for i in range(self.max_hp):
            bar = (self.hp_x + bar_scale * i, self.hp_y, bar_scale, 20)
            pygame.draw.rect(game, red, bar)

        for i in range(self.current_hp):
            bar = (self.hp_x + bar_scale * i, self.hp_y, bar_scale, 20)
            pygame.draw.rect(game, green, bar)

        # display "HP" text
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render(f'HP: {self.current_hp} / {self.max_hp}', True, black)
        text_rect = text.get_rect()
        text_rect.x = self.hp_x
        text_rect.y = self.hp_y + 30
        game.blit(text, text_rect)

    
    def get_rect(self):

        return Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

def display_message(message):

    # draw a white box with black border
    pygame.draw.rect(game, white, (10, 350, 480, 140))
    pygame.draw.rect(game, black, (10, 350, 480, 140), 3)

    # display the message
    font = pygame.font.Font(pygame.font.get_default_font(), 20)
    text = font.render(message, True, black)
    text_rect = text.get_rect()
    text_rect.x = 30
    text_rect.y = 410
    game.blit(text, text_rect)

    pygame.display.update()

def create_button(width, height, left, top, text_cx, text_cy, label):

    # position of the mouse cursor
    mouse_cursor = pygame.mouse.get_pos()

    button = Rect(left, top, width, height)

    # highlight the button if mouse is pointing to it
    if button.collidepoint(mouse_cursor):
        pygame.draw.rect(game, gold, button)
    else:
        pygame.draw.rect(game, white, button)

    # add the label to the button
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render(f'{label}', True, black)
    text_rect = text.get_rect(center=(text_cx, text_cy))
    game.blit(text, text_rect)

    return button

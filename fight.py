import pygame, sys # this imports pygame
from pygame.locals import * # imports pygame Rect which basicaly stores rectangular coordinates
import random # this imports random - randomness is key in a game like this
import time # this imports time - for time between attacks and stuff
import math # this imports math

pygame.init()

# the game window
game_width = 500
game_height = 500
size = (game_width, game_height)
game = pygame.display.set_mode(size)
pygame.display.set_caption("Dynamon Battle")

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

        display_message(f'{self.name} used {move.name}')

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


# create the starter dynamons
level = 30
kickflik = Dynamon('Kickflick', level, 25, 150) # used mine and fairbanks old program to help me make this - thats why some dynamon content was accidently written in my last commit
torchip = Dynamon('Torchip', level, 175, 150)
snorky = Dynamon('Snorky', level, 325, 150)
dynamons = [kickflik, torchip, snorky]

# the player's and rival's selected dynamon
# none means no value but still makes it a variable for later :)
player_dynamon = None
rival_dynamon = None

# game loop
game_status = 'select dynamon'
while game_status != 'quit':

    for event in pygame.event.get():
        if event.type == QUIT:
            game_status = 'quit'

        # detect keypress
        if event.type == KEYDOWN:

            # play again
            if event.key == K_y:
                # reset the dynamons
                kickflik = Dynamon('Kickflick', level, 25, 150)
                torchip = Dynamon('Torchip', level, 175, 150)
                snorky = Dynamon('Snorky', level, 325, 150)
                dynamons = [kickflik, torchip, snorky]
                game_status = 'select dynamon'

            # quit
            elif event.key == K_n:
                game_status = 'quit'


        # detect mouse click
        if event.type == MOUSEBUTTONDOWN:

            # coordinates of the mouse click
            mouse_click = event.pos

            # for selecting a dynamon
            if game_status == 'select dynamon':

                # check which dynamon was clicked on
                for i in range(len(dynamons)):

                    if dynamons[i].get_rect().collidepoint(mouse_click):

                        # assign the player's and rival's dynamon
                        player_dynamon = dynamons[i]
                        rival_dynamon = dynamons[(i + 1) % len(dynamons)]

                        # lower the rival dynamon's level to make the battle easier
                        rival_dynamon.level = int(rival_dynamon.level * .75)

                        # set the coordinates of the hp bars
                        player_dynamon.hp_x = 275
                        player_dynamon.hp_y = 250
                        rival_dynamon.hp_x = 50
                        rival_dynamon.hp_y = 50

                        game_status = 'prebattle'

            # for selecting fight or use potion
            elif game_status == 'player turn':

                # check if fight button was clicked
                if fight_button.collidepoint(mouse_click):
                    game_status = 'player move'

                # check if potion button was clicked
                if potion_button.collidepoint(mouse_click):

                    # force to attack if there are no more potions
                    if player_dynamon.num_potions == 0:
                        display_message('No more potions left')
                        time.sleep(2)
                        game_status = 'player move'
                    else:
                        player_dynamon.use_potion()
                        display_message(f'{player_dynamon.name} used potion')
                        time.sleep(2)
                        game_status = 'rival turn'

            # for selecting a move
            elif game_status == 'player move':

                # check which move button was clicked
                for i in range(len(move_buttons)):
                    button = move_buttons[i]

                    if button.collidepoint(mouse_click):
                        move = player_dynamon.moves[i]
                        player_dynamon.perform_attack(rival_dynamon, move)

                        # check if the rival's dynamon fainted
                        if rival_dynamon.current_hp == 0:
                            game_status = 'fainted'
                        else:
                            game_status = 'rival turn'

    if game_status == 'prebattle':
    
        # draw the selected dynamon
        game.fill(white)
        player_dynamon.draw()
        pygame.display.update()

        player_dynamon.set_moves()
        rival_dynamon.set_moves()

        # reposition the dynamons
        player_dynamon.x = -50
        player_dynamon.y = 100
        rival_dynamon.x = 250
        rival_dynamon.y = -50

        # resize the sprites
        player_dynamon.size = 300
        rival_dynamon.size = 300
        player_dynamon.set_sprite('back_default')
        rival_dynamon.set_sprite('front_default')

        game_status = 'start battle'

    # start battle animation
    if game_status == 'start battle':

        # rival sends out their dynamon
        alpha = 0
        while alpha < 255:

            game.fill(white)
            rival_dynamon.draw(alpha)
            display_message(f'Rival sent out {rival_dynamon.name}!')
            alpha += .4

            pygame.display.update()

        # pause for 1 second
        time.sleep(1)

        # player sends out their dynamon
        alpha = 0
        while alpha < 255:

            game.fill(white)
            rival_dynamon.draw()
            player_dynamon.draw(alpha)
            display_message(f'Go {player_dynamon.name}!')
            alpha += .4

            pygame.display.update()

        # draw the hp bars
        player_dynamon.draw_hp()
        rival_dynamon.draw_hp()

        # who goes first
        if rival_dynamon.speed > player_dynamon.speed:
            game_status = 'rival turn'
        else:
            game_status = 'player turn'

        pygame.display.update()

        # pause for 1 second
        time.sleep(1)

    # display the fight and use potion buttons
    if game_status == 'player turn':

        game.fill(white)
        player_dynamon.draw()
        rival_dynamon.draw()
        player_dynamon.draw_hp()
        rival_dynamon.draw_hp()

        # create the fight and use potion buttons
        fight_button = create_button(240, 140, 10, 350, 130, 412, 'Fight')
        potion_button = create_button(240, 140, 250, 350, 370, 412, f'Use Potion ({player_dynamon.num_potions})')

        # draw the black border
        pygame.draw.rect(game, black, (10, 350, 480, 140), 3)

        pygame.display.update()

    # display the move buttons
    if game_status == 'player move':

        game.fill(white)
        player_dynamon.draw()
        rival_dynamon.draw()
        player_dynamon.draw_hp()
        rival_dynamon.draw_hp()

        # create a button for each move
        move_buttons = []
        for i in range(len(player_dynamon.moves)):
            move = player_dynamon.moves[i]
            button_width = 240
            button_height = 70
            left = 10 + i % 2 * button_width
            top = 350 + i // 2 * button_height
            text_center_x = left + 120
            text_center_y = top + 35
            button = create_button(button_width, button_height, left, top, text_center_x, text_center_y, move.name.capitalize())
            move_buttons.append(button)

        # draw the black border
        pygame.draw.rect(game, black, (10, 350, 480, 140), 3)

        pygame.display.update()


    # rival selects a random move to attack with
    if game_status == 'rival turn':

        game.fill(white)
        player_dynamon.draw()
        rival_dynamon.draw()
        player_dynamon.draw_hp()
        rival_dynamon.draw_hp()

        # empty the display box and pause for 2 seconds before attacking
        display_message('')
        time.sleep(2)

        # select a random move
        move = random.choice(rival_dynamon.moves)
        rival_dynamon.perform_attack(player_dynamon, move)

        # check if the player's dynamon fainted
        if player_dynamon.current_hp == 0:
            game_status = 'fainted'
        else:
            game_status = 'player turn'

        pygame.display.update()

    # one of the dynamons fainted
    if game_status == 'fainted':

        alpha = 255
        while alpha > 0:

            game.fill(white)
            player_dynamon.draw_hp()
            rival_dynamon.draw_hp()

            # determine which dynamon fainted
            if rival_dynamon.current_hp == 0:
                player_dynamon.draw()
                rival_dynamon.draw(alpha)
                display_message(f'{rival_dynamon.name} fainted!')
            else:
                player_dynamon.draw(alpha)
                rival_dynamon.draw()
                display_message(f'{player_dynamon.name} fainted!')
            alpha -= .4

            pygame.display.update()

        game_status = 'gameover'

    # gameover :(
    if game_status == 'gameover':
        display_message('Play again (Y/N)?')

pygame.quit()
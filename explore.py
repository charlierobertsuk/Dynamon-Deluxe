import pygame, sys # this imports pygame and system parameters
from random import randint # imports randint but not all the other random stuff

# tree class
class Tree(pygame.sprite.Sprite):
	def __init__(self,pos,group):
		super().__init__(group)
		self.image = pygame.image.load('graphics/tree.png').convert_alpha() # finds the tree image in the graphics folder
		self.rect = self.image.get_rect(topleft = pos) # coordinate of the image is set to the tom left

#player class
class Player(pygame.sprite.Sprite):
    def __init__(self,pos,group):
        super().__init__(group)

        # selects a random gender for the player
        randgender = randint (1,2)
        if randgender == 1:
            self.image = pygame.image.load('graphics/player-m.png').convert_alpha() # finds the player image in the graphics folder
        else:
            self.image = pygame.image.load('graphics/player-w.png').convert_alpha() # finds the player image in the graphics folder

        self.rect = self.image.get_rect(center = pos) # center the image on a given coordinate
        self.direction = pygame.math.Vector2()
        self.speed = 5 # gives player a set speed
            
    def input(self):
        keys = pygame.key.get_pressed() # press a key on the keyboard

        # this is all using wasd to move in the correct directions

        # y coordinates - up and down
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        # x coordinates - left and right
        if keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0
    
    # updates the speed of the player
    def update(self):
        self.input()
        self.rect.center += self.direction * self.speed

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.ground_surface = pygame.image.load("graphics/ground.png").convert_alpha() # add the ground to the world
        self.ground_rect = self.ground_surface.get_rect(topleft = (0, 0))

    def custom_draw(self): # ysort camera - so basicaly the player can now move in front and behind a tree for example to make a sorta fake 3d feel to the world

        # ground
        self.display_surface.blit(self.ground_surface,self.ground_rect) # displays the background

        # active elements
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery): # lambda is an anonymous function without a name - this line sorts the sprites layers
            screen.blit(sprite.image,sprite.rect)

# initiating pygame with the screen size and the clock
pygame.init()
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()

# setup
camera_group = CameraGroup() # linking the camera_group variable to the CameraGroup class
Player((640,360), camera_group) # player starting position

# rendom tree generation
for i in range(20):
    random_x=randint(0,1000)
    random_y=randint(0,1000)
    Tree((random_x,random_y), camera_group)

# game loop - literaly wont run for more than a second without this loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill("#71ddee") # Blue water colour to act as the ocean surrounding the map

    camera_group.update()
    camera_group.custom_draw()

    pygame.display.update()
    clock.tick(60) # fps
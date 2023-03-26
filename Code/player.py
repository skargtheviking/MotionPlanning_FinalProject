# Source: https://github.com/gurb/rpg-game-tutorials/blob/main/004-Generating%20Tile%20Map/player.py
import pygame
import time
import settings
from tilemap import *

TILE_SIZE = settings.TILE_SIZE  ## Gets the size of the tile from the settings file and sets it as a global variable

##############################################################################################################################################################################################################################
#### Things to add to player
####    - Can only go through doors if both tiles match doors
####    - Pick up and keep track of tokens
####    - Pick up event tokens
####    - Player sprite
####    - Win Condition and display
####    - Astar with backpath (actions taken)
####    - Have the player build the map as they go
##############################################################################################################################################################################################################################
def create_player_texture(name):
    image = pygame.transform.scale(name,(TILE_SIZE/4,TILE_SIZE/4))                  ## scales the image to 1/4 of a tile size
    return image                                                                    ## return the token image


class Player(pygame.sprite.Sprite):
    def __init__(self, sprites_group, pos, dim, col):
        self.groups = sprites_group
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = pygame.image.load("Images/Player/GreenKnight.png")
        self.image = create_player_texture(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.Green_Token = 0
        self.Red_Token = 0
        self.Blue_Token = 0

    def update(self):
        self.get_event()

    def get_event(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.move(0, -TILE_SIZE)
            # check if legal move
            # door.north == true and above & dor.south == true allow up
        if keys[pygame.K_s]:
            self.move(0, +TILE_SIZE)
        if keys[pygame.K_a]:
            self.move(-TILE_SIZE, 0)
        if keys[pygame.K_d]:
            self.move(+TILE_SIZE, 0)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        time.sleep(0.5)

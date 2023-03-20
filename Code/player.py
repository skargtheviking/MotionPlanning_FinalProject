## Source: https://github.com/gurb/rpg-game-tutorials/blob/main/004-Generating%20Tile%20Map/player.py
import pygame
import time

class Player(pygame.sprite.Sprite):
    def __init__(self, sprites_group, pos, dim, col, TILE_SIZE):
        self.groups = sprites_group
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = pygame.Surface(dim)
        self.image.fill(col)

        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.TILE_SIZE = TILE_SIZE

    def update(self):
        self.get_event()

    def get_event(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.move(0, -self.TILE_SIZE)
            # check if legal move
            # door.north == true and above & dor.south == true allow up
        if keys[pygame.K_s]:
            self.move(0, +self.TILE_SIZE)
        if keys[pygame.K_a]:
            self.move(-self.TILE_SIZE, 0)
        if keys[pygame.K_d]:
            self.move(+self.TILE_SIZE, 0)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        time.sleep(0.5)

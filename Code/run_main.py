## Source: https://www.letsdevelopgames.com/2021/02/generating-tile-map.html
## Source: https://github.com/gurb/rpg-game-tutorials/blob/main/004-Generating%20Tile%20Map/main.py
import pygame
import random

from player import Player
from tilemap import *

# we initialize pygame module
pygame.init()

clock = pygame.time.Clock()

# dimension of each tiles
TILE_SIZE = 128

# create a surface represent our window
screen = pygame.display.set_mode((640, 640))

sprites_group = pygame.sprite.Group()

player = Player(sprites_group, screen.get_rect().center, (25,25), (0,0,255), TILE_SIZE)

map_data = generate_map(640, 640, TILE_SIZE)

## with a ceter piece if everything goes in a straight line it is 29 + 28 = 57
## Though with turning corners the max possible length a tunnel can go is 22 tiles
## So 22 + 21 for the other direction = 43 x 43 tile is all we need
# 640 for 9 x 9 for 128
# 340 for 3 x 3 for 128
# 5504 for 43 x 43 for 128
# 2752 for 43 x 43 for 64
# 1376 for 43 x 43 for 32
# 7296 for 57 x 57 for 128

def main():
    running = True
    # the game loop
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # draw
        screen.fill((255,255,255))
        draw_map(screen, map_data, TILE_SIZE)
        sprites_group.draw(screen)


        # update
        sprites_group.update()
        pygame.display.flip()

if __name__ == "__main__":
    main()

pygame.quit()
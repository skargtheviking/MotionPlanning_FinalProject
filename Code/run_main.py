## Source: https://www.letsdevelopgames.com/2021/02/generating-tile-map.html
## Source: https://github.com/gurb/rpg-game-tutorials/blob/main/004-Generating%20Tile%20Map/main.py
from re import T
import pygame
import random
from player import Player
from tilemap import *
import settings

# we initialize pygame module
pygame.init()

clock = pygame.time.Clock()

# dimension of each tiles
TILE_SIZE = settings.TILE_SIZE  ## Gets the size of the tile from the settings file and sets it as a global variable


#map_data = generate_map(640, 640, TILE_SIZE)
map_data, max_mins = building_map(9*128, 9*128, TILE_SIZE)

# create a surface represent our window
screen = pygame.display.set_mode((9*TILE_SIZE, 9*TILE_SIZE))

sprites_group = pygame.sprite.Group()

player = Player(sprites_group, screen.get_rect().center, (TILE_SIZE/4,TILE_SIZE/4), (0,0,255))

## with a ceter piece if everything goes in a straight line it is 29 + 28 = 57
## Though with turning corners the max possible length a tunnel can go is 22 tiles
## So 22 + 21 for the other direction = 43 x 43 tile is all we need
# 640 for 5 x 5 for 128
# 340 for 3 x 3 for 128
# 5504 for 43 x 43 for 128
# 2752 for 43 x 43 for 64
# 1376 for 43 x 43 for 32
# 800 for 25 x 25 for 32
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
        draw_map(screen, map_data, max_mins, TILE_SIZE)
        sprites_group.draw(screen)


        # update
        sprites_group.update()
        pygame.display.flip()

if __name__ == "__main__":
    main()

pygame.quit()
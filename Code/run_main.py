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
TILE_SIZE = settings.TILE_SIZE      ## Gets the size of the tile from the settings file and sets it as a global variable
height = 43                         ## sets the estimated hight of the map
width = 43                          ## sets the estimated width of the map

#map_data = generate_map(640, 640, TILE_SIZE)
map_data, max_mins = building_random_map(width, height)

##################################################
############# Premade Map ########################
##################################################
### enter the tile number (base 10) into tile_order
#tile_order = [[16, 20, 4], [2, 1, 6], [23, 12, 15]]

### enter the where you want the top of the tile to be at (U at top, D at bottom, L on the left, and R on the right)
#direction_order = [["U", "U", "D"], ["L", "R", "D"], ["U", "U", "U"]]

### Determines where each tile is on the map
#map_data, max_mins = building_premade_map(height, width, tile_order, direction_order)   

##################################################
############# End Of Premade Map #################
##################################################

# create a surface represent our window
screen = pygame.display.set_mode((max_mins[1]*TILE_SIZE, max_mins[0]*TILE_SIZE))

sprites_group = pygame.sprite.Group()

player = Player(sprites_group, map_data)

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
        draw_map(screen, map_data, TILE_SIZE)
        sprites_group.draw(screen)

        # update
        sprites_group.update()
        pygame.display.flip()

if __name__ == "__main__":
    main()

pygame.quit()
## Source: https://www.letsdevelopgames.com/2021/02/generating-tile-map.html
## Source: https://github.com/gurb/rpg-game-tutorials/blob/main/004-Generating%20Tile%20Map/main.py
# PYGAME_HIDE_SUPPORT_PROMPT  = 1
# import os
# os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
# # PYGAME_HIDE_SUPPORT_PROMPT= ./my_code.py
# from os import environ
# environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
# import pygame

import contextlib
with contextlib.redirect_stdout(None):
    import pygame

from player import Player, create_player_texture
from tilemap import *
import settings
# os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


# dimension of each tiles
TILE_SIZE = settings.TILE_SIZE      ## Gets the size of the tile from the settings file and sets it as a global variable
height = 43                         ## sets the estimated hight of the map
width = 43                          ## sets the estimated width of the map

# we initialize pygame module
pygame.init()

clock = pygame.time.Clock()

################################################
################################################
############# KNOWN MAP ########################
################################################
################################################

##################################################
############# Premade Map ########################
##################################################
### enter the tile number (base 10) into tile_order
#tile_order = [[ 0,  3,  0,  0,  0,  0,  0],  [20, 10,  0,  0,  0,  0,  0], [16,  7,  0,  0, 13, 25, 0], [0, 24,  0,  0,  5,  1, 27], [ 0, 15,  0,  0,  4,  9, 29],  [ 0, 18, 26, 12, 14, 21, 0],  [ 0,  2, 22,  8, 19, 28,  0], [ 0,  0,  6, 23,  0,  0,  0], [ 0,  0, 17, 11, 0, 0,  0]]


##### enter the where you want the top of the tile to be at (U at top, D at bottom, L on the left, and R on the right)
#rotations = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 1], [0, 0, 0, 0, 3, 0, 2], [0, 0, 0, 0, 0, 0, 0], [0, 2, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]

#### Determines where each tile is on the map
#map_data, max_mins = building_premade_map(tile_order, rotations)   

##################################################
############# End Of Premade Map #################
##################################################

#################################################
############# Random Map ########################
#################################################

#map_data = generate_map(640, 640, TILE_SIZE)
map_data, max_mins = building_random_map(width, height)

#################################################
############# End Of Random Map #################
#################################################

## create a surface represent our window
screen = pygame.display.set_mode((max_mins[1]*TILE_SIZE, max_mins[0]*TILE_SIZE+TILE_SIZE))

sprites_group = pygame.sprite.Group()

## Player Set up ##
'''
Player 1  = player, default settings if only one player
Player 2  = player2, once a second player is added, must manually set all player settings
'''

### 1 Player
#player = Player(sprites_group, map_data)

## 2 Player
#player = Player(sprites_group, map_data)
#player2 = Player(sprites_group, map_data)
#player2.active = False
#player2.image = pygame.image.load("Images/Other/magic_meeple_games_makshift_token2.png") 
#player2.image = create_player_texture(player2.image)

#player.otherplayer = player2
#player2.otherplayer = player

### 3 Player
player = Player(sprites_group, map_data, 2, 3, 1)
player2 = Player(sprites_group, map_data, 3, 1, 2)
player2.active = False
player2.image = pygame.image.load("Images/Other/magic_meeple_games_makshift_token2.png") 
player2.image = create_player_texture(player2.image)
player3 = Player(sprites_group, map_data, 1, 2, 3)
player3.active = False
player3.image = pygame.image.load("Images/Other/magic_meeple_games_makshift_token3.png") 
player3.image = create_player_texture(player3.image)

player.otherplayer = player2
player2.otherplayer = player3
player3.otherplayer = player


### 4 Player
#player = Player(sprites_group, map_data, 2, 3, 1)
#player2 = Player(sprites_group, map_data, 3, 1, 2)
#player2.active = False
#player2.image = pygame.image.load("Images/Other/magic_meeple_games_makshift_token2.png") 
#player2.image = create_player_texture(player2.image)
#player3 = Player(sprites_group, map_data, 1, 2, 3)
#player3.active = False
#player3.image = pygame.image.load("Images/Other/magic_meeple_games_makshift_token3.png") 
#player3.image = create_player_texture(player3.image)
#player4 = Player(sprites_group, map_data, 3, 3, 3)
#player4.active = False
#player4.image = pygame.image.load("Images/Other/magic_meeple_games_makshift_token4.png") 
#player4.image = create_player_texture(player4.image)

#player.otherplayer = player2
#player2.otherplayer = player3
#player3.otherplayer = player4
#player4.otherplayer = player


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

################################################
################################################
############# END OF KNOWN MAP #################
################################################
################################################

###########################################################
################ Living (Unkown) Map ######################
###########################################################
##map_data = generate_map(640, 640, TILE_SIZE)
#map_data, max_mins = initalize_living_map(width, height)
#screen = pygame.display.set_mode((max_mins[1]*TILE_SIZE, max_mins[0]*TILE_SIZE))

#sprites_group = pygame.sprite.Group()

#player = Player(sprites_group, map_data)


#player = Player(sprites_group, map_data, True)

### with a ceter piece if everything goes in a straight line it is 29 + 28 = 57
### Though with turning corners the max possible length a tunnel can go is 22 tiles
### So 22 + 21 for the other direction = 43 x 43 tile is all we need
## 640 for 5 x 5 for 128
## 340 for 3 x 3 for 128
## 5504 for 43 x 43 for 128
## 2752 for 43 x 43 for 64
## 1376 for 43 x 43 for 32
## 800 for 25 x 25 for 32
## 7296 for 57 x 57 for 128
#n=3
#def main():
#    # create a surface represent our window
#    running = True
#    # the game loop
#    while running:
#        clock.tick(60)

#        for event in pygame.event.get():
#            if event.type == pygame.QUIT:
#                running = False
#        # draw
#        screen = pygame.display.set_mode((n*TILE_SIZE, n*TILE_SIZE))
#        screen.fill((255,255,255))
#        draw_map(screen, map_data, TILE_SIZE)
#        sprites_group.draw(screen)

#        # update
#        sprites_group.update()
#        pygame.display.flip()

#if __name__ == "__main__":
#    main()

#pygame.quit()

####################################################################
################### End of Living (Unkown) Map ######################
#####################################################################

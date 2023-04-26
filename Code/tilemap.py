## Source: https://github.com/gurb/rpg-game-tutorials/blob/main/004-Generating%20Tile%20Map/tilemap.py
from asyncio.windows_events import NULL
from distutils.command.check import check
import settings
import pygame
import random
import math
import numpy as np

# dimension of each tiles
TILE_SIZE = settings.TILE_SIZE                                                                          ## Gets the size of the tile from the settings file and sets it as a global variable
Names_of_Buildable = []                                                                                 ## keeps track of the names of the tiles that potentially can be built off of (avaliable neighbros and doors) and allows the program to quickly check if tile has been used
Buildable = []                                                                                          ## keeps track of the tiles (instances) that potentially can be built off of (avaliable neighbros and doors)
#placed = []                                                                                             ## determines the order palced (used for debugging)


## Turns the image into the tile texture according to the requested size
def create_texture(name):
    image = pygame.transform.scale(name,(TILE_SIZE,TILE_SIZE))                                          ## scales the image to tile size
    return image                                                                                        ## returns the tile image

## Turns the image into the tile texture according to the requested size
def create_token_texture(name):
    image = pygame.transform.scale(name,(TILE_SIZE/4,TILE_SIZE/4))                                      ## scales the image to 1/4 of a tile size
    return image                                                                                        ## return the token image

Token_Cultist = pygame.image.load("Images/Tokens/Cultist.png")                                          ## Gets the cultist image
Token_Red = pygame.image.load("Images/Tokens/Token_Red.png")                                            ## Gets the red token
Token_Green = pygame.image.load("Images/Tokens/Token_Green.png")                                        ## gets the green token
Token_Blue = pygame.image.load("Images/Tokens/Token_Blue.png")                                          ## gets the blue token
Token_RedEvent = pygame.image.load("Images/Tokens/Token_RedEvent.png")                                  ## Gets the red event token
Token_GreenEvent = pygame.image.load("Images/Tokens/Token_GreenEvent.png")                              ## gets the green evemt token
Token_BlueEvent = pygame.image.load("Images/Tokens/Token_BlueEvent.png")                                ## gets the blue event token
Token_RedEvent_Broken = pygame.image.load("Images/Tokens/Token_RedEvent_Broken.png")                    ## Gets the broken red event token
Token_GreenEvent_Broken = pygame.image.load("Images/Tokens/Token_GreenEvent_Broken.png")                ## gets the broken green evemt token
Token_BlueEvent_Broken = pygame.image.load("Images/Tokens/Token_BlueEvent_Broken.png")                  ## gets the broken blue event token
Token_FireofEidolon = pygame.image.load("Images/Tokens/Token_FireofEidolon.png")                        ## gets the Fire of Eidolon token

token_texture = {                                                                                       ## creates a dictionary of the token displays
    0x0 : create_token_texture(Token_Cultist),                                                          ## the cultists token
    0x1 : create_token_texture(Token_Red),                                                              ## the red token 
    0x2 : create_token_texture(Token_Green),                                                            ## the green token
    0x3 : create_token_texture(Token_Blue),                                                             ## the blue token
    0x4 : create_token_texture(Token_RedEvent),                                                         ## the red event token 
    0x5 : create_token_texture(Token_GreenEvent),                                                       ## the green event token
    0x6 : create_token_texture(Token_BlueEvent),                                                        ## the blue event token
    0x7 : create_token_texture(Token_FireofEidolon),                                                    ## the Fire of Eidolon token
    0x8: create_token_texture(Token_RedEvent_Broken),                                                   ## the broken red event token
    0x9: create_token_texture(Token_GreenEvent_Broken),                                                 ## the broken green event token
    0xa: create_token_texture(Token_BlueEvent_Broken),                                                  ## the broken blue event token
}

token_list = [0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xa]                                    ## reference list for the token dictionary

''' 
30 total tile types
Tiles are named as such: 
Assigned # _ type of tile _ name of tile _ Entrance Directions

Assigned # - Assigned based on first if it's a filler tile, then start tile, (since they have specific placement requirements for the program)
then event tiles, then special tiles, then number of doors, then direction of doors,
then color (Red, Green, Blue)

type of tiles - None: for Filler
                FireofEidolon: for the fire of Eidolon
                RedEvent, GreenEvent, BlueEvent: event of the color
                Start: starting tile
                End: ending Tile
                Secret: secret passage
                Red, Green, Blue: token color

Name of tile: name written on the tile.  All as one word (no spaces) with beginning of signifcant words capitalized

Entrance Directions: U: Up
                     D: Down
                     L: Left
                     R: Right

    presented as UDLR (i.e. DR means down and right)
    from perspective of above view with the name of the tile at the top of the tile

'''

## Creates a class for the tiles
class Tile:                                                                 
    def __init__(self, filepath, parent=None):                                                  ## initalizes the tile class with the path to the file
        ## Gets the image so it can display
        self.image = pygame.image.load(filepath)                                                ## loads the image in
        self.texture = create_texture(self.image)                                               ## creates the appropriate texture for the image
        self.children = []                                                                      ## inializes the children of said tile
        self.parent = parent                                                                    ## indicates the parent of said tile
        
        ## Gets the information hardwritten in the file's name
        self.quickinfo = []                                                                     ## a quick determine which doors are possible to go through
        filename = filepath.split("/")                                                          ## Cuts out all but the name of the image
        title = filename[2].split(".")                                                          ## Cuts out the .jpg or .png
        self.info = title[0].split("_")                                                         ## Breaks the name into useful information
        self.id = self.info[0]                                                                  ## Gets the info from the image name
        self.type = self.info[1]                                                                ## Determine what type of tile this is 
        self.name = self.info[2]                                                                ## Determine the name of the tile
        self.doors = self.info[3]                                                               ## Gets the data on the doors
        self.token = self.Token_grabber()                                                       ## grab the token texture
        self.row = 0                                                                            ## initializes the row
        self.column = 0                                                                         ## initializes the column
        self.secret()

        match self.doors:                                                                       ## determines which doors it has
            case "UDLR":                                                                        ## if it has all doors 
                self.quickinfo.append('u')
                self.quickinfo.append('d')
                self.quickinfo.append('l')
                self.quickinfo.append('r')

            
            case "UDL":                                                                         ## if it has the three doors with UDL
                self.quickinfo.append('u')
                self.quickinfo.append('d')
                self.quickinfo.append('l')
            
            case "UDR":                                                                         ## if it has the three doors with UDR
                self.quickinfo.append('u')
                self.quickinfo.append('d')
                self.quickinfo.append('r')

            case "DLR":                                                                         ## if it has the three doors with DLR
                self.quickinfo.append('d')
                self.quickinfo.append('l')
                self.quickinfo.append('r')

            case "UD":                                                                          ## if it has the two doors with UD
                self.quickinfo.append('u')
                self.quickinfo.append('d')

            case "DL":                                                                          ## if it has the two doors with DL
                self.quickinfo.append('d')
                self.quickinfo.append('l')

            case "DR":                                                                          ## if it has the two doors with DR
                self.quickinfo.append('d')
                self.quickinfo.append('r')

            case "D":                                                                           ## if it has the two doors with D
                self.quickinfo.append('d')


    ## adds a tile as a cild of said token    
    def add_child(self, child):                                                                 ## adds a child node to the tile
        '''
        Add a child node
        '''
        self.children.append(child)                                                             ## adds a connecting tile

    ## Determines what token the tile has    
    def Token_grabber(self):                                                                    ## Determines which token the tile should have
        match self.type:                                                                        ## checks the type listed in the tile's name
            case "Red":                                                                         ## if it's listed as red
                token_number = int(hex(token_list[1]), 16)                                      ## grab the red token
                self.quickinfo.append("rt")                                                     ## adds red token to the quick info
            case "Green":                                                                       ## if it's listed as green
                token_number = int(hex(token_list[2]), 16)                                      ## grab the green token
                self.quickinfo.append("gt")                                                     ## adds red token to the quick info
            case "Blue":                                                                        ## if it's listed as blue
                token_number = int(hex(token_list[3]), 16)                                      ## grab the blue token
                self.quickinfo.append("bt")                                                     ## adds red token to the quick info
            case "RedEvent":                                                                    ## if it's listed as red event
                token_number = int(hex(token_list[4]), 16)                                      ## grab the red event token
                self.quickinfo.append("ret")                                                    ## adds red event token to the quick info
            case "GreenEvent":                                                                  ## if it's listed as green event 
                token_number = int(hex(token_list[5]), 16)                                      ## grab the green event token
                self.quickinfo.append("get")                                                    ## adds red event token to the quick info
            case "BlueEvent":                                                                   ## if it's listed as blue event
                token_number = int(hex(token_list[6]), 16)                                      ## grab the blue event token
                self.quickinfo.append("bet")                                                    ## adds blue event token to the quick info
            case "FireofEidolon":                                                               ## if it's listed as Fire of Eidolon
                token_number = int(hex(token_list[7]), 16)                                      ## grab the Fire of Eidolon token
                self.quickinfo.append("foe")                                                    ## adds Fire of Eidolon token to the quick info
            case "Broken_RedEvent":                                                             ## if it's listed as broken red event
                token_number = int(hex(token_list[8]), 16)                                      ## grab the broken red event token
            case "Broken_GreenEvent":                                                           ## if it's listed as broken green event 
                token_number = int(hex(token_list[9]), 16)                                      ## grab the broken green event token
            case "Broken_BlueEvent":                                                            ## if it's listed as broken blue event
                token_number = int(hex(token_list[10]), 16)                                     ## grab the broken blue event token
            case _:                                                                             ## if no tile is listed
                token_number = None                                                             ## it does not have a token number
        if token_number == None:                                                                ## if there is no token number
            token = None                                                                        ## there is no token
        else:                                                                                   ## otherwise
            token = token_texture[token_number]                                                 ## grab the texture for the token
        return token                                                                            ## return the texture for the token

    ## Rotates the image and the doors clockwise
    def rotate_clockwise(self):                                                                 ## rotates the image and doors clockwise
        ## rotate image
        self.image = pygame.transform.rotate(self.image, -90)                                   ## takes the existing image and rotates it by 90 degrees clockwise
        self.texture = create_texture(self.image)                                               ## creates the appropriate texture for the image
        
        ## rotate doors (Doesn't need to rotate if its "UDLR" or None doors)
        if self.doors == "UDL" or self.doors == "UDR" or self.doors == "DLR":                   ## if it has three doors
            if "u" in self.quickinfo and "l" in self.quickinfo and "d" in self.quickinfo:       ## if in the UDL position
                self.quickinfo.remove("d")                                                      ## move to the URL position
                self.quickinfo.append("r")

            elif "r" in self.quickinfo and "u" in self.quickinfo and "l" in self.quickinfo:     ## if in the URL position
                self.quickinfo.remove("l")                                                      ## move to the UDR position
                self.quickinfo.append("d")

            elif "d" in self.quickinfo and "r" in self.quickinfo and "u" in self.quickinfo:     ## if in the UDR position
                self.quickinfo.remove("u")                                                      ## move to the DLR position
                self.quickinfo.append("l"
                                      )
            elif "l" in self.quickinfo and "d" in self.quickinfo and "r" in self.quickinfo:     ## if in the UDR position
                self.quickinfo.remove("r")                                                      ## move to the UDL position
                self.quickinfo.append("u")

        elif self.doors == "UD" or self.doors == "DL" or self.doors == "DR":                    ## if it has two doors
            if "u" in self.quickinfo and "d" in self.quickinfo:                                 ## if in the UD position
                self.quickinfo.remove("u")                                                      ## move to the LR position
                self.quickinfo.remove("d")
                self.quickinfo.append("l")
                self.quickinfo.append("r")

            elif "l" in self.quickinfo and "r" in self.quickinfo:                               ## if in the LR position
                self.quickinfo.remove("l")                                                      ## move to the UD position
                self.quickinfo.remove("r")
                self.quickinfo.append("d")
                self.quickinfo.append("u")

            elif "d" in self.quickinfo and "l" in self.quickinfo:                               ## if in the DL position
                self.quickinfo.remove("d")                                                      ## move to the UL position
                self.quickinfo.append("u")

            elif "l" in self.quickinfo and "u" in self.quickinfo:                               ## if in the UL position
                self.quickinfo.remove("l")                                                      ## move to the UR position
                self.quickinfo.append("r")

            elif "u" in self.quickinfo and "r" in self.quickinfo:                               ## if in the UR position
                self.quickinfo.remove("u")                                                      ## move to the DR position
                self.quickinfo.append("d")

            elif "r" in self.quickinfo and "d" in self.quickinfo:                               ## if in the DR position
                self.quickinfo.remove("r")                                                      ## move to the DL position
                self.quickinfo.append("l")

        elif self.doors == "D":                                                                 ## if it has one door
            if "d" in self.quickinfo:                                                           ## if in the D position
                self.quickinfo.remove("d")                                                      ## move to the L position
                self.quickinfo.append("l")

            elif "l" in self.quickinfo:                                                         ## if in the L position
                self.quickinfo.remove("l")                                                      ## move to the U position
                self.quickinfo.append("u")

            elif "u" in self.quickinfo:                                                         ## if in the U position
                self.quickinfo.remove("u")                                                      ## move to the R position
                self.quickinfo.append("r")

            elif "u" in self.quickinfo:                                                         ## if in the R position
                self.quickinfo.remove("r")                                                      ## move to the D position
                self.quickinfo.append("d")

    ## checks its neighbors and doors to see if there is a space to build off from
    def check_neighbors(self, map_data):                                                        ## checks if there is a space to build off from
        if (map_data[self.row+1][self.column] == 0 and "d" in self.quickinfo) or (              ## is there a space that has both a door avaliable and a empty tile space
            map_data[self.row-1][self.column] == 0 and "u" in self.quickinfo) or (
            map_data[self.row][self.column+1] == 0 and "r" in self.quickinfo) or (
            map_data[self.row][self.column-1] == 0 and "l" in self.quickinfo):

            if self.name not in Names_of_Buildable:                                             ## if the working tile isn't already part of the list
                Buildable.append(self)                                                          ## adds the class instance to the list
                Names_of_Buildable.append(self.name)                                            ## adds the name of the class instances in buildable for quick comparison searches

    ## checks if the tile is a secret tile
    def secret(self):
        if self.name == "SecretX":                                                              ## if it's the secret X tile
            self.quickinfo.append("x")                                                          ## save info in quickinfo as x
        elif self.name == "SecretY":                                                            ## if its the secret y tile
            self.quickinfo.append("y")                                                          ## save info in quickinfo as y

## Linking the names of the tiles with the location of the images
BackTile = Tile("Images/Tile_Scans/0_None_BackTile_None.jpg")
StartTile = Tile("Images/Tile_Scans/1_Start_StartTile_UDLR.jpg")
FireofEidolon = Tile("Images/Tile_Scans/2_FireofEidolon_FireofEidolon_D.jpg")
VoraxsHeart = Tile("Images/Tile_Scans/3_RedEvent_VoraxsHeart_D.jpg")
VoraxFocus = Tile("Images/Tile_Scans/4_GreenEvent_VoraxFocus_D.jpg")
VoraxsKnowledge = Tile("Images/Tile_Scans/5_BlueEvent_VoraxsKnowledge_D.jpg")
EndTile = Tile("Images/Tile_Scans/6_End_EndTile_UDLR.jpg")
SecretX = Tile("Images/Tile_Scans/7_Secret_SecretX_UDLR.jpg")
SecretY = Tile("Images/Tile_Scans/8_Secret_SecretY_UDLR.jpg")
VoraciousPlant = Tile("Images/Tile_Scans/9_Red_VoraciousPlant_UDLR.jpg")
Minotaur = Tile("Images/Tile_Scans/10_Red_Minotaur_UDLR.jpg")
FloatingStones = Tile("Images/Tile_Scans/11_Green_FloatingStones_UDLR.jpg")
LaughingShadow = Tile("Images/Tile_Scans/12_Blue_LaughingShadow_UDLR.jpg")
Psychomancer = Tile("Images/Tile_Scans/13_Blue_Psychomancer_UDLR.jpg")
Dragonling = Tile("Images/Tile_Scans/14_Red_Dragonling_UDL.jpg")
ParadoxPuzzle = Tile("Images/Tile_Scans/15_Blue_ParadoxPuzzle_UDL.jpg")
FelKnight = Tile("Images/Tile_Scans/16_Red_FelKnight_UDR.jpg")
SpikedPit = Tile("Images/Tile_Scans/17_Green_SpikedPit_UDR.jpg")
DenofSnakes = Tile("Images/Tile_Scans/18_Green_DenofSnakes_UDR.jpg")
ArrowTrap = Tile("Images/Tile_Scans/19_Green_ArrowTrap_DLR.jpg")
Mindeater = Tile("Images/Tile_Scans/20_Blue_Mindeater_DLR.jpg")
SkeletalGuards = Tile("Images/Tile_Scans/21_Red_SkeletalGuards_UD.jpg")
PendulumBlades = Tile("Images/Tile_Scans/22_Green_PendulumBlades_UD.jpg")
AcidJets = Tile("Images/Tile_Scans/23_Green_AcidJets_UD.jpg")
SphynxsRiddle = Tile("Images/Tile_Scans/24_Blue_SphynxsRiddle_UD.jpg")
OgreBrute = Tile("Images/Tile_Scans/25_Red_OgreBrute_DL.jpg")
LavaLake = Tile("Images/Tile_Scans/26_Green_LavaLake_DL.jpg")
DarkSlime = Tile("Images/Tile_Scans/27_Red_DarkSlime_DR.jpg")
HallofIllusion = Tile("Images/Tile_Scans/28_Blue_HallofIllusion_DR.jpg")
MimicChest = Tile("Images/Tile_Scans/29_Blue_MimicChest_D.jpg")

## Assigning values to the tile for the computer to run through them
## Values in Hexidecimal
tile_textures = {
    0x0 : BackTile,
    0x1 : StartTile,
    0x2 : FireofEidolon,
    0x3 : VoraxsHeart,
    0x4 : VoraxFocus,
    0x5 : VoraxsKnowledge,
    0x6 : EndTile,
    0x7 : SecretX,
    0x8 : SecretY,
    0x9 : VoraciousPlant,
    0xa : Minotaur,
    0xb : FloatingStones,
    0xc : LaughingShadow,
    0xd : Psychomancer,
    0xe : Dragonling,
    0xf : ParadoxPuzzle,
    0x10 : FelKnight,
    0x11 : SpikedPit,
    0x12 : DenofSnakes,
    0x13 : ArrowTrap,
    0x14 : Mindeater,
    0x15 : SkeletalGuards,
    0x16 : PendulumBlades,
    0x17 : AcidJets,
    0x18 : SphynxsRiddle,
    0x19 : OgreBrute,
    0x1a : LavaLake,
    0x1b : DarkSlime,
    0x1c : HallofIllusion,
    0x1d : MimicChest
}

## Turns the values of the tile into a list
tiles = [0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xa, 0xb, 0xc, 0xd, 0xe, 0xf, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d]

##############################################################################################################################################################################################################################
#### Things to add to tile map
####    - have function that allows the player to build the map as they go
##############################################################################################################################################################################################################################

## initalizing player builds map as they go
def initalize_living_map(width, height):
    ## initilizing variables                                               
    used = []                                                                                                       ## initializes the list for the tiles already used
    map_data = []                                                                                                   ## Keeps track of what tile is in each location
    
    ## initializes map
    for i in range(height):                                                                                         ## This is the row
        map_data.append([])                                                                                         ## making the map_data a row x column calling
        for j in range(width):                                                                                      ## This is the column
            if i == (math.trunc((height)/2)) and j == (math.trunc((width)/2)):                                      ## if the tile in question is at the center
                rand_index = 1                                                                                      ## put the start tile there (setting rand to 1)
            else:                                                                                                   ## if the tile has been used before
                rand_index = 0                                                                                      ## put in the filler tile to create a blank map
            tile = int(hex(tiles[rand_index]), 16)                                                                  ## get the tile information after converting to hex from intiger value
            map_data[i].append(tile)                                                                                ## add teh tile to the map

    max_mins = [height, width]                                                                                      ## stores the new dimensiosn of the new map in an easy access list
    return map_data, max_mins

##################################################
############# Pre-Determined Map #################
##################################################

## building a pre-determined map    
def building_premade_map(tile_order, rotations):
    height = len(tile_order)                                                                                        ## determine height of the map
    width = len(tile_order[0])                                                                                      ## determine width of the map
    #print(height, width)                                                                                            ## used for debugging
    map_data = np.empty((height, width))                                                                            ## Keeps track of what tile is in each location
    map_rotations = np.zeros((height, width), dtype = int)                                                          ## Keeps track of the direction each tile is facing in each location

    for row in range(height):                                                                                       ## goes over each row
        for column in range(width):                                                                                 ## goes over each column
            spins = rotations[row][column]                                                                          ## gets the number of times it was clockwise rotated
            map_data[row][column] = int(hex(tiles[tile_order[row][column]]), 16)                                    ## stores the tile varilable in its location in the map data
            New_Tile = tile_textures[map_data[row][column]]                                                         ## Calls forth the new tile
            New_Tile.row = row                                                                                      ## tells tile where its row is located in the map
            New_Tile.column = column                                                                                ## tells tile where its column is located in the map
            map_rotations[row][column] = spins                                                                      ## adds direction to the map_rotations                
            while spins > 0:                                                                                        ## reads in the direction
                New_Tile.rotate_clockwise()                                                                         ## rotates the tile clockwise
                spins -= 1                                                                                          ## counts down the number of spins needed

    new_height = len(map_data)                                                                                      ## determines the new_height of the new map
    new_width = len(map_data[0])                                                                                    ## determines the new_wideth of the new map

    max_mins = [new_height, new_width]                                                                              ## stores the new dimensiosn of the new map in an easy access list
    return map_data, max_mins                                                                                       ## returns the map data

##################################################
############# End of Pre-Determined Map ##########
##################################################

#################################################
############# Random Map ########################
#################################################

## building a randomly generated map from center point
def building_random_map(width, height):
    ## initilizing variables                                               
    used = []                                                                                                       ## initializes the list for the tiles already used
    map_data = []                                                                                                   ## Keeps track of what tile is in each location

    map_rotations = np.zeros((height, width), dtype = int)                                                          ## Keeps track of the direction each tile is facing in each location

    ## initializes map
    for i in range(height):                                                                                         ## This is the row
        map_data.append([])                                                                                         ## making the map_data a row x column calling
        for j in range(width):                                                                                      ## This is the column
            if i == (math.trunc((height)/2)) and j == (math.trunc((width)/2)):                                      ## if the tile in question is at the center
                rand_index = 1                                                                                      ## put the start tile there (setting rand to 1)
            else:                                                                                                   ## if the tile has been used before
                rand_index = 0                                                                                      ## put in the filler tile to create a blank map
            tile = int(hex(tiles[rand_index]), 16)                                                                  ## get the tile information after converting to hex from intiger value
            map_data[i].append(tile)                                                                                ## add teh tile to the map

    row = math.trunc((height)/2)                                                                                    ## Start at the center row point
    column = math.trunc((width)/2)                                                                                  ## Start at the center column point

    max_row = row                                                                                                   ## initalizes the max row
    max_column = column                                                                                             ## initalizes the max column
    min_row = row                                                                                                   ## initalizes the min row
    min_column = column                                                                                             ## initalizes the min column
    #print("row and column min max ", min_row, max_row, min_column, max_column)                                      ## used for debugging

    ## Inializes the working tile and records its location
    Working_Tile = tile_textures[map_data[row][column]]                                                             ## indicates this is the working tile
    Working_Tile.row = row                                                                                          ## tells the tile the row its on
    Working_Tile.column = column                                                                                    ## tells the tile the column its on
    
    #number = 0                                                                                                     ## used for debugging tiles
    #testing_direction = [2, 3, 1, 4]                                                                               ## used for debugging directions
    while len(used) <= 27:                                                                                          ## should run until all 27 tiles have been added (not counting start or blank)
        #num_dir = 0                                                                                                 ## used for debugging directions
        #print(len(used))                                                                                            ## debug check to see if all tiles have been used
        walled = True                                                                                               ## if there is a wall going in that direction
        direction = "N"                                                                                             ## which direction is the previous tile
        checked_directions = []                                                                                     ## keeps track of which directions checked
        rand_direction = random.randint(1,4)                                                                        ## generate a random direction
        #rand_direction = testing_direction[num_dir]                                                                 ## used for debugging directions
        match rand_direction:                                                                                       ## picking a random direction
            case 1:                                                                                                 ## randomly moving up
                new_row = row - 1                                                                                   ## Move up by one tile
                new_column = column                                                                                 ## column stays the same
                direction = "U"                                                                                     ## indciates working tile is one space down
                if 'u' in Working_Tile.quickinfo and map_data[new_row][new_column] == 0:                            ## if the current tile has an up door and there isn't a tile already there
                    walled = False                                                                                  ## no longer walled
                #print("name ", Working_Tile.name)                                                                   ## used for debugging
                #print("doors_labeled", Working_Tile.doors)                                                          ## used for debugging
                #print("direction ", direction)                                                                      ## used for debugging
                #print("Door? ", Working_Tile.up)                                                                    ## used for debugging

            case 2:                                                                                                 ## randomly movign down
                new_row = row + 1                                                                                   ## Move down by one tile
                new_column = column                                                                                 ## column stays the same
                direction = "D"                                                                                     ## indciates working tile is one space up
                if 'd' in Working_Tile.quickinfo and map_data[new_row][new_column] == 0:                            ## if the current tile has a down door and there isn't a tile already there
                    walled = False                                                                                  ## no longer walled
                #print("name ", Working_Tile.name)                                                                   ## used for debugging
                #print("doors_labeled", Working_Tile.doors)                                                          ## used for debugging
                #print("direction ", direction)                                                                      ## used for debugging
                #print("Door? ", Working_Tile.up)                                                                    ## used for debugging

            case 3:                                                                                                 ## randomly moving left
                new_row = row                                                                                       ## row stays the same
                new_column = column - 1                                                                             ## Move left by one tile
                direction = "L"                                                                                     ## indciates working tile is one space right
                if 'l' in Working_Tile.quickinfo and map_data[new_row][new_column] == 0:                            ## if the current tile has a left door and there isn't a tile already there
                    walled = False                                                                                  ## no longer walled
                #print("name ", Working_Tile.name)                                                                   ## used for debugging
                #print("doors_labeled", Working_Tile.doors)                                                          ## used for debugging
                #print("direction ", direction)                                                                      ## used for debugging
                #print("Door? ", Working_Tile.up)                                                                    ## used for debugging

            case 4:                                                                                                 ## randomly moving right
                new_row = row                                                                                       ## row stays the same
                new_column = column + 1                                                                             ## Move right by one tile
                direction = "R"                                                                                     ## indciates working tile is one space left
                if 'r' in Working_Tile.quickinfo and map_data[new_row][new_column] == 0:                            ## if the current tile has a right door and there isn't a tile already there
                    walled = False                                                                                  ## no longer walled
                #print("name ", Working_Tile.name)                                                                   ## used for debugging
                #print("doors_labeled", Working_Tile.doors)                                                          ## used for debugging
                #print("direction ", direction)                                                                      ## used for debugging
                #print("Door? ", Working_Tile.up)                                                                    ## used for debugging
        if new_row < 0 or new_column < 0:                                                                           ## if it goes negative
            walled = True                                                                                           ## prevents from wrapping around
        checked_directions.append(rand_direction)                                                                   ## Marks that we checked that direction
        #testing = [11, 3, 4, 16]                                                                                    ## used for debugging tiles
        ##print("checked_direction ", checked_directions)                                                            ## debug checks to see if all surrounding tiles are taken
        #print("walled '", walled)                                                                                   ## used for deubbing
        #print("taken '", map_data[new_row][new_column] != 0)                                                        ## used for deubbing
        #print("row ", row, "column", column)                                                                        ## checking the row and column for dubugging 
        #print("new_row ", new_row, "new_column ", new_column)                                                       ## checking the new row and new column for dubugging 
        
        while (walled == True or map_data[new_row][new_column] != 0)  and len(checked_directions) < 4:              ## if there was a wall in the way, the proposed space was already taken, and we havn't checked every direction run again
            rand_direction = random.randint(1,4)                                                                    ## generate a random direction
            while rand_direction in checked_directions:                                                             ## checks if the number has already been used
                rand_direction = random.randint(1, 4)                                                               ## if already been used get another random number and try again
            #num_dir = num_dir + 1                                                                                   ## used for debugging directions
            #rand_direction = testing_direction[num_dir]                                                             ## used for debugging directions
            match rand_direction:                                                                                   ## picking a random direction
                case 1:                                                                                             ## randomly moving up
                    new_row = row - 1                                                                               ## Move up by one tile
                    new_column = column                                                                             ## column stays the same
                    direction = "U"                                                                                 ## indciates working tile is one space down
                    if 'u' in Working_Tile.quickinfo and map_data[new_row][new_column] == 0:                        ## if the current tile has an up door and there isn't a tile already there
                        walled = False                                                                              ## no longer walled
                        #print("name ", Working_Tile.name)                                                           ## used for debugging
                        #print("doors_labeled", Working_Tile.doors)                                                  ## used for debugging
                        #print("direction ", direction)                                                              ## used for debugging
                        #print("Door? ", Working_Tile.up)                                                            ## used for debugging

                case 2:                                                                                             ## randomly movign down
                    new_row = row + 1                                                                               ## Move down by one tile
                    new_column = column                                                                             ## column stays the same
                    direction = "D"                                                                                 ## indciates working tile is one space up
                    if 'd' in Working_Tile.quickinfo and map_data[new_row][new_column] == 0:                        ## if the current tile has a down door and there isn't a tile already there
                        walled = False                                                                              ## no longer walled
                        #print("name ", Working_Tile.name)                                                           ## used for debugging
                        #print("doors_labeled", Working_Tile.doors)                                                  ## used for debugging
                        #print("direction ", direction)                                                              ## used for debugging
                        #print("Door? ", Working_Tile.up)                                                            ## used for debugging

                case 3:                                                                                             ## randomly moving left
                    new_row = row                                                                                   ## row stays the same
                    new_column = column - 1                                                                         ## Move left by one tile
                    direction = "L"                                                                                 ## indciates working tile is one space right
                    if 'l' in Working_Tile.quickinfo and map_data[new_row][new_column] == 0:                        ## if the current tile has a left door and there isn't a tile already there
                        walled = False                                                                              ## no longer walled
                        #print("name ", Working_Tile.name)                                                           ## used for debugging
                        #print("doors_labeled", Working_Tile.doors)                                                  ## used for debugging
                        #print("direction ", direction)                                                              ## used for debugging
                        #print("Door? ", Working_Tile.up)                                                            ## used for debugging

                case 4:                                                                                             ## randomly moving right
                    new_row = row                                                                                   ## row stays the same
                    new_column = column + 1                                                                         ## Move right by one tile
                    direction = "R"                                                                                 ## indciates working tile is one space left
                    if 'r' in Working_Tile.quickinfo and map_data[new_row][new_column] == 0:                        ## if the current tile has a right door and there isn't a tile already there
                        walled = False                                                                              ## no longer walled 
                        #print("name ", Working_Tile.name)                                                           ## used for debugging
                        #print("doors_labeled", Working_Tile.doors)                                                  ## used for debugging
                        #print("direction ", direction)                                                              ## used for debugging
                        #print("Door? ", Working_Tile.up)                                                            ## used for debugging
            if new_row < 0 or new_column < 0:                                                                       ## if it goes negative
                walled = True                                                                                       ## prevents from wrapping around
            checked_directions.append(rand_direction)                                                               ## marked that we checked that direction

        #print("walled '", walled)                                                                                   ## used for deubbing
        #print("taken '", map_data[new_row][new_column] != 0)                                                        ## used for deubbing
        #print("row ", row, "column", column)                                                                        ## checking the row and column for dubugging 
        #print("new_row ", new_row, "new_column ", new_column)                                                       ## checking the new row and new column for dubugging          

        if map_data[new_row][new_column] != 0 or walled == True:                                                    ## if last direction was blocked by a wall or if was already taken
            if Working_Tile.name in Names_of_Buildable:                                                             ## checks if the stuck working tile is in the list of buildable (just searching names is faster computation)
                Buildable.remove(Working_Tile)                                                                      ## removes it from the buildable list
                Names_of_Buildable.remove(Working_Tile.name)                                                        ## removes its name from the name of buildable list
            if len(Buildable) <= 0:                                                                                 ## if there is no tiles in the buildable list
                print("FAILED")                                                                                     ## let the user know that there is no path to win
                quit()                                                                                              ## ends the program
            else:                                                                                                   ## if there are buidlables in the list
                #print("old ", Working_Tile.name)                                                                    ## used for debugging
                Working_Tile = random.choice(Buildable)                                                             ## pick a random buildable tile
                row = Working_Tile.row                                                                              ## sets the row 
                column = Working_Tile.column                                                                        ## sets the column
                Buildable.remove(Working_Tile)                                                                      ## removes the Working tile from the Buildable set
                Names_of_Buildable.remove(Working_Tile.name)                                                        ## removes the Working tile name from the set of buildable names
                #print("new ", Working_Tile.name)                                                                    ## used for debuggin
                                              
        else:                                                                                                       ## if not trapped
            rand_index = random.randint(2,29)                                                                       ## generates a random number from 2-29 to call the tiles
            while rand_index in used:                                                                               ## checks if the number has already been used
                rand_index = random.randint(2,29)                                                                   ## if already been used get another random number and try again
            #rand_index = testing[number]                                                                           ## used for debugging tiles (or making premade maps)
            tile = int(hex(tiles[rand_index]), 16)                                                                  ## get the tile information after converting to hex from intiger value
            map_data[new_row][new_column] = tile                                                                    ## replaces the blank tile with the new tile value
            New_Tile = tile_textures[map_data[new_row][new_column]]                                                 ## Calls forth the new tile
            New_Tile.row = new_row                                                                                  ## tells tile where its row is located in the map
            New_Tile.column = new_column                                                                            ## tells tile where its column is located in the map
            row = new_row                                                                                           ## sets the row as the new row
            column = new_column                                                                                     ## sets the column as the new column
            used.append(rand_index)                                                                                 ## add the rand_index to the used list
            clockwise_count = 0                                                                                        ## counts how many times the tile was rotated clockwise
            ## lines up the doors from the current tile and the newly placed tile
            match direction:                                                                                        ## checks where the direction of the new tile is placed
                case "U":                                                                                           ## if it was upwards
                    while 'd' not in New_Tile.quickinfo:                                                            ## if the new tile doesen't have a down door to enter from
                        New_Tile.rotate_clockwise()                                                                 ## rotate the tile clockwise
                        clockwise_count += 1                                                                        ## increases clockwise_count by 1
                case "D":                                                                                           ## if the was downwards
                    while 'u' not in New_Tile.quickinfo:                                                            ## if the new tile has an up door
                        New_Tile.rotate_clockwise()                                                                 ## rotate the tile clockwise
                        clockwise_count += 1                                                                        ## increases clockwise_count by 1
                case "L":                                                                                           ## if it was from the left
                    while 'r' not in New_Tile.quickinfo:                                                            ## if the new tile has a right door
                        New_Tile.rotate_clockwise()                                                                 ## rotate the tile clockwise
                        clockwise_count += 1                                                                        ## increases clockwise_count by 1
                case "R":                                                                                           ## if it was from the right    
                    while 'l' not in New_Tile.quickinfo:                                                            ## if the new tile has a left door
                        New_Tile.rotate_clockwise()                                                                 ## rotate the tile clockwise
                        clockwise_count += 1                                                                        ## increases clockwise_count by 1                        
            map_rotations[row][column] = clockwise_count                                                            ## adds the number of times it was rotated clockwise to the map_rotations    
            Working_Tile.add_child(New_Tile)                                                                        ## adds the new tile as a child of the working tile 
            New_Tile.parent = Working_Tile                                                                          ## adds the new tile parent as the working title
            Working_Tile.check_neighbors(map_data)                                                                  ## records if there is an open neighbor
            Working_Tile = New_Tile                                                                                 ## Moves onto the next tile
            #placed.append(Working_Tile.name)                                                                        ## used for debugging
            #number = number + 1                                                                                     ## used for debugging tiles
            
            if new_row > max_row:                                                                                   ## if the new row is bigger than the previously recorded max row
                max_row = new_row                                                                                   ## set the new row to be the new max row
            if new_row < min_row:                                                                                   ## if the new row is smaller than the previously recorded min row
                min_row = new_row                                                                                   ## set the new row to be the new min row
            if new_column > max_column:                                                                             ## if the new column is bigger than the previously recorded max column
                max_column = new_column                                                                             ## set the new column to be the new max columm
            if new_column < min_column:                                                                             ## if the new column is smaller than the previously recorded min column
                min_column = new_column                                                                             ## the the new column to be the new min column

    ## Gets rid of excess rows and columns
    #print("min_row", min_row)                                                                                       ## used for debugging
    #print("max_row", max_row)                                                                                       ## used for debugging
    #print("min_column", min_column)                                                                                 ## used for debugging
    #print("max_column", max_column)                                                                                 ## used for debugging
    #print("mapdata", map_data)                                                                                      ## used for debugging

    delete_rows = []                                                                                                ## initalizing list of rows that need to be deleated
    delete_columns = []                                                                                             ## initalizing list of columns that need to be deleated
    for i in range(max_row+1, height):                                                                              ## determines the numbers of the rows at the bottom of the map that needs to be deleted 
        delete_rows.append(i)                                                                                       ## adds the number of the rows at the bottom of the map that needs to be deleted to the list
    for j in range(0, min_row):                                                                                     ## determines the numbers of the rows at the top of the map that needs to be deleted 
        delete_rows.append(j)                                                                                       ## adds the number of the rows at the top of the map that needs to be deleted to the list
    map_data = np.delete(map_data, delete_rows, 0)                                                                  ## deletes the unnessisary rows from map_data
    map_rotations = np.delete(map_rotations, delete_rows, 0)                                                        ## deletes the unnessisary rows from map_rotations
    #print("mapdata_mid", map_data)                                                                                  ## used for debugging
    for k in range(max_column+1, width):                                                                            ## determines the columns from the right edge of the map that eeed to be deleted
        delete_columns.append(k)                                                                                    ## adds the numbers of the columns at thte right of the map that needs to be deleted to the list
    for p in range(0, min_column):                                                                                  ## determines the columns from the left edge of the map that eeed to be deleted
        delete_columns.append(p)                                                                                    ## adds the numbers of the columns at thte left of the map that needs to be deleted to the list
    map_data = np.delete(map_data, delete_columns, 1)                                                               ## deletes the unnessisary columns from map_data
    #print("new ", map_data)                                                                                         ## used for debugging
    map_rotations = np.delete(map_rotations, delete_columns, 1)                                                     ## deletes the unnessisary columns from map_rotations

    new_height = len(map_data)                                                                                      ## determines the new_height of the new map
    new_width = len(map_data[0])                                                                                    ## determines the new_wideth of the new map

    max_mins = [new_height, new_width]                                                                              ## stores the new dimensiosn of the new map in an easy access list

    print("map_data", map_data)                                                                                     ## prints out so can copy and regenerate the map
    print("map_rotations", map_rotations)                                                                           ## prints out so you can copy and regenerate the map
    #print("max_mins ", max_mins)                                                                                    ## used for debugging
    #print("placed, ", placed)                                                                                       ## used for debugging
    #print("Names of Buildable ", Names_of_Buildable)                                                                ## used for debugging
    return map_data, max_mins                                                                                       ## returns the map data and size of the new map


## This function places all the tiles and tokens for the user to see
def draw_map(screen, map_data, TILE_SIZE):

    MAP_HEIGHT = len(map_data)                                                                                      ## gets the map height
    MAP_WIDTH = len(map_data[0])                                                                                    ## gest the width of the map
    for row in range(MAP_HEIGHT):                                                                                   ## cycle through each row
        for col in range(MAP_WIDTH):                                                                                ## cycle through each column in the row
            screen.blit(tile_textures[map_data[row][col]].texture,                                                  ## Grabs the tile image and displays it at it's current location
                        (col*TILE_SIZE, row*TILE_SIZE))                                                             ## places the tile in it's proper row and column
            if tile_textures[map_data[row][col]].token != None:                                                     ## if the tile has a token
                screen.blit(tile_textures[map_data[row][col]].token,                                                ## display the token at about a 3rd of a TILE_SIZE down and right from the upper left of the tile location
                        (col*TILE_SIZE+TILE_SIZE/3, row*TILE_SIZE+TILE_SIZE/3))                                     ## the token will be placed about a 1/3rd of the way down and a 1/3rd of the way to the right from the upper left corner of the tile

    ## Score Board Section
    font_size = TILE_SIZE//4                                                                                        ## make the font size 1/4th of the actual size
    font = pygame.font.Font(None, font_size)                                                                        ## set the font for the scoreboard

    totalcost_text = font.render(f'Cost: {settings.Player_1.totalcost}', True, (0, 0, 0))                           ## gets the value of the total cost of the actions
    screen.blit(totalcost_text, (10, MAP_HEIGHT*TILE_SIZE))                                                         ## displays the total cost of the actions on the score board

    ## Red Score
    Red_Token_text = font.render(f'Red Token: {settings.Player_1.Red_Token}', True, (0, 0, 0))                      ## displays the count for the Red Token
    if settings.Player_1.Red_Token != 0:                                                                            ## once a red token has been collected
        for i in range(settings.Player_1.Red_Token):                                                                ## add a red token image for each red token collected
            screen.blit(token_texture[1],(font_size*6+(font_size/3)*i, MAP_HEIGHT*TILE_SIZE+font_size//1.5))        ## displays the token
    if settings.Red_Event_Broken == True:                                                                           ## if the Red event hasn't been broken yet
        screen.blit(token_texture[8],(font_size*6+(font_size/3), MAP_HEIGHT*TILE_SIZE+font_size//1.5))              ## displays the broken event token            
    screen.blit(Red_Token_text, (10, MAP_HEIGHT*TILE_SIZE+font_size))                                               ## displays the text and where it should be located

    ## Green Score
    Green_Token_text = font.render(f'Green Token: {settings.Player_1.Green_Token}', True, (0, 0, 0))                ## displays the count for the Green Token
    if settings.Player_1.Green_Token != 0:                                                                          ## once a green token has been collected
        for i in range(settings.Player_1.Green_Token):                                                              ## add a green token image for each green token collected
            screen.blit(token_texture[2],(font_size*6+(font_size/3)*i, MAP_HEIGHT*TILE_SIZE+1.5*font_size))         ## displays the token
    if settings.Green_Event_Broken == True:                                                                         ## if the Green event hasn't been broken yet
        screen.blit(token_texture[9],(font_size*6+(font_size/3), MAP_HEIGHT*TILE_SIZE+1.5*font_size))               ## displays the broken event token
    screen.blit(Green_Token_text, (10, MAP_HEIGHT*TILE_SIZE+font_size*2))                                           ## displays the text and where it should be located

    ## Blue Score
    Blue_Token_text = font.render(f'Blue Token: {settings.Player_1.Blue_Token}', True, (0, 0, 0))                   ## displays the count for the Blue Token
    if settings.Player_1.Blue_Token != 0:                                                                           ## once a blue token has been collected
            for i in range(settings.Player_1.Blue_Token):                                                           ## add a Blue token image for each green token collected
                screen.blit(token_texture[3],(font_size*6+(font_size/3)*i, MAP_HEIGHT*TILE_SIZE+2.5*font_size))     ## displays the token
    if settings.Blue_Event_Broken == True:                                                                          ## if the Blue event hasn't been broken yet
            screen.blit(token_texture[10],(font_size*6+(font_size/3), MAP_HEIGHT*TILE_SIZE+2.5*font_size))          ## displays the broken event token  
    screen.blit(Blue_Token_text, (10, MAP_HEIGHT*TILE_SIZE+font_size*3))                                            ## displays the text and where it should be located

    ## Fire of Eidolon Score
    if settings.FireofEidolon_Grabbed == True:                                                                      ## if the fire of Eidolon has been grabbed
        screen.blit(pygame.transform.scale(token_texture[7],(TILE_SIZE/1.5,TILE_SIZE/1.5)),                         ## display the fire of Eidolon in the center of the score board at a larger scale
                    (TILE_SIZE*MAP_WIDTH//2, MAP_HEIGHT*TILE_SIZE))                                                 ## place it in the center of the score board

    ## Determineing Pathing
    if settings.Win == True:                                                                                        ## if the player has won
        backpaths(settings.Player_1, screen)                                                                        ## get the path the player had traveled

    if settings.planning == True:                                                                                   ## if a planned path was determined
        forwardpath(settings.Player_1, screen)                                                                      ## gets the planned path for the player to follow

    #if settings.seen == True:                                                                                       ## if player has list of explored points in conjunction with planning
    #    explored(settings.Player_1, screen)                                                                         ## displays which tiles have been explored as part of the planning process

## gets the path the player traveled
def backpaths(Player, screen):                                                                                      ## gets the path the player traveled
    gradiant = []
    path = []                                                                                                       ## initalize the path
    for i in range(len(Player.visited)):                                                                            ## for each state the player visited
        path.append([Player.visited[i][1]*TILE_SIZE+TILE_SIZE//2, Player.visited[i][0]*TILE_SIZE+TILE_SIZE//2])     ## converte the state into a path based on the number of pixels
    for j in range(len(path)-1):                                                                                    ## for each of the items in the path (minus the last one)    
        gradiant = (round(255-255*j/len(path)), round(255*(j/len(path))), 0)                                        ## determine the color
        pygame.draw.lines(screen, gradiant, False, [path[j], path[j+1]], width = TILE_SIZE//12)                     ## draw the lines in a clean color gradiant

## gets the path the player plans to travel
def forwardpath(Player, screen):                                                                                    ## gets the path the player plans to travel
    gradiant = []                                                                                                   ## initalize the gradiant value
    path = []                                                                                                       ## initalize the path
    for i in range(len(Player.plans)):                                                                              ## for each state the player plans to visit
        path.append([Player.plans[i][1]*TILE_SIZE+TILE_SIZE//2, Player.plans[i][0]*TILE_SIZE+TILE_SIZE//2])         ## converte the state into a path based on the number of pixels
    for j in range(len(path)-1):                                                                                    ## for each of the items in the path (minus the last one)
        gradiant = (round(255-255*j/len(path)), round(255*(j/len(path))), 0)                                        ## detetermine the value of the gradiant
        if Player.todo[j] == 'x' or Player.todo[j] == 'y':                                                          ## if the player used the secret tunnel
            pygame.draw.circle(screen, gradiant, path[j],  TILE_SIZE//8)                                            ## make a dot at the exntrance of the tunnel
            pygame.draw.circle(screen, gradiant, path[j+1],  TILE_SIZE//8)                                          ## make a dot at the exit of the tunnel
        else:                                                                                                       ## otherwise
            #pygame.draw.aalines(screen, gradiant, False, [path[j], path[j+1]])                                      ## draw the lines in a clean color gradiant
            pygame.draw.lines(screen, gradiant, False, [path[j], path[j+1]], width = TILE_SIZE//12)                 ## draw thicker lines in a not so clean color gradiant

## gets the path the player plans to travel
def explored(Player, screen):                                                                                       ## gets the path the player plans to travel
    gradiant = []                                                                                                   ## initalize the gradiant value
    points = []                                                                                                     ## initalize the path
    for i in range(len(Player.explored)):                                                                           ## for each state the player plans to visit
        points.append([Player.explored[i][1]*TILE_SIZE+TILE_SIZE//2, Player.explored[i][0]*TILE_SIZE+TILE_SIZE//2]) ## converte the state into a path based on the number of pixels
    for j in range(len(points)):                                                                                    ## for each point
        gradiant = (255, 0, 0)                                                                                      ## the color of the circle
        pygame.draw.circle(screen, gradiant, points[j],  TILE_SIZE//8)                                              ## draws the circle at the points that A* explored
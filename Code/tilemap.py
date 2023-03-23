## Source: https://github.com/gurb/rpg-game-tutorials/blob/main/004-Generating%20Tile%20Map/tilemap.py
from this import d
import settings
import pygame
import random
import math

# dimension of each tiles
TILE_SIZE = settings.TILE_SIZE  ## Gets the size of the tile from the settings file and sets it as a global variable

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
    def __init__(self, filepath, parent=None):                            ## initalizes the tile class with the path to the file
        ## Gets the image so it can display
        self.image = pygame.image.load(filepath)                          ## loads the image in
        self.texture = create_texture(self.image)                         ## creates the appropriate texture for the image
        self.children = []                                                ## inializes the children of said tile
        self.parent = parent                                              ## indicates the parent of said tile
        
        ## Gets the information hardwritten in the file's name
        filename = filepath.split("/")                                    ## Cuts out all but the name of the image
        title = filename[2].split(".")                                    ## Cuts out the .jpg or .png
        self.info = title[0].split("_")                                   ## Breaks the name into useful information
        self.id = self.info[0]                                            ## Gets the info from the image name
        self.type = self.info[1]                                          ## Determine what type of tile this is 
        self.name = self.info[2]                                          ## Determine the name of the tile
        self.doors = self.info[3]                                         ## Gets the data on the doors
       
        ## Establishes the Doors
        self.up = False                                                   ## default no door up
        self.down = False                                                 ## default no door down
        self.left = False                                                 ## default no door left
        self.right = False                                                ## default no door right

        match self.doors:                                                 ## determines which doors it has
            case "UDLR":                                                  ## if it has all doors 
                self.up = True                                            ## indicate there is an up door
                self.down = True                                          ## indicate door is a down door 
                self.left = True                                          ## indicate door is a left door
                self.right = True                                         ## indicate door is a right door
            
            case "UDL":                                                   ## if it has the three doors with UDL
                self.up = True                                            ## indicate door is a up door
                self.down = True                                          ## indicate door is a down door
                self.left = True                                          ## indicate door is a left door
            
            case "UDR":                                                   ## if it has the three doors with UDR
                self.up = True                                            ## indicate door is a up door
                self.down = True                                          ## indicate door is a down door
                self.right = True                                         ## indicate door is a right door

            case "DLR":                                                   ## if it has the three doors with DLR
                self.down = True                                          ## indicate door is a down door
                self.left = True                                          ## indicate door is a left door
                self.right = True                                         ## indicate door is a right door

            case "UD":                                                    ## if it has the two doors with UD
                self.up = True                                            ## indicate door is a up door
                self.down = True                                          ## indicate door is a down door

            case "DL":                                                    ## if it has the two doors with DL
                self.down = True                                          ## indicate door is a down door
                self.left = True                                          ## indicate door is a left door

            case "DR":                                                    ## if it has the two doors with DR
                self.down = True                                          ## indicate door is a down door
                self.right = True                                         ## indicate door is a right door

            case "D":                                                     ## if it has the two doors with D
                self.down = True                                          ## indicate door is a down door

        self.token = 0                     
        if self.type == "Red" or self.type == "Green" or self.type == "Blue":
            self.token = 1      
    
    def add_child(self, child):                                           ## adds a child to the tile
        '''
        Add a child node
        '''
        self.children.append(child)                                       ## adds a connecting tile

    def rotate_clockwise(self):
        ## rotate image
        self.image = pygame.transform.rotate(self.image, -90)             ## takes the existing image and rotates it by 90 degrees clockwise
        self.texture = create_texture(self.image)                         ## creates the appropriate texture for the image
        
        ## rotate doors (Doesn't need to rotate if its "UDLR" or None doors)
        if self.doors == "UDL" or self.doors == "UDR" or self.doors == "DLR":       ## if it has three doors
            if self.up == True and self.left == True and self.down == True:        
                self.down = False
                self.right = True
            elif self.right == True and self.up == True and self.left == True:
                self.left = False
                self.down = True
            elif self.down == True and self.right == True and self.up == True:
                self.up = False
                self.left = True
            elif self.left == True and self.down == True and self.right == True:
                self.right = False
                self.up = True
        elif self.doors == "UD" or self.doors == "DL" or self.doors == "DR":
            if self.up == True and self.down == True:
                self.up = False
                self.down = False
                self.left = True
                self.right = True
            elif self.left == True and self.right == True:
                self.left = False
                self.right = False
                self.down = True
                self.up = True
            elif self.down == True and self.left == True:
                self.down = False
                self.up = True
            elif self.left == True and self.up == True:
                self.left = False
                self.right = True
            elif self.up == True and self.right == True:
                self.up = False
                self.down = True
            elif self.right == True and self.down == True:
                self.right = False
                self.left = True
        elif self.doors == "D":
            if self.down == True:
                self.down = False
                self.left = True
            elif self.left == True:
                self.left = False
                self.up = True
            elif self.up == True:
                self.up = False
                self.right = True
            elif self.right == True:
                self.right = False
                self.down = True


        ## Get Directions: Check against dictionary, otherwise false
        ## Create a funciton to rotate tile image (and doors)
        ## save a neighbor Function

## Turns the image into the tile texture according to the requested size
def create_texture(name):
    image = name
    image = pygame.transform.scale(image,(TILE_SIZE,TILE_SIZE))
    return image

## Linking the names of the tiles with the location of the images
BackTile = Tile("Images/Tile_Scans/0_None_BackTile_None.jpg")
StartTile = Tile("Images/Tile_Scans/1_Start_StartTile_UDLR.jpg")
FireofEidolon = Tile("Images/Tile_Scans/2_FireofEidolon_FireofEidolon_D.jpg")
VoraxsHeart = Tile("Images/Tile_Scans/3_RedEvent_VoraxsHeart_D.jpg")
VoraxFocus = Tile("Images/Tile_Scans/4_GreenEvent_VoraxFocus_D.jpg")
VoraxsKnowledge = Tile("Images/Tile_Scans/5_BlueEvent_VoraxsKnowledge_D.jpg")
EndTile = Tile("Images/Tile_Scans/6_End_EndTile_UPLR.jpg")
SecretX = Tile("Images/Tile_Scans/7_Secret_SecretX_UPLR.jpg")
SecretY = Tile("Images/Tile_Scans/8_Secret_SecretY_UPLR.jpg")
VoraciousPlant = Tile("Images/Tile_Scans/9_Red_VoraciousPlant_UPLR.jpg")
Minotaur = Tile("Images/Tile_Scans/10_Red_Minotaur_UPLR.jpg")
FloatingStones = Tile("Images/Tile_Scans/11_Green_FloatingStones_UPLR.jpg")
LaughingShadow = Tile("Images/Tile_Scans/12_Blue_LaughingShadow_UPLR.jpg")
Psychomancer = Tile("Images/Tile_Scans/13_Blue_Psychomancer_UPLR.jpg")
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
## Values in Hexidecimal (don't know why but it works)
textures = {
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
    0x1d : MimicChest,
}

## Turns the values of the tile into a list
tiles = [0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xa, 0xb, 0xc, 0xd, 0xe, 0xf, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d]

## Use this as a general thing to create a self built map later on
# generate with tiles randomly
#def generate_map(width, height, tilesize):
#    map_data = []                                                                                           ## Keeps track of what tile is in each location
#    used = []                                                                                               ## initializes the list for the tiles already used
#    for i in range(height // tilesize):                                                                     ## This is the row
#        map_data.append([])                                                                                 ## making the map_data a row x column calling
#        for j in range(width // tilesize):                                                                  ## This is the column
#            rand_index = random.randint(2,29)                                                               ## generates a random number from 2-29 to call the tiles
#            if i == (math.trunc((height//tilesize)/2)) and j == (math.trunc((width//tilesize)/2)):          ## if the tile in question is at the center
#                rand_index = 1                                                                              ## put the start tile there (setting rand to 1)
#            if rand_index in used:                                                                          ## if the tile has been used before
#                rand_index = 0                                                                              ## put in the filler tile instead (setting rand to zero)
#            else:                                                                                           ## if the tile has not been used before
#                used.append(rand_index)                                                                     ## add the number to the used index
#            # convert to hex from int value
#            tile = int(hex(tiles[rand_index]), 16)                                                          ## get the tile information
            
#            map_data[i].append(tile)                                                                        ## add the tile to the map
#    return map_data

##############################################################################################################################################################################################################################
#### Things to add to tile map
####    - Create a known map
####    - Lining up the doors
####    - Going back and expanding from the start tile a % of the time
####    - Adding tokens
####    - have the display be max_row and max_column big
##############################################################################################################################################################################################################################

## building map from center point
def building_map(width, height, tilesize):
    ## initilizing variables                                               
    used = []                                                                                               ## initializes the list for the tiles already used
    map_data = []                                                                                           ## Keeps track of what tile is in each location
    for i in range(height // tilesize):                                                                     ## This is the row
        map_data.append([])                                                                                 ## making the map_data a row x column calling
        for j in range(width // tilesize):                                                                  ## This is the column
            if i == (math.trunc((height//tilesize)/2)) and j == (math.trunc((width//tilesize)/2)):          ## if the tile in question is at the center
                rand_index = 1                                                                              ## put the start tile there (setting rand to 1)
            else:                                                                                           ## if the tile has been used before
                rand_index = 0                                                                              ## put in the filler tile to create a blank map
            tile = int(hex(tiles[rand_index]), 16)                                                          ## get the tile information after converting to hex from intiger value
            map_data[i].append(tile)                                                                        ## add teh tile to the map

    row = math.trunc((height//tilesize)/2)                                                                  ## Start at the center row point
    column = math.trunc((width//tilesize)/2)                                                                ## Start at the center column point
    Working_Tile = textures[map_data[row][column]]                                                          ## indicates this is the working tile
    
    
    while len(used) <= 27:                                                                                  ## should run until all 27 tiles have been added (not counting start or blank)
        #print(len(used))                                                                                    ## debug check to see if all tiles have been used
        rand_index = random.randint(2,29)                                                                   ## generates a random number from 2-29 to call the tiles
        while rand_index in used:                                                                           ## checks if the number has already been used
            rand_index = random.randint(2,29)                                                               ## if already been used get another random number and try again
        checked_directions = []                                                                             ## keeps track of which directions checked
        rand_direction = random.randint(1,4)                                                                ## generate a random direction
        match rand_direction:                                                                               ## picking a random direction
            case 1:                                                                                         ## randomly moving up
                new_row = row - 1                                                                           ## Move up by one tile
                new_column = column                                                                         ## column stays the same
            case 2:                                                                                         ## randomly movign down
                new_row = row + 1                                                                           ## Move down by one tile
                new_column = column                                                                         ## column stays the same
            case 3:                                                                                         ## randomly moving left
                new_row = row                                                                               ## row stays the same
                new_column = column - 1                                                                     ## Move left by one tile
            case 4:                                                                                         ## randomly moving right
                new_row = row                                                                               ## row stays the same
                new_column = column + 1                                                                     ## Move right by one tile
        checked_directions.append(rand_direction)                                                           ## Marks taht we checked that direction

        ##print("checked_direction ", checked_directions)                                                    ## debug checks to see if all surrounding tiles are taken
        
        while map_data[new_row][new_column] != 0 and len(checked_directions) <= 4:                          ## run again if the new spot is already occupied 
            rand_direction = random.randint(1,4)                                                            ## generate a random direction
            match rand_direction:                                                                           ## picking a random direction
                case 1:                                                                                     ## randomly moving up
                    new_row = row - 1                                                                       ## Move up by one tile
                    new_column = column                                                                     ## column stays the same
                case 2:                                                                                     ## randomly movign down
                    new_row = row + 1                                                                       ## Move down by one tile
                    new_column = column                                                                     ## column stays the same
                case 3:                                                                                     ## randomly moving left
                    new_row = row                                                                           ## row stays the same
                    new_column = column - 1                                                                 ## Move left by one tile
                case 4:                                                                                     ## randomly moving right
                    new_row = row                                                                           ## row stays the same
                    new_column = column + 1                                                                 ## Move right by one tile            
            checked_directions.append(rand_direction)                                                       ## marked that we checked that direction

        if len(checked_directions) >= 4:                                                                    ## if every direction is blocked
            Working_Tile = Working_Tile.parent                                                              ## back up to the parent
        else:                                                                                               ## if not trapped                   
            used.append(rand_index)                                                                         ## add the rand_index to the used list
            row = new_row                                                                                   ## sets the row as the new row
            column = new_column                                                                             ## sets the column as the new column
            tile = int(hex(tiles[rand_index]), 16)                                                          ## get the tile information after converting to hex from intiger value
            New_Tile = textures[map_data[row][column]]                                                      ## Calls forth the new tile
            Working_Tile.add_child(New_Tile)                                                                ## adds the new tile as a child of the working tile 
            New_Tile.parent = Working_Tile                                                                  ## adds the new tile parent as the working title 
            Working_Tile = New_Tile                                                                         ## Moves onto the next tile
            map_data[row][column] = tile                                                                    ## sets the new tile up in the correction location

    return map_data                                                                                         ## returns the map data

def draw_map(screen, map_data, TILE_SIZE):
    MAP_HEIGHT = len(map_data) 
    MAP_WIDTH = len(map_data[0])
    for row in range(MAP_HEIGHT):
        for col in range(MAP_WIDTH):
            screen.blit(textures[map_data[row][col]].texture,
                        (col*TILE_SIZE, row*TILE_SIZE))        
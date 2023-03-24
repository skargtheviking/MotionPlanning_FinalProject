## Source: https://github.com/gurb/rpg-game-tutorials/blob/main/004-Generating%20Tile%20Map/tilemap.py
from asyncio.windows_events import NULL
from distutils.command.check import check
from this import d
import settings
import pygame
import random
import math

# dimension of each tiles
TILE_SIZE = settings.TILE_SIZE  ## Gets the size of the tile from the settings file and sets it as a global variable

## Turns the image into the tile texture according to the requested size
def create_texture(name):
    image = pygame.transform.scale(name,(TILE_SIZE,TILE_SIZE))            ## scales the image to tile size
    return image                                                          ## returns the tile image

## Turns the image into the tile texture according to the requested size
def create_token_texture(name):
    image = pygame.transform.scale(name,(TILE_SIZE/4,TILE_SIZE/4))        ## scales the image to 1/4 of a tile size
    return image                                                          ## return the token image

Cultist = pygame.image.load("Images/Tokens/Cultist.png")                  ## Gets the cultist image
Token_Red = pygame.image.load("Images/Tokens/Token_Red.png")              ## Gets the red token
Token_Green = pygame.image.load("Images/Tokens/Token_Green.png")          ## gets the green token
Token_Blue = pygame.image.load("Images/Tokens/Token_Blue.png")            ## gets the blue token

token_texture = {                                                         ## creates a dictionary of the token displays
    0x0 : create_token_texture(Cultist),                                  ## the cultists token
    0x1 : create_token_texture(Token_Red),                                ## the red token 
    0x2 : create_token_texture(Token_Green),                              ## the green token
    0x3 : create_token_texture(Token_Blue)                                ## the blue token
}
token_list = [0x0, 0x1, 0x2, 0x3]                                         ## reference list for the token dictionary

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
    def __init__(self, filepath, parent=None):                                      ## initalizes the tile class with the path to the file
        ## Gets the image so it can display
        self.image = pygame.image.load(filepath)                                    ## loads the image in
        self.texture = create_texture(self.image)                                   ## creates the appropriate texture for the image
        self.children = []                                                          ## inializes the children of said tile
        self.parent = parent                                                        ## indicates the parent of said tile
        
        ## Gets the information hardwritten in the file's name
        filename = filepath.split("/")                                              ## Cuts out all but the name of the image
        title = filename[2].split(".")                                              ## Cuts out the .jpg or .png
        self.info = title[0].split("_")                                             ## Breaks the name into useful information
        self.id = self.info[0]                                                      ## Gets the info from the image name
        self.type = self.info[1]                                                    ## Determine what type of tile this is 
        self.name = self.info[2]                                                    ## Determine the name of the tile
        self.doors = self.info[3]                                                   ## Gets the data on the doors
        self.token = self.Token_grabber()                                           ## grab the token texture

        ## Establishes the Doors
        self.up = False                                                             ## default no door up
        self.down = False                                                           ## default no door down
        self.left = False                                                           ## default no door left
        self.right = False                                                          ## default no door right

        match self.doors:                                                           ## determines which doors it has
            case "UDLR":                                                            ## if it has all doors 
                self.up = True                                                      ## indicate there is an up door
                self.down = True                                                    ## indicate door is a down door 
                self.left = True                                                    ## indicate door is a left door
                self.right = True                                                   ## indicate door is a right door
            
            case "UDL":                                                             ## if it has the three doors with UDL
                self.up = True                                                      ## indicate door is a up door
                self.down = True                                                    ## indicate door is a down door
                self.left = True                                                    ## indicate door is a left door
            
            case "UDR":                                                             ## if it has the three doors with UDR
                self.up = True                                                      ## indicate door is a up door
                self.down = True                                                    ## indicate door is a down door
                self.right = True                                                   ## indicate door is a right door

            case "DLR":                                                             ## if it has the three doors with DLR
                self.down = True                                                    ## indicate door is a down door
                self.left = True                                                    ## indicate door is a left door
                self.right = True                                                   ## indicate door is a right door

            case "UD":                                                              ## if it has the two doors with UD
                self.up = True                                                      ## indicate door is a up door
                self.down = True                                                    ## indicate door is a down door

            case "DL":                                                              ## if it has the two doors with DL
                self.down = True                                                    ## indicate door is a down door
                self.left = True                                                    ## indicate door is a left door

            case "DR":                                                              ## if it has the two doors with DR
                self.down = True                                                    ## indicate door is a down door
                self.right = True                                                   ## indicate door is a right door

            case "D":                                                               ## if it has the two doors with D
                self.down = True                                                    ## indicate door is a down door


    ## adds a tile as a cild of said token    
    def add_child(self, child):                                                     ## adds a child node to the tile
        '''
        Add a child node
        '''
        self.children.append(child)                                                 ## adds a connecting tile

    ## Determines what token the tile has    
    def Token_grabber(self):                                                        ## Determines which token the tile should have
        match self.type:                                                            ## checks the type listed in the tile's name
            case "Red":                                                             ## if it's listed as red
                token_number = int(hex(token_list[1]), 16)                          ## grab the red token
            case "Green":                                                           ## if it's listed as green
                token_number = int(hex(token_list[2]), 16)                          ## grab the green token
            case "Blue":                                                            ## if it's listed as blue
                token_number = int(hex(token_list[3]), 16)                          ## grab the blue token
            case _:                                                                 ## if no tile is listed
                token_number = None                                                 ## it does not have a token number
        if token_number == None:                                                    ## if there is no token number
            token = None                                                            ## there is no token
        else:                                                                       ## otherwise
            token = token_texture[token_number]                                     ## grab the texture for the token
        return token                                                                ## return the texture for the token

    ## Rotates the image and the doors clockwise
    def rotate_clockwise(self):                                                     ## rotates the image and doors clockwise
        ## rotate image
        self.image = pygame.transform.rotate(self.image, -90)                       ## takes the existing image and rotates it by 90 degrees clockwise
        self.texture = create_texture(self.image)                                   ## creates the appropriate texture for the image
        
        ## rotate doors (Doesn't need to rotate if its "UDLR" or None doors)
        if self.doors == "UDL" or self.doors == "UDR" or self.doors == "DLR":       ## if it has three doors
            if self.up == True and self.left == True and self.down == True:         ## if in the UDL position
                self.down = False                                                   ## move to the URL position
                self.right = True
            elif self.right == True and self.up == True and self.left == True:      ## if in the URL position
                self.left = False                                                   ## move to the UDR position
                self.down = True
            elif self.down == True and self.right == True and self.up == True:      ## if in the UDR position
                self.up = False                                                     ## move to the DLR position
                self.left = True
            elif self.left == True and self.down == True and self.right == True:    ## if in the DLR position
                self.right = False                                                  ## move to the UDL position
                self.up = True
        elif self.doors == "UD" or self.doors == "DL" or self.doors == "DR":        ## if it has two doors
            if self.up == True and self.down == True:                               ## if in the UD position
                self.up = False                                                     ## move to the LR position
                self.down = False
                self.left = True
                self.right = True
            elif self.left == True and self.right == True:                          ## if in the LR position
                self.left = False                                                   ## move to the UD position
                self.right = False
                self.down = True
                self.up = True
            elif self.down == True and self.left == True:                           ## if in DL position
                self.down = False                                                   ## move to the UL position
                self.up = True
            elif self.left == True and self.up == True:                             ## if in UL position
                self.left = False                                                   ## move to the UR position
                self.right = True
            elif self.up == True and self.right == True:                            ## if in UP position
                self.up = False                                                     ## move to the DR position
                self.down = True
            elif self.right == True and self.down == True:                          ## if in DR position
                self.right = False                                                  ## move to the DL position
                self.left = True
        elif self.doors == "D":                                                     ## if it has one door
            if self.down == True:                                                   ## if in D position
                self.down = False                                                   ## move to the L position
                self.left = True                            
            elif self.left == True:                                                 ## if in L positon
                self.left = False                                                   ## move to the U position
                self.up = True
            elif self.up == True:                                                   ## if in the U position
                self.up = False                                                     ## move to the R position
                self.right = True
            elif self.right == True:                                                ## if in the R position
                self.right = False                                                  ## move to the D position
                self.down = True

        ## Get Directions: Check against dictionary, otherwise false
        ## Create a funciton to rotate tile image (and doors)
        ## save a neighbor Function

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
####    - have the display be max_row and max_column big
##############################################################################################################################################################################################################################

## building map from center point
def building_map(width, height, tilesize):
    ## initilizing variables                                               
    used = []                                                                                               ## initializes the list for the tiles already used
    map_data = []                                                                                           ## Keeps track of what tile is in each location
    
    ## initializes map
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
    max_row = row
    max_column = column
    min_row = row
    min_column = column
    print("row and column min max ", min_row, max_row, min_column, max_column)
    Working_Tile = tile_textures[map_data[row][column]]                                                          ## indicates this is the working tile
    
    
    while len(used) <= 3:#27:                                                                                  ## should run until all 27 tiles have been added (not counting start or blank)
        #print(len(used))                                                                                    ## debug check to see if all tiles have been used
        walled = True                                                                                       ## if there is a wall going in that direction
        direction = "N"                                                                                     ## which direction is the previous tile
        checked_directions = []                                                                             ## keeps track of which directions checked
        #checked_directions.clear()
        rand_direction = random.randint(1,4)                                                                ## generate a random direction
        match rand_direction:                                                                               ## picking a random direction
            case 1:                                                                                         ## randomly moving up
                new_row = row - 1                                                                           ## Move up by one tile
                new_column = column                                                                         ## column stays the same
                direction = "U"                                                                             ## indciates working tile is one space down
                print("name '", Working_Tile.name)
                print("Tile? '", Working_Tile.up)
                if Working_Tile.up == True:                                                                 ## if the current tile has an up door
                    walled = False                                                                          ## no longer walled
            case 2:                                                                                         ## randomly movign down
                new_row = row + 1                                                                           ## Move down by one tile
                new_column = column                                                                         ## column stays the same
                direction = "D"                                                                             ## indciates working tile is one space up
                print("name '", Working_Tile.name)
                print("Tile? '", Working_Tile.down)
                if Working_Tile.down == True:                                                               ## if the current tile has a down door
                    walled = False                                                                          ## no longer walled
            case 3:                                                                                         ## randomly moving left
                new_row = row                                                                               ## row stays the same
                new_column = column - 1                                                                     ## Move left by one tile
                direction = "L"                                                                             ## indciates working tile is one space right
                print("name '", Working_Tile.name)
                print("Tile? '", Working_Tile.left)
                if Working_Tile.left == True:                                                               ## if the current tile has a left door
                    walled = False                                                                          ## no longer walled
            case 4:                                                                                         ## randomly moving right
                new_row = row                                                                               ## row stays the same
                new_column = column + 1                                                                     ## Move right by one tile
                direction = "R"                                                                             ## indciates working tile is one space left
                print("name '", Working_Tile.name)
                print("Tile? '", Working_Tile.right)
                if Working_Tile.right == True:                                                              ## if the current tile has a right door
                    walled = False                                                                          ## no longer walled
        checked_directions.append(rand_direction)                                                           ## Marks taht we checked that direction

        ##print("checked_direction ", checked_directions)                                                    ## debug checks to see if all surrounding tiles are taken
        print("direction '", direction)
        print("walled '", walled)
        print("talen '", map_data[new_row][new_column] != 0)
        while (walled == True or map_data[new_row][new_column] != 0)  and len(checked_directions) < 4:
            print("direction ", direction)
            print("walled ", walled)
            print("talen ", map_data[new_row][new_column] != 0)
            rand_direction = random.randint(1,4)                                                            ## generate a random direction
            while rand_direction in checked_directions:                                                                       ## checks if the number has already been used
                print("checked_directions", len(checked_directions))
                rand_direction = random.randint(1, 4)                                                           ## if already been used get another random number and try again
            #while map_data[new_row][new_column] != 0 and len(checked_directions) <= 4:                          ## run again if the new spot is already occupied 

            match rand_direction:                                                                           ## picking a random direction
                case 1:                                                                                     ## randomly moving up
                    new_row = row - 1                                                                       ## Move up by one tile
                    new_column = column                                                                     ## column stays the same
                    direction = "U"                                                                         ## indciates working tile is one space down
                    print("name ", Working_Tile.name)
                    print("Tile? ", Working_Tile.up)
                    if Working_Tile.up == True:                                                             ## if the current tile has an up door
                        walled = False                                                                      ## no longer walled
                case 2:                                                                                     ## randomly movign down
                    new_row = row + 1                                                                       ## Move down by one tile
                    new_column = column                                                                     ## column stays the same
                    direction = "D"                                                                         ## indciates working tile is one space up
                    print("name ", Working_Tile.name)
                    print("Tile? ", Working_Tile.up)
                    if Working_Tile.down == True:                                                           ## if the current tile has a down door
                        walled = False                                                                      ## no longer walled
                case 3:                                                                                     ## randomly moving left
                    new_row = row                                                                           ## row stays the same
                    new_column = column - 1                                                                 ## Move left by one tile
                    direction = "L"                                                                         ## indciates working tile is one space right
                    print("name ", Working_Tile.name)
                    print("Tile? ", Working_Tile.up)
                    if Working_Tile.left == True:                                                           ## if the current tile has a left door
                        walled = False                                                                      ## no longer walled
                case 4:                                                                                     ## randomly moving right
                    new_row = row                                                                           ## row stays the same
                    new_column = column + 1                                                                 ## Move right by one tile
                    print("name ", Working_Tile.name)
                    print("Tile? ", Working_Tile.up)
                    direction = "R"                                                                         ## indciates working tile is one space left
                    if Working_Tile.right == True:                                                          ## if the current tile has a right door
                        walled = False                                                                      ## no longer walled       
            checked_directions.append(rand_direction)                                                       ## marked that we checked that direction
            
        if len(checked_directions) >= 4 or walled == True:                                                                    ## if every direction is blocked
            Working_Tile = Working_Tile.parent                                                              ## back up to the parent
        else:                                                                                               ## if not trapped                   
            rand_index = random.randint(2,29)                                                               ## generates a random number from 2-29 to call the tiles
            while rand_index in used:                                                                       ## checks if the number has already been used
                rand_index = random.randint(2,29)                                                           ## if already been used get another random number and try again
            tile = int(hex(tiles[rand_index]), 16)                                                          ## get the tile information after converting to hex from intiger value
            map_data[new_row][new_column] = tile                                                            ## replaces the blank tile with the new tile value
            New_Tile = tile_textures[map_data[new_row][new_column]]                                         ## Calls forth the new tile
            match direction:
                case "U":
                    if New_Tile.down == False:
                        New_Tile.rotate_clockwise
                case "D":
                    if New_Tile.up == False:
                        New_Tile.rotate_clockwise
                case "L":
                    if New_Tile.right == False:
                        New_Tile.rotate_clockwise
                case "R":
                    if New_Tile.left == False:
                        New_Tile.rotate_clockwise
            Working_Tile.add_child(New_Tile)                                                                ## adds the new tile as a child of the working tile 
            New_Tile.parent = Working_Tile                                                                  ## adds the new tile parent as the working title 
            Working_Tile = New_Tile                                                                         ## Moves onto the next tile
            row = new_row                                                                                   ## sets the row as the new row
            column = new_column                                                                             ## sets the column as the new column
            map_data[row][column] = tile                                                                    ## sets the new tile up in the correction location
            used.append(rand_index)                                                                         ## add the rand_index to the used list
            
            ## for limiting window size (still needs work)
            if row > max_row:
                max_row = row
            if row < min_row:
                min_row = row
            if column > max_column:
                max_column = column
            if column < min_column:
                min_column = column

    max_mins = [min_row, max_row, min_column, max_column]
    print("max_mins ", max_mins)
    return map_data, max_mins                                                                                ## returns the map data

def draw_map(screen, map_data, max_mins, TILE_SIZE):
    
    MAP_HEIGHT = len(map_data) 
    MAP_WIDTH = len(map_data[0])
    for row in range(MAP_HEIGHT):
        for col in range(MAP_WIDTH):
    #for row in range(max_mins[0], max_mins[1]+1):
    #    for col in range(max_mins[2], max_mins[3]+1):
            screen.blit(tile_textures[map_data[row][col]].texture,                                          ## Grabs the tile image and displays it at it's current location
                        (col*TILE_SIZE, row*TILE_SIZE))  
            if tile_textures[map_data[row][col]].token != None:                                             ## if the tile has a token
                screen.blit(tile_textures[map_data[row][col]].token,                                        ## display the token at about a 3rd of a TILE_SIZE down and right from the upper left of the tile location
                        (col*TILE_SIZE+TILE_SIZE/3, row*TILE_SIZE+TILE_SIZE/3))     
## Source: https://github.com/gurb/rpg-game-tutorials/blob/main/004-Generating%20Tile%20Map/tilemap.py
import pygame
import random
import math

# dimension of each tiles
TILE_SIZE = 128

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
class Tile():
    def __init__(filepath):
        self.image = pygame.image.load(filepath)                          ## loads the image in
        filename = filepath.split("/")                                    ## Cuts out all but the name
        title = filename[2].split(".")                                    ## Cuts out the .jpg
        self.info = title[0].split("_")                                   ## Breaks the name into useful information
        self.id = self.info[0]                                            ## 
        self.type = self.info[1]
        self.name = self.info[2]
        self.doors = self.info[3]

    ## Turns the image into the tile texture according to the requested size
    def create_texture(name):
        image = name
        image = pygame.transform.scale(image,(TILE_SIZE,TILE_SIZE))
        return image

    def setup():
        self.texture = create_texture(self.image)                       ## creates the appropriate texture for the image
        exec("%s = %d" % (self.name,self.texture))                      ## turns the name into a variable for the textures list below
        ## call the file
        ## get the image
        ## cut off .jpg and before the /
        ## break it up by _
        ## get id number: Put in data member
        ## Identify tile type: Put in data member
        ## Get file Name: Put in data member
        ## Get Directions: Check against dictionary, otherwise false
        ## Create a funciton to rotate tile image (and doors)
        ## save a neighbor Function



## Linking the names of the tiles with the location of the images
BackTile   = pygame.image.load("Images/Tile_Scans/0_None_BackTile_None.jpg")
Start = pygame.image.load("Images/Tile_Scans/1_Start_StartTile_UDLR.jpg")
FireofEidolon   = pygame.image.load("Images/Tile_Scans/2_FireofEidolon_FireofEidolon_D.jpg") 
VoraxsHeart = pygame.image.load("Images/Tile_Scans/3_RedEvent_VoraxsHeart_D.jpg")
VoraxFocus = pygame.image.load("Images/Tile_Scans/4_GreenEvent_VoraxFocus_D.jpg")
VoraxKnowledge = pygame.image.load("Images/Tile_Scans/5_BlueEvent_VoraxsKnowledge_D.jpg")
End = pygame.image.load("Images/Tile_Scans/6_End_EndTile_UPLR.jpg")
SecretX = pygame.image.load("Images/Tile_Scans/7_Secret_SecretX_UPLR.jpg")
SecretY = pygame.image.load("Images/Tile_Scans/8_Secret_SecretY_UPLR.jpg")
VoraciousPlant = pygame.image.load("Images/Tile_Scans/9_Red_VoraciousPlant_UPLR.jpg")
Minotaur = pygame.image.load("Images/Tile_Scans/10_Red_Minotaur_UPLR.jpg")
FloatingStones = pygame.image.load("Images/Tile_Scans/11_Green_FloatingStones_UPLR.jpg")
LaughingShadow = pygame.image.load("Images/Tile_Scans/12_Blue_LaughingShadow_UPLR.jpg")
Psychomancer = pygame.image.load("Images/Tile_Scans/13_Blue_Psychomancer_UPLR.jpg")
Dragonling = pygame.image.load("Images/Tile_Scans/14_Red_Dragonling_UDL.jpg")
ParadoxPuzzle = pygame.image.load("Images/Tile_Scans/15_Blue_ParadoxPuzzle_UDL.jpg")
FelKnight = pygame.image.load("Images/Tile_Scans/16_Red_FelKnight_UDR.jpg")
SpikedPit = pygame.image.load("Images/Tile_Scans/17_Green_SpikedPit_UDR.jpg")
DenofSnakes = pygame.image.load("Images/Tile_Scans/18_DenofSnakes_UDR.jpg")
ArrowTrap = pygame.image.load("Images/Tile_Scans/19_Green_ArrowTrap_DLR.jpg")
Mindeater = pygame.image.load("Images/Tile_Scans/20_Blue_Mindeater_DLR.jpg")
SkeletalGuards = pygame.image.load("Images/Tile_Scans/21_Red_SkeletalGuards_UD.jpg")
PendulumBlades = pygame.image.load("Images/Tile_Scans/22_Green_PendulumBlades_UD.jpg")
AcidJets = pygame.image.load("Images/Tile_Scans/23_Green_AcidJets_UD.jpg")
SphynxRiddle = pygame.image.load("Images/Tile_Scans/24_Blue_SphynxsRiddle_UD.jpg")
OgreBrute = pygame.image.load("Images/Tile_Scans/25_Red_OgreBrute_DL.jpg")
LavaLake = pygame.image.load("Images/Tile_Scans/26_Green_LavaLake_DL.jpg")
DarkSlime = pygame.image.load("Images/Tile_Scans/27_Red_DarkSlime_DR.jpg")
HallofIllusion = pygame.image.load("Images/Tile_Scans/28_Blue_HallofIllusion_DR.jpg")
MimicChest = pygame.image.load("Images/Tile_Scans/29_Blue_MimicChest_D.jpg")



## Assigning values to the tile for the computer to run through them
## Values in Hexidecimal (don't know why but it works)
textures = {
    0x0 : create_texture(BackTile),
    0x1 : create_texture(Start),
    0x2 : create_texture(FireofEidolon),
    0x3 : create_texture(VoraxsHeart),
    0x4 : create_texture(VoraxFocus),
    0x5 : create_texture(VoraxKnowledge),
    0x6 : create_texture(End),
    0x7 : create_texture(SecretX),
    0x8 : create_texture(SecretY),
    0x9 : create_texture(VoraciousPlant),
    0xa : create_texture(Minotaur),
    0xb : create_texture(FloatingStones),
    0xc : create_texture(LaughingShadow),
    0xd : create_texture(Psychomancer),
    0xe : create_texture(Dragonling),
    0xf : create_texture(ParadoxPuzzle),
    0x10 : create_texture(FelKnight),
    0x11 : create_texture(SpikedPit),
    0x12 : create_texture(DenofSnakes),
    0x13 : create_texture(ArrowTrap),
    0x14 : create_texture(Mindeater),
    0x15 : create_texture(SkeletalGuards),
    0x16 : create_texture(PendulumBlades),
    0x17 : create_texture(AcidJets),
    0x18 : create_texture(SphynxRiddle),
    0x19 : create_texture(OgreBrute),
    0x1a : create_texture(LavaLake),
    0x1b : create_texture(DarkSlime),
    0x1c : create_texture(HallofIllusion),
    0x1d : create_texture(MimicChest),
}

## Turns the values of the tile into a list
tiles = [0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xa, 0xb, 0xc, 0xd, 0xe, 0xf, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d]



# generate with tiles randomly
def generate_map(width, height, tilesize):
    map_data = []
    used = []                                                                                               ## initializes the list for the tiles already used
    for i in range(height // tilesize):
        map_data.append([])
        for j in range(width // tilesize):
            rand_index = random.randint(2,29)                                                               ## generates a random number from 2-29 to call the tiles
            if i == (math.trunc((height//tilesize)/2)) and j == (math.trunc((width//tilesize)/2)):          ## if the tile in question is at the center
                rand_index = 1                                                                              ## put the start tile there (setting rand to 1)
            if rand_index in used:                                                                          ## if the tile has been used before
                rand_index = 0                                                                              ## put in the filler tile instead (setting rand to zero)
            else:                                                                                           ## if the tile has not been used before
                used.append(rand_index)                                                                     ## add the number to the used index
            # convert to hex from string value
            tile = int(hex(tiles[rand_index]), 16)                                                          ## get the tile information
            map_data[i].append(tile)                                                                        ## add the tile to the map
    return map_data


def draw_map(screen, map_data, TILE_SIZE):
    MAP_HEIGHT = len(map_data) 
    MAP_WIDTH = len(map_data[0])
    for row in range(MAP_HEIGHT):
        for col in range(MAP_WIDTH):
            screen.blit(textures[map_data[row][col]],
                        (col*TILE_SIZE, row*TILE_SIZE))        
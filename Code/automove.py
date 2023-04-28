import settings
from tilemap import *


TILE_SIZE = settings.TILE_SIZE  ## Gets the size of the tile from the settings file and sets it as a global variable

def automove(self, step):
    if step == 'u':
        print('U')
        if 'u' in tile_textures[self.map_data[self.row][self.column]].quickinfo:
                if self.row-1 >= 0:                                                                                                                             ## makes sure player doesn't walk off edge
                    if 'd' in tile_textures[self.map_data[self.row-1][self.column]].quickinfo:
                        self.actions.append("U")                                                                                                                ## remembers it moved up
                        self.move(0, -TILE_SIZE)
                        self.keycount += 1
    elif step == 'r':
        print('R')
        if 'r' in tile_textures[self.map_data[self.row][self.column]].quickinfo:
                if self.column+1 < len(self.map_data[0]):                                                                                                       ## makes sure player doesn't walk off edge
                    if 'l' in tile_textures[self.map_data[self.row][self.column+1]].quickinfo:
                        self.actions.append("R")                                                                                                                ## remembers it moved right
                        self.move(+TILE_SIZE, 0)
                        self.keycount += 1
    elif step == 'd':
        print('D')
        if 'd' in tile_textures[self.map_data[self.row][self.column]].quickinfo:
                if self.row+1 < len(self.map_data):                                                                                                             ## makes sure player doesn't walk off edge
                    if 'u' in tile_textures[self.map_data[self.row+1][self.column]].quickinfo:
                        self.actions.append("D")                                                                                                                ## remembers it moved down
                        self.move(0, +TILE_SIZE)
                        self.keycount += 1
    elif step == 'l':
        print('L')
        if 'l' in tile_textures[self.map_data[self.row][self.column]].quickinfo:
                if self.column-1 >= 0:                                                                                                                          ## makes sure player doesn't walk off edge
                    if 'r' in tile_textures[self.map_data[self.row][self.column-1]].quickinfo:
                        self.actions.append("L")                                                                                                                ## remembers it moved left
                        self.move(-TILE_SIZE, 0)
                        self.keycount += 1
    elif step == 'x':
        print('TUNNEL')
        if tile_textures[self.map_data[self.row][self.column]].name == "SecretX":                                                                           ## if on secret X tile              
                self.row = int(self.Y_tile[0])                                                                                                                  ## This is the row the player is at
                self.column = int(self.Y_tile[1])                                                                                                               ## This is the column the player is at
                self.rect.centerx = self.adjust + self.column*TILE_SIZE + TILE_SIZE/2                                                                           ## places the player at the Secret Y's x position
                self.rect.centery = self.row*TILE_SIZE + TILE_SIZE/2                                                                                            ## places the player at the Secret Y's y position
                self.actions.append("X")                                                                                                                        ## Used the secret X tunnel
                self.move(0, 0)                                                                                                                                 ## records where the player went
                self.keycount += 1
    elif step == 'y':
        if tile_textures[self.map_data[self.row][self.column]].name == "SecretY":                                                                         ## if on a secret Y tile                  
                self.row = int(self.X_tile[0])                                                                                                                  ## This is the row the player is at
                self.column = int(self.X_tile[1])                                                                                                               ## This is the column the player is at
                self.rect.centerx = self.adjust + self.column*TILE_SIZE + TILE_SIZE/2                                                                           ## places the player at the Secret Y's x position
                self.rect.centery = self.row*TILE_SIZE + TILE_SIZE/2                                                                                            ## places the player at the Secret Y's y position
                self.actions.append("Y")                                                                                                                        ## Used the secret Y tunnel
                self.move(0, 0)                                                                                                                                 ## records where the player went
                self.keycount += 1
    elif step == 'bt' or step == 'rt' or step == 'gt' or step == 'ret' or step == 'get' or step == 'bet' or step == 'foe':
        if tile_textures[self.map_data[self.row][self.column]].token != None:                                                                               ## If there is a tile there
            match tile_textures[self.map_data[self.row][self.column]].type:                                                                                 ## determine what the tile type is
                case "Red":                                                                                                                                 ## if it's listed as red
                    if (4 - self.Strength + self.keycount) <= 3:
                        self.keycount = 4 - self.Strength + self.keycount
                        self.totalcost = 4 - self.Strength + self.totalcost                                                                                     ## adds cost (1 cost if Strength = 3, 2 cost is Strength = 2, 3 cost is Strength = 1)
                        settings.total_actions_value = 4 - self.Strength + settings.total_actions_value
                        self.Red_Token = self.Red_Token + 1                                                                                                     ## increase the Red_Token by 1
                        settings.total_Red_Tokens += 1
                        tile_textures[self.map_data[self.row][self.column]].token = None                                                                        ## Removes the token
                        tile_textures[self.map_data[self.row][self.column]].quickinfo.remove("rt")                                                              ## Removes the token from quick info
                        self.actions.append("T")
                case "Green":                                                                                                                               ## if it's listed as green
                    if (4 - self.Agility + self.keycount) <= 3:
                        self.keycount = 4 - self.Agility + self.keycount
                        self.totalcost = 4 - self.Agility + self.totalcost                                                                                      ## adds cost (1 cost if Agility = 3, 2 cost is Agility = 2, 3 cost is Agility = 1)
                        settings.total_actions_value = 4 - self.Agility + settings.total_actions_value
                        self.Green_Token = self.Green_Token + 1                                                                                                 ## increase the Green_Token by 1
                        settings.total_Green_Tokens += 1
                        tile_textures[self.map_data[self.row][self.column]].token = None                                                                        ## Removes the token
                        tile_textures[self.map_data[self.row][self.column]].quickinfo.remove("gt")                                                              ## Removes the token from quick info  
                        self.actions.append("T")
                case "Blue":                                                                                                                                ## if it's listed as blue
                    if (4 - self.Intelligence + self.keycount) <= 3:
                        self.keycount = 4 - self.Intelligence + self.keycount
                        self.totalcost = 4 - self.Intelligence + self.totalcost                                                                                 ## adds cost (1 cost if Intelligence = 3, 2 cost is Intelligence = 2, 3 cost is Intelligence = 1)
                        settings.total_actions_value = 4 - self.Intelligence + settings.total_actions_value
                        self.Blue_Token = self.Blue_Token + 1                                                                                                   ## increase the Blue_Token by 1
                        settings.total_Blue_Tokens += 1
                        tile_textures[self.map_data[self.row][self.column]].token = None                                                                        ## Removes the token
                        tile_textures[self.map_data[self.row][self.column]].quickinfo.remove("bt")                                                              ## Removes the token from quick info
                        self.actions.append("T")
                case "RedEvent":                                                                                                                            ## if it's listed as red event
                    if self.Red_Token >= 6 or settings.total_Red_Tokens >= 6:                                                                                                                 ## do you have enough tokens to break the red event
                        self.totalcost = self.totalcost + 1                                                                                                 ## costs 1 action to break event
                        self.keycount += 1
                        settings.total_actions_value += 1
                        settings.Red_Event_Broken = True                                                                                                    ## breaks the red event
                        tile_textures[self.map_data[self.row][self.column]].type = "Broken_RedEvent"                                                        ## displays the broken red event token
                        tile_textures[self.map_data[self.row][self.column]].token = tile_textures[self.map_data[self.row][self.column]].Token_grabber()     ## changes the token visual
                        tile_textures[self.map_data[self.row][self.column]].quickinfo.remove("ret")                                                         ## Removes the token from quick info
                        self.Red_Token = 0
                        self.actions.append("T")
                case "GreenEvent":                                                                                                                          ## if it's listed as green event 
                    if self.Green_Token >= 6 or settings.total_Green_Tokens >= 6:                                                                                                               ## do you have enough tokens to break the green event
                        self.totalcost = self.totalcost + 1                                                                                                 ## costs 1 action to break event
                        settings.total_actions_value += 1
                        settings.Green_Event_Broken = True                                                                                                  ## breaks the green event
                        tile_textures[self.map_data[self.row][self.column]].type = "Broken_GreenEvent"                                                      ## displays the broken green event token
                        tile_textures[self.map_data[self.row][self.column]].token = tile_textures[self.map_data[self.row][self.column]].Token_grabber()     ## changes the token visual
                        tile_textures[self.map_data[self.row][self.column]].quickinfo.remove("get")                                                         ## Removes the token from quick info
                        self.Green_Token = 0
                        self.keycount += 1
                        self.actions.append("T")
                case "BlueEvent":                                                                                                                           ## if it's listed as blue event
                    if self.Blue_Token >= 6 or settings.total_Blue_Tokens >= 6:                                                                                                                ## do you have enough tokens to break the blue event
                        self.totalcost = self.totalcost + 1                                                                                                 ## costs 1 action to break event
                        settings.total_actions_value += 1
                        settings.Blue_Event_Broken = True                                                                                                   ## breaks the blue event
                        tile_textures[self.map_data[self.row][self.column]].type = "Broken_BlueEvent"                                                       ## displays the broken blue event token
                        tile_textures[self.map_data[self.row][self.column]].token = tile_textures[self.map_data[self.row][self.column]].Token_grabber()     ## changes the token visual
                        tile_textures[self.map_data[self.row][self.column]].quickinfo.remove("bet")                                                         ## Removes the token from quick info
                        self.Blue_Token = 0
                        self.keycount += 1
                        self.actions.append("T")
                case "FireofEidolon":                                                                                                                       ## if it's listed as Fire of Eidolon
                    if settings.Red_Event_Broken == True and settings.Green_Event_Broken == True and settings.Blue_Event_Broken == True:                    ## all other events broken?
                        self.totalcost = self.totalcost + 1                                                                                                 ## costs 1 action to grab Fire of Eidolon
                        settings.total_actions_value += 1
                        settings.FireofEidolon_Grabbed = True                                                                                               ## marks that the Fire of Eidolon has been grabbed
                        self.FireofEidolon = 1                                                                                                              ## indicates that the player has the Fire of Eidolon
                        tile_textures[self.map_data[self.row][self.column]].token = None                                                                    ## Removes the token
                        tile_textures[self.map_data[self.row][self.column]].quickinfo.remove("foe")                                                         ## Removes the token from quick info
                        self.keycount += 1
                        self.actions.append("T")

    self.goalUpdate()                                                                                                                              ## updates on what your next goal should be
    #print(self.totalcost)                                                                                                                           ## used for debugging 

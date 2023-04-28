## This file consists of the global variables that are shared from all files in program

TILE_SIZE = 64                      ## sets the TILE_SIZE
Red_Event_Broken = False            ## has the red_event token been broken yet
Green_Event_Broken = False          ## has the green_event token been broken yet
Blue_Event_Broken = False           ## has the blue_event token been broken yet
FireofEidolon_Grabbed = False       ## no one has grabbed the Fire of Eidolon yet
Win = False                         ## did the player win?
planning = False                    ## is the player planning the next move
seen = False                        ## did the player at least try to explore
Players = []                        ## keeps track of player informaiton
Red_Tiles = []                      ## these tiles have red tokens
Green_Tiles = []                    ## these tiles have green tokens
Blue_Tiles = []                     ## these tiles have blue tokens
total_Red_Tokens = 0                ## keeps track of the total red tokens for all the players
total_Green_Tokens = 0              ## keeps track of the total green tokens for all the players
total_Blue_Tokens = 0               ## keeps track of the total blue tokens for all the players
total_actions_value = 0             ## keeps track of the total cost of all the actions taken
Active_Player = None                ## shows which player is active
token_map = []                      ## map of all the tokens locations
red_token_locations = []            ## list of the locations of the red tokens
blue_token_locations = []           ## list of the locations of the blue tokens
green_token_locations = []          ## list of the locations of the green tokens
selfplay = False                    ## the game plays by itself


To run the program type in the terminal "python run_main"

If the program returns "FAILED" in the terminal, then the map generation created a map where it is impossible to win and you will need to run the program again.

If the program successfully creates a map, a separate screen will appear displaying the map created, with all of the players on the starting tile. You can change the size of the tiles before running the program by changing the TILE_SIZE value in the settings.py.  The TILE_SIZE is the number pixels by pixels of the size of the square. The default is 64 x 64 pixels.

The white scoreboard at the bottom of the screen will display which player's turn it is, how many actions that player has left, how many red tokens, green tokens, and blue tokens have been collected by the players. The scoreboard will also display the total cost of actions that have been taken by the players. The suggested path the closest token that Player 1 prefers will also be displayed.  

The default is the blue meeple player will be Player 1 and will prefer blue tokens. It takes the blue meeple player 1 action to pick up blue tokens, 2 actions to pick up red tokens, and 3 actions to pick up green tokens. This is a nod to wizards in TTRPG's.

The red meeple player is Player 2 and will prefer red tokens. It takes the red meeple player 1 action to pick up red tokens, 2 actions to pick up green tokens, and 3 actions to pick up blue tokens. This is a nod to barbarians in TTRPG's.

The green meeple player is Player 3 and will prefer green tokens. It takes the green meeple player 1 action to pick up green tokens, 2 actions to pick up blue tokens, and 3 actions to pick up red tokens. This is a nod to rouges in TTRPG's.

A player's preference is based on the number of actions needed to pick up a token.  You can change a player's preference by going to run_main and change Player(sprites_group, map_data, Strength, Intelligence, Agility). Change Strength to pick up red tokens, Intelligence to pick up blue tokens, and Agility to pick up green tokens. The equation is 4-Value = # of actions to pick up corresponding token color. For example if I wanted to add a player 4 who had the ability to cost 1 action to pick up red tokens, 3 actions to pick up blue tokens, and 2 actions to pick up green tokens I would put "player4 = Player(sprites_group, map_data, 3, 1, 2)".

The players must have at least 6 tokens of a given color to break one of the event tokens. Once 6 tokens of a color have been collected the pathing will considered if the corresponding event token as a potential tile goal and will no longer consider tokens of the color as potential goal points.  It will only ever cost 1 action to break any of the corresponding event tokens. You must break all three event tokens before collecting the Fire of Eidolon.  Once a player grabs the Fire of Eidolon, an image of the Fire of Eidolon will be displayed on the scoreboard and all players will move towards the end tile. The game is considered won when the player who grabbed the Fire of Eidolon reaches the end tile. Once the game is won, the path all players took is displayed on the map, with the statement "YOU WIN" displayed on the score board.

Using the keys ‘w’, ‘a’, ‘s’ and ‘d’ for moving up, left, down and right respectively. The player cannot move through tiles without connected doors. The player also cannot move off the map.

The player can pick up a token or break an event token by using ‘e’. Use ‘q’ to take the secret passage, and ‘p’ to perform a single A* search. The planning button ‘p’ is not necessary for manual gameplay but is available. Press 'r' to remove any pathing instructions. Press 'l' to pass their turn without adding cost to an action. Press 'b' to automatically perform a turn. Press 'u' and the game will play the rest of the game by itself.

If 'u' is pressed, the computer will register '7' key being pressed in between actions.  This is to force the computer to slow down and see each action rather than having the program make the visuals jump at the speed the program run, which is faster than the eye can see.

If I wanted to run a program of a pre-determined map instead of the default of a random map, comment out the line "map_data, max_mins = building_random_map(width, height)" and uncomment the lines, "tile_order = [[ 0,  3,  0,  0,  0,  0,  0],  [20, 10,  0,  0,  0,  0,  0], [16,  7,  0,  0, 13, 25, 0], [0, 24,  0,  0,  5,  1, 27], [ 0, 15,  0,  0,  4,  9, 29],  [ 0, 18, 26, 12, 14, 21, 0],  [ 0,  2, 22,  8, 19, 28,  0], [ 0,  0,  6, 23,  0,  0,  0], [ 0,  0, 17, 11, 0, 0,  0]]", "rotations = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 1], [0, 0, 0, 0, 3, 0, 2], [0, 0, 0, 0, 0, 0, 0], [0, 2, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]" and  "#map_data, max_mins = building_premade_map(tile_order, rotations)"

Change the tile number to match the index of the tile you want at that given location:
    0  : Back Tile/Obstical Tile,
    1  : Start Tile,
    2  : Fire of Eidolon,
    3  : Voraxs Heart,
    4  : Vorax Focus,
    5  : Voraxs Knowledge,
    6  : End Tile,
    7  : SecretX,
    8  : SecretY,
    9  : Voracious Plant,
    10 : Minotaur,
    11 : Floating Stones,
    12 : Laughing Shadow,
    13 : Psychomancer,
    14 : Dragonling,
    15 : Paradox Puzzle,
    16 : Fel Knight,
    17 : Spiked Pit,
    18 : Den of Snakes,
    19 : Arrow Trap,
    20 : Mindeater,
    21 : Skeletal Guards,
    22 : Pendulum Blades,
    23 : Acid Jets,
    24 : Sphynxs Riddle,
    25 : Ogre Brute,
    26 : Lava Lake,
    27 : Dark Slime,
    28 : Hall of Illusion,
    29 : Mimic Chest

Change the rotations to determine how many times a title is rotated 90 degrees clockwise. For example, if I want my tile to be rotate 270 degrees, I would change the number to 3.

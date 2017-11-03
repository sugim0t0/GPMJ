#!/usr/bin/env python

''' GPMJ (General Purpose (Japanese) Mah-Jong library)
    gpmjgame module

Modification History:
===========================================================
Date           Version   Description
===========================================================
31 Oct. 2017   0.1       Creation
01 Nov. 2017   0.2       Add GameConfig class
03 Nov. 2017   0.3       Add setup_round(), print_wall()
-----------------------------------------------------------
'''

import configparser
import random
import gpmjcore

__version__ = "0.3"
__date__    = "03 Nov. 2017"
__author__  = "Shun SUGIMOTO <sugimoto.shun@gmail.com>"

class Game():

    def __init__(self):
        # Config
        self.config = GameConfig()
        # Tiles
        self.tiles = []
        # Wall
        self.wall = []
        self.dead_wall = []
        self.wall_index = 0
        self.dead_wall_index = 0
        # Dora indicators
        self.doras = []
        self.underneath_doras = []
        # Hand judge chain
        self.basic_hand_jc = None
        self.basic_limit_hand_jc = None
        self.seven_pairs_hand_jc = None
        self.seven_pairs_limit_hand_jc = None
        self.thirteen_orphans_j = None
        # Round info.
        self.round_wind = gpmjcore.Winds.EAST
        self.round_number = 1

    def create_tiles(self):
        # Simples
        for suit in range(gpmjcore.Suits.NUM_OF_SIMPLES):
            for number in range(1, 10):
                for x in range(4):
                    tile = gpmjcore.Tile(suit, number)
                    if x < self.config.num_of_red5[suit]:
                        tile.b_red = True
                    self.tiles.append(tile)
        # Winds
        for number in range(gpmjcore.Winds.NUM_OF_WINDS):
            for x in range(4):
                self.tiles.append(gpmjcore.Tile(gpmjcore.Suits.WINDS, number))
        # Dragons
        for number in range(gpmjcore.Dragons.NUM_OF_DRAGONS):
            for x in range(4):
                self.tiles.append(gpmjcore.Tile(gpmjcore.Suits.DRAGONS, number))

    def setup_round(self):
        self.wall_index = 0
        self.dead_wall_index = 0
        # Build walls
        random.shuffle(self.tiles)
        self.wall = []
        self.dead_wall = []
        for x in range(122):
            self.wall.append(self.tiles[x])
        for x in range(122, 136):
            self.dead_wall.append(self.tiles[x])
        # Dora
        self.doras.append(self.dead_wall[4])
        self.underneath_doras.append(self.dead_wall[5])
        return True

    def draw_tile(self):
        tile = self.wall[self.wall_index]
        self.wall_index += 1
        return tile

    def call_kong(self):
        tile = self.dead_wall[self.dead_wall_index]
        self.dead_wall_index += 1
        # New Dora
        self.doras.append(self.dead_wall[4 + (self.dead_wall_index * 2)])
        self.underneath_doras.append(self.dead_wall[5 + (self.dead_wall_index * 2)])
        return tile

    def print_wall(self):
        # wall
        print("[wall]")
        for x in range(4):
            for y in range(17):
                index = (x * 34) + (y * 2)
                if index < len(self.wall):
                    print(self.wall[index].print_char, end="")
            print("")
            for y in range(17):
                index = (x * 34) + (y * 2) + 1
                if index < len(self.wall):
                    print(self.wall[index].print_char, end="")
            print("")
            print("")
        # dead_wall
        print("[dead wall]")
        for y in range(7):
            index = y * 2
            if index < len(self.dead_wall):
                print(self.dead_wall[index].print_char, end="")
        print("")
        for y in range(7):
            index = (y * 2) + 1
            if index < len(self.dead_wall):
                print(self.dead_wall[index].print_char, end="")
        print("")
        print("")


class GameConfig():

    def __init__(self):
        # Number of Red 5 tiles
        self.num_of_red5 = [0, 0, 0]
        # East wind game(=True) / East and South wind game(=False)
        self.east_wind_game = False

    def parse_config(self, cfg_file_path):
        config = configparser.ConfigParser()
        config.read(cfg_file_path)
        default_section = config['default']
        # Number of Red 5 tiles
        self.num_of_red5[gpmjcore.Suits.DOTS] = default_section.getint('num_of_red5_dot')
        self.num_of_red5[gpmjcore.Suits.BAMBOO] = default_section.getint('num_of_red5_bamboo')
        self.num_of_red5[gpmjcore.Suits.CHARACTERS] = default_section.getint('num_of_red5_character')
        # East wind game / East and South wind game
        self.east_wind_game = default_section.getboolean('east_wind_game')

        return True


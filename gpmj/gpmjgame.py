#!/usr/bin/env python

''' GPMJ (General Purpose (Japanese) Mah-Jong library)
    gpmjgame module

Modification History:
===========================================================
Date           Version   Description
===========================================================
31 Oct. 2017   0.1       Creation
01 Nov. 2017   0.2       Add GameConfig class
-----------------------------------------------------------
'''

import configparser
import gpmjcore

__version__ = "0.2"
__date__    = "01 Nov. 2017"
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

    def create_tiles(self, tiles):
        # Simples
        for suit in range(gpmjcore.Suits.NUM_OF_SIMPLES):
            for number in range(1, 10):
                for x in range(4):
                    tiles.append(gpmjcore.Tile(suit, number))
        # Winds
        for number in range(gpmjcore.Winds.NUM_OF_WINDS):
            for x in range(4):
                tiles.append(gpmjcore.Tile(gpmjcore.Suits.WINDS, number))
        # Dragons
        for number in range(gpmjcore.Dragons.NUM_OF_DRAGONS):
            for x in range(4):
                tiles.append(gpmjcore.Tile(gpmjcore.Suits.DRAGONS, number))

    def setup_round(self):
        self.wall_index = 0
        self.dead_wall_index = 0
        # Build walls
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


class GameConfig():

    def __init__():
        self.red_5_tiles = True

    def parse_config(self, cfg_file_path):
        config = configparser.ConfigParser()
        return True


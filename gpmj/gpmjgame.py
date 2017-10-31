#!/usr/bin/env python

''' GPMJ (General Purpose (Japanese) Mah-Jong library)
    gpmjgame module

Modification History:
===========================================================
Date           Version   Description
===========================================================
31 Oct. 2017   0.1       Creation
-----------------------------------------------------------
'''

import configparser
import gpmjcore

__version__ = "0.1"
__date__    = "31 Oct. 2017"
__author__  = "Shun SUGIMOTO <sugimoto.shun@gmail.com>"

class Game():

    def __init__(self):
        # Parse config file
        self.parse_config()
        # Tiles
        self.mountain = []
        self.create_tiles(self.mountain)
        # Hand judge chain
        self.basic_hand_jc = None
        self.basic_limit_hand_jc = None
        self.seven_pairs_hand_jc = None
        self.seven_pairs_limit_hand_jc = None
        # Round info.
        self.round_wind = gpmjcore.Winds.EAST
        self.round_number = 1

    def parse_config(self, cfg_file_path):
        config = configparser.ConfigParser()
        return True

    def create_tiles(self, mountain):
        # Simples
        for suit in range(gpmjcore.Suits.NUM_OF_SIMPLES):
            for number in range(1, 10):
                for x in range(4):
                    mountain.append(gpmjcore.Tile(suit, number))
        # Winds
        for number in range(gpmjcore.Winds.NUM_OF_WINDS):
            for x in range(4):
                mountain.append(gpmjcore.Tile(gpmjcore.Suits.WINDS, number))
        # Dragons
        for number in range(gpmjcore.Dragons.NUM_OF_DRAGONS):
            for x in range(4):
                mountain.append(gpmjcore.Tile(gpmjcore.Suits.DRAGONS, number))

    def setup_round(self):
        return True




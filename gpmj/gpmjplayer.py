#!/usr/bin/env python

''' GPMJ (General Purpose (Japanese) Mah-Jong library)
    gpmjplayer module

Modification History:
===========================================================
Date           Version   Description
===========================================================
31 Oct. 2017   0.1       Creation
11 Dec. 2017   0.2       Add event handler functions
15 Feb. 2018   0.3       Add pickup_tile_after_declared_ready_handler()
-----------------------------------------------------------
'''

import threading, queue
import gpmjcore
import gpmjgame

__version__ = "0.3"
__date__    = "15 Feb. 2018"
__author__  = "Shun SUGIMOTO <sugimoto.shun@gmail.com>"

class Player():

    def __init__(self, name):
        self.name = name
        self.info = None

    # Following functions SHOULD be overridden.

    # Event handler for pick up tile
    def pickup_tile_handler(self, tile):
        return tile

    def pickup_tile_after_declared_ready_handler(self, tile):
        return tile

    def win_selfpick_handler(self, tile):
        return True

    def closed_kong_handler(self, tile, melds):
        return None

    def added_kong_handler(self, tile, melds):
        return None

    def declare_ready_handler(self, tile, tiles):
        return None

    # Event handler for discarded tile
    def win_discard_handler(self, tile):
        return True

    def chow_handler(self, tile, melds):
        return (None, None) # (meld, discard_tile)

    def pong_handler(self, tile, melds):
        return (None, None) # (meld, discard_tile)

    def stolen_kong_handler(self, tile):
        return False


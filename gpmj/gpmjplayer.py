#!/usr/bin/env python

''' GPMJ (General Purpose (Japanese) Mah-Jong library)
    gpmjplayer module

Modification History:
===========================================================
Date           Version   Description
===========================================================
31 Oct. 2017   0.1       Creation
-----------------------------------------------------------
'''

import gpmjcore

__version__ = "0.1"
__date__    = "31 Oct. 2017"
__author__  = "Shun SUGIMOTO <sugimoto.shun@gmail.com>"

class Player():

    def __init__(self, name, seat_wind):
        self.name = name
        self.hand = gpmjcore.Hand()
        self.seat_wind = seat_wind


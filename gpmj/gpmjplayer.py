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

import threading, queue
import gpmjcore
import gpmjgame

__version__ = "0.1"
__date__    = "31 Oct. 2017"
__author__  = "Shun SUGIMOTO <sugimoto.shun@gmail.com>"

class Player():

    def __init__(self, name):
        self.name = name
        self.info = None


class PlayerCtrl(threading.Thread):

    def __init__(self, player):
        super(PlayerCtrl, self).__init__()
        self.player = player

    def run(self):
        ev_player = None
        ev_game = None
        while(True):
            ev_game = self.player.info.ev_game_queue.get(True, None)
            if ev_game.event_id == gpmjgame.EventId.EV_PICKUP_TILE:
                ev_player = self.player.
          #  elif ev_game.event_id == gpmjgame.EventId.EV_CLOSED_KONG:
          #  elif ev_game.event_id == gpmjgame.EventId.EV_ADDED_KONG:
          #  elif ev_game.event_id == gpmjgame.EventId.EV_STOLEN_KONG:
          #  elif ev_game.event_id == gpmjgame.EventId.EV_CHOW:
          #  elif ev_game.event_id == gpmjgame.EventId.EV_PONG:
          #  elif ev_game.event_id == gpmjgame.EventId.EV_WIN_SELFPICK:
          #  elif ev_game.event_id == gpmjgame.EventId.EV_WIN_DISCARD:
            else:
                break
            self.player.info.ev_player_queue.put(ev_player, False, None)


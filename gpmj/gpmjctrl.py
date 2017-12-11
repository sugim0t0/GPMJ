#!/usr/bin/env python

''' GPMJ (General Purpose (Japanese) Mah-Jong library)
    gpmjctrl module

Modification History:
===========================================================
Date           Version   Description
===========================================================
11 Dec. 2017   0.1       Creation
-----------------------------------------------------------
'''

import threading, queue
import gpmjcore
import gpmjgame
import gpmjplayer
from enum import Enum, IntEnum

__version__ = "0.1"
__date__    = "11 Dec. 2017"
__author__  = "Shun SUGIMOTO <sugimoto.shun@gmail.com>"

class PlayerCtrl(threading.Thread):

    def __init__(self, player):
        super(PlayerCtrl, self).__init__()
        self.player = player

    def run(self):
        ev_player = None
        ev_game = None
        while(True):
            ev_game = self.player.info.ev_game_queue.get(True, None)
            if ev_game.event_id == EventFlag.EV_PICKUP_TILE:
                discard_tile
                ev_player = self.player.
          #  elif ev_game.event_id == EventFlag.EV_CLOSED_KONG:
          #  elif ev_game.event_id == EventFlag.EV_ADDED_KONG:
          #  elif ev_game.event_id == EventFlag.EV_STOLEN_KONG:
          #  elif ev_game.event_id == EventFlag.EV_CHOW:
          #  elif ev_game.event_id == EventFlag.EV_PONG:
          #  elif ev_game.event_id == EventFlag.EV_WIN_SELFPICK:
          #  elif ev_game.event_id == EventFlag.EV_WIN_DISCARD:
            else:
                break
            self.player.info.ev_player_queue.put(ev_player, False, None)


class GameCtrl(threading.Thread):

    def __init__(self, game):
        super(GameCtrl, self).__init__()
        self.game = Game()
        self.game.create_tiles()
        self.game.setup_hand_judger()
        self.turn_player = None

    def run(self):
        for player_info in self.game.players_info:
            for next_player_info in self.game.players_info:
                if ((player_info.seat_wind + 1) % gpmjcore.Winds.NUM_OF_WINDS) \
                   == next_player_info.seat_wind:
                    player_info.next_player = next_player_info
                    break
        while(True):
            (b_continued, b_count_keep) = self.__round()
            if not self.game.goto_next_round(b_continued, b_count_keep):
                # GAME OVER
                break

    def __round(self):
        ev_game = None
        ev_player = None
        self.game.setup_round()
        for player_info in self.game.players_info:
            self.game.deal_starttiles(self.game.dealplayer_info.hand)
            if player_info.seat_wind == gpmjcore.Winds.EAST:
                self.turn_player = player_info
        while(True):
            tile = self.game.draw_tile()
            if tile is None:
                return (self.game.round_over(), True)
            # check win by selfpick tile
            if True == self.__check_win_selfpick(self.turn_player, tile, b_last, False):
                if self.turn_player.seat_wind == gpmjcore.Winds.EAST:
                    return (True, True)
                else:
                    return (False, False)
            ev_game = GameEvent(EventFlag.EV_PICKUP_TILE, tile, None)
            self.turn_player.ev_game_queue.put(ev_game, False, None)
            while(True):
                ev_player = self.turn_player.ev_player_queue.get(True, None)
                if ev_player.event_id == EventFlag.EV_DISCARD_TILE or \
                   ev_player.event_id == EventFlag.EV_DECLARE_READY:
                    discard_tile = ev_player.tile
                    # check win by discarded tile
                    b_last = False
                    if len(self.game.wall) == 0:
                        b_last = True
                    self.__check_win_discard(self.turn_player, discard_tile, b_last)
                    if ev_player.event_id == EventFlag.EV_DECLARE_READY:
                        self.game.discard_tile(self.turn_player, discard_tile, True)
                    else:
                        self.game.discard_tile(self.turn_player, discard_tile, False)
                    self.turn_player = self.turn_player.next_player
                    break

    def __check_win_selfpick(self, turn_player, tile, b_last, b_dead_wall_draw):
        if tile.number in turn_player.hand.required[tile.suit]:
            state_flag = turn_player.make_state_flag(False, b_dead_wall_draw, False, b_last)
            score = self.game.get_hand_score(turn_player.hand, state_flag, tile, False, turn_player.seat_wind)
            if not score == (0, 0):
                ev_game = GameEvent(EventFlag.EV_WIN_SELFPICK, tile, None)
                turn_player.ev_game_queue.put(ev_game, False, None)
                ev_player = turn_player.ev_player_queue.get(True, None)
                if ev_player.event_id == EventFlag.EV_WIN_SELFPICK:
                    self.game.win(turn_player, False, gpmjcore.Winds.INVALID, score)
                    return True
        return False

    def __check_win_discard(self, turn_player, tile, b_last, b_robbing_a_quad):
        next_player = turn_player.next_player
        for x in range(3):
            if tile.number in next_player.hand.required[tile.suit]:
                state_flag = next_player.make_state_flag(True, False, b_robbing_a_quad, b_last)
                score = self.game.get_hand_score(next_player.hand, state_flag, tile, True, next_player.seat_wind)
                if not score == (0, 0):
                    ev_game = GameEvent(EventFlag.EV_WIN_DISCARD, tile, None)
                    next_player.ev_game_queue.put(ev_game, False, None)
                    ev_player = next_player.ev_player_queue.get(True, None)
                    if ev_player.event_id == EventFlag.EV_WIN_DISCARD:
                        self.game.win(next_player, True, self.turn_player.seat_wind, score)
                        return True
            next_player = next_player.next_player
        return False


class EventFlag(IntEnum):
 
    # Game -> Player events
    EV_PICKUP_TILE   = 0x00000001
    # Game <- Player events
    EV_DO_NOTHING    = 0x00000000
    EV_DISCARD_TILE  = 0x00000002
    # Game <-> Player events
    EV_CLOSED_KONG   = 0x00000004
    EV_ADDED_KONG    = 0x00000008
    EV_STOLEN_KONG   = 0x00000010
    EV_CHOW          = 0x00000020
    EV_PONG          = 0x00000040
    EV_DECLARE_READY = 0x00000080
    EV_WIN_SELFPICK  = 0x00000100
    EV_WIN_DISCARD   = 0x00000200


class GameEvent():

    def __init__(self, event_id, tile, melds):
        self.event_id = event_id
        self.tile = tile
        self.melds = melds


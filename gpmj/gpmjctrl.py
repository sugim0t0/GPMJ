#!/usr/bin/env python

''' GPMJ (General Purpose (Japanese) Mah-Jong library)
    gpmjctrl module

Modification History:
===========================================================
Date           Version   Description
===========================================================
11 Dec. 2017   0.1       Creation
12 Dec. 2017   0.2       Add PlayerCtrl and GameCtrl classes
14 Dec. 2017   0.3       Add run()@PlayerCtrl
08 Jan. 2018   0.4       Modified to call update_required()
-----------------------------------------------------------
'''

import threading, queue
import gpmjcore
import gpmjgame
import gpmjplayer
from enum import Enum, IntEnum

__version__ = "0.4"
__date__    = "08 Jan. 2018"
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
            # Events from pick up tile
            if ev_game.event_flag & EventFlag.EV_WIN_SELFPICK:
                if self.player.win_selfpick_handler(ev_game.tile):
                    ev_player = GameEvent(EventFlag.EV_WIN_SELFPICK, ev_game.tile, None)
                    self.player.info.ev_player_queue.put(ev_player, False, None)
                    continue
            if ev_game.event_flag & EventFlag.EV_CLOSED_KONG:
                if self.player.closed_kong_handler(ev_game.tile):
                    ev_player = GameEvent(EventFlag.EV_CLOSED_KONG, ev_game.tile, None)
                    self.player.info.ev_player_queue.put(ev_player, False, None)
                    continue
            elif ev_game.event_flag & EventFlag.EV_ADDED_KONG:
                if self.player.added_kong_handler(ev_game.tile):
                    ev_player = GameEvent(EventFlag.EV_ADDED_KONG, ev_game.tile, None)
                    self.player.info.ev_player_queue.put(ev_player, False, None)
                    continue
            if ev_game.event_flag & EventFlag.EV_DECLARE_READY:
                discard_tile = self.player.declare_ready_handler(ev_game.tile)
                if discard_tile is not None:
                    ev_player = GameEvent(EventFlag.EV_DECLARE_READY, discard_tile, None)
                    self.player.info.ev_player_queue.put(ev_player, False, None)
                    continue
            if ev_game.event_flag & EventFlag.EV_PICKUP_TILE:
                discard_tile = self.player.pickup_tile_handler(ev_game.tile)
                ev_player = GameEvent(EventFlag.EV_DISCARD_TILE, discard_tile, None)
                self.player.info.ev_player_queue.put(ev_player, False, None)
                continue
            # Events from discarded tile
            if ev_game.event_flag & EventFlag.EV_WIN_DISCARD:
                if self.player.win_discard_handler(ev_game.tile):
                    ev_player = GameEvent(EventFlag.EV_WIN_DISCARD, ev_game.tile, None)
                    self.player.info.ev_player_queue.put(ev_player, False, None)
                    continue
            if ev_game.event_flag == EventFlag.EV_STOLEN_KONG:
                if self.player.stolen_kong_handler(ev_game.tile):
                    ev_player = GameEvent(EventFlag.EV_STOLEN_KONG, ev_game.tile, None)
                    self.player.info.ev_player_queue.put(ev_player, False, None)
                    continue
            if ev_game.event_flag == EventFlag.EV_PONG:
                meld = self.player.pong_handler(ev_game.tile, ev_game.melds)
                if meld is not None:
                    ev_player = GameEvent(EventFlag.EV_PONG, None, meld)
                    self.player.info.ev_player_queue.put(ev_player, False, None)
                    continue
            if ev_game.event_flag == EventFlag.EV_CHOW:
                meld = self.player.chow_handler(ev_game.tile, ev_game.melds)
                if meld is not None:
                    ev_player = GameEvent(EventFlag.EV_CHOW, None, meld)
                    self.player.info.ev_player_queue.put(ev_player, False, None)
                    continue
            else:
                break


class GameCtrl(threading.Thread):

    def __init__(self):
        super(GameCtrl, self).__init__()
        self.game = gpmjgame.Game()
        self.game.config.parse_config("./gpmj.cfg")
        self.game.create_tiles()
        self.game.setup_hand_judger()
        self.turn_player = None

    def set_playerctrl(self, playerctrl):
        playerctrl.player.info = self.game.set_player(playerctrl.player.name)

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
            # Reset player info
            for player_info in self.game.players_info:
                player_info.reset_round(b_continued)

    def __round(self):
        ev_game = None
        ev_player = None
        self.game.setup_round()
        b_last = False
        self.game.print_players_score()
        for player_info in self.game.players_info:
            self.game.deal_starttiles(player_info.hand)
            if player_info.seat_wind == gpmjcore.Winds.EAST:
                self.turn_player = player_info
        while(True):
            tile = self.game.draw_tile()
            if tile is None:
                return (self.game.round_over(), True)
            if len(self.game.wall) == 0:
                b_last = True
            self.turn_player.hand.sort_tiles()
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
                self.game.pickup_tile(self.turn_player, tile)
                if ev_player.event_flag == EventFlag.EV_DISCARD_TILE or \
                   ev_player.event_flag == EventFlag.EV_DECLARE_READY:
                    discard_tile = ev_player.tile
                    if ev_player.event_flag == EventFlag.EV_DECLARE_READY:
                        self.game.discard_tile(self.turn_player, discard_tile, True)
                    else:
                        self.game.discard_tile(self.turn_player, discard_tile, False)
                    self.turn_player.print_discards()
                    # check win by discarded tile
                    if True == self.__check_win_discard(self.turn_player, discard_tile, b_last, False):
                        if self.turn_player.seat_wind == gpmjcore.Winds.EAST:
                            return (True, True)
                        else:
                            return (False, False)
                    self.turn_player.hand.update_required()
                    self.turn_player = self.turn_player.next_player
                    break

    def __check_win_selfpick(self, turn_player, tile, b_last, b_dead_wall_draw):
        if tile.number in turn_player.hand.required[tile.suit]:
            state_flag = turn_player.make_state_flag(False, b_dead_wall_draw, False, b_last)
            win_hand = self.game.get_winhand(turn_player.hand, state_flag, tile, False, turn_player.seat_wind)
            if win_hand is not None:
                ev_game = GameEvent(EventFlag.EV_WIN_SELFPICK, tile, None)
                turn_player.ev_game_queue.put(ev_game, False, None)
                ev_player = turn_player.ev_player_queue.get(True, None)
                if ev_player.event_flag == EventFlag.EV_WIN_SELFPICK:
                    score = self.game.get_hand_score(win_hand)
                    win_hand.print_win_hand()
                    self.game.win(turn_player, False, gpmjcore.Winds.INVALID, score)
                    return True
        return False

    def __check_win_discard(self, turn_player, tile, b_last, b_robbing_a_quad):
        next_player = turn_player.next_player
        for x in range(3):
            if tile.number in next_player.hand.required[tile.suit]:
                state_flag = next_player.make_state_flag(True, False, b_robbing_a_quad, b_last)
                win_hand = self.game.get_winhand(next_player.hand, state_flag, tile, True, next_player.seat_wind)
                if win_hand is not None:
                    ev_game = GameEvent(EventFlag.EV_WIN_DISCARD, tile, None)
                    next_player.ev_game_queue.put(ev_game, False, None)
                    ev_player = next_player.ev_player_queue.get(True, None)
                    if ev_player.event_flag == EventFlag.EV_WIN_DISCARD:
                        score = self.game.get_hand_score(win_hand)
                        win_hand.print_win_hand()
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

    def __init__(self, event_flag, tile, melds):
        self.event_flag = event_flag
        self.tile = tile
        self.melds = melds


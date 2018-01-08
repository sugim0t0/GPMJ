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
04 Nov. 2017   0.4       Add setup_hand_judger()
05 Nov. 2017   0.5       Add get_hand_score()
11 Nov. 2017   0.6       Add get_num_of_dora()
12 Nov. 2017   0.7       Add print_dead_wall()
18 Nov. 2017   0.8       Add PlayerInfo class
20 Nov. 2017   0.9       Add print_players_score()
26 Nov. 2017   0.10      Add discard_tile(), game_over()
03 Dec. 2017   0.11      Add GameCtrl class
04 Dec. 2017   0.12      Add make_state_flag()
06 Dec. 2017   0.13      Add __check_win_selfpick() and __check_win_discard()
09 Dec. 2017   0.14      Add __round()
11 Dec. 2017   0.15      Divide GameCtrl class into gpmjctrl module
-----------------------------------------------------------
'''

import configparser
import random
import queue
import gpmjcore
from enum import Enum, IntEnum

__version__ = "0.15"
__date__    = "11 Dec. 2017"
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
        # Dora indicators
        self.doras = []
        self.underneath_doras = []
        # Kong count
        self.kong_count = 0
        # Hand judger
        self.basic_hand_jc = None
        self.basic_limit_hand_jc = None
        self.seven_pairs_hand_jc = None
        self.seven_pairs_limit_hand_jc = None
        self.thirteen_orphans_j = None
        # Round info.
        self.round_wind = gpmjcore.Winds.EAST
        self.round_number = 1
        self.round_continue_count = 0
        # Number of declared ready sticks
        self.num_of_declared_ready_sticks = 0
        # Players info.
        self.players_info = []

    def set_player(self, name):
        if len(self.players_info) == gpmjcore.Winds.NUM_OF_WINDS:
            return None
        player_info = PlayerInfo(name, len(self.players_info))
        self.players_info.append(player_info)
        return player_info

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

    def setup_hand_judger(self):
        # Basic hand (4 melds and 1 eye)
        basic_hand_j = gpmjcore.HandJudge()
        self.basic_hand_jc = gpmjcore.HandJudgeChain(basic_hand_j)
        self.basic_limit_hand_jc = gpmjcore.HandJudgeChain(basic_hand_j)
        # Seven pairs (7 eyes)
        seven_pairs_j = gpmjcore.SevenPairsJudge()
        self.seven_pairs_hand_jc = gpmjcore.HandJudgeChain(seven_pairs_j)
        self.seven_pairs_limit_hand_jc = gpmjcore.HandJudgeChain(seven_pairs_j)
        # 13 orphans
        self.thirteen_orphans_j = gpmjcore.ThirteenOrphansJudge()

        # ValuedDragon(s)
        white_dragon_j = gpmjcore.ValuedDragonJudge(gpmjcore.HandFlag.WHITE_DRAGON, \
                                                     gpmjcore.Dragons.WHITE)
        white_dragon_jc = gpmjcore.HandJudgeChain(white_dragon_j)
        green_dragon_j = gpmjcore.ValuedDragonJudge(gpmjcore.HandFlag.GREEN_DRAGON, \
                                                     gpmjcore.Dragons.GREEN)
        green_dragon_jc = gpmjcore.HandJudgeChain(green_dragon_j)
        red_dragon_j = gpmjcore.ValuedDragonJudge(gpmjcore.HandFlag.RED_DRAGON, \
                                                   gpmjcore.Dragons.RED)
        red_dragon_jc = gpmjcore.HandJudgeChain(red_dragon_j)
        # SeatWind
        seat_wind_j = gpmjcore.SeatWindJudge()
        seat_wind_jc = gpmjcore.HandJudgeChain(seat_wind_j)
        # RoundWind
        round_wind_j = gpmjcore.RoundWindJudge()
        round_wind_jc = gpmjcore.HandJudgeChain(round_wind_j)
        # NoPointsHand
        no_points_hand_j = gpmjcore.NoPointsHandJudge()
        no_points_hand_jc = gpmjcore.HandJudgeChain(no_points_hand_j)
        # OneSetOfIdenticalSequences
        one_set_of_identical_sequences_j = gpmjcore.OneSetOfIdenticalSequencesJudge()
        one_set_of_identical_sequences_jc = gpmjcore.HandJudgeChain(one_set_of_identical_sequences_j)
        # AllSimples
        all_simples_j = gpmjcore.AllSimplesJudge()
        all_simples_jc = gpmjcore.HandJudgeChain(all_simples_j)
        all_simples_7p_jc = gpmjcore.HandJudgeChain(all_simples_j)
        # ThreeColorStraight
        three_color_straight_j = gpmjcore.ThreeColorStraightJudge()
        three_color_straight_jc = gpmjcore.HandJudgeChain(three_color_straight_j)
        # Straight
        straight_j = gpmjcore.StraightJudge()
        straight_jc = gpmjcore.HandJudgeChain(straight_j)
        # TerminalOrHonorInEachSet
        terminal_or_honor_in_each_set_j = gpmjcore.TerminalOrHonorInEachSetJudge()
        terminal_or_honor_in_each_set_jc = gpmjcore.HandJudgeChain(terminal_or_honor_in_each_set_j)
        # AllTripletHand
        all_triplet_hand_j = gpmjcore.AllTripletHandJudge()
        all_triplet_hand_jc = gpmjcore.HandJudgeChain(all_triplet_hand_j)
        # ThreeClosedTriplets
        three_closed_triplets_j = gpmjcore.ThreeClosedTripletsJudge()
        three_closed_triplets_jc = gpmjcore.HandJudgeChain(three_closed_triplets_j)
        # ThreeColorTriplets
        three_color_triplets_j = gpmjcore.ThreeColorTripletsJudge()
        three_color_triplets_jc = gpmjcore.HandJudgeChain(three_color_triplets_j)
        # ThreeKongs
        three_kongs_j = gpmjcore.ThreeKongsJudge()
        three_kongs_jc = gpmjcore.HandJudgeChain(three_kongs_j)
        # AllTerminalsAndHonors
        all_terminals_and_honors_j = gpmjcore.AllTerminalsAndHonorsJudge()
        all_terminals_and_honors_jc = gpmjcore.HandJudgeChain(all_terminals_and_honors_j)
        all_terminals_and_honors_7p_jc = gpmjcore.HandJudgeChain(all_terminals_and_honors_j)
        # LittleThreeDragons 
        little_three_dragons_j = gpmjcore.LittleThreeDragonsJudge()
        little_three_dragons_jc = gpmjcore.HandJudgeChain(little_three_dragons_j)
        # TerminalInEachSet
        terminal_in_each_set_j = gpmjcore.TerminalInEachSetJudge()
        terminal_in_each_set_jc = gpmjcore.HandJudgeChain(terminal_in_each_set_j)
        # HalfFlush
        half_flush_j = gpmjcore.HalfFlushJudge()
        half_flush_jc = gpmjcore.HandJudgeChain(half_flush_j)
        half_flush_7p_jc = gpmjcore.HandJudgeChain(half_flush_j)
        # TwoSetOfIdenticalSequences
        two_set_of_identical_sequences_j = gpmjcore.TwoSetOfIdenticalSequencesJudge()
        two_set_of_identical_sequences_jc = gpmjcore.HandJudgeChain(two_set_of_identical_sequences_j)
        # Flush
        flush_j = gpmjcore.FlushJudge()
        flush_jc = gpmjcore.HandJudgeChain(flush_j)
        flush_7p_jc = gpmjcore.HandJudgeChain(flush_j)
        # FourConcealedTriplets
        four_concealed_triplets_j = gpmjcore.FourConcealedTripletsJudge()
        four_concealed_triplets_jc = gpmjcore.HandJudgeChain(four_concealed_triplets_j)
        # BigThreeDragons
        big_three_dragons_j = gpmjcore.BigThreeDragonsJudge()
        big_three_dragons_jc = gpmjcore.HandJudgeChain(big_three_dragons_j)
        # LittleFourWinds
        little_four_winds_j = gpmjcore.LittleFourWindsJudge()
        little_four_winds_jc = gpmjcore.HandJudgeChain(little_four_winds_j)
        # BigFourWinds
        big_four_winds_j = gpmjcore.BigFourWindsJudge()
        big_four_winds_jc = gpmjcore.HandJudgeChain(big_four_winds_j)
        # AllHonors
        all_honors_j = gpmjcore.AllHonorsJudge()
        all_honors_jc = gpmjcore.HandJudgeChain(all_honors_j)
        all_honors_7p_jc = gpmjcore.HandJudgeChain(all_honors_j)
        # AllTerminals
        all_terminals_j = gpmjcore.AllTerminalsJudge()
        all_terminals_jc = gpmjcore.HandJudgeChain(all_terminals_j)
        # AllGreen
        all_green_j = gpmjcore.AllGreenJudge()
        all_green_jc = gpmjcore.HandJudgeChain(all_green_j)
        # NineGates
        nine_gates_j = gpmjcore.NineGatesJudge()
        nine_gates_jc = gpmjcore.HandJudgeChain(nine_gates_j)
        # FourKongs
        four_kongs_j = gpmjcore.FourKongsJudge()
        four_kongs_jc = gpmjcore.HandJudgeChain(four_kongs_j)

        # connect basic limit hand judge chains
        self.basic_limit_hand_jc.connect_chain(nine_gates_jc, None)
        nine_gates_jc.connect_chain(None, all_honors_jc)
        all_honors_jc.connect_chain(big_three_dragons_jc, big_three_dragons_jc)
        big_three_dragons_jc.connect_chain(four_concealed_triplets_jc, big_four_winds_jc)
        big_four_winds_jc.connect_chain(four_concealed_triplets_jc, little_four_winds_jc)
        little_four_winds_jc.connect_chain(four_concealed_triplets_jc, all_green_jc)
        all_green_jc.connect_chain(four_concealed_triplets_jc, all_terminals_jc)
        all_terminals_jc.connect_chain(four_concealed_triplets_jc, four_concealed_triplets_jc)
        four_concealed_triplets_jc.connect_chain(four_kongs_jc, four_kongs_jc)
        four_kongs_jc.connect_chain(None, None)
        # connect basic hand judge chains
        self.basic_hand_jc.connect_chain(all_simples_jc, None)
        all_simples_jc.connect_chain(no_points_hand_jc, white_dragon_jc)
        white_dragon_jc.connect_chain(green_dragon_jc, green_dragon_jc)
        green_dragon_jc.connect_chain(red_dragon_jc, red_dragon_jc)
        red_dragon_jc.connect_chain(seat_wind_jc, seat_wind_jc)
        seat_wind_jc.connect_chain(round_wind_jc, round_wind_jc)
        round_wind_jc.connect_chain(little_three_dragons_jc, terminal_in_each_set_jc)
        terminal_in_each_set_jc.connect_chain(no_points_hand_jc, little_three_dragons_jc)
        little_three_dragons_jc.connect_chain(half_flush_jc, half_flush_jc)
        half_flush_jc.connect_chain(terminal_or_honor_in_each_set_jc, terminal_or_honor_in_each_set_jc)
        terminal_or_honor_in_each_set_jc.connect_chain(no_points_hand_jc, straight_jc)
        straight_jc.connect_chain(no_points_hand_jc, all_terminals_and_honors_jc)
        all_terminals_and_honors_jc.connect_chain(three_kongs_jc, no_points_hand_jc)
        no_points_hand_jc.connect_chain(two_set_of_identical_sequences_jc, three_kongs_jc)
        three_kongs_jc.connect_chain(three_closed_triplets_jc, three_closed_triplets_jc)
        three_closed_triplets_jc.connect_chain(three_color_triplets_jc, three_color_triplets_jc)
        three_color_triplets_jc.connect_chain(all_triplet_hand_jc, all_triplet_hand_jc)
        all_triplet_hand_jc.connect_chain(flush_jc, two_set_of_identical_sequences_jc)
        two_set_of_identical_sequences_jc.connect_chain(flush_jc, one_set_of_identical_sequences_jc)
        one_set_of_identical_sequences_jc.connect_chain(three_color_straight_jc, three_color_straight_jc)
        three_color_straight_jc.connect_chain(None, flush_jc)
        flush_jc.connect_chain(None, None)
        # connect 7 pairs limit hand judge chains
        self.seven_pairs_limit_hand_jc.connect_chain(all_honors_7p_jc, None)
        all_honors_7p_jc.connect_chain(None, None)
        # connect 7 pairs hand judge chains
        self.seven_pairs_hand_jc.connect_chain(all_simples_7p_jc, None)
        all_simples_7p_jc.connect_chain(None, flush_7p_jc)
        flush_7p_jc.connect_chain(None, half_flush_7p_jc)
        half_flush_7p_jc.connect_chain(all_terminals_and_honors_7p_jc, all_terminals_and_honors_7p_jc)
        all_terminals_and_honors_7p_jc.connect_chain(None, None)

    def goto_next_round(self, b_continued, b_count_keep):
        '''
        True  : Go to next round
        False : GAME OVER
        '''
        if b_continued:
            self.round_continue_count += 1
            return True
        if b_count_keep:
            self.round_continue_count += 1
        else:
            self.round_continue_count = 0
        if self.round_number < 4:
            self.round_number += 1
        else:
            if self.config.east_wind_game or \
               self.round_wind >= gpmjcore.Winds.SOUTH:
                for player_info in self.players_info:
                    if player_info.score >= self.config.min_score_gameover:
                        # GAME OVER
                        return False
            self.round_number = 1
            if self.round_wind < gpmjcore.Winds.NORTH:
                self.round_wind += 1
            else:
                self.round_wind = gpmjcore.Winds.EAST
        for player_info in self.players_info:
            player_info.seat_wind = (player_info.seat_wind + 1) % gpmjcore.Winds.NUM_OF_WINDS
        return True

    def setup_round(self):
        # Build walls
        # shuffle tiles
        random.shuffle(self.tiles)
        self.wall = []
        self.dead_wall = []
        # stack tiles
        for x in range(122):
            self.wall.append(self.tiles[x])
        for x in range(122, 136):
            self.dead_wall.append(self.tiles[x])
        # Dora
        self.kong_count = 0
        for x in range(5):
            self.doras.append(self.dead_wall[9 - (x * 2)])
            self.underneath_doras.append(self.dead_wall[8 - (x * 2)])

    def deal_starttiles(self, hand):
        for x in range(13):
            hand.append_tile(self.wall.pop())

    def get_hand_score(self, hand, state_flag, last_tile, b_discarded, seat_wind):
        win_hand = None
        hand.append_tile(last_tile)
        # 13 orphans
        if self.thirteen_orphans_j.judge_13orphans_hand(hand.pure_tiles):
            win_hand = gpmjcore.WinHand()
            win_hand.set_property(state_flag, last_tile, b_discarded, seat_wind, self.round_wind)
            win_hand.hand_value += 13
        else:
            # basic hand
            win_hands = hand.get_winhands_basic(state_flag, last_tile, b_discarded, seat_wind, self.round_wind)
            if win_hands is not None:
                for w_h in win_hands:
                    self.basic_limit_hand_jc.judge_chain(w_h)
                    if w_h.hand_flag & gpmjcore.HandFlag.LIMIT_HAND:
                        win_hand = w_h
                        break
                    else:
                        w_h.hand_value = 0
                        self.basic_hand_jc.judge_chain(w_h)
                        if (win_hand is None) or (win_hand.hand_value < w_h.hand_value):
                            w_h.calc_points()
                            win_hand = w_h
                        elif win_hand.hand_value == w_h.hand_value:
                            w_h.calc_points()
                            if win_hand.hand_point < w_h.hand_point:
                                win_hand = w_h
            # 7 pairs
            else:
                win_hand = hand.get_winhand_7pairs(state_flag, last_tile, b_discarded, seat_wind, self.round_wind)
                if win_hand is not None:
                    self.seven_pairs_limit_hand_jc.judge_chain(win_hand)
                    if not win_hand.hand_flag & gpmjcore.HandFlag.LIMIT_HAND:
                        win_hand.hand_value = 0
                        self.seven_pairs_hand_jc.judge_chain(win_hand)
                        win_hand.calc_points()
        if win_hand is None:
            return (0, 0)
        b_declared_ready = False
        if state_flag & (gpmjcore.StateFlag.DECLARE_READY | gpmjcore.StateFlag.DECLARE_DOUBLE_READY):
            b_declared_ready = True
        num_of_dora = self.get_num_of_dora(hand, b_declared_ready)
        score = win_hand.calc_score(num_of_dora)
        if self.round_continue_count > 0:
            if b_discarded:
                return (score[0] + 300 * self.round_continue_count, 0)
            elif seat_wind == gpmjcore.Winds.EAST:
                return (score[0] + 100 * self.round_continue_count, 0)
            else:
                return (score[0] + 100 * self.round_continue_count, score[1] + 100 * self.round_continue_count)
        else:
            return score

    def draw_tile(self):
        if len(self.wall) > 0:
            return self.wall.pop()
        else:
            return None

    def pickup_tile(self, player_info, tile):
        player_info.hand.append_tile(tile)

    def discard_tile(self, player_info, tile, b_declare_ready):
        player_info.hand.remove_tile(tile)
        player_info.discards.append(tile)
        if b_declare_ready:
            if player_info.score >= 1000:
                player_info.score -= 1000
                self.num_of_declared_ready_sticks += 1
            else:
                return False
            if player_info.b_first_pick:
                player_info.b_declared_double_ready = True
            else:
                player_info.b_declared_ready = True
            player_info.b_one_shot = True
        elif player_info.b_one_shot:
            player_info.b_one_shot = False
        if player_info.b_first_pick:
            player_info.b_first_pick = False
        return True

    def win(self, win_player_info, b_discarded, discard_player_wind, score):
        if b_discarded:
            for player_info in self.players_info:
                if player_info.seat_wind == discard_player_wind:
                    win_player_info.score += score[0]
                    player_info.score -= score[0]
                    break
            else:
                return False
        else:
            if win_player_info.seat_wind == gpmjcore.Winds.EAST:
                for player_info in self.players_info:
                    if player_info is not win_player_info:
                        win_player_info.score += score[0]
                        player_info.score -= score[0]
            else:
                for player_info in self.players_info:
                    if player_info is not win_player_info:
                        if player_info.seat_wind == gpmjcore.Winds.EAST:
                            win_player_info.score += score[1]
                            player_info.score -= score[1]
                        else:
                            win_player_info.score += score[0]
                            player_info.score -= score[0]
        if self.num_of_declared_ready_sticks > 0:
            win_player_info.score += (1000 * self.num_of_declared_ready_sticks)
            self.num_of_declared_ready_sticks = 0
        return True

    def round_over(self):
        b_dealer_ready = False
        num_of_ready_players = 0
        for player_info in self.players_info:
            b_ready = False
            for suit in range(gpmjcore.Suits.NUM_OF_SUITS):
                if len(player_info.hand.required[suit]) > 0:
                    player_info.b_ready = True
                    if player_info.seat_wind == gpmjcore.Winds.EAST:
                        b_dealer_ready = True
                    num_of_ready_players += 1
                    break
        if num_of_ready_players > 0 and num_of_ready_players < 4:
            for player_info in self.players_info:
                if player_info.b_ready:
                    player_info.score += (3000 // num_of_ready_players)
                else:
                    player_info.score -= (3000 // (4 - num_of_ready_players))
        if self.config.continue_by_dealer_ready:
            return b_dealer_ready
        else:
            return False

    def game_over(self):
        top_player_info = None
        for player_info in self.players_info:
            if top_player_info is None or top_player_info.score < player_info.score:
                top_player_info = player_info
            elif top_player_info.score == player_info.score and \
                 top_player_info.start_seat_wind > player_info.start_seat_wind:
                top_player_info = player_info
        if self.num_of_declared_ready_sticks > 0:
            top_player_info.score += (1000 * self.num_of_declared_ready_sticks)

    def call_kong(self):
        if self.kong_count < 4 and len(self.wall) > 0:
            self.kong_count += 1
            tile = self.dead_wall.pop()
            self.dead_wall.insert(0, self.wall.pop(0))
            return tile
        else:
            return None

    def get_num_of_dora(self, hand, b_declared_ready):
        num_of_dora = 0
        doras = []
        underneath_doras = []
        for x in range(self.kong_count + 1):
            doras.append(self.doras[x].get_dora_from_indicator())
        if b_declared_ready and self.config.available_underneath_dora:
            for x in range(self.kong_count + 1):
                underneath_doras.append(self.underneath_doras[x].get_dora_from_indicator())
        for suit in range(gpmjcore.Suits.NUM_OF_SUITS):
            for tile in hand.pure_tiles[suit]:
                for dora in doras:
                    # dora is tuple (suit, number)
                    if tile.suit == dora[0] and tile.number == dora[1]:
                        num_of_dora += 1
                for dora in underneath_doras:
                    if tile.suit == dora[0] and tile.number == dora[1]:
                        num_of_dora += 1
                if tile.b_red:
                    num_of_dora += 1
        for meld in hand.exposed:
            for tile in meld.tiles:
                for dora in doras:
                    # dora is tuple (suit, number)
                    if tile.suit == dora[0] and tile.number == dora[1]:
                        num_of_dora += 1
                for dora in underneath_doras:
                    if tile.suit == dora[0] and tile.number == dora[1]:
                        num_of_dora += 1
                if tile.b_red:
                    num_of_dora += 1
        return num_of_dora

    def print_wall(self):
        # wall
        print("[wall]")
        rest_of_tile = len(self.wall)
        if rest_of_tile == 0:
            print("No tiles in wall")
            return
        elif rest_of_tile == 1:
            print("")
            print(self.wall[0].print_char)
            return
        remainder = rest_of_tile % 34
        if (remainder % 2) == 0:
            upper_index = len(self.wall) - 1
            downer_index = len(self.wall) - 2
        else:
            upper_index = len(self.wall) - 2
            downer_index = len(self.wall) - 1
        if remainder > 0:
            # Upper tiles of wall
            if (remainder % 2) == 0:
                space = (34 - remainder) // 2
            else:
                space = ((34 - remainder) // 2) + 1
            for x in range(space):
                print("    ", end="")
            for x in range(17 - space):
                print(self.wall[upper_index].print_char, end="")
                upper_index -= 2
                rest_of_tile -= 1
            print("")
            # Downer tiles of wall
            space = (34 - remainder) // 2
            for x in range(space):
                print("    ", end="")
            for x in range(17 - space):
                print(self.wall[downer_index].print_char, end="")
                downer_index -= 2
                rest_of_tile -= 1
            print("")
            print("")
        while rest_of_tile > 0:
            # Upper tiles of wall
            for x in range(17):
                print(self.wall[upper_index].print_char, end="")
                upper_index -= 2
                rest_of_tile -= 1
            print("")
            # Downer tiles of wall
            for x in range(17):
                print(self.wall[downer_index].print_char, end="")
                downer_index -= 2
                rest_of_tile -= 1
            print("")
            print("")
        return

    def print_dead_wall(self):
        # dead wall
        print("[dead wall]")
        if (self.kong_count % 2) == 0:
            upper_index = 13
            downer_index = 12
        else:
            upper_index = 12
            downer_index = 13
            print("    ", end="")
        # Upper tiles of dead wall
        for x in range(7):
            print(self.dead_wall[upper_index].print_char, end="")
            upper_index -= 2
        print("")
        # Downer tiles of dead wall
        for x in range(7):
            print(self.dead_wall[downer_index].print_char, end="")
            downer_index -= 2
        print("")
        print("")

    def print_players_score(self):
        for player_info in self.players_info:
            print(player_info.name + ":" + str(player_info.score))


class PlayerInfo():

    def __init__(self, name, seat_wind):
        self.name = name
        self.score = 25000
        self.start_seat_wind = seat_wind
        self.seat_wind = seat_wind
        self.reset_round(True)
        self.next_player = None
        self.ev_game_queue = queue.Queue()   # Game -> Player
        self.ev_player_queue = queue.Queue() # Game <- Player

    def reset_round(self, b_continued):
        self.hand = gpmjcore.Hand()
        self.b_ready = False
        self.b_first_pick = True
        self.b_declared_ready = False
        self.b_declared_double_ready = False
        self.b_one_shot = False
        self.b_stolen = False
        self.discards = []
        if not b_continued:
            self.seat_wind = (self.seat_wind + 3) % gpmjcore.Winds.NUM_OF_WINDS

    def make_state_flag(self, b_discarded, b_dead_wall_draw, b_robbing_a_quad, b_last):
        state_flag = 0x0
        # LIMIT STATES
        if self.b_first_pick:
            if b_discarded:
                state_flag |= gpmjcore.StateFlag.HAND_OF_MAN
            elif self.seat_wind == gpmjcore.Winds.EAST:
                state_flag |= gpmjcore.StateFlag.HEAVENLY_HAND
            else:
                state_flag |= gpmjcore.StateFlag.HAND_OF_EARTH
            return state_flag
        # NORMAL STATES
        if self.b_declared_double_ready:
            state_flag |= gpmjcore.StateFlag.DECLARE_DOUBLE_READY
        elif self.b_declared_ready:
            state_flag |= gpmjcore.StateFlag.DECLARE_READY
        if self.b_one_shot:
            state_flag |= gpmjcore.StateFlag.ONE_SHOT
        if not self.b_stolen and not b_discarded:
            state_flag |= gpmjcore.StateFlag.SELF_PICK
        if b_last:
            if b_discarded:
                state_flag |= gpmjcore.StateFlag.LAST_DISCARD
            else:
                state_flag |= gpmjcore.StateFlag.LAST_TILE_FROM_THE_WALL
        if b_dead_wall_draw:
            state_flag |= gpmjcore.StateFlag.DEAD_WALL_DRAW
        elif b_robbing_a_quad:
            state_flag |= gpmjcore.StateFlag.ROBBING_A_QUAD
        return state_flag


class GameConfig():

    def __init__(self):
        ## DORA
        # Number of Red 5 tiles
        self.num_of_red5 = [0, 0, 0]
        # Underneath Dora is available
        self.available_underneath_dora = True
        ## GAME
        # East wind game(=True) / East and South wind game(=False)
        self.east_wind_game = False
        # Minimum score for GAME OVER
        self.min_score_gameover = 0
        ## ROUND
        self.continue_by_dealer_ready = True

    def parse_config(self, cfg_file_path):
        config = configparser.ConfigParser()
        config.read(cfg_file_path)
        ## DORA
        dora_section = config['dora']
        # Number of Red 5 tiles
        self.num_of_red5[gpmjcore.Suits.DOTS] = dora_section.getint('num_of_red5_dot')
        self.num_of_red5[gpmjcore.Suits.BAMBOO] = dora_section.getint('num_of_red5_bamboo')
        self.num_of_red5[gpmjcore.Suits.CHARACTERS] = dora_section.getint('num_of_red5_character')
        # Underneath Dora is available
        self.available_underneath_dora = dora_section.getboolean('underneath_dora')
        ## GAME
        game_section = config['game']
        # East wind game / East and South wind game
        self.east_wind_game = game_section.getboolean('east_wind_game')
        # Minimum score for GAME OVER
        self.min_score_gameover = game_section.getint('min_score_gameover')

        ## ROUND
        round_section = config['round']
        # Round is continued by dealer's ready
        self.continue_by_dealer_ready = round_section.getboolean('continue_by_dealer_ready')
        return True



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
-----------------------------------------------------------
'''

import configparser
import random
import gpmjcore

__version__ = "0.5"
__date__    = "05 Nov. 2017"
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

    def goto_next_round(self, b_continued):
        if b_continued:
            self.round_continue_count += 1
            return
        self.round_continue_count = 0
        if self.round_number < 4:
            self.round_number += 1
            return
        if self.round_wind < gpmjcore.Winds.NORTH:
            self.round_wind += 1
        else:
           self.round_wind = gpmjcore.Winds.EAST
        return

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
            self.doras.append(self.dead_wall[4 + (x * 2)])
            self.underneath_doras.append(self.dead_wall[5 + (x * 2)])
        return self.doras[0]

    def deal_starttiles(self, hand):
        for x in range(13):
            hand.pure_tiles.append(self.wall.pop(0))

    def get_hand_score(self, hand, last_tile, b_discarded, seat_wind):
        win_hand = None
        # 13 orphans
        if self.thirteen_orphans_j.judge_13orphans_hand(hand.pure_tiles):
            win_hand = gpmjcore.WinHand()
            win_hand.set_property(last_tile, b_discarded, seat_wind, self.round_wind)
            win_hand.hand_value += 13
        else:
            # basic hand
            win_hands = hand.get_winhands_basic(last_tile, b_discarded, seat_wind, self.round_wind)
            if win_hands is not None:
                for w_h in win_hands:
                    self.basic_limit_hand_jc.judge_chain(w_h)
                    if w_h.hand_flag & gpmjcore.HandFlag.LIMIT_HAND:
                        win_hand = w_h
                        break
                    else:
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
                win_hand = hand.get_winhand_7pairs(last_tile, b_discarded, seat_wind, self.round_wind)
                if win_hand is not None:
                    self.seven_pairs_limit_hand_jc.judge_chain(win_hand)
                    if not win_hand.hand_flag & gpmjcore.HandFlag.LIMIT_HAND:
                        self.seven_pairs_hand_jc.judge_chain(win_hand)
                        win_hand.calc_points()
        if win_hand is None:
            return (0, 0)
        num_of_dora = self.count_dora(hand, False) # To Be Modified
        score = win_hand.calc_score(0) # To Be Modified
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
        return self.wall.pop(0)

    def call_kong(self):
        self.kong_count += 1
        tile = self.dead_wall.pop(0)
        self.dead_wall.append(self.wall.pop())
        return tile

    def count_dora(self, hand, b_reached):
        num_of_dora = 0
        doras = []
        underneath_doras = []
        for x in range(self.kong_count + 1):
            doras.append(self.doras[x].get_dora_from_indicator())
        if b_reached and self.config.available_underneath_dora:
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
        # Underneath Dora is available
        self.available_underneath_dora = True

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
        # Underneath Dora is available
        self.available_underneath_dora = default_section.getboolean('underneath_dora')
        return True


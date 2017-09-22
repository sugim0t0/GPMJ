#!/usr/bin/env python

''' GPMJ (General Purpose (Japanese) Mah-Jong library)

Modification History:
===========================================================
Date           Version   Description
===========================================================
28 Mar. 2017   0.1       Creation
20 Apr. 2017   0.2       Add get_required_13orphans()
26 Apr. 2017   0.3       Add get_required_7differentpairs()
04 Jul. 2017   0.4       Add get_required_basicwinninghand()
02 Sep. 2017   0.5       Add get_melds_chow_able()
06 Sep. 2017   0.6       Add get_melds_pong_able()
06 Sep. 2017   0.7       Add get_meld_kong_able()
11 Sep. 2017   0.8       Add expose_meld()
16 Sep. 2017   0.9       Add judge_implemented_hand() @NoPointsHandJudge
17 Sep. 2017   0.10      Add judge_implemented_hand() @OneSetOfIdenticalSequencesJudge
18 Sep. 2017   0.11      Add judge_implemented_hand() @ThreeColorStraightJudge
                                                      @AllSimplesJudge
19 Sep. 2017   0.12      Add judge_implemented_hand() @StraightJudge
21 Sep. 2017   0.13      Add judge_implemented_hand() @TerminalOrHonorInEachSetJudge
22 Sep. 2017   0.14      Add judge_implemented_hand() @AllTripletHandJudge
-----------------------------------------------------------
'''

from enum import Enum, IntEnum

__version__ = "0.14"
__date__    = "22 Sep. 2017"
__author__  = "Shun SUGIMOTO <sugimoto.shun@gmail.com>"

class Suits(IntEnum):

    # Simples
    DOTS           = 0
    BAMBOO         = 1
    CHARACTERS     = 2
    # Honors
    WINDS          = 3
    DRAGONS        = 4

    NUM_OF_SUITS   = 5
    NUM_OF_SIMPLES = 3

    def __str__(self):
        if self.value == Suits.DOTS.value:
            return "D"
        elif self.value == Suits.BAMBOO.value:
            return "B"
        elif self.value == Suits.CHARACTERS.value:
            return "C"


class Winds(IntEnum):

    EAST           = 0
    SOUTH          = 1
    WEST           = 2
    NORTH          = 3
    NUM_OF_WINDS   = 4

    def __str__(self):
        if self.value == Winds.EAST.value:
            return "Es"
        elif self.value == Winds.SOUTH.value:
            return "St"
        elif self.value == Winds.WEST.value:
            return "Ws"
        elif self.value == Winds.NORTH.value:
            return "Nt"


class Dragons(IntEnum):

    WHITE          = 0
    GREEN          = 1
    RED            = 2
    NUM_OF_DRAGONS = 3

    def __str__(self):
        if self.value == Dragons.WHITE.value:
            return "Wh"
        elif self.value == Dragons.GREEN.value:
            return "Gr"
        elif self.value == Dragons.RED.value:
            return "Rd"


class WinningHand(IntEnum):

    # Flags of winning hands
    # 1 value
  # READY_HAND = 
  # SELF_PICK =
  # ONE_SHOT =
  # LAST_TILE_FROM_THE_WALL =
  # LAST_DISCARD = 
  # DEAD_WALL_DRAW =
  # ROBBING_A_QUAD = 
    NO_POINTS_HAND                 = 0x00000001
    ONE_SET_OF_IDENTICAL_SEQUENCES = 0x00000002
    ALL_SIMPLES                    = 0x00000004
  # HONOR_TILE =
    # 2 value (Closed), 1 value (Open)
    THREE_COLOR_STRAIGHT           = 0x00000008
    STRAIGHT                       = 0x00000010
    TERMINAL_OR_HONOR_IN_EACH_SET  = 0x00000020
    # 2 value
    SEVEN_PAIRS                    = 0x00000040
  # DOUBLE_READY =
    ALL_TRIPLET_HAND               = 0x00000080
    THREE_CLOSED_TRIPLETS          = 0x00000100
    THREE_COLOR_TRIPLETS           = 0x00000200
    THREE_KONGS                    = 0x00000400
    ALL_TERMINALS_AND_HONORS       = 0x00000800
    LITTLE_THREE_DRAGONS           = 0x00001000
    # 3 value (Closed), 2 value (Open)
    TERMINAL_IN_EACH_SET           = 0x00002000
    HALF_FLUSH                     = 0x00004000
    # 3 value
    TWO_SET_OF_IDENTICAL_SEQUENCES = 0x00008000
    # 6 value (Closed), 5 value (Open)
    FLUSH                          = 0x00010000
    # LIMIT HANDS
    THIRTEEN_ORPHANS               = 0x00020000
    FOUR_CONCEALED_TRIPLETS        = 0x00040000
    BIG_THREE_DRAGONS              = 0x00080000
    LITTLE_FOUR_WINDS              = 0x00100000
    BIG_FOUR_WINDS                 = 0x00200000
    ALL_HONORS                     = 0x00400000
    ALL_TERMINALS                  = 0x00800000
    ALL_GREEN                      = 0x01000000
    NINE_GATES                     = 0x02000000
    FOUR_KONGS                     = 0x04000000
  # HEAVENLY_HAND =
  # HAND_OF_EARTH =
  # HAND_OF_MAN =


class HandJudge():

    def __init__(self):
        self.flag = 0x00000000
        self.closed_value = 0
        self.open_value = 0

    def judge_implemented_hand(self, melds, eye, last_tile, b_discarded, \
                               players_wind, prevailing_wind):
        if not len(eye.tiles) == 2 or not len(melds) == 4:
            return False
        for meld in melds:
            if not (len(meld.tiles) == 3 or len(meld.tiles) == 4):
                return False
        return True 


class NoPointsHandJudge(HandJudge):

    def __init__(self):
        self.flag = WinningHand.NO_POINTS_HAND
        self.closed_value = 1

    def judge_implemented_hand(self, melds, eye, last_tile, b_discarded, \
                               players_wind, prevailing_wind):
        if not super().judge_implemented_hand(melds, eye, last_tile, b_discarded, \
                                              players_wind, prevailing_wind):
            return False
        for meld in melds:
            if meld.b_exposed or not meld.b_sequential:
                return False
            if last_tile in meld.tiles:
                if last_tile == meld.tiles[1] or \
                   (last_tile == meld.tiles[0] and last_tile.number == 7) or \
                   (last_tile == meld.tiles[2] and last_tile.number == 3):
                    return False
        if eye.tiles[0].suit == Suits.DRAGONS:
            return False
        if eye.tiles[0].suit == Suits.WINDS and \
           (eye.tiles[0].number == players_wind or \
            eye.tiles[0].number == prevailing_wind):
            return False
        return True


class OneSetOfIdenticalSequencesJudge(HandJudge):

    def __init__(self):
        self.flag = WinningHand.ONE_SET_OF_IDENTICAL_SEQUENCES
        self.closed_value = 1

    def judge_implemented_hand(self, melds, eye, last_tile, b_discarded, \
                               players_wind, prevailing_wind):
        if not super().judge_implemented_hand(melds, eye, last_tile, b_discarded, \
                                              players_wind, prevailing_wind):
            return False
        for meld in melds:
            if meld.b_exposed:
                return False
        for i in range(len(melds)-1):
            if melds[i].b_sequential:
                for j in range(i+1, len(melds)):
                    if melds[j].b_sequential and melds[j].tiles[0].suit == melds[j].tiles[0].suit:
                        for k in range(3):
                            if not melds[i].tiles[k].number == melds[j].tiles[k].number:
                                break
                        else:
                            return True
        else:
            return False


class AllSimplesJudge(HandJudge):

    def __init__(self):
        self.flag = WinningHand.ALL_SIMPLES
        self.closed_value = 1
        self.open_value = 1

    def judge_implemented_hand(self, melds, eye, last_tile, b_discarded, \
                               players_wind, prevailing_wind):
        if not super().judge_implemented_hand(melds, eye, last_tile, b_discarded, \
                                              players_wind, prevailing_wind):
            return False
        for meld in melds:
            if meld.tiles[0].suit == Suits.WINDS or meld.tiles[0].suit == Suits.DRAGONS:
                return False
            for tile in meld.tiles:
                if tile.number == 1 or tile.number == 9:
                    return False
        if eye.tiles[0].suit == Suits.WINDS or \
           eye.tiles[0].suit == Suits.DRAGONS or \
           eye.tiles[0].number == 1 or \
           eye.tiles[0].number == 9:
            return False
        return True


class ThreeColorStraightJudge(HandJudge):

    def __init__(self):
        self.flag = WinningHand.THREE_COLOR_STRAIGHT
        self.closed_value = 2
        self.open_value = 1

    def judge_implemented_hand(self, melds, eye, last_tile, b_discarded, \
                               players_wind, prevailing_wind):
        if not super().judge_implemented_hand(melds, eye, last_tile, b_discarded, \
                                              players_wind, prevailing_wind):
            return False
        all_seqs = [set(), set(), set()]
        for meld in melds:
            if meld.b_sequential:
                all_seqs[meld.tiles[0].suit] = all_seqs[meld.tiles[0].suit] | {meld.tiles[0].number}
        if len(all_seqs[0] & all_seqs[1] & all_seqs[2]):
            return True
        return False


class StraightJudge(HandJudge):

    def __init__(self):
        self.flag = WinningHand.STRAIGHT
        self.closed_value = 2
        self.open_value = 1

    def judge_implemented_hand(self, melds, eye, last_tile, b_discarded, \
                               players_wind, prevailing_wind):
        if not super().judge_implemented_hand(melds, eye, last_tile, b_discarded, \
                                              players_wind, prevailing_wind):
            return False
        all_seqs = [set(), set(), set()]
        for meld in melds:
            if meld.b_sequential:
                all_seqs[meld.tiles[0].suit] = all_seqs[meld.tiles[0].suit] | {meld.tiles[0].number}
        for seqs in all_seqs:
            if len(seqs) >= 3:
                if len({1, 4, 7} & seqs) == 3:
                    return True
        return False


class TerminalOrHonorInEachSetJudge(HandJudge):

    def __init__(self):
        self.flag = WinningHand.TERMINAL_OR_HONOR_IN_EACH_SET
        self.closed_value = 2
        self.open_value = 1

    def judge_implemented_hand(self, melds, eye, last_tile, b_discarded, \
                               players_wind, prevailing_wind):
        if not super().judge_implemented_hand(melds, eye, last_tile, b_discarded, \
                                              players_wind, prevailing_wind):
            return False
        for meld in melds:
            if not (meld.tiles[0].suit == Suits.WINDS or \
                    meld.tiles[0].suit == Suits.DRAGONS) and \
               not (meld.tiles[0].number == 1 or meld.tiles[2].number == 9):
                return False
        if not (eye.tiles[0].suit == Suits.WINDS or \
                eye.tiles[0].suit == Suits.DRAGONS) and \
           not (eye.tiles[0].number == 1 or eye.tiles[0].number == 9):
            return False
        return True


class AllTripletHandJudge(HandJudge):

    def __init__(self):
        self.flag = WinningHand.ALL_TRIPLET_HAND
        self.closed_value = 2
        self.open_value = 2 

    def judge_implemented_hand(self, melds, eye, last_tile, b_discarded, \
                               players_wind, prevailing_wind):
        if not super().judge_implemented_hand(melds, eye, last_tile, b_discarded, \
                                              players_wind, prevailing_wind):
            return False
        for meld in melds:
            if meld.b_sequential:
                return False
        else:
            return True


class Tile():

    def __init__(self, suit, number):
        self.suit = suit
        self.number = number
        # Print characters
        self.print_char = '['
        if suit == Suits.WINDS:
            self.print_char += str(Winds(number))
        elif suit == Suits.DRAGONS:
            self.print_char += str(Dragons(number))
        else:
            self.print_char += str(Suits(suit))
            self.print_char += str(self.number)
        self.print_char += ']'


class Eye():

    def __init__(self):
        self.tiles = []

    def reset(self):
        self.tiles = []

    def add_tile(self, tile):
        if len(self.tiles) == 0:
            self.tiles.append(tile)
        elif len(self.tiles) == 1:
            if self.tiles[0].suit == tile.suit and \
               self.tiles[0].number == tile.number:
                self.tiles.append(tile)
            else:
                return False
        else:
            return False
        return True


class Meld():

    def __init__(self):
        self.tiles = []
        self.b_sequential = False
        self.b_exposed = False

    def reset(self):
        self.tiles = []
        self.b_sequential = False

    def add_tile(self, tile):
        if len(self.tiles) == 0:
            self.tiles.append(tile)
        elif not self.tiles[0].suit == tile.suit:
            return False
        elif len(self.tiles) == 1:
            if self.tiles[0].number == tile.number:
                self.tiles.append(tile)
            elif tile.suit < Suits.WINDS and \
                 abs(self.tiles[0].number - tile.number) <= 2:
                self.b_sequential = True
                if self.tiles[0].number > tile.number:
                    self.tiles.insert(0, tile)
                else:
                    self.tiles.append(tile)
            else:
                return False
        elif len(self.tiles) == 2:
            if self.b_sequential:
                if self.tiles[1].number - self.tiles[0].number == 1:
                    if (self.tiles[0].number - 1) == tile.number:
                        self.tiles.insert(0, tile)
                    elif (self.tiles[1].number + 1) == tile.number:
                        self.tiles.append(tile)
                    else:
                        return False
                else:
                    if (self.tiles[0].number + 1) == tile.number:
                        self.tiles.insert(1, tile)
                    else:
                        return False
            elif self.tiles[0].number == tile.number:
                self.tiles.append(tile)
            else:
                return False
        else:
            return False
        return True

    def remove_tile(self, tile):
        self.tiles.remove(tile)
        if len(self.tiles) == 1:
            self.b_sequential = False

    def make_kong(self, tile):
        if len(self.tiles) == 3 and \
           self.b_sequential == False and \
           self.tiles[0].number == tile.number:
            self.tiles.append(tile)
            return True
        return False


class Hand():

    def __init__(self):
        self.pure_tiles = [[], [], [], [], []]
        self.exposed = []
        self.required = [set(), set(), set(), set(), set()]

    def append_tile(self, tile):
        self.pure_tiles[tile.suit].append(tile)

    def pop_tile(self, suit, index):
        return self.pure_tiles[suit].pop(index)

    def sort_tiles(self):
        # Bubble sort
        for suit in range(Suits.NUM_OF_SUITS):
            if len(self.pure_tiles[suit]) > 1:
                for i in range(len(self.pure_tiles[suit])-1):
                    for j in range(len(self.pure_tiles[suit])-1, i, -1):
                        if self.pure_tiles[suit][j].number < self.pure_tiles[suit][j-1].number:
                            self.pure_tiles[suit][j], self.pure_tiles[suit][j-1] = \
                            self.pure_tiles[suit][j-1], self.pure_tiles[suit][j]

    def print_tiles(self):
        for suit in range(Suits.NUM_OF_SUITS):
            for tile in self.pure_tiles[suit]:
                print(tile.print_char, end="")
        print("")

    def update_required(self, required, melds, eye):
        if len(eye.tiles) == 1:
            required[eye.tiles[0].suit] = required[eye.tiles[0].suit] | {eye.tiles[0].number}
        else:
            for meld in melds:
                if len(meld.tiles) == 2:
                    if meld.tiles[1].number == meld.tiles[0].number:
                        required[meld.tiles[0].suit] = required[meld.tiles[0].suit] | {meld.tiles[0].number}
                        required[eye.tiles[0].suit] = required[eye.tiles[0].suit] | {eye.tiles[0].number}
                    elif meld.tiles[1].number - meld.tiles[0].number == 2:
                        required[meld.tiles[0].suit] = required[meld.tiles[0].suit] | {meld.tiles[0].number+1}
                    elif meld.tiles[0].number == 1:
                        required[meld.tiles[0].suit] = required[meld.tiles[0].suit] | {3}
                    elif meld.tiles[1].number == 9:
                        required[meld.tiles[0].suit] = required[meld.tiles[0].suit] | {7}
                    else:
                        required[meld.tiles[0].suit] = required[meld.tiles[0].suit] | {meld.tiles[0].number-1, meld.tiles[1].number+1}
                    break
        return

    def remove_required_all_used(self, required):
        num_of_required = 0
        for suit in range(Suits.NUM_OF_SUITS):
            for number in required[suit]:
                num_of_used = 0
                for tile in self.pure_tiles[suit]:
                    if tile.number == number:
                        num_of_used += 1
                for meld in self.exposed:
                    for tile in meld:
                        if tile.number == number:
                            num_of_used += 1
                if num_of_used == 4:
                    required[suit] = required[suit] - {number}
            num_of_required += len(required[suit])
        if num_of_required == 0:
            required = None
        return

    def judge_suit_completed_melds(self, suit, tile_index, melds):
        # Recursive function
        for meld in melds:
            if meld.add_tile(self.pure_tiles[suit][tile_index]):
                if (tile_index+1) < len(self.pure_tiles[suit]):
                    if self.judge_suit_completed_melds(suit, tile_index+1, melds):
                        return True
                    else:
                        meld.remove_tile(self.pure_tiles[suit][tile_index])
                else:
                    return True
        return False

    def judge_suit_melds_and_eye(self, suit, required):
        b_ready = False
        num_of_meld = len(self.pure_tiles[suit]) // 3
        melds = []
        for x in range(num_of_meld):
            melds.append(Meld())
        eye = Eye()
        x = 0
        while x < len(self.pure_tiles[suit]):
            if (x+1) < len(self.pure_tiles[suit]) and \
               self.pure_tiles[suit][x].number == self.pure_tiles[suit][x+1].number:
                eye.add_tile(self.pure_tiles[suit].pop(x+1))
            eye.add_tile(self.pure_tiles[suit].pop(x))
            if len(self.pure_tiles[suit]) == 0 or \
               self.judge_suit_melds(suit, 0, eye, melds, required):
                b_ready = True
            # Move tiles in eye into self.pure_tiles[suit]
            while len(eye.tiles) > 0:
                self.pure_tiles[suit].insert(x, eye.tiles.pop())
                x += 1
            # Reset melds
            for meld in melds:
                meld.reset()
            while x < len(self.pure_tiles[suit]):
                if self.pure_tiles[suit][x-1].number == self.pure_tiles[suit][x].number:
                    x += 1
                else:
                    break
        return b_ready

    def judge_suit_melds(self, suit, tile_index, fixed_eye, melds, required):
        b_ready = False
        # Recursive function
        for meld in melds:
            if meld.add_tile(self.pure_tiles[suit][tile_index]):
                if (tile_index+1) < len(self.pure_tiles[suit]):
                    if self.judge_suit_melds(suit, tile_index+1, fixed_eye, melds, required):
                        b_ready = True
                else:
                    self.update_required(required, melds, fixed_eye)
                    b_ready = True
                meld.remove_tile(self.pure_tiles[suit][tile_index])
        return b_ready

    def judge_suits_remained_2tiles(self, suit_1st, suit_2nd, required):
        b_ready = False
        eye = Eye()
        num_of_meld_1st = len(self.pure_tiles[suit_1st]) // 3
        num_of_meld_2nd = len(self.pure_tiles[suit_2nd]) // 3
        melds_1st = []
        melds_2nd = []
        for x in range(num_of_meld_1st):
            melds_1st.append(Meld())
        for x in range(num_of_meld_2nd+1):
            melds_2nd.append(Meld())
        x = 0
        while x < len(self.pure_tiles[suit_1st]):
            if (x+1) < len(self.pure_tiles[suit_1st]) and \
               self.pure_tiles[suit_1st][x].number == \
               self.pure_tiles[suit_1st][x+1].number:
                eye.add_tile(self.pure_tiles[suit_1st].pop(x+1))
                eye.add_tile(self.pure_tiles[suit_1st].pop(x))
                if num_of_meld_1st == 0 or \
                   self.judge_suit_completed_melds(suit_1st, 0, melds_1st):
                    if self.judge_suit_melds(suit_2nd, 0, eye, melds_2nd, required):
                        b_ready = True
                    # Reset melds
                    for meld in melds_2nd:
                        meld.reset()
                # Reset melds
                for meld in melds_1st:
                    meld.reset()
                # Move tiles in eye into self.pure_tiles[suit]
                self.pure_tiles[suit_1st].insert(x, eye.tiles.pop())
                self.pure_tiles[suit_1st].insert(x+1, eye.tiles.pop())
                eye.reset()
            x += 1
        return b_ready

    def get_required_basicwinninghand(self):
        required = [set(), set(), set(), set(), set()]
        suit_remained_one = -1
        suit_remained_two_1st = -1
        suit_remained_two_2nd = -1
        for suit in range(Suits.NUM_OF_SUITS):
            if len(self.pure_tiles[suit]) % 3 == 1:
                if (suit_remained_one >= 0) or (suit_remained_two_1st >= 0):
                    return None
                suit_remained_one = suit
            if len(self.pure_tiles[suit]) % 3 == 2:
                if (suit_remained_one >= 0) or (suit_remained_two_2nd >= 0):
                    return None
                if suit_remained_two_1st >= 0:
                    suit_remained_two_2nd = suit
                else:
                    suit_remained_two_1st = suit
        self.sort_tiles()
        # Judge all completed suits
        for suit in range(Suits.NUM_OF_SUITS):
            if suit == suit_remained_one or \
               suit == suit_remained_two_1st or \
               suit == suit_remained_two_2nd:
                continue
            num_of_meld = len(self.pure_tiles[suit]) // 3
            if num_of_meld == 0:
                continue
            melds = []
            for x in range(num_of_meld):
                melds.append(Meld())
            if not self.judge_suit_completed_melds(suit, 0, melds):
                return None
        # Judge suit remained one
        if suit_remained_one >= 0:
            if not self.judge_suit_melds_and_eye(suit_remained_one, required):
                return None
        else:
            # Judge suits remained two
            self.judge_suits_remained_2tiles(suit_remained_two_1st, suit_remained_two_2nd, required)
            self.judge_suits_remained_2tiles(suit_remained_two_2nd, suit_remained_two_1st, required)
        # Remove required used all tiles in self hand
        self.remove_required_all_used(required)
        return required

    def get_required_13orphans(self):
        required = [set(), set(), set(), set(), set()]
        b_missed = False
        if len(self.exposed) > 0:
            return None
        self.sort_tiles()
        # Simples (Dots, Bamboo, Characters)
        for suit in range(Suits.NUM_OF_SIMPLES):
            required[suit] = required[suit] | {1, 9}
            for tile in self.pure_tiles[suit]:
                if tile.number > 1 and tile.number < 9:
                    return None
                if tile.number in required[suit]:
                    required[suit] = required[suit] - {tile.number}
            if len(required[suit]) > 0:
                if b_missed or len(required[suit]) > 1:
                    return None
                b_missed = True
        # Winds
        for wind in range(Winds.NUM_OF_WINDS):
            required[Suits.WINDS] = required[Suits.WINDS] | {wind}
        for tile in self.pure_tiles[Suits.WINDS]:
            if tile.number in required[Suits.WINDS]:
                required[Suits.WINDS] = required[Suits.WINDS] - {tile.number}
        if len(required[Suits.WINDS]) > 0:
            if b_missed or len(required[Suits.WINDS]) > 1:
                return None
            b_missed = True
        # Dragons
        for dragon in range(Dragons.NUM_OF_DRAGONS):
            required[Suits.DRAGONS] = required[Suits.DRAGONS] | {dragon}
        for tile in self.pure_tiles[Suits.DRAGONS]:
            if tile.number in required[Suits.DRAGONS]:
                required[Suits.DRAGONS] = required[Suits.DRAGONS] - {tile.number}
        if len(required[Suits.DRAGONS]) > 0:
            if b_missed or len(required[Suits.DRAGONS]) > 1:
                return None
            b_missed = True
        if not b_missed:
            for suit in range(Suits.NUM_OF_SIMPLES):
                required[suit] = required[suit] | {1, 9}
            for wind in range(Winds.NUM_OF_WINDS):
                required[Suits.WINDS] = required[Suits.WINDS] | {wind}
            for dragon in range(Dragons.NUM_OF_DRAGONS):
                required[Suits.DRAGONS] = required[Suits.DRAGONS] | {dragon}
        return required

    def get_required_7differentpairs(self):
        required = [set(), set(), set(), set(), set()]
        b_missed = False
        if len(self.exposed) > 0:
            return None
        self.sort_tiles()
        for suit in range(Suits.NUM_OF_SUITS):
            prev_pair_number = -1
            prev_number = -1
            for tile in self.pure_tiles[suit]:
                if prev_number < 0:
                    if prev_pair_number == tile.number:
                        return None
                    prev_number = tile.number
                elif prev_number == tile.number:
                    prev_pair_number = tile.number
                    prev_number = -1
                elif b_missed:
                    return None
                else:
                    b_missed = True
                    required[suit] = required[suit] | {prev_number}
                    prev_number = tile.number
            if prev_number > 0:
                if b_missed:
                    return None
                b_missed = True
                required[suit] = required[suit] | {prev_number}
        return required

    def get_melds_chow_able(self, discarded_tile):
        melds = []
        if discarded_tile.suit == Suits.WINDS or discarded_tile.suit == Suits.DRAGONS:
            return melds
        tile_m2 = None
        tile_m1 = None
        tile_p1 = None
        tile_p2 = None
        for tile in self.pure_tiles[discarded_tile.suit]:
            if tile.number == (discarded_tile.number - 2):
                tile_m2 = tile
            elif tile.number == (discarded_tile.number - 1):
                tile_m1 = tile
            elif tile.number == (discarded_tile.number + 1):
                tile_p1 = tile
            elif tile.number == (discarded_tile.number + 2):
                tile_p2 = tile
        if not tile_m2 == None and not tile_m1 == None:
            meld = Meld()
            meld.add_tile(tile_m2)
            meld.add_tile(tile_m1)
            meld.add_tile(discarded_tile)
            melds.append(meld)
        if not tile_m1 == None and not tile_p1 == None:
            meld = Meld()
            meld.add_tile(tile_m1)
            meld.add_tile(discarded_tile)
            meld.add_tile(tile_p1)
            melds.append(meld)
        if not tile_p1 == None and not tile_p2 == None:
            meld = Meld()
            meld.add_tile(discarded_tile)
            meld.add_tile(tile_p1)
            meld.add_tile(tile_p2)
            melds.append(meld)
        return melds

    def get_melds_pong_able(self, discarded_tile):
        melds = []
        meld = Meld()
        for tile in self.pure_tiles[discarded_tile.suit]:
            if tile.number == discarded_tile.number:
                meld.add_tile(tile)
                if len(meld.tiles) == 2:
                    meld.add_tile(discarded_tile)
                    melds.append(meld)
                    break
        return melds

    def get_meld_kong_able(self, discarded_tile):
        meld = Meld()
        for tile in self.pure_tiles[discarded_tile.suit]:
            if tile.number == discarded_tile.number:
                meld.add_tile(tile)
                if len(meld.tiles) == 3:
                    meld.make_kong(discarded_tile)
                    return meld
        return None

    def expose_meld(self, meld, discarded_tile):
        for tile in meld.tiles:
            if tile in self.pure_tiles[meld.tiles[0].suit]:
                self.pure_tiles[meld.tiles[0].suit].remove(tile)
            elif not tile == discarded_tile:
                return False
        meld.b_exposed = True
        self.exposed.append(meld)
        return True

  #  def judge_winninghand(self, last_tile, b_discarded):
  #      winninghand = 0x0


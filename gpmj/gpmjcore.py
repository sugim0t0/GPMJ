#!/usr/bin/env python

''' GPMJ (General Purpose (Japanese) Mah-Jong library)
    gpmjcore module

Modification History:
===========================================================
Date           Version   Description
===========================================================
28 Mar. 2017   0.1       Creation
20 Apr. 2017   0.2       Add get_required_13orphans()
26 Apr. 2017   0.3       Add get_required_7differentpairs()
04 Jul. 2017   0.4       Add get_required_basic()
02 Sep. 2017   0.5       Add get_melds_chow_able()
06 Sep. 2017   0.6       Add get_melds_pong_able()
06 Sep. 2017   0.7       Add get_meld_kong_able()
11 Sep. 2017   0.8       Add expose_meld()
16 Sep. 2017   0.9       Add judge_basic_hand()     @NoPointsHandJudge
17 Sep. 2017   0.10      Add judge_basic_hand()     @OneSetOfIdenticalSequencesJudge
18 Sep. 2017   0.11      Add judge_basic_hand()     @ThreeColorStraightJudge
                                                    @AllSimplesJudge
19 Sep. 2017   0.12      Add judge_basic_hand()     @StraightJudge
21 Sep. 2017   0.13      Add judge_basic_hand()     @TerminalOrHonorInEachSetJudge
22 Sep. 2017   0.14      Add judge_basic_hand()     @AllTripletHandJudge
23 Sep. 2017   0.15      Add judge_basic_hand()     @ThreeClosedTripletsJudge
                                                    @ThreeColorTripletsJudge
                                                    @ThreeKongsJudge
                                                    @AllTerminalsAndHonorsJudge
                                                    @LittleThreeDragonsJudge
                                                    @TerminalInEachSetJudge
                                                    @HalfFlushJudge
25 Sep. 2017   0.16      Add judge_basic_hand()     @TwoSetOfIdenticalSequencesJudge
                                                    @FlushJudge
                                                    @FourConcealedTripletsJudge
26 Sep. 2017   0.17      Add judge_basic_hand()     @BigThreeDragonsJudge
                                                    @LittleFourWindsJudge
                                                    @BigFourWindsJudge
                                                    @AllHonorsJudge
                                                    @AllTerminalsJudge
                                                    @AllGreenJudge
27 Sep. 2017   0.18      Add judge_basic_hand()     @NineGatesJudge
                                                    @FourKongsJudge
28 Sep. 2017   0.19      Add judge_7pairs_hand()    @AllSimplesJudge
                                                    @AllTerminalsAndHonorsJudge
                                                    @HalfFlushJudge
                                                    @FlushJudge
                                                    @AllHonorsJudge
01 Oct. 2017   0.20      Add judge_7pairs_hand()    @SevenPairsJudge
                         Add judge_13orphans_hand() @ThirteenOrphansJudge
04 Oct. 2017   0.21      Add HandJudgeChain class (but unittest is not done yet)
10 Oct. 2017   0.22      Fix bug of OneSetOfIdenticalSequencesJudge
12 Oct. 2017   0.23      Add declare_kong() and change some small specs..
13 Oct. 2017   0.24      Fix bug of ThreeColorStraightJudge and ThreeColorTripletsJudge
15 Oct. 2017   0.25      Add WinHand class
16 Oct. 2017   0.26      rename judge_basic_hand() to judge_hand() and remove judge_7pairs_hand()
16 Oct. 2017   0.27      Add ValuedDragonJudge and SeatWindJudge and RoundWindJudge classes
18 Oct. 2017   0.28      Add calc_points()
19 Oct. 2017   0.29      Add calc_score()
23 Oct. 2017   0.30      Add MeldEyeTreeNode class
-----------------------------------------------------------
'''

from enum import Enum, IntEnum

__version__ = "0.30"
__date__    = "23 Oct. 2017"
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

    INVALID        = -1

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

    INVALID        = -1

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


class HandFlag(IntEnum):

    # Flags of winning hands
    # 1 value
    WHITE_DRAGON                   = 0x00020000
    GREEN_DRAGON                   = 0x00040000
    RED_DRAGON                     = 0x00080000
    SEAT_WIND                      = 0x00100000
    ROUND_WIND                     = 0x00200000
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
    THIRTEEN_ORPHANS               = 0x10000001
    FOUR_CONCEALED_TRIPLETS        = 0x10000002
    BIG_THREE_DRAGONS              = 0x10000004
    LITTLE_FOUR_WINDS              = 0x10000008
    BIG_FOUR_WINDS                 = 0x10000010
    ALL_HONORS                     = 0x10000020
    ALL_TERMINALS                  = 0x10000040
    ALL_GREEN                      = 0x10000080
    NINE_GATES                     = 0x10000100
    FOUR_KONGS                     = 0x10000200
  # HEAVENLY_HAND =
  # HAND_OF_EARTH =
  # HAND_OF_MAN =


class HandJudgeChain():

    def __init__(self, hand_judge):
        self.hand_judge = hand_judge
        self.next_chain_true = None
        self.next_chain_false = None

    def connect_chain(self, next_chain_true, next_chain_false):
        self.next_chain_true = next_chain_true
        self.next_chain_false = next_chain_false

    def judge_chain(self, win_hand):
        if self.hand_judge.judge_hand(win_hand):
            win_hand.hand_flag = win_hand.hand_flag | self.hand_judge.flag
            if win_hand.b_open:
                win_hand.hand_value += self.hand_judge.open_value
            else:
                win_hand.hand_value += self.hand_judge.closed_value
            if self.next_chain_true == None:
                return True
            else:
                return self.next_chain_true.judge_chain(win_hand)
        else:
            if self.next_chain_false == None:
                return True
            else:
                return self.next_chain_false.judge_chain(win_hand)


class HandJudge():

    def __init__(self):
        self.flag = 0x00000000
        self.closed_value = 0
        self.open_value = 0

    def judge_hand(self, win_hand):
        if not len(win_hand.eyes) == 1 or \
           not len(win_hand.eyes[0].tiles) == 2 or \
           not len(win_hand.melds) == 4:
            return False
        for meld in win_hand.melds:
            if not (len(meld.tiles) == 3 or len(meld.tiles) == 4):
                return False
        return True 


class ValuedDragonJudge(HandJudge):

    def __init__(self, flag, number):
        super().__init__()
        self.flag = flag
        self.closed_value = 1
        self.open_value = 1
        self.number = number

    def judge_hand(self, win_hand):
        for meld in win_hand.melds:
            if meld.tiles[0].suit == Suits.DRAGONS and \
               meld.tiles[0].number == self.number:
                return True
        return False


class SeatWindJudge(HandJudge):

    def __init__(self):
        super().__init__()
        self.flag = HandFlag.SEAT_WIND
        self.closed_value = 1
        self.open_value = 1

    def judge_hand(self, win_hand):
        for meld in win_hand.melds:
            if meld.tiles[0].suit == Suits.WINDS and \
               meld.tiles[0].number == win_hand.seat_wind:
                return True
        return False


class RoundWindJudge(HandJudge):

    def __init__(self):
        super().__init__()
        self.flag = HandFlag.ROUND_WIND
        self.closed_value = 1
        self.open_value = 1

    def judge_hand(self, win_hand):
        for meld in win_hand.melds:
            if meld.tiles[0].suit == Suits.WINDS and \
               meld.tiles[0].number == win_hand.round_wind:
                return True
        return False


class NoPointsHandJudge(HandJudge):

    def __init__(self):
        super().__init__()
        self.flag = HandFlag.NO_POINTS_HAND
        self.closed_value = 1

    def judge_hand(self, win_hand):
        if win_hand.last_tile in win_hand.eyes[0].tiles:
            return False
        last_tile = win_hand.last_tile
        for meld in win_hand.melds:
            if meld.b_stolen or not meld.b_sequential:
                return False
            elif last_tile in meld.tiles:
                if last_tile == meld.tiles[1] or \
                   (last_tile == meld.tiles[0] and last_tile.number == 7) or \
                   (last_tile == meld.tiles[2] and last_tile.number == 3):
                    return False
        eye = win_hand.eyes[0]
        if eye.tiles[0].suit == Suits.DRAGONS:
            return False
        if eye.tiles[0].suit == Suits.WINDS and \
           (eye.tiles[0].number == win_hand.seat_wind or \
            eye.tiles[0].number == win_hand.round_wind):
            return False
        return True


class OneSetOfIdenticalSequencesJudge(HandJudge):

    def __init__(self):
        super().__init__()
        self.flag = HandFlag.ONE_SET_OF_IDENTICAL_SEQUENCES
        self.closed_value = 1

    def judge_hand(self, win_hand):
        for meld in win_hand.melds:
            if meld.b_stolen:
                return False
        meld2_of_first_set = -1
        for i in range(len(win_hand.melds)-1):
            if i == meld2_of_first_set:
                continue
            if win_hand.melds[i].b_sequential:
                for j in range(i+1, len(win_hand.melds)):
                    if j == meld2_of_first_set:
                        continue
                    if win_hand.melds[j].b_sequential and \
                       win_hand.melds[i].tiles[0].suit == win_hand.melds[j].tiles[0].suit and \
                       win_hand.melds[i].tiles[0].number == win_hand.melds[j].tiles[0].number:
                        if meld2_of_first_set < 0:
                            meld2_of_first_set = j
                        else:
                            return False # Second set is existed
        if meld2_of_first_set < 0:
            return False
        else:
            return True


class AllSimplesJudge(HandJudge):

    def __init__(self):
        super().__init__()
        self.flag = HandFlag.ALL_SIMPLES
        self.closed_value = 1
        self.open_value = 1

    def judge_hand(self, win_hand):
        for meld in win_hand.melds:
            if meld.tiles[0].suit == Suits.WINDS or meld.tiles[0].suit == Suits.DRAGONS:
                return False
            for tile in meld.tiles:
                if tile.number == 1 or tile.number == 9:
                    return False
        for eye in win_hand.eyes:
            if eye.tiles[0].suit == Suits.WINDS or \
               eye.tiles[0].suit == Suits.DRAGONS or \
               eye.tiles[0].number == 1 or \
               eye.tiles[0].number == 9:
                return False
        return True


class ThreeColorStraightJudge(HandJudge):

    def __init__(self):
        super().__init__()
        self.flag = HandFlag.THREE_COLOR_STRAIGHT
        self.closed_value = 2
        self.open_value = 1

    def judge_hand(self, win_hand):
        all_seqs = [set(), set(), set()]
        for meld in win_hand.melds:
            if meld.b_sequential and meld.tiles[0].suit < Suits.NUM_OF_SIMPLES:
                all_seqs[meld.tiles[0].suit] = all_seqs[meld.tiles[0].suit] | {meld.tiles[0].number}
        if len(all_seqs[0] & all_seqs[1] & all_seqs[2]):
            return True
        return False


class StraightJudge(HandJudge):

    def __init__(self):
        super().__init__()
        self.flag = HandFlag.STRAIGHT
        self.closed_value = 2
        self.open_value = 1

    def judge_hand(self, win_hand):
        all_seqs = [set(), set(), set()]
        for meld in win_hand.melds:
            if meld.b_sequential:
                all_seqs[meld.tiles[0].suit] = all_seqs[meld.tiles[0].suit] | {meld.tiles[0].number}
        for seqs in all_seqs:
            if len(seqs) >= 3:
                if len({1, 4, 7} & seqs) == 3:
                    return True
        return False


class TerminalOrHonorInEachSetJudge(HandJudge):

    def __init__(self):
        super().__init__()
        self.flag = HandFlag.TERMINAL_OR_HONOR_IN_EACH_SET
        self.closed_value = 2
        self.open_value = 1

    def judge_hand(self, win_hand):
        b_sequential = False
        b_honored = False
        for meld in win_hand.melds:
            if meld.tiles[0].suit == Suits.WINDS or \
               meld.tiles[0].suit == Suits.DRAGONS:
                b_honored = True
            elif not meld.tiles[0].number == 1 and not meld.tiles[2].number == 9:
                return False
            elif meld.b_sequential:
                b_sequential = True
        if not b_sequential:
            return False
        eye = win_hand.eyes[0]
        if eye.tiles[0].suit == Suits.WINDS or \
           eye.tiles[0].suit == Suits.DRAGONS:
            b_honored = True
        elif not eye.tiles[0].number == 1 and not eye.tiles[0].number == 9:
            return False
        if not b_honored:
            return False
        return True


class SevenPairsJudge(HandJudge):

    def __init__(self):
        super().__init__()
        self.flag = HandFlag.SEVEN_PAIRS
        self.closed_value = 2
        self.open_value = 2

    def judge_hand(self, win_hand):
        if not len(win_hand.eyes) == 7:
            return False
        for eye in win_hand.eyes:
            if not len(eye.tiles) == 2:
                return False
        for i in range(len(win_hand.eyes)-1):
            for j in range(i+1, len(win_hand.eyes)):
                if win_hand.eyes[i].tiles[0].suit == win_hand.eyes[j].tiles[0].suit and \
                   win_hand.eyes[i].tiles[0].number == win_hand.eyes[j].tiles[0].number:
                    return False
        return True


class AllTripletHandJudge(HandJudge):

    def __init__(self):
        super().__init__()
        self.flag = HandFlag.ALL_TRIPLET_HAND
        self.closed_value = 2
        self.open_value = 2 

    def judge_hand(self, win_hand):
        for meld in win_hand.melds:
            if meld.b_sequential:
                return False
        else:
            return True


class ThreeClosedTripletsJudge(HandJudge):

    def __init__(self):
        super().__init__()
        self.flag = HandFlag.THREE_CLOSED_TRIPLETS
        self.closed_value = 2
        self.open_value = 2 

    def judge_hand(self, win_hand):
        b_not_closed_triplet = False
        for meld in win_hand.melds:
            if meld.b_sequential or \
               meld.b_stolen or \
               (win_hand.last_tile in meld.tiles and win_hand.b_discarded):
                if b_not_closed_triplet:
                    return False
                else:
                    b_not_closed_triplet = True
        else:
            return True


class ThreeColorTripletsJudge(HandJudge):

    def __init__(self):
        super().__init__()
        self.flag = HandFlag.THREE_COLOR_TRIPLETS
        self.closed_value = 2
        self.open_value = 2 

    def judge_hand(self, win_hand):
        all_triplets = [set(), set(), set()]
        for meld in win_hand.melds:
            if not meld.b_sequential and meld.tiles[0].suit < Suits.NUM_OF_SIMPLES:
                all_triplets[meld.tiles[0].suit] = all_triplets[meld.tiles[0].suit] | {meld.tiles[0].number}
        if len(all_triplets[0] & all_triplets[1] & all_triplets[2]):
            return True
        return False


class ThreeKongsJudge(HandJudge):

    def __init__(self):
        super().__init__()
        self.flag = HandFlag.THREE_KONGS
        self.closed_value = 2
        self.open_value = 2 

    def judge_hand(self, win_hand):
        b_not_kong = False
        for meld in win_hand.melds:
            if meld.b_sequential or \
               not (len(meld.tiles) == 4):
                if b_not_kong:
                    return False
                else:
                    b_not_kong = True
        else:
            return True


class AllTerminalsAndHonorsJudge(HandJudge):

    def __init__(self):
        super().__init__()
        self.flag = HandFlag.ALL_TERMINALS_AND_HONORS
        self.closed_value = 2
        self.open_value = 2 

    def judge_hand(self, win_hand):
        for meld in win_hand.melds:
            if meld.b_sequential or \
               (not (meld.tiles[0].suit == Suits.WINDS or \
                     meld.tiles[0].suit == Suits.DRAGONS) and \
                not (meld.tiles[0].number == 1 or meld.tiles[0].number == 9)):
                return False
        for eye in win_hand.eyes:
            if not (eye.tiles[0].suit == Suits.WINDS or \
                    eye.tiles[0].suit == Suits.DRAGONS) and \
               not (eye.tiles[0].number == 1 or eye.tiles[0].number == 9):
                return False
        return True


class LittleThreeDragonsJudge(HandJudge):

    def __init__(self):
        super().__init__()
        self.flag = HandFlag.LITTLE_THREE_DRAGONS
        self.closed_value = 2
        self.open_value = 2 

    def judge_hand(self, win_hand):
        num_of_dragons = 0
        for meld in win_hand.melds:
            if meld.tiles[0].suit == Suits.DRAGONS:
                num_of_dragons += 1
        if win_hand.eyes[0].tiles[0].suit == Suits.DRAGONS:
            num_of_dragons += 1
        if num_of_dragons < 3:
            return False
        else:
            return True


class TerminalInEachSetJudge(HandJudge):

    def __init__(self):
        super().__init__()
        self.flag = HandFlag.TERMINAL_IN_EACH_SET
        self.closed_value = 3
        self.open_value = 2 

    def judge_hand(self, win_hand):
        b_sequential = False
        for meld in win_hand.melds:
            if meld.tiles[0].suit == Suits.WINDS or \
               meld.tiles[0].suit == Suits.DRAGONS or \
               not (meld.tiles[0].number == 1 or meld.tiles[2].number == 9):
                return False
            elif meld.b_sequential:
                b_sequential = True
        if not b_sequential:
            return False
        eye = win_hand.eyes[0]
        if eye.tiles[0].suit == Suits.WINDS or \
           eye.tiles[0].suit == Suits.DRAGONS or \
           not (eye.tiles[0].number == 1 or eye.tiles[0].number == 9):
            return False
        return True


class HalfFlushJudge(HandJudge):

    def __init__(self):
        super().__init__()
        self.flag = HandFlag.HALF_FLUSH
        self.closed_value = 3
        self.open_value = 2 

    def judge_hand(self, win_hand):
        first_simple_suit = Suits.INVALID
        b_honored = False
        for meld in win_hand.melds:
            if meld.tiles[0].suit == Suits.WINDS or \
               meld.tiles[0].suit == Suits.DRAGONS:
                b_honored = True
            elif not meld.tiles[0].suit == first_simple_suit:
                if first_simple_suit == Suits.INVALID:
                    first_simple_suit = meld.tiles[0].suit
                else:
                    return False
        for eye in win_hand.eyes:
            if eye.tiles[0].suit == Suits.WINDS or \
               eye.tiles[0].suit == Suits.DRAGONS:
                b_honored = True
            elif not eye.tiles[0].suit == first_simple_suit:
                if first_simple_suit == Suits.INVALID:
                    first_simple_suit = eye.tiles[0].suit
                else:
                    return False
        if b_honored and not first_simple_suit == Suits.INVALID:
            return True
        else:
            return False


class TwoSetOfIdenticalSequencesJudge(HandJudge):

    def __init__(self):
        super().__init__()
        self.flag = HandFlag.TWO_SET_OF_IDENTICAL_SEQUENCES
        self.closed_value = 3

    def judge_hand(self, win_hand):
        for meld in win_hand.melds:
            if meld.b_stolen:
                return False
        meld2_of_first_set = -1
        for i in range(len(win_hand.melds)-1):
            if i == meld2_of_first_set:
                continue
            if win_hand.melds[i].b_sequential:
                for j in range(i+1, len(win_hand.melds)):
                    if j == meld2_of_first_set:
                        continue
                    if win_hand.melds[j].b_sequential and \
                       win_hand.melds[i].tiles[0].suit == win_hand.melds[j].tiles[0].suit and \
                       win_hand.melds[i].tiles[0].number == win_hand.melds[j].tiles[0].number:
                        if meld2_of_first_set < 0:
                            meld2_of_first_set = j
                        else:
                            return True
        else:
            return False


class FlushJudge(HandJudge):

    def __init__(self):
        super().__init__()
        self.flag = HandFlag.FLUSH
        self.closed_value = 6
        self.open_value = 5

    def judge_hand(self, win_hand):
        simple_suit = Suits.INVALID
        for meld in win_hand.melds:
            if simple_suit == Suits.INVALID:
                simple_suit = meld.tiles[0].suit
            if meld.tiles[0].suit == Suits.WINDS or \
               meld.tiles[0].suit == Suits.DRAGONS:
                return False
            if not meld.tiles[0].suit == simple_suit:
                return False
        for eye in win_hand.eyes:
            if simple_suit == Suits.INVALID:
                simple_suit = eye.tiles[0].suit
            if eye.tiles[0].suit == Suits.WINDS or \
               eye.tiles[0].suit == Suits.DRAGONS:
                return False
            if not eye.tiles[0].suit == simple_suit:
                return False
        return True


class FourConcealedTripletsJudge(HandJudge):

    def __init__(self):
        super().__init__()
        self.flag = HandFlag.FOUR_CONCEALED_TRIPLETS
        self.closed_value = 13

    def judge_hand(self, win_hand):
        for meld in win_hand.melds:
            if meld.b_sequential or meld.b_stolen or \
               (win_hand.last_tile in meld.tiles and win_hand.b_discarded):
                return False
        else:
            return True


class BigThreeDragonsJudge(HandJudge):

    def __init__(self):
        super().__init__()
        self.flag = HandFlag.BIG_THREE_DRAGONS
        self.closed_value = 13
        self.open_value = 13

    def judge_hand(self, win_hand):
        num_of_dragons = 0
        for meld in win_hand.melds:
            if meld.tiles[0].suit == Suits.DRAGONS:
                num_of_dragons += 1
        if num_of_dragons < 3:
            return False
        else:
            return True


class LittleFourWindsJudge(HandJudge):

    def __init__(self):
        super().__init__()
        self.flag = HandFlag.LITTLE_FOUR_WINDS
        self.closed_value = 13
        self.open_value = 13

    def judge_hand(self, win_hand):
        num_of_winds = 0
        for meld in win_hand.melds:
            if meld.tiles[0].suit == Suits.WINDS:
                num_of_winds += 1
        if num_of_winds == 3 and win_hand.eyes[0].tiles[0].suit == Suits.WINDS:
            return True
        else:
            return False


class BigFourWindsJudge(HandJudge):

    def __init__(self):
        super().__init__()
        self.flag = HandFlag.BIG_FOUR_WINDS
        self.closed_value = 13
        self.open_value = 13

    def judge_hand(self, win_hand):
        num_of_winds = 0
        for meld in win_hand.melds:
            if meld.tiles[0].suit == Suits.WINDS:
                num_of_winds += 1
        if num_of_winds < 4:
            return False
        else:
            return True


class AllHonorsJudge(HandJudge):

    def __init__(self):
        super().__init__()
        self.flag = HandFlag.ALL_HONORS
        self.closed_value = 13
        self.open_value = 13

    def judge_hand(self, win_hand):
        for meld in win_hand.melds:
            if not meld.tiles[0].suit == Suits.WINDS and \
               not meld.tiles[0].suit == Suits.DRAGONS:
                return False
        for eye in win_hand.eyes:
            if not eye.tiles[0].suit == Suits.WINDS and \
               not eye.tiles[0].suit == Suits.DRAGONS:
                return False
        return True


class AllTerminalsJudge(HandJudge):

    def __init__(self):
        super().__init__()
        self.flag = HandFlag.ALL_TERMINALS
        self.closed_value = 13
        self.open_value = 13

    def judge_hand(self, win_hand):
        for meld in win_hand.melds:
            if meld.tiles[0].suit == Suits.WINDS or \
               meld.tiles[0].suit == Suits.DRAGONS or \
               meld.b_sequential or \
               (not meld.tiles[0].number == 1 and \
                not meld.tiles[0].number == 9):
                return False
        eye = win_hand.eyes[0]
        if eye.tiles[0].suit == Suits.WINDS or \
           eye.tiles[0].suit == Suits.DRAGONS or \
           (not eye.tiles[0].number == 1 and \
            not eye.tiles[0].number == 9):
            return False
        else:
            return True


class AllGreenJudge(HandJudge):

    def __init__(self):
        super().__init__()
        self.flag = HandFlag.ALL_GREEN
        self.closed_value = 13
        self.open_value = 13

    def judge_hand(self, win_hand):
        for meld in win_hand.melds:
            if meld.tiles[0].suit == Suits.DRAGONS:
                if not meld.tiles[0].number == Dragons.GREEN:
                    return False
            elif meld.tiles[0].suit == Suits.BAMBOO:
                for tile in meld.tiles:
                    if not tile.number == 2 and \
                       not tile.number == 3 and \
                       not tile.number == 4 and \
                       not tile.number == 6 and \
                       not tile.number == 8:
                        return False
            else:
                return False
        eye = win_hand.eyes[0]
        if eye.tiles[0].suit == Suits.DRAGONS and \
           not eye.tiles[0].number == Dragons.GREEN:
            return False
        elif eye.tiles[0].suit == Suits.BAMBOO:
            if not eye.tiles[0].number == 2 and \
               not eye.tiles[0].number == 3 and \
               not eye.tiles[0].number == 4 and \
               not eye.tiles[0].number == 6 and \
               not eye.tiles[0].number == 8:
                return False
        else:
            return False
        return True


class NineGatesJudge(HandJudge):

    def __init__(self):
        super().__init__()
        self.flag = HandFlag.NINE_GATES
        self.closed_value = 13

    def judge_hand(self, win_hand):
        simple_suit = win_hand.melds[0].tiles[0].suit
        number_counters = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for meld in win_hand.melds:
            if meld.b_stolen or \
               meld.tiles[0].suit == Suits.WINDS or \
               meld.tiles[0].suit == Suits.DRAGONS or \
               not meld.tiles[0].suit == simple_suit:
                return False
            for tile in meld.tiles:
                number_counters[tile.number-1] += 1
        eye = win_hand.eyes[0]
        if eye.tiles[0].suit == Suits.WINDS or \
           eye.tiles[0].suit == Suits.DRAGONS or \
           not eye.tiles[0].suit == simple_suit:
            return False
        number_counters[eye.tiles[0].number-1] += 2
        for i in range(9):
            if (i == 0 or i == 8) and \
               number_counters[i] < 3:
                return False
            elif number_counters[i] < 1:
                return False
        else:
            return True


class FourKongsJudge(HandJudge):

    def __init__(self):
        super().__init__()
        self.flag = HandFlag.FOUR_KONGS
        self.closed_value = 13
        self.open_value = 13

    def judge_hand(self, win_hand):
        for meld in win_hand.melds:
            if meld.b_sequential or \
               not (len(meld.tiles) == 4):
                return False
        else:
            return True


class ThirteenOrphansJudge(HandJudge):

    def __init__(self):
        super().__init__()
        self.flag = HandFlag.THIRTEEN_ORPHANS
        self.closed_value = 13
        self.open_value = 13

    def judge_hand(self, win_hand):
        return False

    def judge_13orphans_hand(self, pure_tiles):
        # Simples
        for suit in range(Suits.NUM_OF_SIMPLES):
            b_1_exist = False
            b_9_exist = False
            for tile in pure_tiles[suit]:
                if tile.number == 1:
                    b_1_exist = True
                elif tile.number == 9:
                    b_9_exist = True
                else:
                    return False
            if not b_1_exist or not b_9_exist:
                return False
        # Winds
        b_winds_exist = [False for i in range(Winds.NUM_OF_WINDS)]
        for tile in pure_tiles[Suits.WINDS]:
            b_winds_exist[tile.number] = True
        else:
            for wind in range(Winds.NUM_OF_WINDS):
                if not b_winds_exist[wind]:
                    return False
        # Dragons
        b_dragons_exist = [False for i in range(Dragons.NUM_OF_DRAGONS)]
        for tile in pure_tiles[Suits.DRAGONS]:
            b_dragons_exist[tile.number] = True
        else:
            for dragon in range(Dragons.NUM_OF_DRAGONS):
                if not b_dragons_exist[dragon]:
                    return False
        return True


class WinHand():

    def __init__(self, last_tile, b_discarded, seat_wind, round_wind):
        self.melds = []
        self.eyes = []
        self.last_tile = last_tile
        self.b_discarded = b_discarded
        self.seat_wind = seat_wind
        self.round_wind = round_wind
        self.b_open = False
        self.hand_flag = 0x0
        self.hand_value = 0
        self.hand_point = 0

    def append_meld(self, meld):
        if len(self.melds) < 4 and len(self.eyes) <= 1 and len(meld.tiles) >= 3:
            self.melds.append(meld)
            if meld.b_stolen:
                self.b_open = True
            return True
        else:
            return False

    def append_eye(self, eye):
        if len(eye.tiles) == 2 and \
           ((len(self.melds) == 0 and len(self.eyes) < 7) or \
            (len(self.melds) > 0 and len(self.eyes) == 0)):
            self.eyes.append(eye)
            return True
        else:
            return False

    def calc_points(self):
        if len(self.eyes) == 7 and len(self.melds) == 0:
            # 7 pairs
            self.hand_point = 25
            return True
        elif len(self.eyes) == 1 and len(self.melds) == 4:
            # basic
            self.hand_point = 20
            # No points hand by self-pick
            if self.hand_flag & HandFlag.NO_POINTS_HAND and not self.b_discarded:
                return True
            if self.eyes[0].tiles[0].suit == Suits.DRAGONS or \
               (self.eyes[0].tiles[0].suit == Suits.WINDS and \
                (self.eyes[0].tiles[0].number == self.seat_wind or \
                 self.eyes[0].tiles[0].number == self.round_wind)):
                self.hand_point += 2
            if self.b_open == False and self.b_discarded:
                self.hand_point += 10
            elif not self.b_discarded:
                self.hand_point += 2
            if self.last_tile in self.eyes[0].tiles:
                self.hand_point += 2
            for meld in self.melds:
                if self.last_tile in meld.tiles and meld.b_sequential:
                    if self.last_tile == meld.tiles[1] or \
                       (self.last_tile == meld.tiles[0] and self.last_tile.number == 7) or \
                       (self.last_tile == meld.tiles[2] and self.last_tile.number == 3):
                        self.hand_point += 2
                if not meld.b_sequential:
                    added_point = 2
                    if meld.tiles[0].suit == Suits.DRAGONS or \
                       meld.tiles[0].suit == Suits.WINDS or \
                       meld.tiles[0].number == 1 or \
                       meld.tiles[0].number == 9:
                        added_point *= 2
                    if len(meld.tiles) == 3 and not meld.b_stolen:
                        added_point *= 2
                    elif len(meld.tiles) == 4:
                        added_point *= 4
                        if not meld.b_stolen:
                            added_point *= 2
                    self.hand_point += added_point
            if (self.hand_point % 10) > 0:
                self.hand_point += 10 - (self.hand_point % 10)
            return True
        else:
            return False

    def calc_score(self):
        '''
        calc_score() MUST be called after calc_points()
        '''
        score = 0
        if self.hand_value >= 13:
            score = 32000 * (self.hand_value // 13)
        elif self.hand_value >= 11:
            score = 24000
        elif self.hand_value >= 8:
            score = 16000
        elif self.hand_value >= 6:
            score = 12000
        elif self.hand_value >= 5:
            score = 8000
        else:
            score = self.hand_point * 4 * (2 ** (self.hand_value + 2))
            if score > 8000:
                score = 8000
        if self.seat_wind == Winds.EAST:
            score = (score // 2) * 3
        if self.b_discarded:
            if (score % 100) > 0:
                score += 100 - (score % 100)
            return (score, 0)
        else:
            payment_dealer = 0
            payment_non_dealer = 0
            if self.seat_wind == Winds.EAST:
                payment_non_dealer = score // 3
                if (payment_non_dealer % 100) > 0:
                    payment_non_dealer += 100 - (payment_non_dealer % 100)
                return (payment_non_dealer, 0)
            else:
                payment_dealer = score // 2
                if (payment_dealer % 100) > 0:
                    payment_dealer += 100 - (payment_dealer % 100)
                payment_non_dealer = score // 4
                if (payment_non_dealer % 100) > 0:
                    payment_non_dealer += 100 - (payment_non_dealer % 100)
                return (payment_non_dealer, payment_non_dealer)


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

    def pop_tile(self):
        return self.tiles.pop(0)


class Meld():

    def __init__(self):
        self.tiles = []
        self.b_sequential = False
        self.b_stolen = False

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

    def pop_tile(self, index):
        ret_tile = self.tiles.pop(index)
        if len(self.tiles) == 1:
            self.b_sequential = False
        return ret_tile

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

    def __update_required(self, required, melds, eye):
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

    def __remove_required_all_used(self, required):
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

    def __judge_suit_completed_melds(self, suit, tile_index, melds):
        # Recursive function
        for meld in melds:
            if meld.add_tile(self.pure_tiles[suit][tile_index]):
                if (tile_index+1) < len(self.pure_tiles[suit]):
                    if self.__judge_suit_completed_melds(suit, tile_index+1, melds):
                        return True
                    else:
                        meld.remove_tile(self.pure_tiles[suit][tile_index])
                else:
                    return True
        return False

    def __judge_suit_melds_and_eye(self, suit, required):
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
               self.__judge_suit_melds(suit, 0, eye, melds, required):
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

    def __judge_suit_melds(self, suit, tile_index, fixed_eye, melds, required):
        b_ready = False
        # Recursive function
        for meld in melds:
            if meld.add_tile(self.pure_tiles[suit][tile_index]):
                if (tile_index+1) < len(self.pure_tiles[suit]):
                    if self.__judge_suit_melds(suit, tile_index+1, fixed_eye, melds, required):
                        b_ready = True
                else:
                    self.__update_required(required, melds, fixed_eye)
                    b_ready = True
                meld.remove_tile(self.pure_tiles[suit][tile_index])
        return b_ready

    def __judge_suits_remained_2tiles(self, suit_1st, suit_2nd, required):
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
                   self.__judge_suit_completed_melds(suit_1st, 0, melds_1st):
                    if self.__judge_suit_melds(suit_2nd, 0, eye, melds_2nd, required):
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

    def get_required_basic(self):
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
            if not self.__judge_suit_completed_melds(suit, 0, melds):
                return None
        # Judge suit remained one
        if suit_remained_one >= 0:
            if not self.__judge_suit_melds_and_eye(suit_remained_one, required):
                return None
        else:
            # Judge suits remained two
            self.__judge_suits_remained_2tiles(suit_remained_two_1st, suit_remained_two_2nd, required)
            self.__judge_suits_remained_2tiles(suit_remained_two_2nd, suit_remained_two_1st, required)
        # Remove required used all tiles in self hand
        self.__remove_required_all_used(required)
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

    def get_required_7pairs(self):
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

    def get_winhands_basic(self, last_tile, b_discarded, seat_wind, round_wind):
        self.append_tile(last_tile)
        self.sort_tiles()
        tree_root = None
        # build exposed melds tree
        exposed_leaf = None
        if len(self.exposed) > 0:
            prev_node = None
            for meld in self.exposed:
                this_node = MeldEyeTreeNode()
                this_node.meld = meld
                if tree_root == None:
                    tree_root = this_node
                if not prev_node == None:
                    prev_node.append_next_node(this_node)
                prev_node = this_node
            else:
                exposed_leaf = this_node
        # build pure melds and eye tree
        pure_meld_eye_root = self.build_meld_eye_tree(None, None, last_tile)
        if tree_root == None:
            tree_root = pure_meld_eye_root
        else:
            exposed_leaf.append_next_node(pure_meld_eye_root)
        win_hands = []
        tree_root.list_winhands(last_tile, b_discarded, seat_wind, round_wind, win_hands)
        if len(win_hands) == 0:
            return None
        return win_hands

    def get_winhand_7pairs(self, last_tile, b_discarded, seat_wind, round_wind):
        if len(self.exposed) > 0:
            return None
        eyes = []
        for x in range(7):
            eyes.append(Eye())
        self.append_tile(last_tile)
        self.sort_tiles()
        tile_index = 0
        for suit in range(Suits.NUM_OF_SUITS):
            for tile in self.pure_tiles[suit]:
                if not eyes[(tile_index // 2)].add_tile(tile):
                    return None
                tile_index += 1
        win_hand = WinHand(last_tile, b_discarded, seat_wind, round_wind)
        for eye in eyes:
            win_hand.append_eye(eye)
        return win_hand

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

    def steal_tile(self, meld, discarded_tile):
        for tile in meld.tiles:
            if tile in self.pure_tiles[meld.tiles[0].suit]:
                self.pure_tiles[meld.tiles[0].suit].remove(tile)
            elif not tile == discarded_tile:
                return False
        meld.b_stolen = True
        self.exposed.append(meld)
        return True

    def declare_kong(self, meld):
        if not len(meld.tiles) == 4:
            return False
        for tile in meld.tiles:
            self.pure_tiles[meld.tiles[0].suit].remove(tile)
        self.exposed.append(meld)
        return True

    def build_meld_eye_tree(self, meld, eye, last_tile):
        meld_eye_tree = MeldEyeTreeNode()
        if not meld == None:
            meld_eye_tree.meld = meld
        elif not eye == None:
            meld_eye_tree.eye = eye
        this_suit = Suits.INVALID
        b_eye_suit = False
        for suit in range(Suits.NUM_OF_SUITS):
            if len(self.pure_tiles[suit]) > 0:
                this_suit = suit
                if len(self.pure_tiles[suit]) % 3 == 2:
                    b_eye_suit = True
                break
        else:
            # No tile (building tree is completed)
            return meld_eye_tree
        self.sort_tiles()
        if self.pure_tiles[this_suit][0].number == self.pure_tiles[this_suit][1].number:
            if b_eye_suit:
                eye = Eye()
                eye.add_tile(self.pop_tile(this_suit, 0))
                eye.add_tile(self.pop_tile(this_suit, 0))
                meld_eye_tree.append_next_node(self.build_meld_eye_tree(None, eye, last_tile))
                self.append_tile(eye.tiles[0])
                self.append_tile(eye.tiles[1])
                self.sort_tiles()
            if len(self.pure_tiles[this_suit]) >= 3 and \
               self.pure_tiles[this_suit][0].number == self.pure_tiles[this_suit][2].number:
                # Triplet meld
                meld = Meld()
                meld.add_tile(self.pop_tile(this_suit, 0))
                meld.add_tile(self.pop_tile(this_suit, 0))
                meld.add_tile(self.pop_tile(this_suit, 0))
                meld_eye_tree.append_next_node(self.build_meld_eye_tree(meld, None, last_tile))
                self.append_tile(meld.tiles[0])
                self.append_tile(meld.tiles[1])
                self.append_tile(meld.tiles[2])
                self.sort_tiles()
        # Sequential meld
        meld = Meld()
        meld.add_tile(self.pop_tile(this_suit, 0))
        prev_number = meld.tiles[0].number
        for tile in self.pure_tiles[this_suit]:
            if tile.number == prev_number:
                continue
            elif tile.number == (prev_number + 1):
                prev_number += 1
                meld.add_tile(tile)
                self.pure_tiles[this_suit].remove(tile)
                if len(meld.tiles) == 3:
                    break
                continue
            else:
                break
        if len(meld.tiles) == 3:
            meld_eye_tree.append_next_node(self.build_meld_eye_tree(meld, None, last_tile))
            if last_tile in meld.tiles:
                for tile in self.pure_tiles[this_suit]:
                    if tile.number == last_tile.number:
                        meld.remove_tile(last_tile)
                        self.append_tile(last_tile)
                        self.pure_tiles[this_suit].remove(tile)
                        meld.append_tile(tile)
                        meld_eye_tree.append_next_node( \
                            self.build_meld_eye_tree(meld, None, last_tile))
                        break
            else:
                for tile in meld.tiles:
                    if tile.number == last_tile.number:
                        meld.remove_tile(tile)
                        self.append_tile(tile)
                        self.pure_tiles[this_suit].remove(last_tile)
                        meld.append_tile(last_tile)
                        meld_eye_tree.append_next_node( \
                            self.build_meld_eye_tree(meld, None, last_tile))
                        break
        for tile in meld.tiles:
            self.append_tile(tile)
        return meld_eye_tree


class MeldEyeTreeNode():

    def __init__(self):
        self.meld = None
        self.eye = None
        next_nodes = []

    def append_next_node(self, next_node):
        self.next_nodes.append(next_node)

    def list_winhands(self, last_tile, b_discarded, seat_wind, round_wind):
        return None


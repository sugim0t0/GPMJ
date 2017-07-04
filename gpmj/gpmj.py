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
-----------------------------------------------------------
'''

from enum import Enum, IntEnum

__version__ = "0.4"
__date__    = "04 Jul. 2017"
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


class Tile():

    def __init__(self, suit, number, b_red):
        self.suit = suit
        self.number = number
        self.b_red = b_red
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


class Hand():

    def __init__(self):
        self.pure_tiles = [[], [], [], [], []]
        self.exposed = []
        self.required = [[], [], [], [], []]

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
            required[eye.tiles[0].suit].append(eye.tiles[0].number)
        else:
            for meld in melds:
                if len(meld.tiles) == 2:
                    if meld.tiles[1].number == meld.tiles[0].number:
                        required[meld.tiles[0].suit].append(meld.tiles[0].number)
                        required[eye.tiles[0].suit].append(eye.tiles[0].number)
                    elif meld.tiles[1].number - meld.tiles[0].number == 2:
                        required[meld.tiles[0].suit].append(meld.tiles[0].number+1)
                    elif meld.tiles[0].number == 1:
                        required[meld.tiles[0].suit].append(3)
                    elif meld.tiles[1].number == 9:
                        required[meld.tiles[0].suit].append(7)
                    else:
                        required[meld.tiles[0].suit].append(meld.tiles[0].number-1)
                        required[meld.tiles[0].suit].append(meld.tiles[1].number+1)
                    break
        return

    def judge_suit_melds(self, suit, tile_index, melds):
        # Recursive function
        for meld in melds:
            if meld.add_tile(self.pure_tiles[suit][tile_index]):
                if (tile_index+1) < len(self.pure_tiles[suit]):
                    if self.judge_suit_melds(suit, tile_index+1, melds):
                        return True
                    else:
                        meld.remove_tile(self.pure_tiles[suit][tile_index])
                else:
                    return True
        return False

    def judge_suit_melds_and_eye(self, suit, melds, eye, required):
        b_ready = False
        x = 0
        while x < len(self.pure_tiles[suit]):
            if (x+1) < len(self.pure_tiles[suit]) and \
               self.pure_tiles[suit][x].number == self.pure_tiles[suit][x+1].number:
                eye.add_tile(self.pure_tiles[suit].pop(x+1))
            eye.add_tile(self.pure_tiles[suit].pop(x))
            if self.judge_suit_melds(suit, 0, melds):
                # Update required
                self.update_required(required, melds, eye)
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

    def get_required_basicwinninghand(self):
        required = [[], [], [], [], []]
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
            if not self.judge_suit_melds(suit, 0, melds):
                return None
        eye = Eye()
        # Judge suit remained one
        if suit_remained_one >= 0:
            num_of_meld = len(self.pure_tiles[suit_remained_one]) // 3
            if num_of_meld == 0:
                required[suit_remained_one].append(self.pure_tiles[suit][0].number)
                return required
            melds = []
            for x in range(num_of_meld):
                melds.append(Meld())
            if self.judge_suit_melds_and_eye(suit_remained_one, melds, eye, required):
                return required
            else:
                return None
        # Judge suits remained two
        num_of_meld_1st = len(self.pure_tiles[suit_remained_two_1st]) // 3
        num_of_meld_2nd = len(self.pure_tiles[suit_remained_two_2nd]) // 3
        melds_1st = []
        melds_2nd = []
        for x in range(num_of_meld_1st):
            melds_1st.append(Meld())
        for x in range(num_of_meld_2nd):
            melds_2nd.append(Meld())
        if self.judge_suit_melds_and_eye(suit_remained_two_1st, melds_1st, eye, required):
            melds_2nd.append(Meld())
            if self.judge_suit_melds(suit_remained_two_2nd, 0, melds_2nd):
                self.update_required(required, melds_2nd, eye)
                return required
        eye.reset()
        melds_1st = []
        melds_2nd = []
        for x in range(num_of_meld_1st):
            melds_1st.append(Meld())
        for x in range(num_of_meld_2nd):
            melds_2nd.append(Meld())
        if self.judge_suit_melds_and_eye(suit_remained_two_2nd, melds_2nd, eye, required):
            melds_1st.append(Meld())
            if self.judge_suit_melds(suit_remained_two_1st, 0, melds_1st):
                self.update_required(required, melds_1st, eye)
                return required
        return None

    def get_required_13orphans(self):
        required = [[], [], [], [], []]
        b_missed = False
        if len(self.exposed) > 0:
            return None
        self.sort_tiles()
        # Simples (Dots, Bamboo, Characters)
        for suit in range(Suits.NUM_OF_SIMPLES):
            required[suit].append(1)
            required[suit].append(9)
            for tile in self.pure_tiles[suit]:
                if tile.number > 1 and tile.number < 9:
                    return None
                if tile.number in required[suit]:
                    required[suit].remove(tile.number)
            if len(required[suit]) > 0:
                if b_missed or len(required[suit]) > 1:
                    return None
                b_missed = True
        # Winds
        for wind in range(Winds.NUM_OF_WINDS):
            required[Suits.WINDS].append(wind)
        for tile in self.pure_tiles[Suits.WINDS]:
            if tile.number in required[Suits.WINDS]:
                required[Suits.WINDS].remove(tile.number)
        if len(required[Suits.WINDS]) > 0:
            if b_missed or len(required[Suits.WINDS]) > 1:
                return None
            b_missed = True
        # Dragons
        for dragon in range(Dragons.NUM_OF_DRAGONS):
            required[Suits.DRAGONS].append(dragon)
        for tile in self.pure_tiles[Suits.DRAGONS]:
            if tile.number in required[Suits.DRAGONS]:
                required[Suits.DRAGONS].remove(tile.number)
        if len(required[Suits.DRAGONS]) > 0:
            if b_missed or len(required[Suits.DRAGONS]) > 1:
                return None
            b_missed = True
        if not b_missed:
            for suit in range(Suits.NUM_OF_SIMPLES):
                required[suit].append(1)
                required[suit].append(9)
            for wind in range(Winds.NUM_OF_WINDS):
                required[Suits.WINDS].append(wind)
            for dragon in range(Dragons.NUM_OF_DRAGONS):
                required[Suits.DRAGONS].append(dragon)
        return required

    def get_required_7differentpairs(self):
        required = [[], [], [], [], []]
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
                    required[suit].append(prev_number)
                    prev_number = tile.number
            if prev_number > 0:
                if b_missed:
                    return None
                b_missed = True
                required[suit].append(prev_number)
        return required


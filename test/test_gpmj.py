#!/usr/bin/env python

import unittest
import gpmj

class TestGpmj(unittest.TestCase):

    all_tiles = [[], [], [], [], []]
    required = None
    hand = None
    # Simples
    for suit in range(gpmj.gpmj.Suits.NUM_OF_SIMPLES):
        for number in range(1, 10):
            for i in range(4):
                all_tiles[suit].append(gpmj.gpmj.Tile(suit, number, False))
    # Winds
    for number in range(gpmj.gpmj.Winds.NUM_OF_WINDS):
        for i in range(4):
            all_tiles[gpmj.gpmj.Suits.WINDS].append(gpmj.gpmj.Tile(gpmj.gpmj.Suits.WINDS, number, False))
    # Dragons
    for number in range(gpmj.gpmj.Dragons.NUM_OF_DRAGONS):
        for i in range(4):
            all_tiles[gpmj.gpmj.Suits.DRAGONS].append(gpmj.gpmj.Tile(gpmj.gpmj.Suits.DRAGONS, number, False))

# Simplified chart:
# Simples >
# ------------------------------------------------------+
# Index   0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|
# Number  1| 1| 1| 1| 2| 2| 2| 2| 3| 3| 3| 3| 4| 4| 4| 4| 
# ------------------------------------------------------+
# Index  16|17|18|19|20|21|22|23|24|25|26|27|28|29|30|31|
# Number  5| 5| 5| 5| 6| 6| 6| 6| 7| 7| 7| 7| 8| 8| 8| 8| 
# ------------------------------------------------------+
# Index  32|33|34|35|
# Number  9| 9| 9| 9| 
# ------------------+
# Winds >
# ------------------------------------------------------+
# Index   0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|
# Number Es|Es|Es|Es|St|St|St|St|Ws|Ws|Ws|Ws|Nt|Nt|Nt|Nt| 
# ------------------------------------------------------+
# Dragons >
# ------------------------------------------+
# Index   0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|
# Number Wh|Wh|Wh|Wh|Gr|Gr|Gr|Gr|Rd|Rd|Rd|Rd| 
# ------------------------------------------+

    def setUp(self):
        self.hand = gpmj.gpmj.Hand()

    def tearDown(self):
        self.hand = None
        self.required = None

    def test_basicwinninghand_wait_nonuple_B1B2B3B4B5B6B7B8B9(self):
        # [B1][B1][B1][B2][B3][B4][B5][B6][B7][B8][B9][B9][B9]
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][1])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][2])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][3])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][4])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][11])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][12])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][19])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][20])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][27])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][28])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][33])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][34])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][35])
        self.required = self.hand.get_required_basicwinninghand()
        self.assertEqual(self.required, [set(),{1,2,3,4,5,6,7,8,9},set(),set(),set()])

    def test_basicwinninghand_wait_octuple_B1B2B4B5B6B7B8B9(self):
        # [B2][B3][B3][B3][B3][B4][B4][B5][B6][B7][B8][B8][B8]
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][7])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][8])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][9])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][10])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][11])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][12])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][13])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][19])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][20])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][27])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][28])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][29])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][30])
        self.required = self.hand.get_required_basicwinninghand()
        self.assertEqual(self.required, [set(),{1,2,4,5,6,7,8,9},set(),set(),set()])

    def test_basicwinninghand_wait_septuple_B1B2B4B5B6B8B9(self):
        # [B2][B3][B3][B3][B3][B4][B5][B6][B7][B7][B7][B7][B8]
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][7])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][8])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][9])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][10])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][11])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][12])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][19])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][20])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][24])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][25])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][26])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][27])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][28])
        self.required = self.hand.get_required_basicwinninghand()
        self.assertEqual(self.required, [set(),{1,2,4,5,6,8,9},set(),set(),set()])

    def test_basicwinninghand_wait_hexatruple_B2B3B5B6B8B9(self):
        # [B2][B3][B4][B4][B4][B4][B5][B6][B7][B8][Rd][Rd][Rd]
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][8])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][9])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][10])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][7])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][8])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][12])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][13])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][14])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][15])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][19])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][20])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][27])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][28])
        self.required = self.hand.get_required_basicwinninghand()
        self.assertEqual(self.required, [set(),{2,3,5,6,8,9},set(),set(),set()])

    def test_basicwinninghand_wait_quintuple_B2B4B5B7B8(self):
        # [B3][B3][B3][B4][B5][B6][B7][D3][D4][D5][Rd][Rd][Rd]
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][8])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][9])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][10])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][9])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][10])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][11])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][12])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][19])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][20])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][24])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][11])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][12])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][16])
        self.required = self.hand.get_required_basicwinninghand()
        self.assertEqual(self.required, [set(),{2,4,5,7,8},set(),set(),set()])

    def test_basicwinninghand_wait_quadruple_D1D4D7Wh(self):
        # [D2][D3][D4][D5][D6][D7][D7][D7][B3][B4][B5][Wh][Wh]
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][2])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][3])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][11])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][12])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][16])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][7])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][8])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][15])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][16])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][23])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][24])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][25])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][26])
        self.required = self.hand.get_required_basicwinninghand()
        self.assertEqual(self.required, [{1,4,7},set(),set(),set(),{0}])

    def test_basicwinninghand_wait_triple_D1D4D7(self):
        # [D2][D3][D4][D5][D6][C8][C8][C8][B3][B4][B5][Wh][Wh]
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][2])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][3])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][11])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][12])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][16])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][7])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][8])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][15])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][16])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][23])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][28])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][29])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][30])
        self.required = self.hand.get_required_basicwinninghand()
        self.assertEqual(self.required, [{1,4,7},set(),set(),set(),set()])

    def test_basicwinninghand_wait_triple_D4D7Wh(self):
        # [D4][D4][D5][D5][D6][D6][D7][D7][B3][B4][B5][Wh][Wh]
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][2])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][3])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][11])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][12])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][16])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][14])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][15])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][16])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][17])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][22])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][23])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][24])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][25])
        self.required = self.hand.get_required_basicwinninghand()
        self.assertEqual(self.required, [{4,7},set(),set(),set(),{0}])

    def test_basicwinninghand_wait_double_eyes_C4Wh(self):
        # [D4][D4][D5][D5][D6][D6][B1][B2][B3][C4][C4][Wh][Wh]
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][2])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][3])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][3])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][7])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][11])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][14])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][15])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][16])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][17])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][22])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][23])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][14])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][15])
        self.required = self.hand.get_required_basicwinninghand()
        self.assertEqual(self.required, [set(),set(),{4},set(),{0}])

    def test_basicwinninghand_wait_double_C3C6(self):
        # [D4][D4][D5][D5][D6][D6][B1][B2][B3][C4][C5][Wh][Wh]
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][2])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][3])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][3])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][7])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][11])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][14])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][15])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][16])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][17])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][22])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][23])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][15])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][16])
        self.required = self.hand.get_required_basicwinninghand()
        self.assertEqual(self.required, [set(),set(),{3,6},set(),set()])

    def test_basicwinninghand_wait_single_eye_D2(self):
        # [D2][D4][D4][D5][D5][D6][D6][B1][B2][B3][Wh][Wh][Wh]
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][0])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][2])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][3])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][3])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][7])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][11])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][4])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][14])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][15])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][16])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][17])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][22])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][23])
        self.required = self.hand.get_required_basicwinninghand()
        self.assertEqual(self.required, [{2},set(),set(),set(),set()])

    def test_7differentpairs_None(self):
        # [D1][D1][D1][D1][C9][C9][Es][St][St][Nt][Nt][Gr][Gr]
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][4])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][7])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.WINDS][15])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.WINDS][13])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.WINDS][7])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.WINDS][0])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.WINDS][5])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][0])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][3])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][32])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][35])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][1])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][2])
        self.required = self.hand.get_required_7differentpairs()
        self.assertEqual(self.required, None)

    def test_7differentpairs_wait_Es(self):
        # [D1][D1][B1][B1][C9][C9][Es][St][St][Nt][Nt][Gr][Gr]
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][4])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][7])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.WINDS][15])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.WINDS][13])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.WINDS][7])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.WINDS][0])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.WINDS][5])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][3])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][2])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][32])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][35])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][1])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][2])
        self.required = self.hand.get_required_7differentpairs()
        self.assertEqual(self.required, [set(),set(),set(),{0},set()])

    def test_13orphans_None(self):
        # [D1][B1][C1][C9][Es][Es][St][Ws][Nt][Wh][Wh][Gr][Rd]
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][2])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][1])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][10])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][5])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.WINDS][13])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.WINDS][4])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.WINDS][0])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.WINDS][10])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.WINDS][2])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][2])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][32])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][3])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][1])
        self.required = self.hand.get_required_13orphans()
        self.assertEqual(self.required, None)

    def test_13orphans_wait_B9(self):
        # [D1][D9][B1][C1][C9][Es][Es][St][Ws][Nt][Wh][Gr][Rd]
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][1])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][10])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][5])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.WINDS][13])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.WINDS][4])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.WINDS][0])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.WINDS][10])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.WINDS][2])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][2])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][32])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][3])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][1])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][35])
        self.required = self.hand.get_required_13orphans()
        self.assertEqual(self.required, [set(),{9},set(),set(),set()])

    def test_13orphans_wait_all13orphans(self):
        # [D1][D9][B1][B9][C1][C9][Es][St][Ws][Nt][Wh][Gr][Rd]
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][1])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][10])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][5])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.WINDS][13])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.WINDS][4])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.WINDS][10])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.WINDS][2])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][2])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][33])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][32])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][3])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][1])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][35])
        self.required = self.hand.get_required_13orphans()
        self.assertEqual(self.required, [{1,9},{1,9},{1,9},{0,1,2,3},{0,1,2}])

if __name__ == '__main__':
    unittest.main()

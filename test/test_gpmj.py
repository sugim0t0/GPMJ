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
        self.assertEqual(self.required, [[],[9],[],[],[]])

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
        self.assertEqual(self.required, [[1,9],[1,9],[1,9],[0,1,2,3],[0,1,2]])

if __name__ == '__main__':
    unittest.main()


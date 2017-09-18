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
                all_tiles[suit].append(gpmj.gpmj.Tile(suit, number))
    # Winds
    for number in range(gpmj.gpmj.Winds.NUM_OF_WINDS):
        for i in range(4):
            all_tiles[gpmj.gpmj.Suits.WINDS].append(gpmj.gpmj.Tile(gpmj.gpmj.Suits.WINDS, number))
    # Dragons
    for number in range(gpmj.gpmj.Dragons.NUM_OF_DRAGONS):
        for i in range(4):
            all_tiles[gpmj.gpmj.Suits.DRAGONS].append(gpmj.gpmj.Tile(gpmj.gpmj.Suits.DRAGONS, number))

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

    def test_ThreeColorStraightJudge_0(self):
        # [D4][D4][D5][D5][D6][D6][B4][B5][B6][C4][C5][Wh][Wh] + [C3]
        judge = gpmj.gpmj.ThreeColorStraightJudge()
        last_tile = self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][10]
        melds = []
        meld1 = gpmj.gpmj.Meld()
        meld1.add_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][15])
        meld1.add_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][16])
        meld1.add_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][20])
        melds.append(meld1)
        meld2 = gpmj.gpmj.Meld()
        meld2.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][14])
        meld2.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][16])
        meld2.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][20])
        melds.append(meld2)
        meld3 = gpmj.gpmj.Meld()
        meld3.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][15])
        meld3.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][17])
        meld3.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][21])
        melds.append(meld3)
        meld4 = gpmj.gpmj.Meld()
        meld4.add_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][15])
        meld4.add_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][16])
        meld4.add_tile(last_tile)
        melds.append(meld4)
        eye = gpmj.gpmj.Eye()
        eye.add_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][0])
        eye.add_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][1])
        result = judge.judge_implemented_hand(melds, eye, last_tile, False, \
                    gpmj.gpmj.Winds.EAST, gpmj.gpmj.Winds.EAST)
        self.assertEqual(result, False)

    def test_ThreeColorStraightJudge_1(self):
        # [D4][D4][D5][D5][D6][D6][B4][B5][B6][C4][C5][Wh][Wh] + [C6]
        judge = gpmj.gpmj.ThreeColorStraightJudge()
        last_tile = self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][20]
        melds = []
        meld1 = gpmj.gpmj.Meld()
        meld1.add_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][15])
        meld1.add_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][16])
        meld1.add_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][20])
        melds.append(meld1)
        meld2 = gpmj.gpmj.Meld()
        meld2.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][14])
        meld2.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][16])
        meld2.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][20])
        melds.append(meld2)
        meld3 = gpmj.gpmj.Meld()
        meld3.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][15])
        meld3.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][17])
        meld3.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][21])
        melds.append(meld3)
        meld4 = gpmj.gpmj.Meld()
        meld4.add_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][15])
        meld4.add_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][16])
        meld4.add_tile(last_tile)
        melds.append(meld4)
        eye = gpmj.gpmj.Eye()
        eye.add_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][0])
        eye.add_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][1])
        result = judge.judge_implemented_hand(melds, eye, last_tile, False, \
                    gpmj.gpmj.Winds.EAST, gpmj.gpmj.Winds.EAST)
        self.assertEqual(result, True)

    def test_AllSimplesJudge_0(self):
        # [D4][D4][D5][D5][D6][D6][B2][B3][B4][C4][C5][Wh][Wh] + [C6]
        judge = gpmj.gpmj.AllSimplesJudge()
        last_tile = self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][20]
        melds = []
        meld1 = gpmj.gpmj.Meld()
        meld1.add_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][12])
        meld1.add_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][7])
        meld1.add_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][11])
        melds.append(meld1)
        meld2 = gpmj.gpmj.Meld()
        meld2.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][14])
        meld2.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][16])
        meld2.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][20])
        melds.append(meld2)
        meld3 = gpmj.gpmj.Meld()
        meld3.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][15])
        meld3.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][17])
        meld3.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][21])
        melds.append(meld3)
        meld4 = gpmj.gpmj.Meld()
        meld4.add_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][15])
        meld4.add_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][16])
        meld4.add_tile(last_tile)
        melds.append(meld4)
        eye = gpmj.gpmj.Eye()
        eye.add_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][0])
        eye.add_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][1])
        result = judge.judge_implemented_hand(melds, eye, last_tile, False, \
                    gpmj.gpmj.Winds.EAST, gpmj.gpmj.Winds.EAST)
        self.assertEqual(result, False)

    def test_AllSimplesJudge_1(self):
        # [D4][D4][D5][D5][D6][D6][B2][B3][B4][C4][C5][C6][C6] + [C6]
        judge = gpmj.gpmj.AllSimplesJudge()
        last_tile = self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][20]
        melds = []
        meld1 = gpmj.gpmj.Meld()
        meld1.add_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][12])
        meld1.add_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][7])
        meld1.add_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][11])
        melds.append(meld1)
        meld2 = gpmj.gpmj.Meld()
        meld2.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][14])
        meld2.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][16])
        meld2.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][20])
        melds.append(meld2)
        meld3 = gpmj.gpmj.Meld()
        meld3.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][15])
        meld3.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][17])
        meld3.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][21])
        melds.append(meld3)
        meld4 = gpmj.gpmj.Meld()
        meld4.add_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][15])
        meld4.add_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][16])
        meld4.add_tile(last_tile)
        melds.append(meld4)
        eye = gpmj.gpmj.Eye()
        eye.add_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][21])
        eye.add_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][22])
        result = judge.judge_implemented_hand(melds, eye, last_tile, False, \
                    gpmj.gpmj.Winds.EAST, gpmj.gpmj.Winds.EAST)
        self.assertEqual(result, True)
    
    def test_OneSetOfIdenticalSequencesJudge_0(self):
        # [D4][D4][D5][D5][D6][D6][B1][B2][B3][C4][C5][Wh][Wh] + [C6]
        judge = gpmj.gpmj.OneSetOfIdenticalSequencesJudge()
        last_tile = self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][20]
        melds = []
        meld1 = gpmj.gpmj.Meld()
        meld1.add_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][3])
        meld1.add_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][7])
        meld1.add_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][11])
        melds.append(meld1)
        meld2 = gpmj.gpmj.Meld()
        meld2.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][14])
        meld2.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][16])
        meld2.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][20])
        melds.append(meld2)
        meld3 = gpmj.gpmj.Meld()
        meld3.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][15])
        meld3.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][17])
        meld3.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][21])
        melds.append(meld3)
        meld4 = gpmj.gpmj.Meld()
        meld4.add_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][15])
        meld4.add_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][16])
        meld4.add_tile(last_tile)
        melds.append(meld4)
        eye = gpmj.gpmj.Eye()
        eye.add_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][2])
        eye.add_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][3])
        result = judge.judge_implemented_hand(melds, eye, last_tile, False, \
                    gpmj.gpmj.Winds.EAST, gpmj.gpmj.Winds.EAST)
        self.assertEqual(result, True)

    def test_OneSetOfIdenticalSequencesJudge_1(self):
        # [D4][D4][D5][D5][D6][D6][D6][B1][B2][B3][Wh][Wh][Wh] + [D3]
        judge = gpmj.gpmj.OneSetOfIdenticalSequencesJudge()
        last_tile = self.all_tiles[gpmj.gpmj.Suits.DOTS][9]
        melds = []
        meld1 = gpmj.gpmj.Meld()
        meld1.add_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][3])
        meld1.add_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][7])
        meld1.add_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][11])
        melds.append(meld1)
        meld2 = gpmj.gpmj.Meld()
        meld2.add_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][1])
        meld2.add_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][2])
        meld2.add_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][3])
        melds.append(meld2)
        meld3 = gpmj.gpmj.Meld()
        meld3.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][15])
        meld3.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][17])
        meld3.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][22])
        melds.append(meld3)
        meld4 = gpmj.gpmj.Meld()
        meld4.add_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][15])
        meld4.add_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][16])
        meld4.add_tile(last_tile)
        melds.append(meld4)
        eye = gpmj.gpmj.Eye()
        eye.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][20])
        eye.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][21])
        result = judge.judge_implemented_hand(melds, eye, last_tile, False, \
                    gpmj.gpmj.Winds.EAST, gpmj.gpmj.Winds.EAST)
        self.assertEqual(result, False)

    def test_NoPointsHandJudge_0(self):
        # [D4][D4][D5][D5][D6][D6][B1][B2][B3][C4][C5][Wh][Wh] + [C6]
        judge = gpmj.gpmj.NoPointsHandJudge()
        last_tile = self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][20]
        melds = []
        meld1 = gpmj.gpmj.Meld()
        meld1.add_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][3])
        meld1.add_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][7])
        meld1.add_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][11])
        melds.append(meld1)
        meld2 = gpmj.gpmj.Meld()
        meld2.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][14])
        meld2.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][16])
        meld2.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][20])
        melds.append(meld2)
        meld3 = gpmj.gpmj.Meld()
        meld3.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][15])
        meld3.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][17])
        meld3.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][21])
        melds.append(meld3)
        meld4 = gpmj.gpmj.Meld()
        meld4.add_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][15])
        meld4.add_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][16])
        meld4.add_tile(last_tile)
        melds.append(meld4)
        eye = gpmj.gpmj.Eye()
        eye.add_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][2])
        eye.add_tile(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][3])
        result = judge.judge_implemented_hand(melds, eye, last_tile, False, \
                    gpmj.gpmj.Winds.EAST, gpmj.gpmj.Winds.EAST)
        self.assertEqual(result, False)

    def test_NoPointsHandJudge_1(self):
        # [D4][D4][D5][D5][D6][D6][B1][B2][B3][C4][C5][Ws][Ws] + [C6]
        judge = gpmj.gpmj.NoPointsHandJudge()
        last_tile = self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][20]
        melds = []
        meld1 = gpmj.gpmj.Meld()
        meld1.add_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][3])
        meld1.add_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][7])
        meld1.add_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][11])
        melds.append(meld1)
        meld2 = gpmj.gpmj.Meld()
        meld2.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][14])
        meld2.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][16])
        meld2.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][20])
        melds.append(meld2)
        meld3 = gpmj.gpmj.Meld()
        meld3.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][15])
        meld3.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][17])
        meld3.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][21])
        melds.append(meld3)
        meld4 = gpmj.gpmj.Meld()
        meld4.add_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][15])
        meld4.add_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][16])
        meld4.add_tile(last_tile)
        melds.append(meld4)
        eye = gpmj.gpmj.Eye()
        eye.add_tile(self.all_tiles[gpmj.gpmj.Suits.WINDS][8])
        eye.add_tile(self.all_tiles[gpmj.gpmj.Suits.WINDS][9])
        result = judge.judge_implemented_hand(melds, eye, last_tile, False, \
                    gpmj.gpmj.Winds.EAST, gpmj.gpmj.Winds.EAST)
        self.assertEqual(result, True)

    def test_NoPointsHandJudge_2(self):
        # [D4][D4][D5][D5][D6][D6][B1][B2][B3][C4][C6][Ws][Ws] + [C5]
        judge = gpmj.gpmj.NoPointsHandJudge()
        last_tile = self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][16]
        melds = []
        meld1 = gpmj.gpmj.Meld()
        meld1.add_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][3])
        meld1.add_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][7])
        meld1.add_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][11])
        melds.append(meld1)
        meld2 = gpmj.gpmj.Meld()
        meld2.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][14])
        meld2.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][16])
        meld2.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][20])
        melds.append(meld2)
        meld3 = gpmj.gpmj.Meld()
        meld3.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][15])
        meld3.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][17])
        meld3.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][21])
        melds.append(meld3)
        meld4 = gpmj.gpmj.Meld()
        meld4.add_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][15])
        meld4.add_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][20])
        meld4.add_tile(last_tile)
        melds.append(meld4)
        eye = gpmj.gpmj.Eye()
        eye.add_tile(self.all_tiles[gpmj.gpmj.Suits.WINDS][8])
        eye.add_tile(self.all_tiles[gpmj.gpmj.Suits.WINDS][9])
        result = judge.judge_implemented_hand(melds, eye, last_tile, False, \
                    gpmj.gpmj.Winds.EAST, gpmj.gpmj.Winds.EAST)
        self.assertEqual(result, False)

    def test_NoPointsHandJudge_3(self):
        # [D4][D4][D5][D5][D6][D6][B1][B2][B3][C8][C9][Ws][Ws] + [C7]
        judge = gpmj.gpmj.NoPointsHandJudge()
        last_tile = self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][27]
        melds = []
        meld1 = gpmj.gpmj.Meld()
        meld1.add_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][3])
        meld1.add_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][7])
        meld1.add_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][11])
        melds.append(meld1)
        meld2 = gpmj.gpmj.Meld()
        meld2.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][14])
        meld2.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][16])
        meld2.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][20])
        melds.append(meld2)
        meld3 = gpmj.gpmj.Meld()
        meld3.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][15])
        meld3.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][17])
        meld3.add_tile(self.all_tiles[gpmj.gpmj.Suits.DOTS][21])
        melds.append(meld3)
        meld4 = gpmj.gpmj.Meld()
        meld4.add_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][28])
        meld4.add_tile(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][32])
        meld4.add_tile(last_tile)
        melds.append(meld4)
        eye = gpmj.gpmj.Eye()
        eye.add_tile(self.all_tiles[gpmj.gpmj.Suits.WINDS][8])
        eye.add_tile(self.all_tiles[gpmj.gpmj.Suits.WINDS][9])
        result = judge.judge_implemented_hand(melds, eye, last_tile, False, \
                    gpmj.gpmj.Winds.EAST, gpmj.gpmj.Winds.EAST)
        self.assertEqual(result, False)

    def test_expose_meld_0(self):
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
        meld = gpmj.gpmj.Meld()
        meld.tiles.append(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][14])
        meld.tiles.append(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][16])
        discarded_tile = self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][20]
        meld.tiles.append(discarded_tile)
        result = self.hand.expose_meld(meld, discarded_tile)
        self.assertEqual(result, False)

    def test_expose_meld_1(self):
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
        meld = gpmj.gpmj.Meld()
        meld.tiles.append(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][15])
        meld.tiles.append(self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][16])
        discarded_tile = self.all_tiles[gpmj.gpmj.Suits.CHARACTERS][20]
        meld.tiles.append(discarded_tile)
        result = self.hand.expose_meld(meld, discarded_tile)
        self.assertEqual(result, True)

    def test_meld_kong_able_0(self):
        # [B1][B1][B1][B2][B3][B4][B5][B6][B7][B8][B8][B9][B9]
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
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][30])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][34])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][35])
        meld = self.hand.get_meld_kong_able(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][29])
        self.assertEqual(meld, None)

    def test_meld_kong_able_1(self):
        # [B1][B1][B1][B2][B3][B4][B5][B6][B7][B8][B8][B9][B9]
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
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][30])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][34])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][35])
        meld = self.hand.get_meld_kong_able(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][0])
        self.assertEqual(meld.tiles[0].suit, gpmj.gpmj.Suits.BAMBOO)
        self.assertEqual(meld.tiles[0].number, 1)
        self.assertEqual(meld.tiles[1].number, 1)
        self.assertEqual(meld.tiles[2].number, 1)
        self.assertEqual(meld.tiles[3].number, 1)

    def test_melds_pong_able_0(self):
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
        melds = self.hand.get_melds_pong_able(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][29])
        self.assertEqual(melds, [])

    def test_melds_pong_able_1(self):
        # [B1][B1][B1][B2][B3][B4][B5][B6][B7][B8][B8][B9][B9]
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
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][30])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][34])
        self.hand.append_tile(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][35])
        melds = self.hand.get_melds_pong_able(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][29])
        self.assertEqual(len(melds), 1)
        self.assertEqual(melds[0].tiles[0].suit, gpmj.gpmj.Suits.BAMBOO)
        self.assertEqual(melds[0].tiles[0].number, 8)
        self.assertEqual(melds[0].tiles[1].number, 8)
        self.assertEqual(melds[0].tiles[2].number, 8)

    def test_melds_chow_able_0(self):
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
        melds = self.hand.get_melds_chow_able(self.all_tiles[gpmj.gpmj.Suits.DRAGONS][0])
        self.assertEqual(melds, [])

    def test_melds_chow_able_3(self):
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
        melds = self.hand.get_melds_chow_able(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][8])
        self.assertEqual(len(melds), 3)
        self.assertEqual(melds[0].tiles[0].suit, gpmj.gpmj.Suits.BAMBOO)
        self.assertEqual(melds[0].tiles[0].number, 1)
        self.assertEqual(melds[0].tiles[1].number, 2)
        self.assertEqual(melds[0].tiles[2].number, 3)
        self.assertEqual(melds[1].tiles[0].suit, gpmj.gpmj.Suits.BAMBOO)
        self.assertEqual(melds[1].tiles[0].number, 2)
        self.assertEqual(melds[1].tiles[1].number, 3)
        self.assertEqual(melds[1].tiles[2].number, 4)
        self.assertEqual(melds[2].tiles[0].suit, gpmj.gpmj.Suits.BAMBOO)
        self.assertEqual(melds[2].tiles[0].number, 3)
        self.assertEqual(melds[2].tiles[1].number, 4)
        self.assertEqual(melds[2].tiles[2].number, 5)

    def test_melds_chow_able_2(self):
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
        melds = self.hand.get_melds_chow_able(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][5])
        self.assertEqual(len(melds), 2)
        self.assertEqual(melds[0].tiles[0].suit, gpmj.gpmj.Suits.BAMBOO)
        self.assertEqual(melds[0].tiles[0].number, 1)
        self.assertEqual(melds[0].tiles[1].number, 2)
        self.assertEqual(melds[0].tiles[2].number, 3)
        self.assertEqual(melds[1].tiles[0].suit, gpmj.gpmj.Suits.BAMBOO)
        self.assertEqual(melds[1].tiles[0].number, 2)
        self.assertEqual(melds[1].tiles[1].number, 3)
        self.assertEqual(melds[1].tiles[2].number, 4)

    def test_melds_chow_able_1(self):
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
        melds = self.hand.get_melds_chow_able(self.all_tiles[gpmj.gpmj.Suits.BAMBOO][0])
        self.assertEqual(len(melds), 1)
        self.assertEqual(melds[0].tiles[0].suit, gpmj.gpmj.Suits.BAMBOO)
        self.assertEqual(melds[0].tiles[0].number, 1)
        self.assertEqual(melds[0].tiles[1].number, 2)
        self.assertEqual(melds[0].tiles[2].number, 3)

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


#!/usr/bin/env python

import unittest
# from gpmj import gpmjgame
# from gpmj import gpmjcore
import gpmjgame
import gpmjcore

class TestGpmjGame(unittest.TestCase):
    
    game = None

    def setUp(self):
        self.game = gpmjgame.Game()

    def tearDown(self):
        self.game = None

    def setup_game(self):
        self.game.create_tiles()
        self.game.setup_round()
        self.game.setup_hand_judger()

    def test_create_tiles(self):
        self.game.create_tiles()
        self.assertEqual(len(self.game.tiles), 136)

    def test_setup_round(self):
        self.game.create_tiles()
        self.game.setup_round()
        print("")
        self.game.print_wall()
        self.assertEqual(len(self.game.wall), 122)
        self.assertEqual(len(self.game.dead_wall), 14)

    def test_parse_config(self):
        self.game.config.parse_config("./gpmj.cfg")
        self.game.create_tiles()
        self.assertEqual(self.game.config.num_of_red5[0], 1)
        self.assertEqual(self.game.config.num_of_red5[1], 1)
        self.assertEqual(self.game.config.num_of_red5[2], 1)

    def test_get_hand_score_0(self):
        # [D1][D9][B1][B9][C1][C9][Es][St][Ws][Nt][Nt][Gr][Rd] + [Es]
        self.setup_game()
        hand = gpmjcore.Hand()
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DOTS, 1))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DOTS, 9))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 1))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 9))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 1))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 9))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.EAST))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.SOUTH))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.WEST))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.NORTH))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DRAGONS, gpmjcore.Dragons.WHITE))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DRAGONS, gpmjcore.Dragons.GREEN))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DRAGONS, gpmjcore.Dragons.RED))
        last_tile = gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.EAST)
        score = self.game.get_hand_score(hand, last_tile, False, gpmjcore.Winds.SOUTH)
        self.assertEqual(score[0], 8000)
        self.assertEqual(score[1], 16000)

    def test_get_hand_score_1(self):
        # [D1][D9][B1][B9][C1][C9][Es][St][Ws][Nt][Nt][Gr][Rd] + [Es]
        self.setup_game()
        self.game.goto_next_round(True)
        self.game.goto_next_round(True)
        self.game.goto_next_round(True)
        hand = gpmjcore.Hand()
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DOTS, 1))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DOTS, 9))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 1))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 9))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 1))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 9))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.EAST))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.SOUTH))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.WEST))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.NORTH))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DRAGONS, gpmjcore.Dragons.WHITE))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DRAGONS, gpmjcore.Dragons.GREEN))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DRAGONS, gpmjcore.Dragons.RED))
        last_tile = gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.EAST)
        score = self.game.get_hand_score(hand, last_tile, False, gpmjcore.Winds.SOUTH)
        self.assertEqual(score[0], 8300)
        self.assertEqual(score[1], 16300)

    def test_get_hand_score_2(self):
        # [D1][D9][B1][B9][C1][C9][Es][St][Ws][Nt][Nt][Gr][Rd] + [Es]
        self.setup_game()
        self.game.goto_next_round(True)
        self.game.goto_next_round(True)
        hand = gpmjcore.Hand()
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DOTS, 1))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DOTS, 9))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 1))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 9))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 1))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 9))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.EAST))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.SOUTH))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.WEST))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.NORTH))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DRAGONS, gpmjcore.Dragons.WHITE))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DRAGONS, gpmjcore.Dragons.GREEN))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DRAGONS, gpmjcore.Dragons.RED))
        last_tile = gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.EAST)
        score = self.game.get_hand_score(hand, last_tile, True, gpmjcore.Winds.SOUTH)
        self.assertEqual(score[0], 32600)
        self.assertEqual(score[1], 0)

    def test_get_hand_score_3(self):
        # [D1][D9][B1][B9][C1][C9][Es][St][Ws][Nt][Nt][Gr][Rd] + [Es]
        self.setup_game()
        self.game.goto_next_round(True)
        self.game.goto_next_round(True)
        hand = gpmjcore.Hand()
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DOTS, 1))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DOTS, 9))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 1))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 9))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 1))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 9))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.EAST))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.SOUTH))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.WEST))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.NORTH))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DRAGONS, gpmjcore.Dragons.WHITE))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DRAGONS, gpmjcore.Dragons.GREEN))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DRAGONS, gpmjcore.Dragons.RED))
        last_tile = gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.EAST)
        score = self.game.get_hand_score(hand, last_tile, False, gpmjcore.Winds.EAST)
        self.assertEqual(score[0], 16200)
        self.assertEqual(score[1], 0)

    def test_get_hand_score_4(self):
        # [D1][D9][B1][B9][C1][C9][Es][St][Ws][Nt][Nt][Gr][Rd] + [Es]
        self.setup_game()
        self.game.goto_next_round(True)
        self.game.goto_next_round(True)
        self.game.goto_next_round(True)
        hand = gpmjcore.Hand()
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DOTS, 1))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DOTS, 9))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 1))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 9))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 1))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 9))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.EAST))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.SOUTH))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.WEST))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.NORTH))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DRAGONS, gpmjcore.Dragons.WHITE))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DRAGONS, gpmjcore.Dragons.GREEN))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DRAGONS, gpmjcore.Dragons.RED))
        last_tile = gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.EAST)
        score = self.game.get_hand_score(hand, last_tile, True, gpmjcore.Winds.EAST)
        self.assertEqual(score[0], 48900)
        self.assertEqual(score[1], 0)

if __name__ == '__main__':
    unittest.main()


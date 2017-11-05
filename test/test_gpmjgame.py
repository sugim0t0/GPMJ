#!/usr/bin/env python

import unittest
# from gpmj import gpmjgame
import gpmjgame

class TestGpmjGame(unittest.TestCase):
    
    game = None

    def setUp(self):
        self.game = gpmjgame.Game()

    def tearDown(self):
        self.game = None

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

    def test_setup_hand_judger(self):
        self.game.setup_hand_judger()

    def test_parse_config(self):
        self.game.config.parse_config("./gpmj.cfg")
        self.game.create_tiles()
        self.assertEqual(self.game.config.num_of_red5[0], 1)
        self.assertEqual(self.game.config.num_of_red5[1], 1)
        self.assertEqual(self.game.config.num_of_red5[2], 1)


if __name__ == '__main__':
    unittest.main()


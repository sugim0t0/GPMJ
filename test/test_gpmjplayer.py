#!/usr/bin/env python

import unittest
# from gpmj import gpmjplayer
# from gpmj import gpmjgame
# from gpmj import gpmjcore
import gpmjplayer
import gpmjgame
import gpmjcore

class TestGpmjPlayer(unittest.TestCase):
    
    player = None

    def setUp(self):
        self.player = gpmjplayer.Player("Sugimoto")

    def tearDown(self):
        self.player = None

    def test_pickup_tile_handler(self):
        tile = gpmjcore.Tile(gpmjcore.Suits.DOTS, 1)
        result = self.player.pickup_tile_handler(tile)
        self.assertEqual(result, tile)

    def test_pickup_tile_after_declared_ready_handler(self):
        tile = gpmjcore.Tile(gpmjcore.Suits.DOTS, 1)
        result = self.player.pickup_tile_after_declared_ready_handler(tile)
        self.assertEqual(result, tile)

    def test_win_selfpick_handler(self):
        tile = gpmjcore.Tile(gpmjcore.Suits.DOTS, 1)
        result = self.player.win_selfpick_handler(tile)
        self.assertEqual(result, True)

    def test_closed_kong_handler(self):
        melds = []
        tile = gpmjcore.Tile(gpmjcore.Suits.DOTS, 1)
        result = self.player.closed_kong_handler(tile, melds)
        self.assertIsNone(result)

    def test_added_kong_handler(self):
        melds = []
        tile = gpmjcore.Tile(gpmjcore.Suits.DOTS, 1)
        result = self.player.added_kong_handler(tile, melds)
        self.assertIsNone(result)

    def test_declare_ready_handler(self):
        tiles = []
        tile = gpmjcore.Tile(gpmjcore.Suits.DOTS, 1)
        result = self.player.declare_ready_handler(tile, tiles)
        self.assertIsNone(result)

    def test_win_discard_handler(self):
        tile = gpmjcore.Tile(gpmjcore.Suits.DOTS, 1)
        result = self.player.win_discard_handler(tile)
        self.assertEqual(result, True)

    def test_chow_handler(self):
        melds = []
        tile = gpmjcore.Tile(gpmjcore.Suits.DOTS, 1)
        (result1, result2) = self.player.chow_handler(tile, melds)
        self.assertIsNone(result1)
        self.assertIsNone(result2)

    def test_pong_handler(self):
        melds = []
        tile = gpmjcore.Tile(gpmjcore.Suits.DOTS, 1)
        (result1, result2) = self.player.pong_handler(tile, melds)
        self.assertIsNone(result1)
        self.assertIsNone(result2)

    def test_stolen_kong_handler(self):
        tile = gpmjcore.Tile(gpmjcore.Suits.DOTS, 1)
        result = self.player.stolen_kong_handler(tile)
        self.assertEqual(result, False)

if __name__ == '__main__':
    unittest.main()


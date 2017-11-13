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

    def set_doras(self, doras, underneath_doras):
        self.game.doras = doras
        self.game.underneath_doras = underneath_doras

    def test_goto_next_round(self):
        self.setup_game()
        self.game.goto_next_round(False)
        self.assertEqual(self.game.round_number, 2)
        self.assertEqual(self.game.round_wind, gpmjcore.Winds.EAST)
        self.assertEqual(self.game.round_continue_count, 0)
        self.game.goto_next_round(True)
        self.assertEqual(self.game.round_number, 2)
        self.assertEqual(self.game.round_wind, gpmjcore.Winds.EAST)
        self.assertEqual(self.game.round_continue_count, 1)
        self.game.goto_next_round(False)
        self.game.goto_next_round(False)
        self.game.goto_next_round(False)
        self.assertEqual(self.game.round_number, 1)
        self.assertEqual(self.game.round_wind, gpmjcore.Winds.SOUTH)
        self.assertEqual(self.game.round_continue_count, 0)
        self.game.goto_next_round(False)
        self.game.goto_next_round(False)
        self.game.goto_next_round(False)
        self.game.goto_next_round(False)
        self.assertEqual(self.game.round_number, 1)
        self.assertEqual(self.game.round_wind, gpmjcore.Winds.WEST)
        self.assertEqual(self.game.round_continue_count, 0)
        self.game.goto_next_round(False)
        self.game.goto_next_round(False)
        self.game.goto_next_round(False)
        self.game.goto_next_round(False)
        self.game.goto_next_round(False)
        self.game.goto_next_round(False)
        self.game.goto_next_round(False)
        self.game.goto_next_round(False)
        self.assertEqual(self.game.round_number, 1)
        self.assertEqual(self.game.round_wind, gpmjcore.Winds.EAST)
        self.assertEqual(self.game.round_continue_count, 0)

    def test_deal_starttiles(self):
        self.setup_game()
        hand = gpmjcore.Hand()
        self.game.deal_starttiles(hand)
        hand.sort_tiles()
        print("")
        hand.print_tiles()
        num_of_tiles = 0
        for suit in range(gpmjcore.Suits.NUM_OF_SUITS):
            num_of_tiles += len(hand.pure_tiles[suit])
        self.assertEqual(num_of_tiles, 13)

    def test_call_kong(self):
        self.setup_game()
        num_of_walltiles = len(self.game.wall)
        tile = self.game.call_kong()
        self.assertEqual(self.game.kong_count, 1)
        self.assertEqual(len(self.game.wall), (num_of_walltiles - 1))
        tile = self.game.call_kong()
        self.assertEqual(self.game.kong_count, 2)
        self.assertEqual(len(self.game.wall), (num_of_walltiles - 2))
        tile = self.game.call_kong()
        self.assertEqual(self.game.kong_count, 3)
        self.assertEqual(len(self.game.wall), (num_of_walltiles - 3))
        tile = self.game.call_kong()
        self.assertEqual(self.game.kong_count, 4)
        self.assertEqual(len(self.game.wall), (num_of_walltiles - 4))
        tile = self.game.call_kong()
        self.assertIsNone(tile)
        self.assertEqual(self.game.kong_count, 4)
        self.assertEqual(len(self.game.wall), (num_of_walltiles - 4))

    def test_draw_tile(self):
        self.setup_game()
        num_of_walltiles = len(self.game.wall)
        for x in range(num_of_walltiles):
            tile = self.game.draw_tile()
            self.assertIsNotNone(tile)
        else:
            tile = self.game.draw_tile()
            self.assertIsNone(tile)

    def test_get_num_of_dora_0(self):
        # [D1][D2][D3][B2][B3][B4][C3][C4][C5][Nt][Nt][Nt][Rd] + [Rd]
        # Not be declared ready
        # dora indicator -> [B1], [Ws]
        # underneath dora indicator -> [D9], [B4]
        self.game.create_tiles()
        self.game.kong_count = 1
        self.game.doras.append(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 1))
        self.game.doras.append(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.WEST))
        self.game.underneath_doras.append(gpmjcore.Tile(gpmjcore.Suits.DOTS, 9))
        self.game.underneath_doras.append(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 4))
        hand = gpmjcore.Hand()
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DOTS, 1))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DOTS, 2))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DOTS, 3))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 2))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 3))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 4))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 3))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 4))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 5))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.NORTH))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.NORTH))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.NORTH))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DRAGONS, gpmjcore.Dragons.RED))
        last_tile = gpmjcore.Tile(gpmjcore.Suits.DRAGONS, gpmjcore.Dragons.RED)
        hand.append_tile(last_tile)
        num_of_dora = self.game.get_num_of_dora(hand, False)
        self.assertEqual(num_of_dora, 4)

    def test_get_num_of_dora_1(self):
        # [D1][D2][D3][B2][B3][B4][C3][C4][C5][Nt][Nt][Nt][Rd] + [Rd]
        # Be declared ready
        # dora indicator -> [B1], [Ws]
        # underneath dora indicator -> [D9], [B4]
        self.game.create_tiles()
        self.game.kong_count = 1
        self.game.doras.append(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 1))
        self.game.doras.append(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.WEST))
        self.game.underneath_doras.append(gpmjcore.Tile(gpmjcore.Suits.DOTS, 9))
        self.game.underneath_doras.append(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 4))
        hand = gpmjcore.Hand()
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DOTS, 1))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DOTS, 2))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DOTS, 3))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 2))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 3))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 4))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 3))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 4))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 5))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.NORTH))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.NORTH))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.NORTH))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DRAGONS, gpmjcore.Dragons.RED))
        last_tile = gpmjcore.Tile(gpmjcore.Suits.DRAGONS, gpmjcore.Dragons.RED)
        hand.append_tile(last_tile)
        num_of_dora = self.game.get_num_of_dora(hand, True)
        self.assertEqual(num_of_dora, 5)

    def test_get_num_of_dora_2(self):
        # [D1][D2][D3][B2][B3][B4][C3][C4][C5] ([Nt][Nt][Nt][Nt]) [Rd] + [Rd]
        # Be declared ready
        # dora indicator -> [B1], [Ws]
        # underneath dora indicator -> [D9], [B4]
        self.game.create_tiles()
        self.game.kong_count = 1
        self.game.doras.append(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 1))
        self.game.doras.append(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.WEST))
        self.game.underneath_doras.append(gpmjcore.Tile(gpmjcore.Suits.DOTS, 9))
        self.game.underneath_doras.append(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 4))
        hand = gpmjcore.Hand()
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DOTS, 1))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DOTS, 2))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DOTS, 3))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 2))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 3))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 4))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 3))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 4))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 5))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.NORTH))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.NORTH))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.NORTH))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.NORTH))
        hand.declare_kong(gpmjcore.Suits.WINDS, gpmjcore.Winds.NORTH)
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DRAGONS, gpmjcore.Dragons.RED))
        last_tile = gpmjcore.Tile(gpmjcore.Suits.DRAGONS, gpmjcore.Dragons.RED)
        hand.append_tile(last_tile)
        num_of_dora = self.game.get_num_of_dora(hand, True)
        self.assertEqual(num_of_dora, 6)

    def test_get_num_of_dora_3(self):
        # [D1][D2][D3][B2][B3][B4][C3][C4][C5] ([Nt][Nt][Nt][Nt]) [Rd] + [Rd]
        # Be declared ready
        # dora indicator -> [B1], [Ws]
        # underneath dora indicator -> [D9], [Ws]
        self.game.create_tiles()
        self.game.kong_count = 1
        self.game.doras.append(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 1))
        self.game.doras.append(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.WEST))
        self.game.underneath_doras.append(gpmjcore.Tile(gpmjcore.Suits.DOTS, 9))
        self.game.underneath_doras.append(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.WEST))
        hand = gpmjcore.Hand()
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DOTS, 1))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DOTS, 2))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DOTS, 3))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 2))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 3))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 4))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 3))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 4))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 5))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.NORTH))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.NORTH))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.NORTH))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.NORTH))
        hand.declare_kong(gpmjcore.Suits.WINDS, gpmjcore.Winds.NORTH)
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DRAGONS, gpmjcore.Dragons.RED))
        last_tile = gpmjcore.Tile(gpmjcore.Suits.DRAGONS, gpmjcore.Dragons.RED)
        hand.append_tile(last_tile)
        num_of_dora = self.game.get_num_of_dora(hand, True)
        self.assertEqual(num_of_dora, 10)

    def test_get_num_of_dora_4(self):
        # [D1][D2][D3][B2][B3][B4][C3][C4][C5] ([D5][D5][D5][D5]) [Rd] + [Rd]
        # Be declared ready
        # dora indicator -> [B1], [Ws]
        # underneath dora indicator -> [D9], [Ws]
        self.game.create_tiles()
        self.game.kong_count = 1
        self.game.doras.append(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 1))
        self.game.doras.append(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.WEST))
        self.game.underneath_doras.append(gpmjcore.Tile(gpmjcore.Suits.DOTS, 9))
        self.game.underneath_doras.append(gpmjcore.Tile(gpmjcore.Suits.WINDS, gpmjcore.Winds.WEST))
        hand = gpmjcore.Hand()
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DOTS, 1))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DOTS, 2))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DOTS, 3))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 2))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 3))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 4))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 3))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 4))
        red_c5 = gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 5)
        red_c5.b_red = True
        hand.append_tile(red_c5)
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DOTS, 5))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DOTS, 5))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DOTS, 5))
        red_d5 = gpmjcore.Tile(gpmjcore.Suits.DOTS, 5)
        red_d5.b_red = True
        hand.append_tile(red_d5)
        hand.declare_kong(gpmjcore.Suits.DOTS, 5)
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DRAGONS, gpmjcore.Dragons.RED))
        last_tile = gpmjcore.Tile(gpmjcore.Suits.DRAGONS, gpmjcore.Dragons.RED)
        hand.append_tile(last_tile)
        num_of_dora = self.game.get_num_of_dora(hand, True)
        self.assertEqual(num_of_dora, 4)

    def test_create_tiles(self):
        self.game.create_tiles()
        self.assertEqual(len(self.game.tiles), 136)

    def test_setup_round(self):
        self.game.create_tiles()
        self.game.setup_round()
        print("")
        self.game.print_wall()
        self.game.print_dead_wall()
        self.assertEqual(len(self.game.wall), 122)
        self.assertEqual(len(self.game.dead_wall), 14)
        tile = self.game.draw_tile()
        self.assertIsNotNone(tile)
        self.game.print_wall()
        tile = self.game.call_kong()
        self.assertIsNotNone(tile)
        self.game.print_dead_wall()
        for x in range(119):
            tile = self.game.draw_tile()
        self.game.print_wall()
        tile = self.game.draw_tile()
        self.assertIsNotNone(tile)
        self.game.print_wall()
        tile = self.game.draw_tile()
        self.assertIsNone(tile)

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
        score = self.game.get_hand_score(hand, 0, last_tile, False, gpmjcore.Winds.SOUTH)
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
        score = self.game.get_hand_score(hand, 0, last_tile, False, gpmjcore.Winds.SOUTH)
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
        score = self.game.get_hand_score(hand, 0, last_tile, True, gpmjcore.Winds.SOUTH)
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
        score = self.game.get_hand_score(hand, 0, last_tile, False, gpmjcore.Winds.EAST)
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
        score = self.game.get_hand_score(hand, 0, last_tile, True, gpmjcore.Winds.EAST)
        self.assertEqual(score[0], 48900)
        self.assertEqual(score[1], 0)

    def test_get_hand_score_5(self):
        # [D1][D1][D1][B2][B3][B4][B4][B4][C7][C7][C7][C8][C8] + [C9]
        self.setup_game()
        hand = gpmjcore.Hand()
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DOTS, 1))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DOTS, 1))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DOTS, 1))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 2))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 3))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 4))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 4))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 4))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 7))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 7))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 7))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 8))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 8))
        last_tile = gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 9)
        score = self.game.get_hand_score(hand, 0, last_tile, False, gpmjcore.Winds.EAST)
        self.assertEqual(score[0], 0)
        self.assertEqual(score[1], 0)

    def test_get_hand_score_6(self):
        # [D1][D1][D1][B2][B3][B4][B4][B4][C7][C7][C7][C8][C8] + [C8]
        self.setup_game()
        doras = []
        underneath_doras = []
        doras.append(gpmjcore.Tile(gpmjcore.Suits.DRAGONS, gpmjcore.Dragons.RED))
        doras.append(gpmjcore.Tile(gpmjcore.Suits.DRAGONS, gpmjcore.Dragons.WHITE))
        doras.append(gpmjcore.Tile(gpmjcore.Suits.DRAGONS, gpmjcore.Dragons.GREEN))
        underneath_doras.append(gpmjcore.Tile(gpmjcore.Suits.DRAGONS, gpmjcore.Dragons.RED))
        underneath_doras.append(gpmjcore.Tile(gpmjcore.Suits.DRAGONS, gpmjcore.Dragons.WHITE))
        underneath_doras.append(gpmjcore.Tile(gpmjcore.Suits.DRAGONS, gpmjcore.Dragons.GREEN))
        self.set_doras(doras, underneath_doras)
        hand = gpmjcore.Hand()
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DOTS, 1))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DOTS, 1))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DOTS, 1))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 2))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 3))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 4))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 4))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 4))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 7))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 7))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 7))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 8))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 8))
        last_tile = gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 8)
        state_flag = gpmjcore.StateFlag.SELF_PICK
        score = self.game.get_hand_score(hand, state_flag, last_tile, False, gpmjcore.Winds.EAST)
        self.assertEqual(score[0], 2600)
        self.assertEqual(score[1], 0)

if __name__ == '__main__':
    unittest.main()


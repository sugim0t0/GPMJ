#!/usr/bin/env python

''' GPMJ (General Purpose (Japanese) Mah-Jong library)
    Sample application

Modification History:
===========================================================
Date           Version   Description
===========================================================
23 Dec. 2017   0.1       Creation
03 Jan. 2018   0.2       Discarding all pick up tiles version
03 Feb. 2018   0.3       Implement each handlers
-----------------------------------------------------------
'''

import gpmjcore
import gpmjgame
import gpmjplayer
import gpmjctrl

__version__ = "0.3"
__date__    = "03 Feb. 2018"
__author__  = "Shun SUGIMOTO <sugimoto.shun@gmail.com>"

class ManualPlayer(gpmjplayer.Player):

    def __init__(self, name):
        super(ManualPlayer, self).__init__(name)

    def pickup_tile_handler(self, tile):
        self.print_tiles(tile)
        self.print_cmd_pickup_tile(tile)
        cmd = input(">> ")
        if cmd == " ":
            return tile
        else:
            return self.get_discard_tile(cmd)

    def win_selfpick_handler(self, tile):
        self.print_tiles(tile)
        self.print_cmd_win()
        while(True):
            cmd = input(">> ")
            if cmd == "y":
                print("Win by selfpick")
                return True
            elif cmd == "n":
                return False
            else:
                print("input y or n")

    def closed_kong_handler(self, tile, melds):
        self.print_tiles(tile)
        self.print_cmd_closed_kong(melds)
        while(True):
            cmd = input(">> ")
            if cmd == "n":
                return None
            else:
                return self.get_element_from_cmd(cmd, melds)

    def added_kong_handler(self, tile, tiles):
        self.print_tiles(tile)
        self.print_cmd_added_kong(tiles)
        while(True):
            cmd = input(">> ")
            if cmd == "n":
                return None
            else:
                return self.get_element_from_cmd(cmd, tiles)

    def declare_ready_handler(self, tile, tiles):
        self.print_tiles(tile)
        self.print_cmd_declare_ready(tiles)
        while(True):
            cmd = input(">> ")
            if cmd == "n":
                return None
            else:
                return self.get_element_from_cmd(cmd, tiles)

    # Event handler for discarded tile
    def win_discard_handler(self, tile):
        self.print_tiles(None)
        self.print_cmd_win()
        while(True):
            cmd = input(">> ")
            if cmd == "y":
                print("Win by discard")
                return True
            elif cmd == "n":
                return False
            else:
                print("input y or n")

    def chow_handler(self, tile, melds):
        self.print_tiles(None)
        self.print_cmd_chow(tile, melds)
        while(True):
            cmd = input(">> ")
            if cmd == "n":
                return (None, None)
            else:
                meld = self.get_element_from_cmd(cmd, melds)
                break
        self.print_tiles(None)
        self.print_cmd_pickup_tile(None)
        while(True):
            cmd = input(">> ")
            discard_tile = self.get_discard_tile(cmd)
            if discard_tile in meld.tiles:
                print("select tile not included stolen meld")
            else:
                return (meld, discard_tile)

    def pong_handler(self, tile, melds):
        self.print_tiles(None)
        self.print_cmd_pong(tile, melds)
        while(True):
            cmd = input(">> ")
            if cmd == "n":
                return (None, None)
            else:
                meld = self.get_element_from_cmd(cmd, melds)
                break
        self.print_tiles(None)
        self.print_cmd_pickup_tile(None)
        while(True):
            cmd = input(">> ")
            discard_tile = self.get_discard_tile(cmd)
            if discard_tile in meld.tiles:
                print("select tile not included stolen meld")
            else:
                return (meld, discard_tile)

    def stolen_kong_handler(self, tile):
        self.print_tiles(None)
        self.print_cmd_stolen_kong(tile)
        while(True):
            cmd = input(">> ")
            if cmd == "y":
                print("Kong")
                return True
            elif cmd == "n":
                return False
            else:
                print("input y or n")

    # Tools for manual player
    def print_tiles(self, pickup_tile):
        self.info.hand.print_pure_tiles()
        if pickup_tile is not None:
            print(" :"+pickup_tile.print_char, end="")
        self.info.hand.print_exposed_tiles()
        print("")

    def print_cmd_pickup_tile(self, pickup_tile):
        num_pure_tiles = self.info.hand.get_num_of_pure_tiles()
        for i in range(ord("a"), ord("a")+num_pure_tiles):
            print("  "+chr(i)+" ", end="")
        else:
            if pickup_tile is not None:
                print(" :<SP>", end="")
        print("")

    def print_cmd_win(self):
        print("Win?")
        print("y: win")
        print("n: not win")

    def print_cmd_closed_kong(self, melds):
        print("Closed kong?")
        for i in range(len(melds)):
            print(chr(ord("a") + i)+": ", end="")
            melds[i].print_meld()
            print("")
        print("n: not kong")

    def print_cmd_added_kong(self, tiles):
        print("Added kong?")
        for i in range(len(tiles)):
            print(chr(ord("a") + i)+": ", end="")
            tiles[i].print_tile()
            print("")
        print("n: not kong")

    def print_cmd_declare_ready(self, tiles):
        print("Declare ready?")
        for i in range(len(tiles)):
            print(chr(ord("a") + i)+": ", end="")
            tiles[i].print_tile()
            print("")
        print("n: not declare ready")

    def print_cmd_stolen_kong(self, tile):
        print("Kong? ", end="")
        tile.print_tile()
        print("")
        print("y: kong")
        print("n: not kong")

    def print_cmd_pong(self, tile, melds):
        print("Pong? ", end="")
        tile.print_tile()
        print("")
        for i in range(len(melds)):
            print(chr(ord("a") + i)+": ", end="")
            melds[i].print_meld()
            print("")
        print("n: not pong")

    def print_cmd_chow(self, tile, melds):
        print("Chow? ", end="")
        tile.print_tile()
        print("")
        for i in range(len(melds)):
            print(chr(ord("a") + i)+": ", end="")
            melds[i].print_meld()
            print("")
        print("n: not chow")

    def get_discard_tile(self, cmd):
        offset = ord(cmd) - ord("a")
        (suit, index) = self.info.hand.convert_overall_index_into_suit_index(offset)
        return self.info.hand.pure_tiles[suit][index]

    def get_element_from_cmd(self, cmd, objs):
        offset = ord(cmd) - ord("a")
        return objs[offset]


# main
if __name__ == '__main__':

    print("Sample application started!")
    print("1. Create GameCtrl")
    game_ctrl = gpmjctrl.GameCtrl()
    print("2. Create 3 auto PlayerCtrls")
    ikenaga = gpmjctrl.PlayerCtrl(gpmjplayer.Player("ikenaga"))
    yoshida = gpmjctrl.PlayerCtrl(gpmjplayer.Player("yoshida"))
    ozaki = gpmjctrl.PlayerCtrl(gpmjplayer.Player("ozaki"))
    print("3. Create 1 manual PlayerCtrl")
    sugimoto = gpmjctrl.PlayerCtrl(ManualPlayer("sugimoto"))
    print("4. Set players")
    game_ctrl.set_playerctrl(ikenaga)
    game_ctrl.set_playerctrl(yoshida)
    game_ctrl.set_playerctrl(ozaki)
    game_ctrl.set_playerctrl(sugimoto)
    print("5. Start players")
    ikenaga.start()
    yoshida.start()
    ozaki.start()
    sugimoto.start()
    print("6. Start game")
    game_ctrl.start()




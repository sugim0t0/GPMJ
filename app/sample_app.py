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

    def closed_kong_handler(self, tile):
        self.print_tiles(tile)
        self.print_cmd_kong()
        while(True):
            cmd = input(">> ")
            if cmd == "y":
                print("Closed kong")
                return True
            elif cmd == "n":
                return False
            else:
                print("input y or n")

    def added_kong_handler(self, tile):
        self.print_tiles(tile)
        self.print_cmd_kong()
        while(True):
            cmd = input(">> ")
            if cmd == "y":
                print("Added kong")
                return True
            elif cmd == "n":
                return False
            else:
                print("input y or n")

    def declare_ready_handler(self, tile):
        self.print_tiles(tile)
        self.print_cmd_declare_ready()
        while(True):
            cmd = input(">> ")
            if cmd == "y":
                print("Declare ready")
                self.print_tiles(tile)
                self.print_cmd_pickup_tile(tile)
                cmd = input(">> ")
                if cmd == " ":
                    return tile
                else:
                    return self.get_discard_tile(cmd)
            elif cmd == "n":
                return None
            else:
                print("input y or n")

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
        return None

    def pong_handler(self, tile, melds):
        return None

    def stolen_kong_handler(self, tile):
        return False


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




#!/usr/bin/env python

''' GPMJ (General Purpose (Japanese) Mah-Jong library)
    GUI application

    This application provides GUI Mah-jong game.

Modification History:
===========================================================
Date           Version   Description
===========================================================
15 Apr. 2018   0.1       Creation
-----------------------------------------------------------
'''

import tkinter as tk

import gpmjcore
import gpmjgame
import gpmjplayer
import gpmjctrl

__version__ = "0.1"
__date__    = "15 Apr. 2018"
__author__  = "Shun SUGIMOTO <sugimoto.shun@gmail.com>"

tile_img_width  = 18 # pixel
tile_img_height = 24

class MahjongApp():

    tile_images = [[], [], [], [], [], []]

    def __init__(self, master):
        canvas = tk.Canvas(master, bg='green', width=600, height=600, bd=2)
        canvas.place(x=0, y=0)
        self.img = tk.PhotoImage(file='tiles/j1.png')
        canvas.create_image(20, 20, image=self.img, tag="img1")
        canvas.delete("img1")
        # test
        self.create_tile_images()
        hand = gpmjcore.Hand()
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DOTS, 1))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DOTS, 9))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 1))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.BAMBOO, 9))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 1))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.CHARACTERS, 9))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, 0))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, 1))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, 2))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.WINDS, 3))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DRAGONS, 0))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DRAGONS, 1))
        hand.append_tile(gpmjcore.Tile(gpmjcore.Suits.DRAGONS, 2))
        self.draw_hand(canvas, hand, 20, 100)

    def draw_hand(self, canvas, hand, x, y):
        index = 0
        hand.sort_tiles()
        for suit in range(gpmjcore.Suits.NUM_OF_SUITS):
            for tile in hand.pure_tiles[suit]:
                canvas.create_image(x+index*tile_img_width, y, image=self.get_tile_image(tile, False))
                index += 1

    def create_tile_images(self):
        self.tile_images[gpmjcore.Suits.DOTS].append(tk.PhotoImage(file='tiles/p1.png'))
        self.tile_images[gpmjcore.Suits.DOTS].append(tk.PhotoImage(file='tiles/p2.png'))
        self.tile_images[gpmjcore.Suits.DOTS].append(tk.PhotoImage(file='tiles/p3.png'))
        self.tile_images[gpmjcore.Suits.DOTS].append(tk.PhotoImage(file='tiles/p4.png'))
        self.tile_images[gpmjcore.Suits.DOTS].append(tk.PhotoImage(file='tiles/p5.png'))
        self.tile_images[gpmjcore.Suits.DOTS].append(tk.PhotoImage(file='tiles/p6.png'))
        self.tile_images[gpmjcore.Suits.DOTS].append(tk.PhotoImage(file='tiles/p7.png'))
        self.tile_images[gpmjcore.Suits.DOTS].append(tk.PhotoImage(file='tiles/p8.png'))
        self.tile_images[gpmjcore.Suits.DOTS].append(tk.PhotoImage(file='tiles/p9.png'))
        self.tile_images[gpmjcore.Suits.DOTS].append(tk.PhotoImage(file='tiles/pe.png'))
        self.tile_images[gpmjcore.Suits.BAMBOO].append(tk.PhotoImage(file='tiles/s1.png'))
        self.tile_images[gpmjcore.Suits.BAMBOO].append(tk.PhotoImage(file='tiles/s2.png'))
        self.tile_images[gpmjcore.Suits.BAMBOO].append(tk.PhotoImage(file='tiles/s3.png'))
        self.tile_images[gpmjcore.Suits.BAMBOO].append(tk.PhotoImage(file='tiles/s4.png'))
        self.tile_images[gpmjcore.Suits.BAMBOO].append(tk.PhotoImage(file='tiles/s5.png'))
        self.tile_images[gpmjcore.Suits.BAMBOO].append(tk.PhotoImage(file='tiles/s6.png'))
        self.tile_images[gpmjcore.Suits.BAMBOO].append(tk.PhotoImage(file='tiles/s7.png'))
        self.tile_images[gpmjcore.Suits.BAMBOO].append(tk.PhotoImage(file='tiles/s8.png'))
        self.tile_images[gpmjcore.Suits.BAMBOO].append(tk.PhotoImage(file='tiles/s9.png'))
        self.tile_images[gpmjcore.Suits.BAMBOO].append(tk.PhotoImage(file='tiles/se.png'))
        self.tile_images[gpmjcore.Suits.CHARACTERS].append(tk.PhotoImage(file='tiles/m1.png'))
        self.tile_images[gpmjcore.Suits.CHARACTERS].append(tk.PhotoImage(file='tiles/m2.png'))
        self.tile_images[gpmjcore.Suits.CHARACTERS].append(tk.PhotoImage(file='tiles/m3.png'))
        self.tile_images[gpmjcore.Suits.CHARACTERS].append(tk.PhotoImage(file='tiles/m4.png'))
        self.tile_images[gpmjcore.Suits.CHARACTERS].append(tk.PhotoImage(file='tiles/m5.png'))
        self.tile_images[gpmjcore.Suits.CHARACTERS].append(tk.PhotoImage(file='tiles/m6.png'))
        self.tile_images[gpmjcore.Suits.CHARACTERS].append(tk.PhotoImage(file='tiles/m7.png'))
        self.tile_images[gpmjcore.Suits.CHARACTERS].append(tk.PhotoImage(file='tiles/m8.png'))
        self.tile_images[gpmjcore.Suits.CHARACTERS].append(tk.PhotoImage(file='tiles/m9.png'))
        self.tile_images[gpmjcore.Suits.CHARACTERS].append(tk.PhotoImage(file='tiles/me.png'))
        self.tile_images[gpmjcore.Suits.WINDS].append(tk.PhotoImage(file='tiles/j1.png'))
        self.tile_images[gpmjcore.Suits.WINDS].append(tk.PhotoImage(file='tiles/j2.png'))
        self.tile_images[gpmjcore.Suits.WINDS].append(tk.PhotoImage(file='tiles/j3.png'))
        self.tile_images[gpmjcore.Suits.WINDS].append(tk.PhotoImage(file='tiles/j4.png'))
        self.tile_images[gpmjcore.Suits.DRAGONS].append(tk.PhotoImage(file='tiles/j5.png'))
        self.tile_images[gpmjcore.Suits.DRAGONS].append(tk.PhotoImage(file='tiles/j6.png'))
        self.tile_images[gpmjcore.Suits.DRAGONS].append(tk.PhotoImage(file='tiles/j7.png'))
        self.tile_images[gpmjcore.Suits.NUM_OF_SUITS].append(tk.PhotoImage(file='tiles/j9.png'))

    def get_tile_image(self, tile, b_back):
        if b_back:
            return self.tile_images[gpmjcore.Suits.NUM_OF_SUITS][0]
        if tile.suit == gpmjcore.Suits.DOTS or \
           tile.suit == gpmjcore.Suits.BAMBOO or \
           tile.suit == gpmjcore.Suits.CHARACTERS:
            if tile.number == 5 and tile.b_red:
                return self.tile_images[tile.suit][9]
            else:
                return self.tile_images[tile.suit][tile.number - 1]
        else:
            # Winds or Dragons
            return self.tile_images[tile.suit][tile.number]


# main
if __name__ == '__main__':

    root = tk.Tk()
    # Title
    root.title('Mahjong')
    # Size
    root.geometry("600x600")
    # App.
    app = MahjongApp(root)

    root.mainloop()


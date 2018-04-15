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

from tkinter import *
from tkinter import ttk

import gpmjcore
import gpmjgame
import gpmjplayer
import gpmjctrl

__version__ = "0.1"
__date__    = "15 Apr. 2018"
__author__  = "Shun SUGIMOTO <sugimoto.shun@gmail.com>"


# main
if __name__ == '__main__':

    root = Tk()
    root.title('GPMJ GUI App.')

    #frame = ttk.Frame(root, height=400, width=400, relief='sunken', borderwidth=5)
    #frame.grid()
    canvas = Canvas(root, width=500, height=300, relief=RIDGE, bd=2)
    canvas.place(x=0, y=0)
    img = PhotoImage(file='tiles/j1.png')
    canvas.create_image(10, 10, image=img, anchor=NW)

    root.mainloop()


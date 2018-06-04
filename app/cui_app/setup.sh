#!/bin/sh

if [ ! -e gpmjcore.py ]; then ln -s ../../gpmj/gpmjcore.py gpmjcore.py; fi
if [ ! -e gpmjgame.py ]; then ln -s ../../gpmj/gpmjgame.py gpmjgame.py; fi
if [ ! -e gpmjplayer.py ]; then ln -s ../../gpmj/gpmjplayer.py gpmjplayer.py; fi
if [ ! -e gpmjctrl.py ]; then ln -s ../../gpmj/gpmjctrl.py gpmjctrl.py; fi
if [ ! -e gpmj.cfg ]; then ln -s ../../gpmj/gpmj.cfg gpmj.cfg; fi

echo setup done

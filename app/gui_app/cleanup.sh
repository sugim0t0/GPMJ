#!/bin/sh

if [ -e gpmjcore.py ]; then rm gpmjcore.py; fi
if [ -e gpmjgame.py ]; then rm gpmjgame.py; fi
if [ -e gpmjplayer.py ]; then rm gpmjplayer.py; fi
if [ -e gpmjctrl.py ]; then rm gpmjctrl.py; fi
if [ -e gpmj.cfg ]; then rm gpmj.cfg; fi

if [ -d tiles ]; then rm -rf tiles; fi

echo cleanup done

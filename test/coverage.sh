#!/bin/bash

start_or_cleanup=$1

if [ "$start_or_cleanup" != "start" ] && [ "$start_or_cleanup" != "cleanup" ] ; then
    echo "usage: $0 <start|cleanup>"
elif [ "$start_or_cleanup" == "start" ] ; then
    if [ ! -e gpmjcore.py ] ; then
        ln -s ../gpmj/gpmjcore.py gpmjcore.py
    fi
    if [ ! -e gpmjgame.py ] ; then
        ln -s ../gpmj/gpmjgame.py gpmjgame.py
    fi
    if [ ! -e gpmjplayer.py ] ; then
        ln -s ../gpmj/gpmjplayer.py gpmjplayer.py
    fi
    python3-coverage run test_gpmjcore.py
    mv .coverage .coverage.core
    python3-coverage run test_gpmjgame.py
    mv .coverage .coverage.game
    python3-coverage run test_gpmjplayer.py
    mv .coverage .coverage.player
    python3-coverage combine
    python3-coverage html
else ## "$start_or_cleanup" == "cleanup"
    if [ -e gpmjcore.py ] ; then
        rm gpmjcore.py
    fi
    if [ -e gpmjgame.py ] ; then
        rm gpmjgame.py
    fi
    if [ -e gpmjplayer.py ] ; then
        rm gpmjplayer.py
    fi
    if [ -e .coverage ] ; then
        rm -rf .coverage
    fi
    if [ -e htmlcov ] ; then
        rm -rf htmlcov
    fi
fi


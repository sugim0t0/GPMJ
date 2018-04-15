# GPMJ
&#127001;
&#127009;
&#126992;
&#127000;
&#126983;
&#126991;
&#126976;
&#126976;
&#126977;
&#126978;
&#126979;
&#126982;
&#126981;
&#126980;  
GPMJ is General Purpose (Japanese) Mah-Jong library for Python 3.  
GPMJ includes following modules.  
1. ./gpmj/gpmjcore.py
  - Core module
  - This module provides functions to judge each hand and structures of tile, meld, eye and hand.
2. ./gpmj/gpmjgame.py
  - Game module
  - This module provides functions to process game and to manage game configurations.
3. ./gpmj/gpmjplayer.py
  - Player module
  - This module provides Player template class included each handler fuction.
  - User should implement each handler function to subclass Player class.
4. ./gpmj/gpmjctrl.py
  - Controller module
  - This module provides controller for player and game.
***
## Sample application
sample_app.py is sample application used GPMJ library.  
1. ./app/cui_app/sample_app.py
  - This application provides simple command line Mah-jong game.
2. ./app/cui_app/setup.sh
  - Shell script for setup sample application.

### Usage
    $ cd app/cui_app
    $ source setup.sh
    $ python sample_app.py
***
## Install
    $ python setup.py install [--user] --record files.txt

## Uninstall
    $ cat files.txt | xargs rm -rf
    $ rm files.txt

## Unit test
    $ python -m unittest discover test/

## Coverage
    $ cd test/
    $ ln -s ../gpmj/gpmjcore.py gpmjcore.py
Edit test_gpmjcore.py  
Comment out `# from gpmj import gpmjcore`  
And uncomment `import gpmjcore`  

    $ coverage run test_gpmjcore.py
    $ coverage html gpmjcore.py
    $ open htmlcov/index.html

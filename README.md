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

## Install
`$ python setup.py install [--user] --record files.txt`

## Uninstall
`$ cat files.txt | xargs rm -rf`  
`$ rm files.txt`

## Unit test
`$ python -m unittest discover test/`

## Coverage
`$ cd test/`  
`$ ln -s ../gpmj/gpmjcore.py gpmjcore.py`  
Edit test_gpmjcore.py  
Comment out `# from gpmj import gpmjcore`  
And uncomment `import gpmjcore`  
`$ coverage run test_gpmjcore.py`  
`$ coverage html gpmjcore.py`  
`$ open htmlcov/index.html`  

from distutils.core import setup

setup(
    name='gpmj',
    version='0.30',
    packages=['gpmj'],
    package_dir={'gpmj': './gpmj'},
    )

# INSTALL
# python setup.py install [--user]

# UNINSTALL
# python setup.py install [--user] --record files.txt
# cat files.txt | xargs rm -rf
# rm files.txt


from distutils.core import setup
import py2exe

setup(windows=['tetris.py'])

setup(windows = [{"script":"tetris.py", "icon_resources": [(1, "bm.ico")]}])
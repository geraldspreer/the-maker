from distutils.core import setup
import py2exe

setup(
    windows=[{"script": "maker.py", "icon_resources": [(1, "system/tags.ico")]}],
)

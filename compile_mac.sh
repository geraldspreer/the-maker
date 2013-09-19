#!/bin/bash
rm -rf build dist
python setup.py py2app --iconfile system/maker.icns --site-packages -r system
cp CHANGES dist
cp LICENSE dist
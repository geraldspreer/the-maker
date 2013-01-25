#!/bin/bash

echo "removing zip files..."
rm *.zip

rm maker-src
mkdir maker-src

echo "Gathering source..."
echo "All files..."
cp -v -f *.* maker-src
echo "System..."
cp -R -P -v -f system maker-src/system
cp -R -P -v -f XRCed_Files maker-src/XRCed_Files

echo "removing zip files..."
rm maker-src/*.zip

echo "removing .pyc files..."
rm maker-src/*.pyc 

echo "removing Entitlements..."
rm maker-src/Entitlements.plist

echo "removing App Store Setup..."
rm maker-src/setup_app_store.py

echo "removing Packages..."
rm maker-src/TheMaker.pkg

echo "removing Tools..."
rm -v maker-src/gatherSource.sh

zip -r the-maker-src maker-src/.

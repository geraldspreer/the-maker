#!/bin/bash

echo "removing zip files..."
rm *.zip

version=$(python ./makerVersion.py)
dashed_version=$(python ./makerVersion.py --use-dash)

target=the-maker-$version-src
dash=the-maker-$dashed_version-src

rm $target
mkdir $target

echo "Gathering source..."
echo "All files..."
cp -v -f *.* $target
echo "System..."
cp -R -P -v -f system $target/system
cp -R -P -v -f XRCed_Files $target/XRCed_Files

echo "removing zip files..."
rm $target/*.zip

echo "removing .pyc files..."
rm $target/*.pyc 

echo "removing Entitlements..."
rm $target/Entitlements.plist

echo "removing App Store Setup..."
rm $target/setup_app_store.py

echo "removing App Store compile script..."
rm $target/compile.sh

echo "removing Packages..."
rm $target/TheMaker.pkg

echo "removing Tools..."
rm -v $target/gatherSource.sh

echo "Packaging..."
zip -r $dash $target/.

echo "Renaming..."
mv $dash.zip $target.zip

echo "removing tmp files..."
rm -rf $target
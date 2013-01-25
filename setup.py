from distutils.core import setup
import sys

plist = dict(
             LSApplicationCategoryType = "public.app-category.developer-tools",
             CFBundleVersion = "1.6", 
             CFBundleDisplayName = "TheMaker",
             CFBundleIdentifier = "com.barnhouse.maker",
             NSHumanReadableCopyright = "Gerald Spreer"
  
)

if sys.platform == 'darwin':
    import py2app
    buildstyle = 'app'
    print "#---------------------------------------------------------"
    print "building with py2app version: ", py2app.__version__
    print "#---------------------------------------------------------"


setup(
      options=dict(py2app=dict(plist=plist)),
      name="TheMaker",
      **{buildstyle : ['maker.py']}
)


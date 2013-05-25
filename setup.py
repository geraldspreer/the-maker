from distutils.core import setup
import sys
import makerVersion

plist = {
             'CFBundleDocumentTypes': [
  
            {
                'CFBundleTypeExtensions': ['makerProject'],
                'CFBundleTypeIconFile': 'maker.icns',
                'CFBundleTypeName': 'TheMaker Project',
                'CFBundleTypeRole': 'Editor',
                'LSTypeIsPackage': True,
            },
        ],
             "LSApplicationCategoryType" : "public.app-category.developer-tools",
             "CFBundleVersion" : makerVersion.appVersion, 
             "CFBundleDisplayName" : "TheMaker",
             "NSHumanReadableCopyright" : "Gerald Spreer"
  
}

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


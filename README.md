This is the 1.6 release of "TheMaker". The maker is a Content Management System 
(CMS) for websites. The Maker is running on your local computer and after you 
made your changes you are publishing via FTP. 

All that is required is some webspace with FTP access.

TheMaker is developed for OS X but should run on Linux and Windows as well.
	
We hope you have a pleasant experience using the maker. If you have any feedback
you are welcome to contact us at [info at makercms dot org] .
   
   
You will find a tutorial and videos at: [http://www.makercms.org/tutorial]

__________________________________________

To run TheMaker from source using Python you need:

- Python 2.7 
- wxPython 2.9.0.0 (Cocoa build for OS X) .
- python-markdown2 (http://code.google.com/p/python-markdown2/) 

------------------------------------------

To build "TheMaker" you will need:

- py2app 
- py2exe

To build, rust run: 

$ ./compile_mac.sh

or on Windows

$ ./compile_win.sh

--------------------------------------------

To run from source:

python ./maker.py

____________________________________________

See LICENSE for license information.


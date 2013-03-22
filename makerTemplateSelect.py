from makerUtilities import writeFile

class TemplateView:
    
    def __init__(self, templateDir ,targetDir):
        
        self.templates = templateDir
        self.target = targetDir
    
    
    def createHTML(self):
        
        scaffold = """ 
<html>
    <head>

        <style type="text/css">

        html {

            background:#ccc; 

        }

        body {

            width:700px;
            padding: 10px 20px;

        }

        p 

        </style>

    </head>
    <body>


    <a href="#-TAGRGET">Click me</a>
    <a href="#_other_template">Other Template</a>
    <a href="#_something else">Something else</a>
    </body>

</html>



        
        
        
        """
        
        writeFile(targetDir, scaffold)
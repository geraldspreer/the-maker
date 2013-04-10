from makerUtilities import writeFile
from makerUtilities import readFile
import os

def scaffold(systemDir):
    
    return """<!DOCTYPE html>
<html>
    <head>
     <meta charset="utf-8" />
         <script src='file://""" + os.path.join(systemDir, "jquery.min.js") + """'></script>
        

        
        
       <style type="text/css">

        html {

            background: -webkit-gradient(linear, left top, left bottom, from(#000), to(rgb(93,94,120)));
            background-attachment:fixed;
        }

        body {

            font-family: "Helvetica Neue";
            font-size: 14px;
            width:auto;
            /* max-width:694px; */
            color:#fff;
            padding:20px 20px;


        }

        a {

            text-decoration:none;
            color:#000;
            cursor:default;
        }



        p {
            font-weight:lighter;
            color:#fff;
            letter-spacing:0.09em;
            float:left;
            font-size:0.9em;
            line-height:1.45em;
            text-align:justify;
            margin:-6px 0px 24px 10px;

        }

        
     
        h5 {
            font-weight:lighter;
            letter-spacing:0.050em;
            margin:-28px 0px 0px 8px;
            line-height:3em;
            font-size:20px;
            cursor:default;
            
        
        }

        img {
            border:1px solid #333;
                
            width:100%;
            height:100%;
            -webkit-box-reflect: below 0px -webkit-gradient(linear, left top, left bottom, from(transparent), color-stop(50%, transparent), to(rgba(0,0,0,0.2)));
            /* -webkit-transform: perspective( 600px ) rotateY( 20deg );        */    
            margin-bottom:40px;
                }


        .row {
            
            width:100%;
            margin:0px 0px 40px 10px;
            float:left;
            clear:both;
            
        
        }

        .thumbnail {

            width:17%;
            border: 1px solid rgba(0,0,0,0);
            padding:20px 20px 10px 20px;
            margin:0px 20px 0px 0px;
            float:left;
            clear:right;
            -webkit-border-radius:10px;
        -webkit-transition: border-color, 0.5s;
    
        }

        .thumbnail img {
        
            -webkit-border-radius:8px;
        
        }

        .thumbnail p {
            
            text-align:center;
            margin:-24px 0px 0px 0px;
            width:100%;
            font-size:14px;
            cursor:default;
        
        }

        .thumbnail:hover {
        
            border-color: #aaa;
            padding:20px 20px 10px 20px;
        -webkit-border-radius:10px;
       
        }


        .info {
        
            width:92%;
            float:left;
            clear:both;
            display:none;
            margin:20px 10px 0px 10px;
            
        
        }
        
        .info p {
            
            float:left;
            clear:right;
            cursor:default;
        
        }

        .info img {

            width:280px;
            height:auto;
            float:left;
            clear:right;
            margin:0px 20px 0px 0px;
            -webkit-transform: perspective( 600px ) rotateY( 10deg );
            -webkit-transition: width, 0.5s; 
                
        }

        .info img:hover {

            width:320px;
            -webkit-transform: perspective( 600px ) rotateY( 0deg ); 
                
        }

        a.button {
            
            cursor:default;
            color:#000;
        
        }

        a.button:active {

            color:#000;
            background:  -webkit-gradient(linear, left top, left bottom, from(#eee), to(#bbb));
        
        }



    </style>




    <script type="text/javascript">
    
        $(document).ready(function(){
              $('.thumbnail').hover(function(){
                      $('.info').hide();
                      
                  $($(this).data('info')).show();
     
              });
        }); 
    
    
    </script>


    </head>
    <body>


""" + createThumbnails(systemDir) + createInfo(systemDir) + """ 
    </body>

</html>

"""



def buildView(systemDir, viewPath):
    writeFile(os.path.join(viewPath,"yourTemplates.html"), scaffold(systemDir))
    
    return os.path.join(viewPath,"yourTemplates.html")
    
    
def createThumbnails(systemDir):
    
    thumbnails = "<div class='row'>\n"
    
    for template in os.listdir(os.path.join(systemDir, "templates")):
        if not template.startswith("."):
            thumbnails += makeThumbnail(systemDir, template)
    
    thumbnails += "</div>"     
    return thumbnails
    
    
def createInfo(systemDir):
    
    info = "<div class='row'>\n"
    
    for template in os.listdir(os.path.join(systemDir, "templates")):
        
        if not template.startswith("."):
            s = readFile(os.path.join(systemDir, "templates", template, "parts","info.json")) 
            print "template is:", template
            data = eval(s)
        
            info += makeInfo(systemDir, template, data)
    
    info += "</div>"     
    return info


def makeInfo(systemDir, templateName, data):
    
    previewImage = os.path.join(systemDir, "templates", templateName, "parts/preview.jpg")
    info = """
    
    <div class="info" id="info-""" + data["Title"] + """">
        <h5>""" + data["Title"] + """</h5>
        <p><img src='""" + previewImage + """' />""" + data["Description"] + """</p>
        </div>
    
    
    """
    
    return info



def makeThumbnail(systemDir, templateName):
    
    previewImage = os.path.join(systemDir, "templates", templateName, "parts/preview.jpg")
    thumbnail = """
    
     <div class='thumbnail' data-info='#info-""" + templateName + """'>
                <a href='--""" + templateName + """--'>
        <img src='""" + previewImage + """' />
        <p>""" + templateName + """</p></a>
    </div>
    
    """
    
    
    return thumbnail
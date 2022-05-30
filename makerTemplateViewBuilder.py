from makerUtilities import writeFile
from makerUtilities import readFile
import os


def scaffold(systemDir, defaultTheme):

    return (
        """<!DOCTYPE html>
<html>
    <head>
     <meta charset="utf-8" />
         <script src='file://"""
        + os.path.join(systemDir, "jquery.min.js")
        + """'></script>
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
            -webkit-transform: perspective( 600px );
        }

        a {
            color: #ddd;
            }

        .thumbnail a {

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
            text-align:left;
            margin:-6px 0px 24px 10px;
        }

        h5 {
            font-weight:lighter;
            letter-spacing:0.050em;
            margin:-28px 0px 0px 8px;
            line-height:3em;
            font-size:22px;
            cursor:default;
        }

        img {
            border:1px solid #333;
            width:100%;
            height:100%;
            -webkit-box-reflect: below 0px -webkit-gradient(linear, left top, left bottom, from(transparent), color-stop(50%, transparent), to(rgba(0,0,0,0.2)));
            -webkit-transform: perspective( 600px ) rotateY( 0deg);    
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
            padding:20px 20px 10px 20px;
            margin:0px 20px 0px 0px;
            float:left;
            clear:right;
            background:none;
        }

        .thumbnail img {
            height:100px;
        }

        .thumbnail p {
            text-align:center;
            margin:-24px 0px 0px 0px;
            width:100%;
            font-size:14px;
            cursor:default;
        }

           .thumbnail.selected {
            border:1px solid #777;
            padding:20px 20px 10px 20px;
            -webkit-border-radius:10px;
            background: -webkit-gradient(linear, left top, left bottom, from(rgba(140,140,140,0.1)), to(rgba(170,170,170,0.2)));
        }

        .info {
            width:92%;
            float:left;
            clear:both;
            display:none;
            margin:40px 10px 0px 10px;
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
            margin:0px 48px 0px 8px;
            -webkit-transform: perspective( 600px ) rotateY( 10deg );
            /* 
            -webkit-transition: width, 0.5s; 
            */  
        }

        /*
        .info img:hover {

            width:320px;
            -webkit-transform: perspective( 600px ) rotateY( 0deg ); 
        }
        */

        .info h5 {
            margin-top:0px;
        }

        .info h5, p {
            width:380px;
            float:left;
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
             $('#"""
        + defaultTheme
        + """').addClass('selected');
             $('#info-"""
        + defaultTheme
        + """').show();
              $('.thumbnail').click(function(){
                    $('.info').hide();
                    $('.thumbnail').removeClass('selected') 
                     $(this).addClass('selected');
                  $($(this).data('info')).show();
              });
        }); 
    </script>
    </head>
    <body>
"""
        + createThumbnails(systemDir)
        + createInfo(systemDir)
        + """ 
    </body>
</html>

"""
    )


def buildView(systemDir, viewPath):
    writeFile(
        os.path.join(viewPath, "yourTemplates.html"),
        scaffold(systemDir, defaultTemplate()),
    )

    return os.path.join(viewPath, "yourTemplates.html")


def defaultTemplate():

    # ===========================================================================
    #  This is used to set the default template for the application
    # ===========================================================================

    return "Simple-Markdown"


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
            s = readFile(
                os.path.join(systemDir, "templates", template, "parts", "info.json")
            )

            data = eval(s)
            info += makeInfo(systemDir, template, data)

    info += "</div>"
    return info


def makeInfo(systemDir, templateName, data):
    previewImage = os.path.join(
        systemDir, "templates", templateName, "parts/preview.jpg"
    )
    info = (
        """
    <div class="info" id="info-"""
        + data["Title"]
        + """">
        <img src='"""
        + previewImage
        + """' />
        <h5>"""
        + data["Title"]
        + """</h5>
        <p>"""
        + data["Description"]
        + """<br /><br />
        Credit: """
        + data["Credit"]
        + """<br />
        Support: <a href='"""
        + data["Support"]
        + """'>www.makercms.org</a><br />
        </p>
        </div>
    """
    )

    return info

def makeThumbnail(systemDir, templateName):

    previewImage = os.path.join(
        systemDir, "templates", templateName, "parts/preview.jpg"
    )
    thumbnail = (
        """
     <div class='thumbnail' id='"""
        + templateName
        + """' data-info='#info-"""
        + templateName
        + """'>
                <a href='--"""
        + templateName
        + """--'>
        <img src='"""
        + previewImage
        + """' />
        <p>"""
        + templateName
        + """</p></a>
    </div>
    """
    )

    return thumbnail

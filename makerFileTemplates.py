def getTemplate(type=None):
    """ returns a string containing the template text """
    
    if type == ".html":
        return """
 <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
        <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
        <meta http-equiv="expires" content="0" />
        <meta name="generator" content="the maker - www.makercms.org" />
        <title>    </title>
   </head>
        <body>
        
        </body>
</html>

                """
    elif type == ".xml":
        return '<?xml version="1.0" encoding="ISO-8859-1" ?>\n'
    
    elif type == ".php":
        return """ <?php\n\n  echo "Hello World"; \n\n?> """
          
    else: 
        return ""
    
    
    
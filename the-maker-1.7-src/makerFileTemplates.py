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
      
    elif type == ".css":
        theTemplate  = '/* Before entering a new definition '
        theTemplate += 'make sure it is not already defined below */\n\n'
        for t in tags():
            theTemplate +=  t + '{\n\n}\n\n'

        return theTemplate
    
    else: 
        return ""
    
    
    
    
def tags():
        return ['html', 'body', 'div', 'span', 'applet', 'object',
                'iframe', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 
                'blockquote', 'pre', 'a', 'abbr', 'acronym', 'address',
                'big', 'cite', 'code', 'del', 'dfn', 'em', 'font', 'img',
                'ins', 'kbd', 'q', 's', 'samp', 'small', 'strike', 'strong',
                'sub', 'sup', 'tt', 'var', 'dl', 'dt', 'dd', 'ol', 'ul', 'li',
                'fieldset', 'form', 'label', 'legend', 'table', 'caption',
                'tbody', 'tfoot', 'thead', 'tr', 'th', 'td'
                ]

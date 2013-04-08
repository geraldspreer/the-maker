import sys

appVersion = "1.8"


def main():
    """ used for making src package """

    try: 
        if sys.argv[1] == "--use-dash":
            # use dash in version number
            print appVersion.replace(".", "-")
        
        else:
            print appVersion
        
    except:
        print appVersion

    
if __name__ == '__main__':
    main()
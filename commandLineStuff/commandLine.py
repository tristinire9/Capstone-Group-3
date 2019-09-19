import sys
import requests
from requests.exceptions import HTTPError
import re
from datetime import datetime
#'https://intense-stream-78237.herokuapp.com/upload'
url="http://127.0.0.1:5000/"

def send_Function(file,fileName,versionNumber):
    try:
        response = requests.post(url+'component', files={'file':open(file,'rb')}, params={'ver':versionNumber, 'Fname':fileName})

    # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    except FileNotFoundError:
        print("FILE NOT FOUND")
    else:
        if response.status_code==200:
            sys.exit(0)
        else:
            sys.exit(1)


def get_filename_from_cd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]

def download_Function(fileName, versionNumber):
    try:
        response = requests.post(url+'download',data={'key':fileName})
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        filename = get_filename_from_cd(response.headers.get('content-disposition'))
        open(filename, 'wb').write(response.content)
        if response.status_code==200:
            sys.exit(0)
        else:
            sys.exit(1)


def help():
    print("""\n\n***Welcome to ITL's Software Component Command Line tool!*** \nThis tool is used to store, retrieve, and look up components in the Store\n (Server)\n
To use this tool correctly, follow the examples below:\n""")
    print("""\nPUSH \"filename.xxx\" \"NAME\" \"1.1.1.1\" - Sends file (relative path) to Store.
PULL \"filename.xxx\" \"1.1.1.1\"- Sends retrieve request to Store.\n
\n
You must specify a command (Push/Pull), the File (relative path), name the Component, and the version number.\n
You cannot have duplicates in the store, \ne.g: matching component name and version number.
""")

if not len(sys.argv) > 3 or sys.argv[1].lower() not in ["push", "pull"]:
    help()
elif sys.argv[1].lower()=="push":
    send_Function(sys.argv[2],sys.argv[3],sys.argv[4])
elif sys.argv[1].lower()=="pull":
    download_Function(sys.argv[2],sys.argv[3])

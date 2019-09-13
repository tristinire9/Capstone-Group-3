import sys
import requests
from requests.exceptions import HTTPError
#'https://intense-stream-78237.herokuapp.com/upload'
def send_Function(file,fileName,versionNumber):
    try:
        response = requests.post('https://intense-stream-78237.herokuapp.com/component', files={'file':open(file,'rb')})

    # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    except FileNotFoundError:
        print("FILE NOT FOUND")
    else:
        print('Success!')
        
        print(response)

def download_Function(fileName, versionNumber):
    try:
        response = requests.post('https://intense-stream-78237.herokuapp.com/download',form={'key':fileName})
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')
        print(response)


def help():
    print("""\nPUSH \"filename.xxx\" \"NAME\" \"1.1.1.1\" - Sends file (relative path) to Store.
PULL \"filename.xxx\" \"1.1.1.1\"- Sends pull request to Store.
""")

if not len(sys.argv) > 3 or sys.argv[1].lower() not in ["push", "pull"]:
    help()
elif sys.argv[1].lower()=="push":
    send_Function(sys.argv[2],sys.argv[3],sys.argv[4])
elif sys.argv[1].lower()=="pull":
    download_Function(sys.argv[2],sys.argv[3])

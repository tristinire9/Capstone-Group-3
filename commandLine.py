import sys
import requests
from requests.exceptions import HTTPError

for url in ['https://api.github.com', 'http://localhost:8080']:
    try:
        response = requests.get(url)

        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')

print(response)
# print ("This is the name of the script: ", sys.argv[0])
# print ("Number of arguments: ", len(sys.argv))
# print ("The arguments are: " , str(sys.argv))
def help():
    print("""\nPUSH \"filename.xxx\" - Sends file (relative path) to Store.
PULL \"filename.xxx\" - Sends pull request to Store.
""")

if not len(sys.argv) > 1 or sys.argv[1].lower() not in ["push", "pull"]:
    help()

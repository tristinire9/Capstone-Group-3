import sys
import requests
from requests.exceptions import HTTPError
import re
import zipfile
import os
import shutil
import fnmatch

def retrieve_file_paths(dirName):

  # setup file paths variable
  filePaths = []

  # Read all directory, subdirectories and file lists
  for root, directories, files in os.walk(dirName):
    for filename in files:
        # Create the full filepath by using os module.
        filePath = os.path.join(root, filename)
        filePaths.append(filePath)

  # return all paths
  return filePaths

#Zips single files/directories, otherwise renames the file if it's already zipped
def ensureZipped(file,fileName):
    if os.path.isfile(file):
        if file.split(".")[1]=="zip":
            os.rename(file,fileName+".zip")
        else:
            zipf = zipfile.ZipFile(fileName+".zip",'w',zipfile.ZIP_DEFLATED)
            zipf.write(file)
            zipf.close()
    else:
        filePaths = retrieve_file_paths(file)
        zipf = zipfile.ZipFile(fileName+'.zip', 'w', zipfile.ZIP_DEFLATED)
        for file in filePaths:
            zipf.write(file)
        zipf.close()

#'https://intense-stream-78237.herokuapp.com/'
url="https://intense-stream-78237.herokuapp.com/"

def send_Function(file,fileName,versionNumber):
    try:
        ensureZipped(file,fileName)
        response = requests.post(url+'component', files={'file':open(fileName+".zip",'rb')}, params={'ver':versionNumber, 'Fname':fileName})
    # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
        if response.status_code==400:
            print("The Server denied the request most likely because that Component name and version already exists in the database.")

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

def download_Function(fileName, versionNumber,location="",recipeDownload=False):
    try:
        response = requests.get(url+'retrieve',params={'ver':versionNumber, 'Fname':fileName})
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        filename = get_filename_from_cd(response.headers.get('content-disposition'))
        if location!="":
            open(str(location+'/'+filename), 'wb').write(response.content)
        else:
            open(filename, 'wb').write(response.content)
        if recipeDownload==False:
            if response.status_code==200:
                sys.exit(0)
            else:
                sys.exit(1)

def put_components_to_right_places(recipe_destination, components_destinations_dictionary):
    all_components = os.listdir(recipe_destination)

    all_components_names_without_extensions = []
    for component in all_components:
        if "." in component:
            all_components_names_without_extensions.append(component.partition('.')[0])
        else:
            all_components_names_without_extensions.append(component)

    for i in range(0, len(all_components)):
        source = recipe_destination + "/" + all_components[i]
        destination = recipe_destination + components_destinations_dictionary[all_components_names_without_extensions[i]]
        if os.path.exists(destination):
            pass
        else:
            os.mkdir(destination)
        shutil.move(source, destination)
    return 0


def get_Components(recipeName, recipeVersion, recipe_destination):
    response = requests.get(url+'fetchRecipeComponents',params={'softwareName':recipeName, 'ver':recipeVersion})
    if not os.path.exists(recipe_destination):
        os.makedirs(recipe_destination)
    data_json = response.json()

    components_destinations_dictionary = dict()
    for i in data_json:
        download_Function(i[1],i[2],str(recipe_destination),True)
        version_number = i[2].replace(".", "")
        components_destinations_dictionary[i[1]+version_number] = i[-2]

    put_components_to_right_places(recipe_destination, components_destinations_dictionary)

    pattern = '*.zip'
    for root, dirs, files in os.walk(recipe_destination):
        for filename in fnmatch.filter(files, pattern):
            zipfile.ZipFile(os.path.join(root, filename)).extractall(os.path.join(root, os.path.splitext(filename)[0]))
            os.remove(os.path.join(root, filename))

    return 0

def help():
    print("""\n\n***Welcome to ITL's Software Component Command Line tool!*** \nThis tool is used to store, retrieve, and look up components in the Store\n (Server)\n
To use this tool correctly, follow the examples below:\n""")
    print("""\nPUSH \"filename.xxx\" \"NAME\" \"1.1.1.1\" - Sends file (relative path) to Store.
PULL \"filename.xxx\" \"1.1.1.1\" \"C:\\Users...\"- Sends retrieve request to Store.\n
If you don't specify a download location, default download is relative to this script.
\n
You must specify a command (Push/Pull), the File (relative path), name the Component, and the version number.\n
You cannot have duplicates in the store, \ne.g: matching component name and version number.
""")

if not len(sys.argv) > 3 or sys.argv[1].lower() not in ["push", "pull","assemble"]:
    help()
elif sys.argv[1].lower()=="push":
    send_Function(sys.argv[2],sys.argv[3],sys.argv[4])
elif sys.argv[1].lower()=="pull":
    if len(sys.argv)>4:
        download_Function(sys.argv[2],sys.argv[3],sys.argv[4])
    else:
        download_Function(sys.argv[2],sys.argv[3])
elif sys.argv[1].lower()=="assemble":
    get_Components(sys.argv[2],sys.argv[3], sys.argv[4])

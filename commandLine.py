import sys

# print ("This is the name of the script: ", sys.argv[0])
# print ("Number of arguments: ", len(sys.argv))
# print ("The arguments are: " , str(sys.argv))
def help():
    print("""\nPUSH \"filename.xxx\" - Sends file (relative path) to Store.
PULL \"filename.xxx\" - Sends pull request to Store.
""")

if not len(sys.argv) > 1 or sys.argv[1].lower() not in ["unzip", "create", "grade"]:
    help()

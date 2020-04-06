This is a very simple updater I made for when I give my programs to others.
It is designed to work from a base python install for ease of install.

How to use:
1.Add a global VERSION var that is used in comparison on a .py file. Can be in the main file or a nearby one.
2.Update lines 8-12 in Installer.py
    the default values are as examples to show it working
    CHECK_FILE: points to file that has VERSION var
    UPDATE_FILE_LINK: points to either a github repo or a static link. Will be used to download the update info file
    IS_GITHUB_LINK: if True then the installer will ensure it goes to the latest release to find the update info file
    UPDATE_FILE_NAME: so the installer knows which file is the update file
    NEEDED_IMPORTS: will ensure any missing modules will be installed on the system
3.Make an update info file
    Only the INSTRUCTIONS dict matters
        'VERSION' is compared to VERSION to CHECK_FILE
        'prep' is sent to exec() unless its 'prep func', then it will call the prep_func for more complex prep code
        'dl' contains the links to files that need to be downloaded. $R$ gets replaced by the latest repo download link str to try to enable cleanliness
        'cleanup' acts the same as prep but runs after downloading files. use 'cleanup func' to call its function

I recommend modifying update.py in my latest release for ease of use

wifipassword is a rarely seen module used which I use only to show how the module installer works.

Maybe useful functions:
ensure_minimum_imports(import_dict: dict):
    test for each module, and if it doesnt import, pip installs it
dl_from_link(url, file_name):
	takes a link to something, and downloads the data to the file_name

The Idea:
ensure imports are there
get update info file
compare versions between home and on git
if different, use the update file to download new stuff

How to try it:
Download the installer from the latest release and run it. Done.

main.py is the the 'main' file with version var.
there is some support with using text files for CHECK_FILE which is nothing but version str and UPDATE_FILE_NAME which only contains the dict which gets evaled.
by setting IS_GITHUB_LINK to False, UPDATE_FILE_LINK becomes a static location for where to find the update file

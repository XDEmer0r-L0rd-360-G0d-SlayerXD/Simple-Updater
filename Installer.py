import subprocess
import sys
import os
import importlib
# written in 3.8, 3.5 minimum due to function typing

# These are to designed to be changed by user
CHECK_FILE = 'hold.txt'  # file that contains the version (will be imported, should be in same dir as installer.py)
UPDATE_FILE_LINK = 'link to repo'  # where to find the update file
IS_GITHUB_LINK = True  # runs extra code when its a repo, otherwise assume UPDATE_FILE_LINK is static
UPDATE_FILE_NAME = 'update.py'  # will eval a .txt and run a .py. must still follow a specified format
NEEDED_IMPORTS = {'wifiPassword': 'wifipassword', 'requests': 'requests'}  # {'import name': 'pip install name'}


def ensure_minimum_imports(import_dict):
    """
    Will install any missing imports.
    :param import_dict: is a dict because some modules have different names when importing and installing ex. {'bs4': 'beautifulsoup4'}
    :return: None
    """
    failed_installs = set()
    for (a, b) in import_dict.items():
        try:
            importlib.import_module(a)
        except ModuleNotFoundError:
            print(f'need {a}')
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--user', b])
            try:
                importlib.import_module(a)
            except Exception:
                print(f'Cannot install {a}')
                failed_installs.add((a, b))
    importlib.invalidate_caches()
    if len(failed_installs) > 0:
        print('failed:', failed_installs)
        exit()


def dl_from_link(url, file_name):
    """
    Does as name implies.
    :param url: file source
    :param file_name: where to put it, and what to name it
    :return: None
    """

    print(f'dl: {file_name}')
    with open(file_name, 'wb') as f:
        f.write(requests.get(url).content)


def get_current_version(target_program):
    """
    Will return current installed version.
    wid: check for existence, import if .py, will be treated as .txt and read if not.
    This allows the version text to be in the main file or stored elsewhere
    python file must have a global VERSION variable
    :param target_program: Name of file that contains the version
    :return: version str
    """
    if not os.path.isfile(target_program):
        return 'file does not exist'
    if target_program.__contains__('.py'):
        mod = importlib.import_module(target_program.replace('.py', ''))
        return mod.VERSION
    with open(target_program, 'r') as f:
        text = f.read()
    return text


def get_update_file(update_link, is_github, file_name) -> str:
    """
    Only used to find and get the update file.
    limitations: no '/' file names (prob not possible)
    :param update_link: link used to find update file, either a github repo or a static link
    :param is_github: An explicit way to ensure file is found correctly
    :param file_name: Used to find correct file on github and will also be the name of saved file
    :return: A base repo site if github is used for later
    """
    # if static link, then use it directly
    if not is_github:
        dl_from_link(update_link, file_name)
        return ''
    base_repo_site = 'https://github.com'

    # url correction
    if update_link.split('/')[-1] == '':
        update_link = update_link[:-1]
    fixed_link = update_link + '/latest' if update_link.split('/')[-1] == 'releases' else update_link + '/releases' + '/latest'
    print('Checking:', fixed_link)

    # go to newest release
    r = requests.get(fixed_link)
    tree = html.fromstring(r.content)
    parts = tree.xpath("//a[@class='d-flex flex-items-center min-width-0']/@href")
    if len(parts) == 0:
        # todo error handling
        print('latest release has no update file')
        exit()
    download_href = base_repo_site + '/'.join(parts[0].split('/')[:-1]) + '/'
    # print(download_href)
    dl_from_link(download_href + file_name, file_name)
    return download_href


if __name__ == '__main__':
    mandatory_modules = {'requests': 'requests', 'lxml': 'lxml'}
    ensure_minimum_imports(mandatory_modules)
    import requests
    import lxml.html as html
    print('running')
    get_update_file('https://github.com/XDEmer0r-L0rd-360-G0d-SlayerXD/Simple-Updater', True, UPDATE_FILE_NAME)
    exit()
    ensure_minimum_imports(NEEDED_IMPORTS)
    current_version = get_current_version(CHECK_FILE)
    github_dl_href = get_update_file(UPDATE_FILE_LINK, IS_GITHUB_LINK, UPDATE_FILE_NAME)
    print(current_version)

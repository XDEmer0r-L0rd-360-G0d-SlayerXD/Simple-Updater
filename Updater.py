import requests
import os
import subprocess
import lxml.html as html


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


def check_for_git_repo_update(target_program: str, repo: str):
    # the part that gets cut of in hrefs (designed for github only right now)
    base_repo_site = 'https://github.com'

    # get current program version
    if os.path.isfile(target_program):
        stream = os.popen(f'python {target_program} -version')
        current_version = stream.read().strip()
    else:
        current_version = 'something that should never be a version name'
    print('current version', current_version)

    # url correction
    fixed_link = repo if repo.split('/')[-1] == 'releases' else repo + '/releases'
    print('Checking:', fixed_link)

    # go to newest release
    r = requests.get(fixed_link)
    tree = html.fromstring(r.content)

    # trying to use the most dynamic items to zero in on newest version
    next_link = tree.xpath("//div[@class='release-entry']//div[@class='release-header']//div[@class='d-flex flex-items-start']/div/a/@href")[0]

    # tag name is version used to compare
    scanned_version = tree.xpath(f"//div[@class='d-flex flex-items-start']/div/a/text()")[0]

    # checks if update is needed
    if current_version == scanned_version:
        print('Up to date.')
        return
    print('Updating.')

    # prep links for downloading
    next_link = next_link.replace('tag', 'download')

    # download update data
    chosen_link = f'{base_repo_site}{next_link}/update.txt'
    dl_from_link(chosen_link, 'update_info_data.txt')
    run_update('update_info_data.txt', base_repo_site + next_link + '/')


def run_update(file_name, updated_repo_link):
    """
    Executes data in dict in downloaded text file
    :param file_name: name of file with update data
    :param updated_repo_link: link pointing to latest version of files
    :return: None
    """
    # read update file
    with open(f'{file_name}', 'r') as f:
        # turn file into dict, replace is used to simplify text
        instructions = eval(f.read().replace('$updated_repo$', updated_repo_link))
    """
    file contains:
    version
    dl link
    dl file name
    extra
    """
    # check version, download files, run extra code
    print(instructions['version'])
    for num_a, a in enumerate(instructions['dl links']):
        dl_from_link(a, instructions['dl names'][num_a])
    if instructions['extra'] != '':
        exec(instructions['extra'])
    os.remove(f'{file_name}')


def main():
    check_for_git_repo_update(target_check, repo_link)
    print('done')


if __name__ == '__main__':
    # will run python program.py -version, program should print(version);exit()
    target_check = 'program.py'
    # where to look for updates
    repo_link = 'https://github.com/XDEmer0r-L0rd-360-G0d-SlayerXD/Pixel_placer'
    main()

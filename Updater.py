import requests
import os
import subprocess
import lxml.html as html


def dl_from_link(url, file_name):
    print(f'dl: {file_name}')
    with open(file_name, 'wb') as f:
        f.write(requests.get(url).content)


def check_for_git_repo_update(target_program: str, repo: str):
    # designed for github only right now
    base_repo_site = 'https://github.com'
    # get current program version
    # stream = os.popen(f'python {target_program} -v')
    stream = os.popen('echo v0.0')
    current_version = stream.read()
    print('current version', current_version)
    # go to newest release
    fixed_link = repo if repo.split('/')[-1] == 'releases' else repo + '/releases'
    print('fixed', fixed_link)
    r = requests.get(fixed_link)
    tree = html.fromstring(r.content)
    tree = tree.xpath("//div[@class='release-entry']")[0]
    tree = tree.xpath("//div[@class='release-header']")[0]
    next_link = tree.xpath("//div[@class='d-flex flex-items-start']/div/a/@href")[0]
    print('next', next_link)
    scanned_version = tree.xpath(f"//div[@class='d-flex flex-items-start']/div/a/text()")[0]
    if current_version.strip() == scanned_version:
        print('up to date')
        return
    print('updating')
    # exit()
    # download update file
    # r = requests.get(base_repo_site + next_link)
    # tree = html.fromstring(r.content)
    # tree = tree.xpath('//details')
    # print(tree)
    # input('hold')
    # dl_links = tree.xpath("//a/@href")
    chosen_link = f'{base_repo_site}{next_link}/update.txt'
    # for a in dl_links:
    #     a = str(a)
    #     if a.startswith('update') and a.endswith('.txt'):
    #         chosen_link = a
    # if chosen_link == '':
    #     print('fixed_link', fixed_link)
    #     print('next_link', next_link)
    #     print('chosen_link', chosen_link)
    #     print('dl_links', dl_links)
    #     input('error.>')
    # print('chosen', chosen_link)
    dl_from_link(chosen_link.replace('tag', 'download'), 'update_info_data.txt')
    # read update file
    with open('update_info_data.txt', 'r') as f:
        instructions = eval(f.read().replace('$updated_repo$', base_repo_site + next_link.replace('tag', 'download') + '/'))
    """
    file contains:
    version
    dl link
    dl file name
    extra
    """
    if instructions['version'] != current_version:
        for num_a, a in enumerate(instructions['dl links']):
            dl_from_link(a, instructions['dl names'][num_a])
        if instructions['extra'] != '':
            exec(instructions['extra'])
    os.remove('update_info_data.txt')


def main():
    check_for_git_repo_update(target_check, repo_link)
    print('done')


if __name__ == '__main__':

    target_check = 'program.py'
    repo_link = 'https://github.com/XDEmer0r-L0rd-360-G0d-SlayerXD/Pixel_placer'
    main()

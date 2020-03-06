This is a very simple updater I made for when I give my programs to others.

How to use:
change target_check to name of a program that will return a version value and nothing after that.
repo_link is where it gets the update file from.
It should now search the github, compare the version on computer and the tag on github, and if different, download an update file.

dl_from_link(url, file_name):
	takes a link to something, and downloads the data to the file_name
check_for_git_repo_update(target_program, repo):
	Checks if update is needed, prepares for it, and runs run_update()
run_update(file_name, updated_repo_link):
	uses the update file to get needed stuff via file_name and needs updated_repo_link due to a simplification I made.


How update file works:

{
'version': 'v1.0',
'dl links': ['$updated_repo$test.txt'],
'dl names': ['test.txt'],
'extra': "print('extra test')"
}

dl links and dl names get matched up and put into dl_from_link()
$updated_repo$ is designed to make this text more readable and gets replaced with real repo link in run_update()
extra will execute extra custom code if desired at the end. Indended for things like cleanup or something simmilar.
version is unneeded due to other checks in other places.

The Idea:
compare versions between home and on git
if different, find and download the update file
use the update file to download new files, and maybe do clean up or something with 'extra'
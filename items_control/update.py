from git import Repo
import os
from items_control import settings

dir_path = os.path.dirname(os.path.realpath(__file__))
repo = Repo(dir_path + "/../")


def check_commits():
    global repo
    branch = settings.get('update_branch')
    commits_behind = list(repo.iter_commits('%s..origin/%s' % (branch, branch)))
    return commits_behind


def need_update():
    return check_commits() == 0


behind = check_commits()
print(repo)

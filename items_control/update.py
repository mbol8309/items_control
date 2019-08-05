from git import Repo
import os
from items_control import settings
import wx
from items_control.ui.dialogs import UpdateDialog
dir_path = os.path.dirname(os.path.realpath(__file__))
repo = Repo(dir_path + "/../")


def check_commits():
    branch = settings.get('update_branch')
    commits_behind = list(repo.iter_commits('%s..origin/%s' % (branch, branch)))
    return commits_behind


def update_ref(progress=None):
    origin = repo.remotes.origin
    origin.fetch(progress=progress)


def need_update():
    return len(check_commits()) > 0


def do_update(progress=None):
    branch_name = settings.get('update_branch')
    branch = repo.branches[branch_name]
    repo.git.pull(progress=progress)


def change_branch(branch_name):
    if branch_name in repo.branches:
        repo.git.checkout(branch_name)
        settings.set('update_branch', branch_name)


def check_update():
    # app = wx.App()
    # update_ref(UpdateDialog.progress)
    update_ref()
    if need_update():
        if wx.MessageBox('Hay actualizacion disponible. Actualizar?', 'Actualizar',
                         wx.OK | wx.CANCEL | wx.ICON_QUESTION) == wx.OK:
            # do_update(UpdateDialog.progress)
            do_update()
    # app.MainLoop()

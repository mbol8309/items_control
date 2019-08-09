from items_control.ui.dialogs import MainWindow
from six.moves import tkinter as tk
from items_control import update
import wx

ITEMS_CONTROL_VERSION = "0.1"


if __name__ == "__main__":
    app = wx.App()
    # try:
    #     update.check_update()
    # except:
    #     print("Exception ocurred")

    MainWindow.create()
    app.MainLoop()

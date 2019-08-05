from items_control.ui.dialogs import MainWindow
from six.moves import tkinter as tk
from items_control import update

ITEMS_CONTROL_VERSION = "0.1"


if __name__ == "__main__":
    update.check_update()

    MainWindow.create()

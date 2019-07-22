# from items_control.ui.design.ui_mainwindows import Ui_MainWindow
# from PyQt5 import QtWidgets 
from items_control.data import db
# from items_control.ui import clientedialog
# import Tkinter as tk
# import Tkinter, Tkconstants, tkFileDialog
from items_control.data import db
# from items_control.ui import *
from items_control.ui.clientedialog import ClientesDialog
import wx
from items_control import settings
import os
from items_control.ui.design_wx import items_control_wx as design_wx
from items_control.ui.procedencia_dialog import ProcedenciaDialog
from items_control.ui.items_dialog import ItemsDialog
from items_control.ui.itementry import ItemsEntryDialog


class MainWindow(design_wx.MainWindows):
    def __init__(self):
        design_wx.MainWindows.__init__(self, None)
        # wx.Frame.__init__(self, None)
        # self.setupUI()
        recent = settings.get('recents')
        if len(recent) > 0:
            for i in recent:
                if os.path.exists(i) and os.path.isfile(i):
                    item = self.recent_menu.Append(wx.ID_ANY, "Abrir...%s" % os.path.basename(i), i)
                    self.Bind(wx.EVT_MENU, lambda event: self.openRecent(event, i), item)

    def openRecent(self, e, filename):
        if os.path.exists(filename) and os.path.isfile(filename):
            db.open_db(filename)
            self._enable_menus()

    def exit_menu_click(self, event):
        self.Close()

    def open_menu_click(self, event):
        with wx.FileDialog(self, "Selecciona DB", wildcard="Sqlite files (*.sqlite)|*.sqlite",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

                # Proceed loading the file chosen by the user
            filename = fileDialog.GetPath()
            recent = settings.get('recents')
            recent.append(filename)
            recent = recent[-4:]
            settings.set('recents', recent)

            db.open_db(filename)
            self._enable_menus()

    def _enable_menus(self, enable=True):

        self.client_menu.Enable(enable)
        self.proc_menu.Enable(enable)
        self.item_menu.Enable(enable)
        self.entry_menu.Enable(enable)

    def create_menu_click(self, event):
        with wx.FileDialog(self, "Selecciona DB", wildcard="Sqlite files (*.sqlite)|*.sqlite",
                           style=wx.FD_OPEN | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

                # Proceed loading the file chosen by the user
            filename = fileDialog.GetPath()
        # filename = tkFileDialog.askopenfilename(initialdir="~", title="Select file",
        #                                         filetypes=(("Sqlite files", "*.sqlite"), ("all files", "*.*")))
        # if len(filename) > 0:
            db.create_db(filename)

    def entry_menu_click(self, event):
        ie = ItemsEntryDialog(self)
        ie.ShowModal()
        ie.Destroy()

    def client_menu_click(self, event):
        cd = ClientesDialog(self)
        cd.ShowModal()
        cd.Destroy()

    def proc_dato_click(self, event):
        pd = ProcedenciaDialog(self)
        pd.ShowModal()
        pd.Destroy()

    def items_menu_click(self, event):
        im = ItemsDialog(self)
        im.ShowModal()
        im.Destroy()


    @staticmethod
    def create():
        app = wx.App()
        main = MainWindow()
        main.Show()
        app.MainLoop()

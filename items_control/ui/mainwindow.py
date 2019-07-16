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

    # def setupUI(self):
    #     menubar = wx.MenuBar()
    #
    #     # filemenu
    #     filemenu = wx.Menu()
    #
    #     #open
    #     file_open = filemenu.Append(wx.ID_ANY, "Abrir DB","Abrir una base de Datos")
    #     self.Bind(wx.EVT_MENU, self.openDB, file_open)
    #
    #     #open recents
    #
    #
    #     #create
    #     file_create = filemenu.Append(wx.ID_ANY, "Crear DB", "Crear Base de Datos")
    #     self.Bind(wx.EVT_MENU, self.createDB, file_create)
    #
    #     #salir
    #     filemenu.AppendSeparator()
    #     file_exit_item = filemenu.Append(wx.ID_EXIT, "Salir", "Salir de aqui!!!")
    #     self.Bind(wx.EVT_MENU, self.onQuit, file_exit_item)
    #
    #
    #
    #
    #     menubar.Append(filemenu, "&Archivo")
    #
    #     configmenu = wx.Menu()
    #     configmenu_clientes = configmenu.Append(wx.ID_ANY, "Clientes", "Ver informacion de clientes")
    #     self.Bind(wx.EVT_MENU, self.openClientWindow, configmenu_clientes)
    #     menubar.Append(configmenu, "Datos")
    #
    #     self.SetMenuBar(menubar)
    #
    #     self.SetTitle("Control de Ropa")
    #     self.SetSize((500, 500))
    #     self.Centre()

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

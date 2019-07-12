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


class MainWindow(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None)
        self.setupUI()

    def setupUI(self):
        menubar = wx.MenuBar()

        # filemenu
        filemenu = wx.Menu()
        file_exit_item = filemenu.Append(wx.ID_EXIT, "Salir", "Salir de aqui!!!")
        self.Bind(wx.EVT_MENU, self.onQuit, file_exit_item)

        menubar.Append(filemenu, "&Archivo")

        configmenu = wx.Menu()
        configmenu_clientes = configmenu.Append(wx.ID_ANY, "Clientes", "Ver informacion de clientes")
        self.Bind(wx.EVT_MENU, self.openClientWindow, configmenu_clientes)
        menubar.Append(configmenu, "Datos")

        self.SetMenuBar(menubar)

        self.SetTitle("Control de Ropa")
        self.SetSize((500, 500))
        self.Centre()

    def onQuit(self, e):
        self.Close()

    def openDB(self):
        # filename = tkFileDialog.askopenfilename(initialdir="~", title="Select file",
        #                                         filetypes=(("Sqlite files", "*.sqlite"), ("all files", "*.*")))
        # if len(filename) > 0:
        #     db.open_db(filename)
        pass

    def createDB(self):
        # filename = tkFileDialog.askopenfilename(initialdir="~", title="Select file",
        #                                         filetypes=(("Sqlite files", "*.sqlite"), ("all files", "*.*")))
        # if len(filename) > 0:
        #     db.create_db(filename)
        pass

    def openClientWindow(self, e):
        cd = ClientesDialog(self)
        cd.ShowModal()
        cd.Destroy()

    def openProcWindow(self):
        pass

    def openUsuarioWindow(self):
        pass

    def openItemsWindow(self):
        pass

    @staticmethod
    def create():
        app = wx.App()
        main = MainWindow()
        main.Show()
        app.MainLoop()

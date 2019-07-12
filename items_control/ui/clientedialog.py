# from items_control.ui.design import ui_clientesdialog
# from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QHeaderView
from items_control import orm
from items_control.data import db
# import Tkinter as tk
# from items_control.ui.models import clientetablemodel
# from items_control.ui import addClientDialog
import wx


class ClientesDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        wx.Dialog.__init__(self, *args, **kw)

        self.setupUI()

    def setupUI(self):
        self.SetTitle("Clientes")

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        panel = wx.Panel(self)

        self.list = wx.ListCtrl(panel, wx.ID_ANY, style=wx.LC_REPORT)

        self.list.InsertColumn(0, 'Nombre', width=140)
        self.list.InsertColumn(1, 'Telefono', width=130)
        self.list.InsertColumn(2, 'Direccion')

        self.session = db.session()
        self.users = self.session.query(orm.Cliente).all()

        idx = 0
        for u in self.users:
            index = self.list.InsertItem(u.nombre)
            self.list.SetItem(index, 1, u.telefono)
            self.list.SetItem(index, 2, u.direccion)
            idx += 1

        hbox.Add(self.list, 1, wx.EXPAND)
        panel.SetSizer(hbox)

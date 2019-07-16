from items_control import orm
from items_control.data import db
from items_control.ui import ClientDataDialog
import wx
from items_control.ui.design_wx import items_control_wx as design_wx


class ClientesDialog(design_wx.ClientList):
    def __init__(self, parent):
        design_wx.ClientList.__init__(self, parent)
        self.parent = parent

        # self.setupUI()
        self.FillList()

    def UpdateClients(self):
        self.list.ClearAll()
        self.FillList()

    def FillList(self):
        self.list.InsertColumn(0, 'Nombre', width=140)
        self.list.InsertColumn(1, 'Telefono', width=130)
        self.list.InsertColumn(2, 'Direccion')
        self.list.InsertColumn(3, 'Tipo')

        self.session = db.session()
        self.users = self.session.query(orm.Cliente).all()

        self.rowdict = {}
        idx = 0
        for u in self.users:
            index = self.list.InsertItem(idx, u.nombre)
            self.list.SetItem(index, 1, u.telefono)
            self.list.SetItem(index, 2, u.direccion)
            self.list.SetItem(index, 3, u.tipo.name)
            self.rowdict[index] = u
            idx += 1

    def okClick(self, event):
        self.Close()

    def add_client_click(self, event):
        client = ClientDataDialog.ClientDataDialog.addClient(self)
        if client is ClientDataDialog.CLIENT_OK:
            self.UpdateClients()

    def edit_client_click(self, event):
        item = self.list.GetFirstSelected()
        if item == -1:
            return
        user = self.rowdict[item]
        results = ClientDataDialog.ClientDataDialog.addClient(self, user, self.session)
        if results is ClientDataDialog.CLIENT_OK:
            self.UpdateClients()

    def del_client_click(self, event):
        item = self.list.GetFirstSelected()
        if item == -1:
            return
        user = self.rowdict[item]

        result = wx.MessageBox("Desea eliminar al usuario: %s" % user.nombre, "Eliminar",
                               wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        if result == wx.CANCEL:
            return
        if result == wx.OK:
            self.session.delete(user)
            self.session.commit()
            self.UpdateClients()

    def showContext(self, e):
        self.PopupMenu(ClientContextMenu(self.list), e.GetPosition())

    def OnClose(self, e):
        self.Close()

# from items_control.ui.design import ui_addclient
# from PyQt5.QtWidgets import QDialog
from items_control import orm
from items_control.ui.design_wx import items_control_wx as design_wx
import wx
from items_control.data import db

# class addclientDialogController(humblewx.Controller):
#     def on_add_clicked(self,e):
#         self.view.Close()

CLIENT_OK, CLIENT_CANCEL = range(2)


class ClientDataDialog(design_wx.ClientDataDialog):

    def __init__(self, parent=None, client=None, session=None):
        design_wx.ClientDataDialog.__init__(self, parent)
        self.client = client
        self.session = session
        self.fillCombo()
        if client is not None:
            self.updateInfo()

    def updateInfo(self):
        self.name_txt.SetValue(self.client.nombre)
        self.telefono_txt.SetValue(self.client.telefono)
        self.address_txt.SetValue(self.client.direccion)
        self.tipo_cb.SetStringSelection(self.client.tipo.name)

    def fillCombo(self):
        for i in orm.TipoClienteEnum:
            self.tipo_cb.Append(i.name)
        self.tipo_cb.SetSelection(0)

    def okClick(self, event):
        client = None
        if self.client is not None:
            client = self.client
        else:
            client = orm.Cliente()
        client.nombre = self.name_txt.GetValue()
        client.telefono = self.telefono_txt.GetValue()
        client.direccion = self.address_txt.GetValue()

        # tipo
        for i in orm.TipoClienteEnum:
            if i.name == self.tipo_cb.GetStringSelection():
                client.tipo = i
                break

        # adds session to DB
        if self.client is None:
            session = db.session()
            session.add(client)
        else:
            session = self.session

        session.commit()

        self.EndModal(CLIENT_OK)
        self.Close()

    def cancelClick(self, event):
        self.EndModal(CLIENT_CANCEL)
        self.Close()

    @staticmethod
    def addClient(parent=None, client=None, session=None):
        m = ClientDataDialog(parent, client, session)
        client = m.ShowModal()
        m.Destroy()
        return client


if __name__ == "__main__":
    app = wx.App()
    dialog = ClientDataDialog(None)
    print (dialog.ShowModal())
    dialog.Destroy()

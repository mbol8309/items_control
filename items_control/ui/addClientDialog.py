from items_control.ui.design import ui_addclient
from PyQt5.QtWidgets import QDialog
from items_control import orm

class addClientDialog(QDialog, ui_addclient.Ui_addClientDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self,parent)
        self.setupUi(self)
        self.user = orm.Cliente()

        self.buttonBox.accepted.connect(self.close_dialog)
        self.buttonBox.rejected.connect(self.cancel)

        self.typeCombo.addItem(orm.TipoClienteEnum.MAYORITARIO.name)
        self.typeCombo.addItem(orm.TipoClienteEnum.MINORITARIO.name)
        # self.typeCombo.currentIndexChanged.connect(self.combochanged)

    def close_dialog(self):
        self.user.nombre = self.nombreEdit.text()
        self.user.telefono = self.phoneEdit.text()
        self.user.direccion = self.addressEdit.document().toPlainText()
        
        ct = self.typeCombo.currentText()
        for j in orm.TipoClienteEnum:
            if ct == j.name:
                self.user.tipo = j
                break
        self.close()

    def cancel(self):
        self.user = None
        self.close()




    
    @staticmethod
    def addClient(parent=None):
        m = addClientDialog(parent)
        m.exec_()
        return m.user

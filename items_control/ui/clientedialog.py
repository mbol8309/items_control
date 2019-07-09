from items_control.ui.design import ui_clientesdialog
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QHeaderView
from items_control import orm
from items_control.data import db
from items_control.ui.models import clientetablemodel 
from items_control.ui import addClientDialog


class ClientesDialog(QDialog, ui_clientesdialog.Ui_ClienteDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self,parent)
        self.setupUi(self)


        #create table view
        self.session = db.session()
        self.users = self.session.query(orm.Cliente).all()
        self.model = clientetablemodel.ClienteTableModel(self.users)

        self.clientTableView.setModel(self.model)


        self.buttonBox.accepted.connect(self.close)
        self.clientTableView.resizeColumnsToContents()
        self.addButton.clicked.connect(self.newClient)
        self.buttonBox.accepted.connect(self.close)

        # self.clientTableView.horizontalHeader.set
        # ui->tableView->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
    def accept(self):
        self.session.commit()
        self.close()

    def newClient(self):
        user = addClientDialog.addClientDialog.addClient(self)
        if user != None:
            self.session.add(user)
            self.model.updateData(self.session.query(orm.Cliente).all())
            self.session.commit()
            self.clientTableView









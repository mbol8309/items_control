from items_control.ui.design.ui_mainwindows import Ui_MainWindow
from PyQt5 import QtWidgets 
from items_control.data import db
from items_control.ui import clientedialog

class MainWindow(QtWidgets.QMainWindow,  Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        self.actionAbrir_DB.triggered.connect(self.opendb)
        self.actionNueva_DB.triggered.connect(self.createdb)
        self.actionClientes.triggered.connect(self.openClienteDialog)


    def opendb(self):
        f,_ =  QtWidgets.QFileDialog.getOpenFileName(self, "Abrir DB","~","Sqlite files(*.sqlite *.db)")
        db.open_db(f)

    def createdb(self):
        f,_ =  QtWidgets.QFileDialog.getOpenFileName(self, "Nueva DB","~","Sqlite files(*.sqlite *.db)")
        db.create_db(f)
    
    def openClienteDialog(self):
        d = clientedialog.ClientesDialog(self)
        d.show()

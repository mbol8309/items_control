from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from items_control import orm
from items_control.data import db

NAME, PHONE, ADDRESS, TYPE = range(4)

class ClienteTableModel(QAbstractTableModel):
    def __init__(self,clientedata,parent=None):
        QAbstractTableModel.__init__(self,parent)
        self.clientedata = clientedata

    def updateData(self, data):
        self.clientedata = data
        self.dataChanged()
    
    def columnCount(self,parent):
        return 4

    def rowCount(self,parent):
        return len(self.clientedata)

    def data(self,index,role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.clientedata)):
            return QVariant()

        cliente = self.clientedata[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            if column== NAME:
                return QVariant(cliente.nombre)
            if column== PHONE:
                return QVariant(cliente.telefono)
            if column== ADDRESS:
                return QVariant(cliente.direccion)
            if column== TYPE:
                return QVariant(cliente.tipo.name)

    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return QVariant(int(Qt.AlignLeft|Qt.AlignVCenter))
            return QVariant(int(Qt.AlignRight|Qt.AlignVCenter))

        if role != Qt.DisplayRole:
            return QVariant()
        if role== Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == NAME:
                    return QVariant("Nombre")
                elif section == PHONE:
                    return QVariant("Telefono")
                elif section == ADDRESS:
                    return QVariant("Direccion")
                elif section == TYPE:
                    return QVariant("Tipo")
            if orientation == Qt.Vertical:
                return QVariant(self.clientedata[section].id)

    def addUser(self, user):
        self.clientedata.append(user)
        session = db.session()
        session.add(user)
        session.commit()

    # def sortTable(self, section):
    # if section in (NAME, TIPO):
    #     self.model.sortByCountryOwner()
        
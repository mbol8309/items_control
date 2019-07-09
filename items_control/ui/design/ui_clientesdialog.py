# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'clientes.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ClienteDialog(object):
    def setupUi(self, ClienteDialog):
        ClienteDialog.setObjectName("ClienteDialog")
        ClienteDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ClienteDialog.resize(794, 528)
        ClienteDialog.setLayoutDirection(QtCore.Qt.RightToLeft)
        ClienteDialog.setAutoFillBackground(True)
        ClienteDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(ClienteDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.addButton = QtWidgets.QPushButton(ClienteDialog)
        self.addButton.setObjectName("addButton")
        self.verticalLayout_2.addWidget(self.addButton)
        self.editButton = QtWidgets.QPushButton(ClienteDialog)
        self.editButton.setObjectName("editButton")
        self.verticalLayout_2.addWidget(self.editButton)
        self.delButton = QtWidgets.QPushButton(ClienteDialog)
        self.delButton.setObjectName("delButton")
        self.verticalLayout_2.addWidget(self.delButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.clientTableView = QtWidgets.QTableView(ClienteDialog)
        self.clientTableView.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.clientTableView.setObjectName("clientTableView")
        self.horizontalLayout.addWidget(self.clientTableView)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(ClienteDialog)
        self.buttonBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ClienteDialog)
        QtCore.QMetaObject.connectSlotsByName(ClienteDialog)

    def retranslateUi(self, ClienteDialog):
        _translate = QtCore.QCoreApplication.translate
        ClienteDialog.setWindowTitle(_translate("ClienteDialog", "Clientes"))
        self.addButton.setText(_translate("ClienteDialog", "+"))
        self.editButton.setText(_translate("ClienteDialog", "edit"))
        self.delButton.setText(_translate("ClienteDialog", "-"))



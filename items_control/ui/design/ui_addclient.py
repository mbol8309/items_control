# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_cliente.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_addClientDialog(object):
    def setupUi(self, addClientDialog):
        addClientDialog.setObjectName("addClientDialog")
        addClientDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        addClientDialog.resize(581, 349)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(addClientDialog.sizePolicy().hasHeightForWidth())
        addClientDialog.setSizePolicy(sizePolicy)
        addClientDialog.setAutoFillBackground(True)
        addClientDialog.setSizeGripEnabled(False)
        addClientDialog.setModal(True)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(addClientDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(addClientDialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_2 = QtWidgets.QLabel(addClientDialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.nombreEdit = QtWidgets.QLineEdit(addClientDialog)
        self.nombreEdit.setObjectName("nombreEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.nombreEdit)
        self.phoneEdit = QtWidgets.QLineEdit(addClientDialog)
        self.phoneEdit.setObjectName("phoneEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.phoneEdit)
        self.label_3 = QtWidgets.QLabel(addClientDialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.addressEdit = QtWidgets.QPlainTextEdit(addClientDialog)
        self.addressEdit.setObjectName("addressEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.addressEdit)
        self.label_4 = QtWidgets.QLabel(addClientDialog)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.typeCombo = QtWidgets.QComboBox(addClientDialog)
        self.typeCombo.setObjectName("typeCombo")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.typeCombo)
        self.verticalLayout_2.addLayout(self.formLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(addClientDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(addClientDialog)
        self.buttonBox.accepted.connect(addClientDialog.accept)
        self.buttonBox.rejected.connect(addClientDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(addClientDialog)

    def retranslateUi(self, addClientDialog):
        _translate = QtCore.QCoreApplication.translate
        addClientDialog.setWindowTitle(_translate("addClientDialog", "Adicionar Cliente"))
        self.label.setText(_translate("addClientDialog", "Nombre"))
        self.label_2.setText(_translate("addClientDialog", "Telefono"))
        self.label_3.setText(_translate("addClientDialog", "Direccion"))
        self.label_4.setText(_translate("addClientDialog", "Tipo"))


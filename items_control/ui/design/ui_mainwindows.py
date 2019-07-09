# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './MainWindowsUI.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(767, 492)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 767, 24))
        self.menubar.setObjectName("menubar")
        self.menuPrincipal = QtWidgets.QMenu(self.menubar)
        self.menuPrincipal.setObjectName("menuPrincipal")
        self.menuDatos = QtWidgets.QMenu(self.menubar)
        self.menuDatos.setObjectName("menuDatos")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAbrir_DB = QtWidgets.QAction(MainWindow)
        self.actionAbrir_DB.setObjectName("actionAbrir_DB")
        self.actionNueva_DB = QtWidgets.QAction(MainWindow)
        self.actionNueva_DB.setObjectName("actionNueva_DB")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionClientes = QtWidgets.QAction(MainWindow)
        self.actionClientes.setObjectName("actionClientes")
        self.actionUsuarios = QtWidgets.QAction(MainWindow)
        self.actionUsuarios.setObjectName("actionUsuarios")
        self.actionProcedencia = QtWidgets.QAction(MainWindow)
        self.actionProcedencia.setObjectName("actionProcedencia")
        self.actionItems = QtWidgets.QAction(MainWindow)
        self.actionItems.setObjectName("actionItems")
        self.menuPrincipal.addAction(self.actionAbrir_DB)
        self.menuPrincipal.addAction(self.actionNueva_DB)
        self.menuPrincipal.addSeparator()
        self.menuPrincipal.addAction(self.actionExit)
        self.menuDatos.addAction(self.actionClientes)
        self.menuDatos.addAction(self.actionUsuarios)
        self.menuDatos.addAction(self.actionProcedencia)
        self.menuDatos.addAction(self.actionItems)
        self.menubar.addAction(self.menuPrincipal.menuAction())
        self.menubar.addAction(self.menuDatos.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuPrincipal.setTitle(_translate("MainWindow", "Principal"))
        self.menuDatos.setTitle(_translate("MainWindow", "Datos"))
        self.actionAbrir_DB.setText(_translate("MainWindow", "Abrir DB..."))
        self.actionNueva_DB.setText(_translate("MainWindow", "Nueva DB..."))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionClientes.setText(_translate("MainWindow", "Clientes"))
        self.actionUsuarios.setText(_translate("MainWindow", "Usuarios"))
        self.actionProcedencia.setText(_translate("MainWindow", "Procedencia"))
        self.actionItems.setText(_translate("MainWindow", "Items"))


from PyQt5 import QtWidgets
from items_control.ui.mainwindow import MainWindow
import sys



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
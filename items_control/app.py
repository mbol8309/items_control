# from PyQt5 import QtWidgets
from items_control.ui import MainWindow
from six.moves import tkinter as tk


if __name__ == "__main__":
    app = tk.Tk()
    MainWindow(app).pack(side="top", fill="both", expand=True)
    app.mainloop()

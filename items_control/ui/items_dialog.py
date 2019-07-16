from items_control.ui.design_wx import items_control_wx as design_wx
from items_control import orm
from items_control.data import db


class ItemsDialog(design_wx.ItemsDialog):
    def __init__(self, parent):
        design_wx.ItemsDialog.__init__(self, parent)

    def FillList(self):
        self.session = db.sess

    def ok_click(self, event):
        self.Close()

from items_control.ui.design_wx import items_control_wx as design_wx
from items_control import orm
from items_control.data import db
from items_control.ui.detail_dialog import DetailDialog
import wx


class ItemsDialog(design_wx.ItemsDialog):
    def __init__(self, parent):
        design_wx.ItemsDialog.__init__(self, parent)
        self.FillList()

    def UpdateList(self):
        self.item_list.ClearAll()
        self.FillList()

    def FillList(self):
        self.session = db.session()

        itemsp = self.session.query(orm.ItemPadre).all()
        self.rowdict = {}

        self.item_list.InsertColumn(0, "Nombre")
        self.item_list.InsertColumn(1, "Marca")
        self.item_list.InsertColumn(2, "Foto")

        idx = 0
        for i in itemsp:
            index = self.item_list.InsertItem(idx, i.nombre)
            self.item_list.SetItem(index, 1, i.marca)
            # self.item_list.SetItem(index, 2, i.foto)   #TODO: Put foto in listctrl
            self.rowdict[index] = i
            idx += 1

    def ok_click(self, event):
        self.Close()

    def add_click(self, event):
        idd = ItemsDataDialog(self)
        result = idd.ShowModal()
        if result == ITEM_OK:
            self.UpdateList()

    def edit_click(self, event):
        index = self.item_list.GetFirstSelected()
        if index == -1:
            return

        item = self.rowdict[index]

        idd = ItemsDataDialog(self, item, self.session)
        result = idd.ShowModal()
        if result == ITEM_OK:
            self.UpdateList()

    def del_click(self, event):
        index = self.item_list.GetFirstSelected()
        if index == -1:
            return

        item = self.rowdic[index]

        result = wx.MessageBox("Desea eliminar los articulos: %s" % item.nombre, "Eliminar",
                               wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        if result == wx.OK:
            self.session.delete(item)
            self.session.commit()
            self.UpdateList()

    def item_clicked(self, event):
        index = self.item_list.GetFirstSelected()
        if index == -1:
            return

        item = self.rowdict[index]
        DetailDialog.ItemXArt(item, self)


# ----------------------------------------------------------------------

ITEM_OK, ITEM_CANCEL = range(2)


class ItemsDataDialog(design_wx.ItemsDataDialog):
    def __init__(self, parent, item=None, session=None):
        design_wx.ItemsDataDialog.__init__(self, parent)
        self.session = session
        self.item = item

        if item is not None:
            self._fill_item()

    def _fill_item(self):
        self.name_txt.SetValue(self.item.nombre)
        self.marca_txt.SetValue(self.item.marca)
        # self.photo_txt.SetValue(self.item.photo)

    def ok_click(self, event):
        if self.item is not None:
            item = self.item
        else:
            item = orm.ItemPadre()

        item.nombre = self.name_txt.GetValue()
        item.marca = self.marca_txt.GetValue()
        # item.foto = self.photo_txt.GetValue()

        if self.session is not None:
            session = self.session
        else:
            session = db.session()
            session.add(item)

        session.commit()

        self.EndModal(ITEM_OK)
        self.Close()

    def cancel_click(self, event):
        self.EndModal(ITEM_CANCEL)
        self.Close()

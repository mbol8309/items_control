from items_control.ui.design_wx import items_control_wx as design_wx
from items_control import orm
from items_control.data import db
import wx

ITEM_PROC, ITEM_ITEM, ITEM_CANTIDAD, ITEM_MOVE_OK, ITEM_MOVE_CANCEL = range(5)


class ItemMove(design_wx.EntityMove):
    def __init__(self, item, parent):
        design_wx.EntityMove.__init__(self, parent)
        self.item = item
        self.fillItemData(self.item)
        self.return_item = None

    def cancel_button_click(self, event):
        self.EndModal(ITEM_MOVE_CANCEL)
        self.Close()

    def ok_button_click(self, event):
        if isinstance(self.item, orm.Item):
            im = orm.ItemMovido()
            im.item = self.item
            im.cantidad = self.cant_txt.GetValue()
            im.observaciones = self.observaciones_txt.GetValue()
            self.return_item = im

        if isinstance(self.item, orm.ItemMovido):
            self.item.cantidad = self.cant_txt.GetValue()
            self.item.observaciones = self.observaciones_txt.GetValue()
            self.return_item = self.item

        self.EndModal(ITEM_MOVE_OK)
        self.Close()

    def fillItemData(self, item):
        if isinstance(item, orm.Item):
            self.article_label.SetLabel(item.parent.nombre)
            self.proc_label.SetLabel(item.procedencia.nombre)
            self.cant_txt.SetValue(item.restantes)
            self.cant_txt.SetMax(item.restantes)

        if isinstance(item, orm.ItemMovido):
            self.article_label.SetLabel(item.item.parent.nombre)
            self.proc_label.SetLabel(item.item.procedencia.nombre)
            self.cant_txt.SetValue(item.cantidad)
            self.cant_txt.SetMax(item.item.restantes)
            self.observaciones_txt.SetValue(item.observaciones)

    def getReturn(self):
        return self.return_item

    @staticmethod
    def getItemMove(item, parent=None):
        """
        Get and item and return a ItemMovido
        :param item orm.Item:
        :return:
        """

        if not isinstance(item, orm.Item):
            return None

        im = ItemMove(item, parent)
        result = im.ShowModal()
        if result == ITEM_MOVE_CANCEL:
            return None
        if result == ITEM_MOVE_OK:
            item = im.getReturn()
            im.Destroy()
            return item

    @staticmethod
    def getEditItemMove(item, parent=None):

        if not isinstance(item, orm.ItemMovido):
            return None

        im = ItemMove(item, parent)
        result = im.ShowModal()

        if result == ITEM_MOVE_CANCEL:
            return None

        if result == ITEM_MOVE_OK:
            item = im.getReturn()
            im.Destroy()
            return item


class MovimientoDialog(design_wx.MovementDialog):
    def __init__(self, parent):
        design_wx.MovementDialog.__init__(self, parent)

        self.session = db.session()

        self._fill_clients()
        self._reset_tables()

        self.item_left_dict = {}
        self.item_client_take_dict = {}

        self._restart_item_left()

    def cancel_click(self, event):
        self.Close()

    def _reset_tables(self):

        lists = [self.item_left_list, self.item_client_has, self.item_client_take, self.item_dev_list]

        for l in lists:
            l.ClearAll()
            l.InsertColumn(ITEM_PROC, "Procedencia")
            l.InsertColumn(ITEM_ITEM, "Articulo")
            l.InsertColumn(ITEM_CANTIDAD, "Cantidad")

    def _restart_item_left(self):

        self.item_left_list.DeleteAllItems()
        items = self.session.query(orm.Item).all()

        idx = 0
        for i in items:
            i.custom_id = id(i)
            index = self.item_left_list.InsertItem(idx, i.procedencia.nombre)
            self.item_left_list.SetItem(index, ITEM_ITEM, i.parent.nombre)
            self.item_left_list.SetItem(index, ITEM_CANTIDAD, str(i.restantes))
            self.item_left_list.SetItemData(index, i.custom_id)
            idx += 1
            self.item_left_dict[i.custom_id] = i

    def client_cb_change(self, event):
        self.item_dev_list.DeleteAllItems()
        self.item_client_take.DeleteAllItems()

    def _fill_clients(self):
        session = self.session
        clients = session.query(orm.Cliente).all()

        self.client_cb.Clear()

        for c in clients:
            self.client_cb.Append(c.nombre)

        self.client_cb.SetSelection(0)

    def _add_item_salida(self, item):

        lista = self.item_client_take

        count = lista.GetItemCount()
        item.custom_id = id(item)
        index = lista.InsertItem(count, item.item.procedencia.nombre)
        lista.SetItem(index, ITEM_ITEM, item.item.parent.nombre)
        lista.SetItem(index, ITEM_CANTIDAD, str(item.cantidad))
        lista.SetItemData(index, item.custom_id)
        self.item_client_take_dict[item.custom_id] = item

    def salida_add_click(self, event):
        index = self.item_left_list.GetFirstSelected()
        if index == -1:
            return

        item = self.item_left_dict[self.item_left_list.GetItemData(index)]

        result = ItemMove.getItemMove(item, self)
        if result is None:
            return
        if isinstance(result, orm.ItemMovido):
            self._add_item_salida(result)

    def item_client_take_click(self, event):
        index = self.item_client_take.GetFirstSelected()
        if index == -1:
            return

        item = self.item_client_take_dict[self.item_client_take.GetItemData(index)]

        result = ItemMove.getEditItemMove(item, self)
        if result is None:
            return
        if isinstance(result, orm.ItemMovido):
            self.item_client_take.SetItem(index, ITEM_CANTIDAD, str(result.cantidad))
            self.item_client_take_dict[item.custom_id] = result

    def salida_del_click(self, event):
        index = self.item_client_take.GetFirstSelected()
        if index == -1:
            return

        item = self.item_client_take_dict[self.item_client_take.GetItemData(index)]

        del self.item_client_take_dict[item.custom_id]
        self.item_client_take.DeleteItem(index)


if __name__ == "__main__":
    app = wx.App()
    db.open_db("//home/mbolivar//Projects//items_control//items_control//data//db.sqlite")
    main = MovimientoDialog(None)

    main.Show()
    app.MainLoop()

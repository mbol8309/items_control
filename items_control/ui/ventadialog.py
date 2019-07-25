from items_control.ui.design_wx import items_control_wx as design_wx
from items_control.ui.ClientDataDialog import ClientDataDialog, CLIENT_OK
from items_control.data import db
from items_control import orm
import wx
from datetime import datetime
from items_control import utils

ITEM_OK, ITEM_CANCEL = range(2)


class VentaItemDialog(design_wx.VentaItemDialog):
    def __init__(self, item, parent=None):
        design_wx.VentaItemDialog.__init__(self, parent)
        self.item = item

        if isinstance(item, orm.Item):  # si es para crear uno nuevo sino es editar
            self.return_item = orm.Venta()
            self.return_item.item = item
            self.uni_price = item.getPrecioinDate().precio
        else:
            self.return_item = item
            self.uni_price = item.item.getPrecioinDate().precio

    def cantidad_change_value(self, event):
        value = self.cantidad_txt.GetValue()
        self.precio_txt.SetValue(value * self.uni_price)

    def getReturn(self):
        return self.return_item

    def cancel_click(self, event):
        self.EndModal(ITEM_CANCEL)
        self.Close()

    def ok_click(self, event):
        self.return_item.precio = self.precio_txt.GetValue()
        self.return_item.cantidad = self.cantidad_txt.GetValue()
        self.return_item.observaciones = self.observaciones_txt.GetValue()
        self.EndModal(ITEM_OK)
        self.Close()

    @staticmethod
    def getItemDetail(item, parent=None):
        """
        Obtiene una venta para un item
        :param item: orm.Item
        :param parent:
        :return: orm.Venta or None
        """
        if not isinstance(item, orm.Item):
            return None
        vid = VentaItemDialog(item, parent)
        vid.procedencia_label.SetLabel(item.procedencia.nombre)
        vid.item_label.SetLabel(item.parent.nombre)

        # cantidad
        if hasattr(item, "tiene"):
            vid.cantidad_txt.SetValue(item.tiene)
            vid.cantidad_txt.SetMax(item.tiene)
            vid.precio_txt.SetValue(item.getPrecioinDate().precio * item.tiene)
        else:
            vid.cantidad_txt.SetValue(item.restantes)
            vid.cantidad_txt.SetMax(item.restantes)
            vid.precio_txt.SetValue(item.getPrecioinDate().precio * item.restantes)

        # #precio
        # if hasattr(item, "tiene"):  #si lo tenia un cliente
        #     vid.precio_txt.SetValue(item.getPrecioinDate().precio) #TODO: Calcular el precio que se le dio a ese cliente
        #     # vid.cantidad_txt.SetMax(item.getPrecioinDate())
        # else:
        #     vid.precio_txt.SetValue(item.getPrecioinDate().precio)
        #     # vid.cantidad_txt.SetMax(item.getPrecioinDate())

        result = vid.ShowModal()
        if result == ITEM_CANCEL:
            return None
        if result == ITEM_OK:
            return vid.getReturn()

    @staticmethod
    def getEditItemDetail(item, parent=None):
        if not isinstance(item, orm.Venta):
            return None
        vid = VentaItemDialog(item, parent)
        vid.procedencia_label.SetLabel(item.item.procedencia.nombre)
        vid.item_label.SetLabel(item.item.parent.nombre)

        # cantidad
        if hasattr(item.item, "tiene"):
            vid.cantidad_txt.SetValue(item.cantidad)
            vid.cantidad_txt.SetMax(item.item.tiene)
        else:
            vid.cantidad_txt.SetValue(item.cantidad)
            vid.cantidad_txt.SetMax(item.item.restantes)

        # precio
        if hasattr(item.item, "tiene"):  # si lo tenia un cliente
            vid.precio_txt.SetValue(item.precio)  # TODO: Calcular el precio que se le dio a ese cliente
            # vid.cantidad_txt.SetMax(item.getPrecioinDate())
        else:
            vid.precio_txt.SetValue(item.precio)
            # vid.cantidad_txt.SetMax(item.getPrecioinDate())

        vid.observaciones_txt.SetValue(item.observaciones)

        result = vid.ShowModal()
        if result == ITEM_CANCEL:
            return None
        if result == ITEM_OK:
            return vid.getReturn()


ITEM_PROC, ITEM_NAME, ITEM_CANTIDAD, ITEM_PRICE = range(4)
TAB_TIENE, TAB_LEFT = range(2)


class VentaDialog(design_wx.VentaDialog):
    def __init__(self, parent=None):
        design_wx.VentaDialog.__init__(self, parent)

        # dict for searching
        self.client_cb_dict = {}
        self.list_client_has_dict = {}
        self.list_item_left_dict = {}
        self.list_client_paid_dict = {}

        # setup tables
        self._setup_tables()

        # populate combos and list
        self._fill_clients()
        self._fill_item_left()

    def cancel_button_click(self, event):
        self.Close()

    def _fill_clients(self):
        session = db.session()
        self.client_cb.Clear()
        clients = session.query(orm.Cliente).all()
        idx = 0
        for c in clients:
            c.custom_id = id(c)
            self.client_cb.Append(c.nombre, c.custom_id)
            # self.client_cb.SetClientData(index, c.custom_id)
            self.client_cb_dict[c.custom_id] = c

        self.client_cb.SetSelection(0)
        self._fill_client_has()

    def _setup_tables(self):

        # client has
        for list in [self.list_client_has, self.list_item_left, self.list_client_paid]:
            list.ClearAll()
            list.InsertColumn(ITEM_PROC, "Procedencia")
            list.InsertColumn(ITEM_NAME, "Nombre")
            list.InsertColumn(ITEM_CANTIDAD, "Cantidad")
            list.InsertColumn(ITEM_PRICE, "Precio")

    def _fill_client_has(self):
        client = self.client_cb_dict[self.client_cb.GetClientData(self.client_cb.GetCurrentSelection())]
        items = client.posession_items()
        self.list_client_has.DeleteAllItems()
        idx = 0
        for i in items:
            i.custom_id = id(i)
            index = self.list_client_has.InsertItem(idx, i.procedencia.nombre)
            self.list_client_has.SetItem(index, ITEM_NAME, i.parent.nombre)
            self.list_client_has.SetItem(index, ITEM_CANTIDAD, str(i.tiene))
            self.list_client_has.SetItem(index, ITEM_PRICE, str(i.getPrecioinDate().precio))
            self.list_client_has.SetItemData(index, i.custom_id)
            self.list_client_has_dict[i.custom_id] = i
            idx += 1

    def _fill_item_left(self):
        self.list_item_left.DeleteAllItems()
        session = db.session()
        items = session.query(orm.Item).filter(orm.Item.restantes > 0)

        idx = 0
        for i in items:
            i.custom_id = id(i)
            index = self.list_item_left.InsertItem(idx, i.procedencia.nombre)
            self.list_item_left.SetItem(index, ITEM_NAME, i.parent.nombre)
            self.list_item_left.SetItem(index, ITEM_CANTIDAD, str(i.restantes))
            self.list_item_left.SetItem(index, ITEM_PRICE, str(i.getPrecioinDate().precio))
            self.list_item_left.SetItemData(index, i.custom_id)
            idx += 1
            self.list_item_left_dict[i.custom_id] = i

    def client_cb_change(self, event):
        self._fill_client_has()
        self.list_client_paid_dict = {}
        self.list_client_paid.DeleteAllItems()
        self._update_total()

    def _update_total(self):
        total = 0
        for i in self.list_client_paid_dict:
            total += self.list_client_paid_dict[i].precio
        self.total_label.SetLabel("$%.2f" % total)

    def _add_client_paid(self, item):
        if not isinstance(item, orm.Venta):
            return
        count = self.list_client_paid.GetItemCount()
        item.custom_id = id(item)
        index = self.list_client_paid.InsertItem(count, item.item.procedencia.nombre)
        self.list_client_paid.SetItem(index, ITEM_NAME, item.item.parent.nombre)
        self.list_client_paid.SetItem(index, ITEM_CANTIDAD, str(item.cantidad))
        self.list_client_paid.SetItem(index, ITEM_PRICE, str(item.precio))
        self.list_client_paid.SetItemData(index, item.custom_id)
        self.list_client_paid_dict[item.custom_id] = item

        self._update_total()

    def edit_sale_click(self, event):
        index = self.list_client_paid.GetFirstSelected()
        if index == -1:
            return
        venta = self.list_client_paid_dict[self.list_client_paid.GetItemData(index)]
        result = VentaItemDialog.getEditItemDetail(venta, self)
        if result is None:
            return
        self.list_client_paid.SetItem(index, ITEM_CANTIDAD, str(result.cantidad))
        self.list_client_paid.SetItem(index, ITEM_PRICE, str(result.precio))
        self.list_client_paid_dict[result.custom_id] = result
        self._update_total()

    def add_sale_click(self, event):
        s = self.item_tabs.GetSelection()
        if s == TAB_TIENE:
            if self.list_client_has.GetFirstSelected() == -1:
                return
            item = self.list_client_has_dict[self.list_client_has.GetItemData(self.list_client_has.GetFirstSelected())]
            result = VentaItemDialog.getItemDetail(item, self)
            if result is None:
                return
            result.comes_from = TAB_TIENE
            self._add_client_paid(result)
        if s == TAB_LEFT:
            if self.list_item_left.GetFirstSelected() == -1:
                return
            item = self.list_item_left_dict[self.list_item_left.GetItemData(self.list_item_left.GetFirstSelected())]
            result = VentaItemDialog.getItemDetail(item, self)
            if result is None:
                return
            result.comes_from = TAB_LEFT
            self._add_client_paid(result)

    def ok_button_click(self, event):
        venta_directa = []
        venta_moviendo = []

        for i in self.list_client_paid_dict:
            if self.list_client_paid_dict[i].comes_from == TAB_TIENE:
                venta_directa.append(self.list_client_paid_dict[i])
            if self.list_client_paid_dict[i].comes_from == TAB_LEFT:
                venta_moviendo.append(self.list_client_paid_dict[i])

        if len(venta_directa) == 0 or len(venta_moviendo) == 0:
            return

        result = wx.MessageBox("Esta seguro que desea realizar esta venta?", "Venta",
                               wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        if result != wx.OK:
            return

        cliente_id = self.client_cb_dict[self.client_cb.GetClientData(self.client_cb.GetSelection())].id
        del self.client_cb_dict  # for session

        if len(venta_moviendo) > 0:  # si se escogio alguno que teniamos
            movimiento = orm.Movimiento()

            movimiento.cliente_id = cliente_id
            movimiento.fecha = utils._wxdate2pydate(self.date_cb.GetValue())
            movimiento.tipo = orm.TipoMovimiento.SALIDA

            for v in venta_moviendo:
                im = orm.ItemMovido()
                im.observaciones = "Movido para vender"
                im.cantidad = v.cantidad
                im.item = v.item
                movimiento.items.append(im)

            session = db.session()
            session = session.object_session(movimiento)
            session.add(movimiento)
            session.commit()

        session = db.session()

        venta_directa = venta_directa + venta_moviendo
        session = session.object_session(venta_directa[0])
        for v in venta_directa:
            v.cliente_id = cliente_id
            v.fecha = utils._wxdate2pydate(self.date_cb.GetValue())
            # session = session.object_session(v)
            # session.add(v)

        session.bulk_save_objects(venta_directa)
        session.commit()

        self.Close()

    def del_sale_click(self, event):
        index = self.list_client_paid.GetFirstSelected()
        if index == -1:
            return
        del self.list_client_paid_dict[self.list_client_paid.GetItemData(index)]
        self.list_client_paid.DeleteItem(index)
        self._update_total()

    def add_client_click(self, event):

        cdd = ClientDataDialog(self)
        result = cdd.ShowModal()
        if result == CLIENT_OK:
            self._fill_clients()
            self.client_cb.SetSelection(self.client_cb.GetCount() - 1)


if __name__ == "__main__":
    app = wx.App()
    db.open_db("//home/mbolivar//Projects//items_control//items_control//data//db.sqlite")
    main = VentaDialog(None)

    main.Show()
    app.MainLoop()

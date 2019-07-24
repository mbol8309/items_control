from items_control.ui.design_wx import items_control_wx as design_wx
from items_control import orm
from items_control.data import db
import wx
from datetime import datetime

ITEM_PROC, ITEM_ITEM, ITEM_CANTIDAD, ITEM_MOVE_OK, ITEM_MOVE_CANCEL = range(5)


class ItemMove(design_wx.EntityMove):
    def __init__(self, item, parent, dev=False):
        design_wx.EntityMove.__init__(self, parent)
        self.dev = dev
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
            if self.dev is False:
                self.cant_txt.SetValue(item.restantes)
                self.cant_txt.SetMax(item.restantes)
            else:
                self.cant_txt.SetValue(item.tiene)
                self.cant_txt.SetMax(item.tiene)

        if isinstance(item, orm.ItemMovido):
            self.article_label.SetLabel(item.item.parent.nombre)
            self.proc_label.SetLabel(item.item.procedencia.nombre)
            if self.dev is False:
                self.cant_txt.SetValue(item.cantidad)
                self.cant_txt.SetMax(item.item.restantes)
            else:
                self.cant_txt.SetValue(item.cantidad)
                self.cant_txt.SetMax(item.item.tiene)
            self.observaciones_txt.SetValue(item.observaciones)

    def getReturn(self):
        return self.return_item

    @staticmethod
    def getItemMove(item, parent=None, dev=False):

        if not isinstance(item, orm.Item):
            return None

        im = ItemMove(item, parent, dev)
        result = im.ShowModal()
        if result == ITEM_MOVE_CANCEL:
            return None
        if result == ITEM_MOVE_OK:
            item = im.getReturn()
            im.Destroy()
            return item

    @staticmethod
    def getEditItemMove(item, parent=None, dev=False):

        if not isinstance(item, orm.ItemMovido):
            return None

        im = ItemMove(item, parent, dev)
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
        # dictionaries
        self.clients_dict = {}
        self.item_client_has_dict = {}
        self.item_left_dict = {}
        self.item_client_take_dict = {}
        self.item_dev_list_dict = {}

        # self.session = db.session()

        self._reset_tables()
        self._fill_clients()

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

        session = db.getScopedSession()
        self.item_left_list.DeleteAllItems()
        items = session.query(orm.Item).all()

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
        session = db.getScopedSession()
        clients = session.query(orm.Cliente).all()

        self.client_cb.Clear()

        for c in clients:
            c.custom_id = id(c)
            index = self.client_cb.Append(c.nombre)
            self.client_cb.SetClientData(index, c.custom_id)
            self.clients_dict[c.custom_id] = c

        self.client_cb.SetSelection(0)
        self._fill_client_items_has()

    def _fill_client_items_has(self):
        client = self.clients_dict[self.client_cb.GetClientData(self.client_cb.GetCurrentSelection())]
        session = db.getScopedSession()
        client = session.query(type(client)).populate_existing().get(client.id)
        # session.query(type(some_object)).populate_existing().get(some_object.id)
        items_has = client.posession_items()

        self.item_client_has.DeleteAllItems()
        idx = 0
        for i in items_has:
            i.custom_id = id(i)
            index = self.item_client_has.InsertItem(idx, i.procedencia.nombre)
            self.item_client_has.SetItem(index, ITEM_ITEM, i.parent.nombre)
            self.item_client_has.SetItem(index, ITEM_CANTIDAD, str(i.tiene))
            self.item_client_has.SetItemData(index, i.custom_id)
            self.item_client_has_dict[i.custom_id] = i
            idx += 1

    def dev_del_click(self, event):
        index = self.item_dev_list.GetFirstSelected()
        if index == -1:
            return

        item = self.item_dev_list_dict[self.item_dev_list.GetItemData(index)]
        del self.item_dev_list_dict[item.custom_id]
        self.item_dev_list.DeleteItem(index)

    def dev_add_click(self, event):
        index = self.item_client_has.GetFirstSelected()
        if index == -1:
            return
        item = self.item_client_has_dict[self.item_client_has.GetItemData(index)]

        result = ItemMove.getItemMove(item, self, True)  # True para especificar una devolucion y poner bien el maximo
        if result is None:
            return
        if isinstance(result, orm.ItemMovido):
            self._add_item_devuelto(result)

    def _add_item_devuelto(self, item):
        count = self.item_dev_list.GetItemCount()
        item.custom_id = id(item)
        index = self.item_dev_list.InsertItem(count, item.item.procedencia.nombre)
        self.item_dev_list.SetItem(index, ITEM_ITEM, item.item.parent.nombre)
        self.item_dev_list.SetItem(index, ITEM_CANTIDAD, str(item.cantidad))
        self.item_dev_list.SetItemData(index, item.custom_id)
        self.item_dev_list_dict[item.custom_id] = item

    def item_dev_list_click(self, event):
        index = self.item_dev_list.GetFirstSelected()
        if index == -1:
            return

        item = self.item_dev_list_dict[self.item_dev_list.GetItemData(index)]

        result = ItemMove.getEditItemMove(item, self,
                                          True)  # True para especificar una devolucion y poner bien el maximo
        if result is None:
            return
        if isinstance(result, orm.ItemMovido):
            self.item_dev_list.SetItem(index, ITEM_CANTIDAD, str(result.cantidad))
            self.item_dev_list_dict[item.custom_id] = result

    def client_cb_change(self, event):
        self._fill_client_items_has()


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

    def ok_click(self, event):

        session = db.getScopedSession()
        cliente_id = self.clients_dict[self.client_cb.GetClientData(self.client_cb.GetCurrentSelection())].id

        del self.clients_dict  # for unataching
        cliente = session.query(orm.Cliente).populate_existing().get(cliente_id)
        session = session.object_session(cliente)

        result = wx.MessageBox("Realizar movimientos? Seguro?", "Movimientos", wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        if result == wx.CANCEL:
            return
        if result == wx.OK:
            if len(self.item_client_take_dict) > 0:
                m_salida = orm.Movimiento()
                m_salida.tipo = orm.TipoMovimiento.SALIDA

                for items in self.item_client_take_dict:
                    m_salida.items.append(self.item_client_take_dict[items])

                m_salida.cliente_id = cliente_id
                # m_salida.fecha = datetime.now()

                session.add(m_salida)
                session.commit()

            if len(self.item_dev_list_dict) > 0:
                m_devolucion = orm.Movimiento()
                m_devolucion.tipo = orm.TipoMovimiento.DEVOLUCION

                for items in self.item_dev_list_dict:
                    m_devolucion.items.append(self.item_dev_list_dict[items])

                m_devolucion.cliente_id = cliente_id
                # m_devolucion.fecha = datetime.now()

                session = session.object_session(m_devolucion)
                session.add(m_devolucion)
                session.commit()

            self.Close()


if __name__ == "__main__":
    app = wx.App()
    db.open_db("//home/mbolivar//Projects//items_control//items_control//data//db.sqlite")
    main = MovimientoDialog(None)

    main.Show()
    app.MainLoop()

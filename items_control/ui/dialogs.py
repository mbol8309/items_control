import wx
from items_control import settings
import os
from items_control.ui.design_wx import items_control_wx as design_wx
from items_control.ui.dialogs import *
from items_control import utils
from items_control.data import db
from items_control import orm

import datetime


class MainWindow(design_wx.MainWindows):
    def __init__(self):
        design_wx.MainWindows.__init__(self, None)
        # wx.Frame.__init__(self, None)
        # self.setupUI()
        recent = settings.get('recents')
        if len(recent) > 0:
            for i in recent:
                if os.path.exists(i) and os.path.isfile(i):
                    item = self.recent_menu.Append(wx.ID_ANY, "Abrir...%s" % os.path.basename(i), i)
                    self.Bind(wx.EVT_MENU, lambda event: self.openRecent(event, i), item)

    def openRecent(self, e, filename):
        if os.path.exists(filename) and os.path.isfile(filename):
            db.open_db(filename)
            self._enable_menus()

    def exit_menu_click(self, event):
        self.Close()

    def open_menu_click(self, event):
        with wx.FileDialog(self, "Selecciona DB", wildcard="Sqlite files (*.sqlite)|*.sqlite",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

                # Proceed loading the file chosen by the user
            filename = fileDialog.GetPath()
            recent = settings.get('recents')
            recent.append(filename)
            recent = recent[-4:]
            settings.set('recents', recent)

            db.open_db(filename)
            self._enable_menus()

    def _enable_menus(self, enable=True):

        self.client_menu.Enable(enable)
        self.proc_menu.Enable(enable)
        self.item_menu.Enable(enable)
        self.entry_menu.Enable(enable)
        self.mov_submenu.Enable(enable)
        self.venta_menu.Enable(enable)
        self.gasto_menu.Enable(enable)

    def ventamenu_click(self, event):
        venta = VentaDialog(self)
        venta.ShowModal()
        venta.Destroy()

    def create_menu_click(self, event):
        with wx.FileDialog(self, "Selecciona DB", wildcard="Sqlite files (*.sqlite)|*.sqlite",
                           style=wx.FD_OPEN | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

                # Proceed loading the file chosen by the user
            filename = fileDialog.GetPath()
            # filename = tkFileDialog.askopenfilename(initialdir="~", title="Select file",
            #                                         filetypes=(("Sqlite files", "*.sqlite"), ("all files", "*.*")))
            # if len(filename) > 0:
            db.create_db(filename)

    def entry_menu_click(self, event):
        ie = ItemsEntryDialog(self)
        ie.ShowModal()
        ie.Destroy()

    def client_menu_click(self, event):
        cd = ClientesDialog(self)
        cd.ShowModal()
        cd.Destroy()

    def proc_dato_click(self, event):
        pd = ProcedenciaDialog(self)
        pd.ShowModal()
        pd.Destroy()

    def items_menu_click(self, event):
        im = ItemsDialog(self)
        im.ShowModal()
        im.Destroy()

    def mov_menu_click(self, event):
        m = MovimientoDialog(self)
        m.ShowModal()
        m.Destroy()

    def gasto_menu_click(self, event):
        g = GastoDialog(self)
        g.ShowModal()
        g.Destroy()

    @staticmethod
    def create():
        app = wx.App()
        main = MainWindow()
        main.Show()
        app.MainLoop()


GASTO_CANTIDAD, GASTO_DESCRIPCION = range(2)


class GastoDialog(design_wx.GastoDialog):
    def __init__(self, parent):
        design_wx.GastoDialog.__init__(self, parent)
        self.procedencia_dict = {}
        self.gasto_list_dict = {}
        self._fill_procedencia()
        self._setup_gasto_table()
        self.procedencia_change(None)

    def ok_button_click(self, event):
        self.Close()

    def _setup_gasto_table(self):
        self.gasto_list.InsertColumn(GASTO_CANTIDAD, "Cantidad")
        self.gasto_list.InsertColumn(GASTO_DESCRIPCION, "Descripcion")

    def _fill_procedencia(self):
        session = db.session()
        procedencias = session.query(orm.Procedencia).all()
        for p in procedencias:
            p.custom_id = id(p)
            index = self.procedencia_txt.Append(p.nombre)
            self.procedencia_txt.SetClientData(index, p.custom_id)
            self.procedencia_dict[p.custom_id] = p
        self.procedencia_txt.SetSelection(0)

    def procedencia_change(self, event):
        procedencia = self.procedencia_dict[self.procedencia_txt.GetClientData(self.procedencia_txt.GetSelection())]

        session = db.session()
        gastos = session.query(orm.Gasto).filter(orm.Gasto.procedencia == procedencia).all()
        idx = 0
        self.gasto_list.DeleteAllItems()
        for g in gastos:
            g.custom_id = id(g)
            index = self.gasto_list.InsertItem(idx, str(g.cantidad))
            self.gasto_list.SetItem(index, GASTO_DESCRIPCION, g.descripcion)
            self.gasto_list.SetItemData(index, g.custom_id)
            self.gasto_list_dict[g.custom_id] = g
            idx += 1

    def del_button_click(self, event):
        index = self.gasto_list.GetFirstSelected()
        if index == -1:
            return

        if wx.MessageBox("Esta seguro que desea eliminarlo", "Eliminar", wx.OK | wx.CANCEL | wx.ICON_QUESTION) == wx.OK:
            gasto = self.gasto_list_dict[self.gasto_list.GetItemData(index)]
            session = db.session().object_session(gasto)
            del (self.gasto_list_dict[gasto.custom_id])
            session.delete(gasto)
            self.gasto_list.DeleteItem(index)
            session.commit()

    def add_button_click(self, event):
        if self.cantidad_txt.GetValue() > 0 and len(self.descripcion_txt.GetValue()) > 0 and \
                wx.MessageBox("Agregar gasto?", "Agregar", wx.OK | wx.CANCEL | wx.ICON_QUESTION) == wx.OK:
            gasto = orm.Gasto()
            gasto.cantidad = self.cantidad_txt.GetValue()
            gasto.descripcion = self.descripcion_txt.GetValue()
            gasto.procedencia_id = self.procedencia_dict[
                self.procedencia_txt.GetClientData(self.procedencia_txt.GetSelection())].id
            session = db.session()
            session.add(gasto)
            session.commit()
            self.procedencia_change(None)


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
        if hasattr(item, "tiene"):  # TODO:calcular al precio que se le dio
            vid.cantidad_txt.SetValue(item.tiene)
            vid.cantidad_txt.SetMax(item.tiene)
            vid.precio_txt.SetValue(item.getPrecioinDate().precio * item.tiene)
        else:
            vid.cantidad_txt.SetValue(item.restantes)
            vid.cantidad_txt.SetMax(item.restantes)
            vid.precio_txt.SetValue(item.getPrecioinDate().precio * item.restantes)

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
        session = db.session()

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


CLIENT_OK, CLIENT_CANCEL = range(2)


class ClientDataDialog(design_wx.ClientDataDialog):

    def __init__(self, parent=None, client=None, session=None):
        design_wx.ClientDataDialog.__init__(self, parent)
        self.client = client
        self.session = session
        self.fillCombo()
        if client is not None:
            self.updateInfo()

    def updateInfo(self):
        self.name_txt.SetValue(self.client.nombre)
        self.telefono_txt.SetValue(self.client.telefono)
        self.address_txt.SetValue(self.client.direccion)
        self.tipo_cb.SetStringSelection(self.client.tipo.name)

    def fillCombo(self):
        for i in orm.TipoClienteEnum:
            self.tipo_cb.Append(i.name)
        self.tipo_cb.SetSelection(0)

    def okClick(self, event):
        client = None
        if self.client is not None:
            client = self.client
        else:
            client = orm.Cliente()
        client.nombre = self.name_txt.GetValue()
        client.telefono = self.telefono_txt.GetValue()
        client.direccion = self.address_txt.GetValue()

        # tipo
        for i in orm.TipoClienteEnum:
            if i.name == self.tipo_cb.GetStringSelection():
                client.tipo = i
                break

        # adds session to DB
        if self.client is None:
            session = db.session()
            session.add(client)
        else:
            session = self.session

        session.commit()

        self.EndModal(CLIENT_OK)
        self.Close()

    def cancelClick(self, event):
        self.EndModal(CLIENT_CANCEL)
        self.Close()

    @staticmethod
    def addClient(parent=None, client=None, session=None):
        m = ClientDataDialog(parent, client, session)
        client = m.ShowModal()
        m.Destroy()
        return client


class ClientesDialog(design_wx.ClientList):
    def __init__(self, parent):
        design_wx.ClientList.__init__(self, parent)
        self.parent = parent

        # self.setupUI()
        self.FillList()

    def UpdateClients(self):
        self.list.ClearAll()
        self.FillList()

    def FillList(self):
        self.list.InsertColumn(0, 'Nombre', width=140)
        self.list.InsertColumn(1, 'Telefono', width=130)
        self.list.InsertColumn(2, 'Direccion')
        self.list.InsertColumn(3, 'Tipo')

        self.session = db.session()
        self.users = self.session.query(orm.Cliente).all()

        self.rowdict = {}
        idx = 0
        for u in self.users:
            index = self.list.InsertItem(idx, u.nombre)
            self.list.SetItem(index, 1, u.telefono)
            self.list.SetItem(index, 2, u.direccion)
            self.list.SetItem(index, 3, u.tipo.name)
            self.rowdict[index] = u
            idx += 1

    def okClick(self, event):
        self.Close()

    def add_client_click(self, event):
        client = ClientDataDialog.ClientDataDialog.addClient(self)
        if client is ClientDataDialog.CLIENT_OK:
            self.UpdateClients()

    def edit_client_click(self, event):
        item = self.list.GetFirstSelected()
        if item == -1:
            return
        user = self.rowdict[item]
        results = ClientDataDialog.ClientDataDialog.addClient(self, user, self.session)
        if results is ClientDataDialog.CLIENT_OK:
            self.UpdateClients()

    def del_client_click(self, event):
        item = self.list.GetFirstSelected()
        if item == -1:
            return
        user = self.rowdict[item]

        result = wx.MessageBox("Desea eliminar al usuario: %s" % user.nombre, "Eliminar",
                               wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        if result == wx.CANCEL:
            return
        if result == wx.OK:
            self.session.delete(user)
            self.session.commit()
            self.UpdateClients()

    # def showContext(self, e):
    #     self.PopupMenu(ClientContextMenu(self.list), e.GetPosition())

    def OnClose(self, e):
        self.Close()


class DetailDialog(design_wx.DetailDialog):
    def __init__(self, parent=None):
        design_wx.DetailDialog.__init__(self, parent)
        self.parent = parent

    def ok_button_click(self, event):
        self.Close()

    def item_activated_itemxart(self, event):
        index = self.item_list.GetFirstSelected()
        if index == -1:
            return
        item = self.itemdict[index]

        DetailDialog.ItemDetail(item, self)

    def item_activated(self, event):
        if self.redirect_click is not None:
            self.redirect_click(event)

    @staticmethod
    def ItemDetail(item, parent):
        if not isinstance(item, orm.Item):
            return None

        d = DetailDialog(parent)
        d.SetTitle("Detalles de articulos")
        d.item_label.SetLabel(
            "Articulo: %s [%s] de [%s]" % (item.parent.nombre, item.parent.marca, item.procedencia.nombre))

        d.item_list.InsertColumn(0, "Fecha inicio")
        d.item_list.InsertColumn(1, "Fecha fin")
        d.item_list.InsertColumn(2, "Fecha precio")

        idx = 0
        d.itemdict = {}
        for p in item.precio:
            index = d.item_list.InsertItem(idx, str(p.fecha_inicio))
            d.item_list.SetItem(index, 1, str(p.fecha_final))
            d.item_list.SetItem(index, 2, str(p.precio))
            idx += 1
            d.itemdict[index] = p

        d.ShowModal()
        d.Destroy()

    @staticmethod
    def ItemXArt(item, parent=None):
        if not isinstance(item, orm.ItemPadre):
            return None

        d = DetailDialog(parent)
        d.SetTitle("Items X Articulos")
        d.item_label.SetLabel("Articulo: %s [%s]" % (item.nombre, item.marca))

        d.item_list.InsertColumn(0, "Procedencia")
        d.item_list.InsertColumn(1, "Cantidad")
        d.item_list.InsertColumn(2, "Ultimo Precio")
        d.item_list.InsertColumn(3, "Costo")
        d.item_list.InsertColumn(4, "Restantes")
        d.item_list.InsertColumn(5, "Por pagar")
        d.item_list.InsertColumn(6, "Vendidos")

        d.idx = 0
        d.itemdict = {}
        for i in item.items:
            index = d.item_list.InsertItem(d.idx, i.procedencia.nombre)
            d.item_list.SetItem(index, 1, str(i.cantidad))
            d.item_list.SetItem(index, 2, str(i.precio[-1].precio))
            d.item_list.SetItem(index, 3, str(i.costo))
            d.item_list.SetItem(index, 4, str(i.restantes))
            d.item_list.SetItem(index, 5, str(i.salidas - i.vendidos - i.devoluciones))
            d.item_list.SetItem(index, 6, str(i.vendidos))
            d.idx += 1
            d.itemdict[index] = i

        d.redirect_click = d.item_activated_itemxart

        d.ShowModal()
        d.Destroy()


C_PROC, C_ITEM, C_CANT, C_COST, C_PRECIO = range(5)


# class ItemsEntryListItem(wx.ListItem):
#     def __init__(self, parent=None):


class ItemsEntryDialog(design_wx.ItemEntryDialog):
    def __init__(self, parent):
        design_wx.ItemEntryDialog.__init__(self, parent)
        self.session = db.session()
        self.procedencias = None
        self.itemsp = None

        self._fill_items()
        self._fill_proc()
        self._config_table()
        self.entry_items_dict = {}

    def _config_table(self):
        self.item_list.InsertColumn(C_PROC, "Procedencia")
        self.item_list.InsertColumn(C_ITEM, "Item")
        self.item_list.InsertColumn(C_CANT, "Cantidad")
        self.item_list.InsertColumn(C_COST, "Costo")
        self.item_list.InsertColumn(C_PRECIO, "Precio")

    def _get_selected_item(self):
        index = self.item_choice.GetSelection()
        if index == -1:
            return None
        return self.itemdict[index]

    def _get_selected_proc(self):
        index = self.proc_choice.GetSelection()
        if index == -1:
            return None
        return self.proc_dict[index]

    def _fill_proc(self):
        self.proc_choice.Clear()
        self.procedencias = self.session.query(orm.Procedencia).all()
        self.proc_choice.Clear()
        self.proc_dict = {}
        for p in self.procedencias:
            index = self.proc_choice.Append(p.nombre)
            self.proc_dict[index] = p
        self.proc_choice.SetSelection(0)

    def _fill_items(self):
        self.item_choice.Clear()
        self.itemsp = self.session.query(orm.ItemPadre).all()
        self.item_choice.Clear()
        self.itemdict = {}
        for i in self.itemsp:
            index = self.item_choice.Append("%s [%s]" % (i.nombre, i.marca))
            self.itemdict[index] = i
        self.item_choice.SetSelection(0)

    def _reset_values(self):
        self.cost_txt.SetValue(0)
        self.price_txt.SetValue(0)
        self.cantidad_txt.SetValue(0)

    def _insert_item(self, item):

        count = self.item_list.GetItemCount()
        item.custom_id = id(item)
        index = self.item_list.InsertItem(count, item.procedencia.nombre)
        self.item_list.SetItem(index, C_ITEM, item.parent.nombre)
        self.item_list.SetItem(index, C_CANT, str(item.cantidad))
        self.item_list.SetItem(index, C_COST, str(item.costo))
        self.item_list.SetItem(index, C_PRECIO, str(item.precio[-1].precio))
        self.item_list.SetItemData(index, item.custom_id)
        self.entry_items_dict[item.custom_id] = item

    def add_click(self, event):
        for i in [self.cantidad_txt, self.cost_txt, self.price_txt]:
            value = i.GetValue()
            if value == '' or value == None or value == 0 or value == "0":
                wx.MessageBox("Debe llenar los datos!!", "Datos", wx.OK | wx.ICON_EXCLAMATION)
                return

        newitem = orm.Item()
        newitem.parent = self._get_selected_item()
        newitem.procedencia = self._get_selected_proc()
        newitem.cantidad = self.cantidad_txt.GetValue()
        newitem.costo = self.cost_txt.GetValue()
        precio_t = self.price_txt.GetValue()

        newitem.precio.append(orm.PrecioVenta.newPrecio(precio_t))

        self._insert_item(newitem)
        self._reset_values()

    def add_item_button_click(self, event):
        idd = ItemsDataDialog(self)
        result = idd.ShowModal()
        if result == ITEM_OK:
            self._fill_items()
            self.item_choice.SetSelection(self.item_choice.GetCount() - 1)

    def add_proc_button_click(self, event):
        pdd = ProcedenciaDataDialog(self)
        result = pdd.ShowModal()
        if result == PROCEDENCIA_OK:
            self._fill_proc()
            self.proc_choice.SetSelection(self.proc_choice.GetCount() - 1)

    def cancel_click(self, event):
        self.Close()

    def eliminar_click(self, event):
        index = self.item_list.GetFirstSelected()
        if index == -1:
            return

        data = self.item_list.GetItemData(index)
        del (self.entry_items_dict[data])

        self.item_list.DeleteItem(index)

    def ok_click(self, event):
        for i in self.entry_items_dict:
            self.session.add(self.entry_items_dict[i])
        self.session.commit()
        self.Close()


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


import wx

PROCEDENCIA_OK, PROCEDENCIA_CANCEL = range(2)


class ProcedenciaDialog(design_wx.ProcDialog):
    def __init__(self, parent=None):
        design_wx.ProcDialog.__init__(self, parent)

        self.FillList()

    def UpdateList(self):
        self.proc_list.ClearAll()
        self.FillList()

    def FillList(self):

        self.session = db.session()
        procedencias = self.session.query(orm.Procedencia).all()
        self.proc_list.InsertColumn(0, "Nombre")
        self.proc_list.InsertColumn(1, "Fecha")
        self.proc_list.InsertColumn(2, "Detalle")

        self.rowdict = {}
        idx = 0
        for p in procedencias:
            if p.detalle is None:
                p.detalle = ""
            index = self.proc_list.InsertItem(idx, p.nombre)
            self.proc_list.SetItem(index, 1, datetime.datetime.strftime(p.fecha, '%d//%m//%y'))
            self.proc_list.SetItem(index, 2, p.detalle)
            self.rowdict[index] = p
            idx += 1

    def add_click(self, event):
        pd = ProcedenciaDataDialog(self, None, self.session)
        result = pd.ShowModal()
        if result == PROCEDENCIA_OK:
            self.UpdateList()

    def edit_click(self, event):
        index = self.proc_list.GetFirstSelected()
        if index == -1:
            return
        procedencia = self.rowdict[index]

        pd = ProcedenciaDataDialog(self, procedencia, self.session)
        result = pd.ShowModal()
        if result == PROCEDENCIA_OK:
            self.UpdateList()

    def ok_click(self, event):
        self.Close()

    def del_click(self, event):
        index = self.proc_list.GetFirstSelected()
        if index == -1:
            return
        proc = self.rowdict[index]

        result = wx.MessageBox("Desea borrar la procedencia: %s" % proc.nombre, "Eliminar",
                               wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        if result == wx.CANCEL:
            return
        if result == wx.OK:
            self.session.delete(proc)
            self.session.commit()
            self.UpdateList()


class ProcedenciaDataDialog(design_wx.ProcDatosDialog):
    def __init__(self, parent=None, procedencia=None, session=None):
        design_wx.ProcDatosDialog.__init__(self, parent)
        self.procedencia = procedencia
        self.session = session
        if procedencia is not None:
            self.FillUserData()

    def FillUserData(self):
        self.name_txt.SetValue(self.procedencia.nombre)
        self.date_txt.SetValue(utils._pydate2wxdate(self.procedencia.fecha))
        self.detalle_txt.SetValue(self.procedencia.detalle)

    def cancel_click(self, event):
        self.EndModal(PROCEDENCIA_CANCEL)
        self.Close()

    def ok_click(self, event):
        if self.procedencia is None:
            procedencia = orm.Procedencia()
        else:
            procedencia = self.procedencia

        session = db.session()

        # data
        procedencia.nombre = self.name_txt.GetValue()

        procedencia.fecha = utils._wxdate2pydate(self.date_txt.GetValue())
        procedencia.detalle = self.detalle_txt.GetValue()

        if self.procedencia is None:
            session.add(procedencia)
            session.commit()
        else:
            self.session.commit()

        self.EndModal(PROCEDENCIA_OK)
        self.Close()


ITEM_PROC, ITEM_ITEM, ITEM_CANTIDAD, ITEM_PRECIO, ITEM_MOVE_OK, ITEM_MOVE_CANCEL = range(6)


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

        lists_price = [self.item_left_list, self.item_client_take]
        lists = [self.item_client_has, self.item_dev_list]

        for l in lists:
            l.ClearAll()
            l.InsertColumn(ITEM_PROC, "Procedencia")
            l.InsertColumn(ITEM_ITEM, "Articulo")
            l.InsertColumn(ITEM_CANTIDAD, "Cantidad")

        for l in lists_price:
            l.ClearAll()
            l.InsertColumn(ITEM_PROC, "Procedencia")
            l.InsertColumn(ITEM_ITEM, "Articulo")
            l.InsertColumn(ITEM_CANTIDAD, "Cantidad")
            l.InsertColumn(ITEM_PRECIO, "Precio")

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
            self.item_left_list.SetItem(index, ITEM_PRECIO, str(i.precio[-1].precio))
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
        lista.SetItem(index, ITEM_PRECIO, str(item.item.precio[-1].precio))
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

        session = db.session()
        cliente_id = self.clients_dict[self.client_cb.GetClientData(self.client_cb.GetCurrentSelection())].id

        del self.clients_dict  # for unataching
        # cliente = session.query(orm.Cliente).populate_existing().get(cliente_id)
        # session = session.object_session(cliente)

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
                session = session.object_session(m_salida)
                session.add(m_salida)
                session.commit()

            if len(self.item_dev_list_dict) > 0:
                m_devolucion = orm.Movimiento()
                m_devolucion.tipo = orm.TipoMovimiento.DEVOLUCION

                for items in self.item_dev_list_dict:
                    m_devolucion.items.append(self.item_dev_list_dict[items])

                m_devolucion.cliente_id = cliente_id
                # m_devolucion.fecha = datetime.now()

                # session = db.session()
                session = session.object_session(m_devolucion)
                session.add(m_devolucion)
                session.commit()

            self.Close()

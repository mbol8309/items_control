import wx
from items_control import settings
import os
# from items_control.ui.design_wx import  items_control_wx as design_wx
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
        self.client_mov_venta.Enable(enable)
        self.procedencia_status_menu.Enable(enable)
        self.item_tracker_menu.Enable(enable)

    def item_tracker_click(self, event):
        it = ItemTrackerDialog(self)
        it.ShowModal()
        it.Destroy()

    def procedencia_status_click(self, event):
        p = ProcedenciaStatus(self)
        p.ShowModal()
        p.Destroy()

    def cliente_mov_venta_click(self, event):
        cmv = ClienteMovVenta(self)
        cmv.ShowModal()
        cmv.Destroy()

    def ventamenu_click(self, event):
        venta = VentaDialog(self)
        venta.ShowModal()
        venta.Destroy()

    def create_menu_click(self, event):
        with wx.FileDialog(self, "Selecciona DB", wildcard="Sqlite files (*.sqlite)|*.sqlite",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

                # Proceed loading the file chosen by the user
            filename = fileDialog.GetPath()
            # filename = tkFileDialog.askopenfilename(initialdir="~", title="Select file",
            #                                         filetypes=(("Sqlite files", "*.sqlite"), ("all files", "*.*")))
            # if len(filename) > 0:
            db.create_db(filename)
            self._enable_menus()

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
        # app = wx.App()
        main = MainWindow()
        main.Show()
        # app.MainLoop()


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

TAB_TIENE, TAB_LEFT = range(2)


class VentaDialog(design_wx.VentaDialog):
    def __init__(self, parent=None):
        design_wx.VentaDialog.__init__(self, parent)

        self.session = db.getScopedSession()
        # setup tables
        self._setup_tables_combo()

        # populate combos and list
        self._fill_clients()
        self._fill_item_left()

    def cancel_button_click(self, event):
        self.Close()

    def _fill_clients(self):
        session = self.session
        clients = session.query(orm.Cliente).all()
        self.client_cb.UpdateData(clients)
        self._fill_client_has()

    def _setup_tables_combo(self):

        # client has
        for list in [self.list_client_has, self.list_item_left, self.list_client_paid]:
            list.ConfigColumns(["Procedencia", "Nombre", "Cantidad", "Precio"])

        # combo config
        self.client_cb.SetLambda(lambda c: c.nombre)

        # list item client has
        self.list_client_has.SetLambdas([
            lambda i: i.procedencia.nombre,
            lambda i: i.parent.nombre,
            lambda i: str(i.tiene),
            lambda i: str(i.getPrecioinDate().precio)
        ])

        # list item left
        self.list_item_left.SetLambdas([
            lambda i: i.procedencia.nombre,
            lambda i: i.parent.nombre,
            lambda i: str(i.restantes),
            lambda i: str(i.getPrecioinDate().precio)
        ])

        # list client paid
        self.list_client_paid.SetLambdas([
            lambda i: i.item.procedencia.nombre,
            lambda i: i.item.parent.nombre,
            lambda i: str(i.cantidad),
            lambda i: str(i.precio)
        ])


    def _fill_client_has(self):
        client = self.client_cb.GetActiveItem()
        items = client.posession_items()

        self.list_client_has.UpdateData(items)

    def _fill_item_left(self):
        session = self.session
        items = session.query(orm.Item).filter(orm.Item.restantes > 0)
        self.list_item_left.UpdateData(items)


    def client_cb_change(self, event):
        self._fill_client_has()
        self.list_client_paid.DeleteAllItems()
        self._update_total()

    def _update_total(self):
        total = 0
        for i in self.list_client_paid.GetItems():
            total += i.precio
        self.total_label.SetLabel("$%.2f" % total)

    def _add_client_paid(self, item):
        if not isinstance(item, orm.Venta):
            return
        self.list_client_paid.AppendData(item)

        self._update_total()

    def edit_sale_click(self, event):
        index = self.list_client_paid.GetFirstSelected()
        if index == -1:
            return
        venta = self.list_client_paid.GetItem(index)
        result = VentaItemDialog.getEditItemDetail(venta, self)
        if result is None:
            return
        self.list_client_paid.UpdateItem(index, result)
        self._update_total()

    def add_sale_click(self, event):
        s = self.item_tabs.GetSelection()
        if s == TAB_TIENE:
            if self.list_client_has.GetFirstSelected() == -1:
                return
            item = self.list_client_has.GetItem(self.list_client_has.GetFirstSelected())
            result = VentaItemDialog.getItemDetail(item, self)
            if result is None:
                return
            result.comes_from = TAB_TIENE
            self._add_client_paid(result)
        if s == TAB_LEFT:
            if self.list_item_left.GetFirstSelected() == -1:
                return
            item = self.list_item_left.GetItem(self.list_item_left.GetFirstSelected())
            result = VentaItemDialog.getItemDetail(item, self)
            if result is None:
                return
            result.comes_from = TAB_LEFT
            self._add_client_paid(result)

    def ok_button_click(self, event):
        venta_directa = []
        venta_moviendo = []
        session = self.session

        for i in self.list_client_paid.GetItems():
            if i.comes_from == TAB_TIENE:
                venta_directa.append(i)
            if i.comes_from == TAB_LEFT:
                venta_moviendo.append(i)

        if len(venta_directa) == 0 and len(venta_moviendo) == 0:
            return

        result = wx.MessageBox("Esta seguro que desea realizar esta venta?", "Venta",
                               wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        if result != wx.OK:
            return

        cliente = self.client_cb.GetActiveItem()
        # del self.client_cb_dict  # for session

        if len(venta_moviendo) > 0:  # si se escogio alguno que teniamos
            movimiento = orm.Movimiento()

            movimiento.cliente = cliente
            movimiento.fecha = utils._wxdate2pydate(self.date_cb.GetValue())
            movimiento.tipo = orm.TipoMovimiento.SALIDA

            for v in venta_moviendo:
                im = orm.ItemMovido()
                im.observaciones = "Movido para vender"
                im.cantidad = v.cantidad
                im.item = v.item
                movimiento.items.append(im)

            # session = session.object_session(movimiento)
            session.add(movimiento)
            session.commit()


        venta_directa = venta_directa + venta_moviendo
        for v in venta_directa:
            v.cliente = cliente
            v.fecha = utils._wxdate2pydate(self.date_cb.GetValue())

        session.bulk_save_objects(venta_directa)
        session.commit()

        self.Close()

    def del_sale_click(self, event):
        index = self.list_client_paid.GetFirstSelected()
        if index == -1:
            return
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
        client = ClientDataDialog.addClient(self)
        if client is CLIENT_OK:
            self.UpdateClients()

    def edit_client_click(self, event):
        item = self.list.GetFirstSelected()
        if item == -1:
            return
        user = self.rowdict[item]
        results = ClientDataDialog.addClient(self, user, self.session)
        if results is CLIENT_OK:
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


class ItemsEntryDialog(design_wx.ItemEntryDialog):
    def __init__(self, parent):
        design_wx.ItemEntryDialog.__init__(self, parent)
        self.session = db.getScopedSession()

        self._config_control()
        self._fill_items()
        self._fill_proc()
        self.entry_items_dict = {}

    def _config_control(self):
        self.item_list.ConfigColumns(["Procedencia", "Item", "Cantidad", "Costo", "Precio"])
        self.item_list.SetLambdas([
            lambda i: i.procedencia.nombre,
            lambda i: i.parent.nombre,
            lambda i: str(i.cantidad),
            lambda i: "$ %.2f" % i.costo,
            lambda i: "$ %.2f" % i.getPrecioinDate().precio
        ])
        self.proc_choice.SetLambda(lambda p: p.nombre)
        self.item_choice.SetLambda(lambda i: "%s [%s]" % (i.nombre, i.marca))

    # def _get_selected_item(self):
    #     index = self.item_choice.GetSelection()
    #     if index == -1:
    #         return None
    #     return self.itemdict[index]
    #
    # def _get_selected_proc(self):
    #     index = self.proc_choice.GetSelection()
    #     if index == -1:
    #         return None
    #     return self.proc_dict[index]

    def _fill_proc(self):
        session = self.session  # db.getScopedSession()
        procedencias = session.query(orm.Procedencia).all()
        self.proc_choice.UpdateData(procedencias)


    def _fill_items(self):
        session = self.session  # db.getScopedSession()
        itemsp = session.query(orm.ItemPadre).all()
        self.item_choice.UpdateData(itemsp)

    def _reset_values(self):
        self.cost_txt.SetValue(0)
        self.price_txt.SetValue(0)
        self.cantidad_txt.SetValue(0)

    # def _insert_item(self, item):
    #
    #     self.item_list.AppendData(item)

    # count = self.item_list.GetItemCount()
    # item.custom_id = id(item)
    # index = self.item_list.InsertItem(count, item.procedencia.nombre)
    # self.item_list.SetItem(index, C_ITEM, item.parent.nombre)
    # self.item_list.SetItem(index, C_CANT, str(item.cantidad))
    # self.item_list.SetItem(index, C_COST, str(item.costo))
    # self.item_list.SetItem(index, C_PRECIO, str(item.precio[-1].precio))
    # self.item_list.SetItemData(index, item.custom_id)
    # self.entry_items_dict[item.custom_id] = item

    def add_click(self, event):
        for i in [self.cantidad_txt, self.cost_txt, self.price_txt]:
            value = i.GetValue()
            if value == '' or value == None or value == 0 or value == "0":
                wx.MessageBox("Debe llenar los datos!!", "Datos", wx.OK | wx.ICON_EXCLAMATION)
                return

        session = self.session  # db.getScopedSession()
        newitem = orm.Item()

        newitem.parent = session.query(orm.ItemPadre).filter(
            orm.ItemPadre.id == self.item_choice.GetActiveItem().id).one()
        newitem.procedencia = session.query(orm.Procedencia).filter(
            orm.Procedencia.id == self.proc_choice.GetActiveItem().id).one()
        newitem.cantidad = self.cantidad_txt.GetValue()
        newitem.costo = self.cost_txt.GetValue()
        precio_t = self.price_txt.GetValue()

        newitem.addPrecio(precio_t)

        self.item_list.AppendData(newitem)
        self._reset_values()

    def add_item_button_click(self, event):
        idd = ItemsDataDialog(self, session=self.session)
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

        session = self.session  # db.getScopedSession()
        items = self.item_list.GetItems()
        for i in items:
            # session = session.object_session(i)
            session.add(i)
            # session.commit()
        # session.bulk_save_objects(items)
        session.commit()
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

        session = self.session  # db.session()
        if self.item is None:
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
        # self.session = session
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

        self.session = db.getScopedSession()

        self._setup_controls()
        self._fill_clients()

        self._restart_item_left()

    def cancel_click(self, event):
        self.Close()

    def _setup_controls(self):
        lists_price = [self.item_left_list, self.item_client_take]
        lists = [self.item_client_has, self.item_dev_list]

        for l in lists:
            l.ConfigColumns(['Procedencia', 'Articulo', 'Cantidad'])

        for l in lists_price:
            l.ConfigColumns(['Procedencia', 'Articulo', 'Cantidad', 'Precio'])

        self.item_left_list.SetLambdas([
            lambda i: i.procedencia.nombre,
            lambda i: i.parent.nombre,
            lambda i: str(i.restantes),
            lambda i: str(i.getPrecioinDate().precio)
        ])
        self.item_client_take.SetLambdas([
            lambda i: i.item.procedencia.nombre,
            lambda i: i.item.parent.nombre,
            lambda i: str(i.cantidad),
            lambda i: str(i.item.getPrecioinDate().precio)
        ])
        self.item_client_has.SetLambdas([
            lambda i: i.procedencia.nombre,
            lambda i: i.parent.nombre,
            lambda i: str(i.tiene)
        ])
        self.item_dev_list.SetLambdas([
            lambda i: i.item.procedencia.nombre,
            lambda i: i.item.parent.nombre,
            lambda i: str(i.cantidad)
        ])

        self.client_cb.SetLambda(lambda c: c.nombre)

    def _restart_item_left(self):

        session = self.session
        items = session.query(orm.Item).all()
        self.item_left_list.UpdateData(items)

    def client_cb_change(self, event):
        self.item_dev_list.DeleteAllItems()
        self.item_client_take.DeleteAllItems()

    def _fill_clients(self):
        session = self.session
        clients = session.query(orm.Cliente).all()

        self.client_cb.UpdateData(clients)
        self._fill_client_items_has()

    def _fill_client_items_has(self):
        client = self.client_cb.GetActiveItem()
        session = self.session
        items_has = client.posession_items()
        self.item_client_has.UpdateData(items_has)

    def dev_del_click(self, event):
        index = self.item_dev_list.GetFirstSelected()
        if index == -1:
            return
        self.item_dev_list.DeleteItem(index)

    def dev_add_click(self, event):
        index = self.item_client_has.GetFirstSelected()
        if index == -1:
            return

        item = self.item_client_has.GetItem(index)

        result = ItemMove.getItemMove(item, self, True)  # True para especificar una devolucion y poner bien el maximo
        if result is None:
            return
        if isinstance(result, orm.ItemMovido):
            self._add_item_devuelto(result)

    def _add_item_devuelto(self, item):
        self.item_dev_list.AppendData(item)

    def item_dev_list_click(self, event):
        index = self.item_dev_list.GetFirstSelected()
        if index == -1:
            return

        item = self.item_dev_list.GetItem(index)

        result = ItemMove.getEditItemMove(item, self,
                                          True)  # True para especificar una devolucion y poner bien el maximo
        if result is None:
            return
        if isinstance(result, orm.ItemMovido):
            self.item_dev_list.UpdateItem(index, item)

    def client_cb_change(self, event):
        self._fill_client_items_has()

    def _add_item_salida(self, item):

        self.item_client_take.AppendData(item)

    def salida_add_click(self, event):
        index = self.item_left_list.GetFirstSelected()
        if index == -1:
            return

        item = self.item_left_list.GetItem(index)

        result = ItemMove.getItemMove(item, self)
        if result is None:
            return
        if isinstance(result, orm.ItemMovido):
            self._add_item_salida(result)

    def item_client_take_click(self, event):
        index = self.item_client_take.GetFirstSelected()
        if index == -1:
            return

        item = self.item_client_take.GetItem(index)

        result = ItemMove.getEditItemMove(item, self)
        if result is None:
            return
        if isinstance(result, orm.ItemMovido):
            self.item_client_take.UpdateItem(index, item)

    def salida_del_click(self, event):
        index = self.item_client_take.GetFirstSelected()
        if index == -1:
            return
        self.item_client_take.DeleteItem(index)

    def client_add_click(self, event):
        if ClientDataDialog.addClient(self, None, self.session) == CLIENT_OK:
            self._fill_clients()


    def ok_click(self, event):
        if self.item_client_take.GetItemCount() == 0 and \
                self.item_dev_list.GetItemCount() == 0:
            self.Close()
        result = wx.MessageBox("Realizar movimientos? Seguro?", "Movimientos", wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        if result == wx.CANCEL:
            return

        if result == wx.OK:
            session = self.session
            cliente = self.client_cb.GetActiveItem()
            if self.item_client_take.GetItemCount() > 0:
                m_salida = orm.Movimiento()
                m_salida.tipo = orm.TipoMovimiento.SALIDA
                item_take = self.item_client_take.GetItems()
                for items in item_take:
                    m_salida.items.append(items)

                m_salida.cliente_id = cliente.id
                m_salida.fecha = utils._wxdate2pydate(self.datetxt.GetValue())
                session.add(m_salida)
            if self.item_dev_list.GetItemCount() > 0:
                m_devolucion = orm.Movimiento()
                m_devolucion.tipo = orm.TipoMovimiento.DEVOLUCION
                items_dev = self.item_dev_list.GetItems()
                for items in items_dev:
                    m_devolucion.items.append(items)

                m_devolucion.cliente_id = cliente.id
                m_devolucion.fecha = utils._wxdate2pydate(self.datetxt.GetValue())
                m_devolucion = self.session.merge(m_devolucion)
                # session.add(m_devolucion)

            session.commit()

            self.Close()


class ClienteMovVenta(design_wx.ClienteMovVenta):

    def __init__(self, parent):
        design_wx.ClienteMovVenta.__init__(self, parent)
        # self.cliente_cb_dict = {}
        # # self.item_client_has_dict = {}
        # self.cliente_mov_list_dict = {}
        # self.cliente_item_list_dict = {}
        # self.cliente_item_venta_dict = {}

        self._setup_controls()
        self._Fill_Client_List()
        self.cliente_change(None)

    def ok_button_click(self, event):
        self.Close()

    def _setup_controls(self):

        self.cliente_cb.SetLambda(lambda c: c.nombre)

        for lista in [self.cliente_item_list, self.cliente_mov_items_list]:
            lista.ConfigColumns(['Articulo', 'Procedencia', 'Cantidad', 'Costo'])

        self.cliente_item_list.SetLambdas([
            lambda i: i.parent.nombre,
            lambda i: i.procedencia.nombre,
            lambda i: str(i.tiene),
            lambda i: str(i.getPrecioinDate().precio)
        ])

        self.cliente_mov_items_list.SetLambdas([
            lambda i: i.item.parent.nombre,
            lambda i: i.item.procedencia.nombre,
            lambda i: str(i.cantidad),
            lambda i: str(i.item.getPrecioinDate().precio)
        ])

        self.cliente_mov_list.ConfigColumns(['Fecha', 'Tipo'])
        self.cliente_mov_list.SetLambdas([
            lambda i: str(datetime.datetime.strftime(i.fecha, '%d/%m/%Y')),
            lambda i: i.tipo.name
        ])

        self.cliente_venta_list.ConfigColumns(["Fecha", "Articulo", "Procedencia", "Cantidad", "Precio"])
        self.cliente_venta_list.SetLambdas([
            lambda i: str(datetime.datetime.strftime(i.fecha, '%d/%m/%Y')),
            lambda v: v.item.parent.nombre,
            lambda v: v.item.procedencia.nombre,
            lambda v: str(v.cantidad),
            lambda v: str('$%.2f' % v.precio)
        ])

    def _Fill_Client_List(self):
        session = db.session()
        clientes = session.query(orm.Cliente).all()
        self.cliente_cb.UpdateData(clientes)


    def Update_Ventas(self):
        cliente = self.cliente_cb.GetActiveItem()
        session = db.session()
        ventas = session.query(orm.Venta).filter(orm.Venta.cliente_id == cliente.id). \
            filter(orm.Venta.fecha >= utils._wxdate2pydate(self.from_date.GetValue())). \
            filter(orm.Venta.fecha <= utils._wxdate2pydate(self.to_date.GetValue())).all()
        self.cliente_venta_list.UpdateData(ventas)

    def cliente_change(self, event):
        cliente = self.cliente_cb.GetActiveItem()
        items = cliente.posession_items()
        self.cliente_item_list.UpdateData(items)
        self._update_movs()
        self.Update_Ventas()

    def _update_movs(self):
        cliente = self.cliente_cb.GetActiveItem()
        session = db.session()
        # session = session.object_session(cliente)

        movs = session.query(orm.Movimiento).filter(orm.Movimiento.cliente_id == cliente.id). \
            filter(orm.Movimiento.fecha > utils._wxdate2pydate(self.from_date.GetValue())). \
            filter(orm.Movimiento.fecha < utils._wxdate2pydate(self.to_date.GetValue())).all()

        self.cliente_mov_list.UpdateData(movs)
        self.cliente_mov_items_list.DeleteAllItems()

    def from_date_change(self, event):
        self._update_movs()
        self.Update_Ventas()

    def to_date_change(self, event):
        self._update_movs()
        self.Update_Ventas()

    def cliente_mov_selected(self, event):
        index = self.cliente_mov_list.GetFirstSelected()
        if index == -1:
            return

        mov = self.cliente_mov_list.GetItem(index)
        session = db.session()
        mov = session.query(orm.Movimiento).filter(orm.Movimiento.id == mov.id).one()
        items = mov.items
        if items is not None and isinstance(items, list):
            self.cliente_mov_items_list.UpdateData(items)


from git.remote import RemoteProgress


class UpdateProgress(RemoteProgress):

    def __init__(self):
        RemoteProgress.__init__(self)
        self.progress = UpdateDialog()
        self.progress.setProgress(0)
        self.progress.Show()

    def update(self, op_code, cur_count, max_count=None, message=''):

        if max_count is not None:
            self.progress.setStatus('%d / %d restante' % (max_count - cur_count, max_count)). \
                setProgress(cur_count / max_count * 100)
        else:
            self.progress.setStatus('%d items' % cur_count).setProgress(0)

        if op_code & RemoteProgress.END == 0:
            self.progress.Close()
            self.progress.Destroy()

    def __del__(self):
        self.progress.Close()
        self.progress.Destroy()



class UpdateDialog(design_wx.UpdateDialog):
    instance = None

    @staticmethod
    def Instance():
        if UpdateDialog.instance is None:
            UpdateDialog.instance = UpdateDialog()
        return UpdateDialog.instance

    def __init__(self, parent=None):
        design_wx.UpdateDialog.__init__(self, parent)

    def setProgress(self, progress):
        if not isinstance(progress, int):
            return None
        self.progress_bar.SetValue(progress)
        return self

    def setStatus(self, status):
        self.status_label.SetLabel(status)
        return self

    @staticmethod
    def progress(op_code, cur_count, max_count=None):
        if UpdateDialog.instance is None:
            UpdateDialog.Instance().ShowModal()

        if max_count is not None:
            UpdateDialog.Instance().setStatus('%d / %d restante' % (max_count - cur_count, max_count)). \
                setProgress(cur_count / max_count * 100)
        else:
            UpdateDialog.Instance().setStatus('%d items' % cur_count).setProgress(0)

        if op_code & RemoteProgress.END == 0:
            UpdateDialog.Instance().Close()
            UpdateDialog.Instance().Destroy()
            UpdateDialog.instance = None


class ProcedenciaStatus(design_wx.ProcedenciaStatus):
    def __init__(self, parent):
        design_wx.ProcedenciaStatus.__init__(self, parent)

        self._setup_controls()
        self._fill_procedencia()

    def collapsible_pane_changed(self, event):
        event.EventObject.GetParent().Layout()
        self.Layout()

    def _setup_controls(self):

        self.procedencia_cb.SetLambda(lambda p: p.nombre)

        self.stock_vendido.ConfigColumns(['Fecha', 'Articulo', 'Cantidad', "Precio"])
        self.stock_vendido.SetLambdas([
            lambda v: str(datetime.datetime.strftime(v.fecha, '%d/%m/%Y')),
            lambda v: "%s [%s]" % (v.item.parent.nombre, v.item.parent.marca),
            lambda v: str(v.cantidad),
            lambda v: "$ %.2f" % v.precio
        ])

        self.stock_cliente.ConfigColumns(['Cliente', 'Articulo', 'Cantidad', 'Precio'])
        self.stock_cliente.SetLambdas([
            lambda i: i.cliente.nombre,
            lambda i: "%s [%s]" % (i.item.parent.nombre, i.item.parent.marca),
            lambda i: str(i.tiene),
            lambda i: "$ %.2f" % i.item.getPrecioinDate().precio
        ])

        self.stock_local.ConfigColumns(['Articulo', 'Cantidad', 'Precio'])
        self.stock_local.SetLambdas([
            lambda i: "%s [%s]" % (i.parent.nombre, i.parent.marca),
            lambda i: str(i.restantes),
            lambda i: "$ %.2f" % i.getPrecioinDate().precio
        ])

    def _fill_procedencia(self):
        session = db.session()
        ps = session.query(orm.Procedencia).all()
        self.procedencia_cb.UpdateData(ps)
        self.procedencia_change(None)

    def ok_button_click(self, event):
        self.Close()

    def procedencia_change(self, event):
        ps = self.procedencia_cb.GetActiveItem()
        session = db.session()

        item_left = session.query(orm.Item).filter(orm.Item.procedencia_id == ps.id).all()
        self.stock_local.UpdateData(item_left)
        total = 0.0
        for i in item_left:
            total += i.getPrecioinDate().precio * i.restantes
        self.stock_local_label.SetLabel("$ %.2f" % total)

        item_vendidos = session.query(orm.Venta).filter(orm.Item.procedencia_id == ps.id). \
            filter(orm.Venta.item_id == orm.Item.id).all()
        self.stock_vendido.UpdateData(item_vendidos)
        total = 0.0
        for i in item_vendidos:
            total += i.cantidad * i.precio
        self.stock_vendido_label.SetLabel("$ %.2f" % total)

        itemxclient = orm.Item.getItemsByClient(ps.id)
        self.stock_cliente.UpdateData(itemxclient)
        total = 0.0
        for i in itemxclient:
            total += i.item.getPrecioinDate().precio * i.tiene
        self.stock_cliente_label.SetLabel("$ %.2f" % total)


class ItemTrackerDialog(design_wx.ItemTrackerDialog):
    def __init__(self, parent):
        design_wx.ItemTrackerDialog.__init__(self, parent)

        self._setup_controls()
        self._fill_procedencia()

    def _setup_controls(self):
        self.procedencia_cb.SetLambda(lambda p: p.nombre)
        self.article_cb.SetLambda(lambda a: "%s (%s) [%d]" % (a.parent.nombre, a.parent.marca, a.cantidad))

        self.item_list.ConfigColumns(['Fecha', 'Evento', 'Cantidad', 'Cliente', 'Valor'])
        self.item_list.SetLambdas([
            lambda r: str(datetime.datetime.strftime(r.fecha, '%d/%m/%Y')),
            lambda r: r.tipo,
            lambda r: str(r.cantidad),
            lambda r: r.cliente.nombre,
            lambda r: "$ %.2f" % r.valor
        ])

    def procedencia_change(self, event):
        self._fill_article()

    def _fill_procedencia(self):
        session = db.session()
        ps = session.query(orm.Procedencia).all()
        self.procedencia_cb.UpdateData(ps)
        self._fill_article()

    def _fill_article(self):
        p = self.procedencia_cb.GetActiveItem()
        session = db.session()
        articles = session.query(orm.Item).filter(orm.Item.procedencia_id == p.id).all()
        self.article_cb.UpdateData(articles)
        self.item_list.DeleteAllItems()

    def ok_button_click(self, event):
        self.Close()

    def show_button_click(self, event):
        item = self.article_cb.GetActiveItem()
        results = item.getTracker()
        self.item_list.UpdateData(results)

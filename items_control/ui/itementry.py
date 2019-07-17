from items_control.ui.design_wx import items_control_wx as design_wx
import wx
from items_control.data import db
from items_control import orm
from items_control.ui.items_dialog import ItemsDataDialog, ITEM_OK
from items_control.ui.procedencia_dialog import ProcedenciaDataDialog, PROCEDENCIA_OK

C_PROC, C_ITEM, C_CANT, C_COST, C_PRECIO = range(5)


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
        index = self.item_list.InsertItem(count, item.procedencia.nombre)
        self.item_list.SetItem(index, C_ITEM, item.parent.nombre)
        self.item_list.SetItem(index, C_CANT, str(item.cantidad))
        self.item_list.SetItem(index, C_COST, str(item.costo))
        self.item_list.SetItem(index, C_PRECIO, str(item.precio[-1].precio))
        self.entry_items_dict[index] = item

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

    def ok_click(self, event):
        for i in self.entry_items_dict:
            self.session.add(self.entry_items_dict[i])
        self.session.commit()
        self.Close()


if __name__ == "__main__":
    app = wx.App()
    db.open_db("//home/mbolivar//Projects//items_control//items_control//data//db.sqlite")
    main = ItemsEntryDialog(None)

    main.Show()
    app.MainLoop()

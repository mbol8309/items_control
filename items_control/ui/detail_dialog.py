from items_control.ui.design_wx import items_control_wx as design_wx
from items_control import orm


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

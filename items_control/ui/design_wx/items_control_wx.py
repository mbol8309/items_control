# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun  5 2019)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

from items_control.ui.custom_controls import CustomListCtrl
import wx
import wx.xrc
import wx.adv

###########################################################################
## Class ClientDataDialog
###########################################################################

class ClientDataDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Datos Cliente", pos=wx.DefaultPosition,
                           size=wx.Size(489, 333), style=wx.DEFAULT_DIALOG_STYLE, name=u"add_client")

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer7 = wx.BoxSizer(wx.VERTICAL)

        gSizer1 = wx.GridSizer(4, 2, 10, 0)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"Nombre:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)

        gSizer1.Add(self.m_staticText1, 0, wx.ALL, 5)

        self.name_txt = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer1.Add(self.name_txt, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u"Telefono:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)

        gSizer1.Add(self.m_staticText2, 0, wx.ALL, 5)

        self.telefono_txt = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer1.Add(self.telefono_txt, 1, wx.ALL | wx.EXPAND, 5)

        self.m_staticText3 = wx.StaticText(self, wx.ID_ANY, u"Direccion:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText3.Wrap(-1)

        gSizer1.Add(self.m_staticText3, 0, wx.ALL, 5)

        self.address_txt = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                       wx.TE_MULTILINE | wx.TE_WORDWRAP)
        gSizer1.Add(self.address_txt, 0, wx.ALL | wx.EXPAND, 5)

        self.Tipo = wx.StaticText(self, wx.ID_ANY, u"Tipo:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Tipo.Wrap(-1)

        gSizer1.Add(self.Tipo, 0, wx.ALL, 5)

        tipo_cbChoices = []
        self.tipo_cb = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, tipo_cbChoices, 0)
        self.tipo_cb.SetSelection(0)
        gSizer1.Add(self.tipo_cb, 0, wx.ALL | wx.EXPAND, 5)

        bSizer7.Add(gSizer1, 1, wx.ALL | wx.EXPAND, 5)

        bSizer6 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer6.SetMinSize(wx.Size(-1, 50))
        self.m_button1 = wx.Button(self, wx.ID_ANY, u"Ok", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer6.Add(self.m_button1, 0, wx.ALIGN_RIGHT, 5)

        self.m_button2 = wx.Button(self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer6.Add(self.m_button2, 0, wx.ALIGN_RIGHT, 5)

        bSizer7.Add(bSizer6, 2, wx.ALIGN_RIGHT | wx.ALL | wx.TOP, 10)

        self.SetSizer(bSizer7)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_button1.Bind(wx.EVT_BUTTON, self.okClick)
        self.m_button2.Bind(wx.EVT_BUTTON, self.cancelClick)

    def __del__(self):
        pass


    # Virtual event handlers, overide them in your derived class
    def okClick(self, event):
        event.Skip()

    def cancelClick(self, event):
        event.Skip()


###########################################################################
## Class ClientList
###########################################################################

class ClientList(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Lista de clientes", pos=wx.DefaultPosition,
                           size=wx.Size(-1, -1), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.Size(-1, 300), wx.Size(-1, 500))

        bSizer10 = wx.BoxSizer(wx.VERTICAL)

        self.list = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, -1), wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.list.SetMinSize(wx.Size(500, 300))

        self.client_options_context = wx.Menu()
        self.add_client = wx.MenuItem(self.client_options_context, wx.ID_ANY, u"Agregar", wx.EmptyString,
                                      wx.ITEM_NORMAL)
        self.client_options_context.Append(self.add_client)

        self.edit_client = wx.MenuItem(self.client_options_context, wx.ID_ANY, u"Editar", wx.EmptyString,
                                       wx.ITEM_NORMAL)
        self.client_options_context.Append(self.edit_client)

        self.del_client = wx.MenuItem(self.client_options_context, wx.ID_ANY, u"Eliminar", wx.EmptyString,
                                      wx.ITEM_NORMAL)
        self.client_options_context.Append(self.del_client)

        self.list.Bind(wx.EVT_RIGHT_DOWN, self.listOnContextMenu)

        bSizer10.Add(self.list, 0, wx.ALL | wx.EXPAND, 5)

        bSizer11 = wx.BoxSizer(wx.HORIZONTAL)

        self.okButton = wx.Button(self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer11.Add(self.okButton, 0, wx.ALL, 5)

        bSizer10.Add(bSizer11, 1, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.SetSizer(bSizer10)
        self.Layout()
        bSizer10.Fit(self)

        self.Centre(wx.BOTH)

        # Connect Events
        self.list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.edit_client_click)
        self.Bind(wx.EVT_MENU, self.add_client_click, id=self.add_client.GetId())
        self.Bind(wx.EVT_MENU, self.edit_client_click, id=self.edit_client.GetId())
        self.Bind(wx.EVT_MENU, self.del_client_click, id=self.del_client.GetId())
        self.okButton.Bind(wx.EVT_BUTTON, self.okClick)

    def __del__(self):
        pass


    # Virtual event handlers, overide them in your derived class
    def edit_client_click(self, event):
        event.Skip()

    def add_client_click(self, event):
        event.Skip()

    def del_client_click(self, event):
        event.Skip()

    def okClick(self, event):
        event.Skip()

    def listOnContextMenu(self, event):
        self.list.PopupMenu(self.client_options_context, event.GetPosition())


###########################################################################
## Class MainWindows
###########################################################################

class MainWindows(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Control Ropa", pos=wx.DefaultPosition,
                          size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        self.m_menubar1 = wx.MenuBar(0)
        self.m_menu2 = wx.Menu()
        self.open_menu = wx.MenuItem(self.m_menu2, wx.ID_ANY, u"Abrir DB", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu2.Append(self.open_menu)

        self.recent_menu = wx.Menu()
        self.m_menu2.AppendSubMenu(self.recent_menu, u"Reciente...")

        self.create_menu = wx.MenuItem(self.m_menu2, wx.ID_ANY, u"Crear DB", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu2.Append(self.create_menu)

        self.m_menu2.AppendSeparator()

        self.exit_menu = wx.MenuItem(self.m_menu2, wx.ID_ANY, u"Salir", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu2.Append(self.exit_menu)

        self.m_menubar1.Append(self.m_menu2, u"Archivo")

        self.data_menu = wx.Menu()
        self.client_menu = wx.MenuItem(self.data_menu, wx.ID_ANY, u"Clientes", wx.EmptyString, wx.ITEM_NORMAL)
        self.data_menu.Append(self.client_menu)
        self.client_menu.Enable(False)

        self.proc_menu = wx.MenuItem(self.data_menu, wx.ID_ANY, u"Procedencia", wx.EmptyString, wx.ITEM_NORMAL)
        self.data_menu.Append(self.proc_menu)
        self.proc_menu.Enable(False)

        self.item_menu = wx.MenuItem(self.data_menu, wx.ID_ANY, u"Items", wx.EmptyString, wx.ITEM_NORMAL)
        self.data_menu.Append(self.item_menu)
        self.item_menu.Enable(False)

        self.m_menubar1.Append(self.data_menu, u"Datos")

        self.mov_menu = wx.Menu()
        self.entry_menu = wx.MenuItem(self.mov_menu, wx.ID_ANY, u"Entrada", wx.EmptyString, wx.ITEM_NORMAL)
        self.mov_menu.Append(self.entry_menu)
        self.entry_menu.Enable(False)

        self.mov_submenu = wx.MenuItem(self.mov_menu, wx.ID_ANY, u"Movimientos", wx.EmptyString, wx.ITEM_NORMAL)
        self.mov_menu.Append(self.mov_submenu)
        self.mov_submenu.Enable(False)

        self.venta_menu = wx.MenuItem(self.mov_menu, wx.ID_ANY, u"Ventas", wx.EmptyString, wx.ITEM_NORMAL)
        self.mov_menu.Append(self.venta_menu)
        self.venta_menu.Enable(False)

        self.gasto_menu = wx.MenuItem(self.mov_menu, wx.ID_ANY, u"Gastos", wx.EmptyString, wx.ITEM_NORMAL)
        self.mov_menu.Append(self.gasto_menu)
        self.gasto_menu.Enable(False)

        self.m_menubar1.Append(self.mov_menu, u"Movimientos")

        self.report_menu = wx.Menu()
        self.client_mov_venta = wx.MenuItem(self.report_menu, wx.ID_ANY, u"Movimientos x Cliente", wx.EmptyString,
                                            wx.ITEM_NORMAL)
        self.report_menu.Append(self.client_mov_venta)
        self.client_mov_venta.Enable(False)

        self.m_menubar1.Append(self.report_menu, u"Reportes")

        self.SetMenuBar(self.m_menubar1)

        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(wx.EVT_MENU, self.open_menu_click, id=self.open_menu.GetId())
        self.Bind(wx.EVT_MENU, self.create_menu_click, id=self.create_menu.GetId())
        self.Bind(wx.EVT_MENU, self.exit_menu_click, id=self.exit_menu.GetId())
        self.Bind(wx.EVT_MENU, self.client_menu_click, id=self.client_menu.GetId())
        self.Bind(wx.EVT_MENU, self.proc_dato_click, id=self.proc_menu.GetId())
        self.Bind(wx.EVT_MENU, self.items_menu_click, id=self.item_menu.GetId())
        self.Bind(wx.EVT_MENU, self.entry_menu_click, id=self.entry_menu.GetId())
        self.Bind(wx.EVT_MENU, self.mov_menu_click, id=self.mov_submenu.GetId())
        self.Bind(wx.EVT_MENU, self.ventamenu_click, id=self.venta_menu.GetId())
        self.Bind(wx.EVT_MENU, self.gasto_menu_click, id=self.gasto_menu.GetId())
        self.Bind(wx.EVT_MENU, self.cliente_mov_venta_click, id=self.client_mov_venta.GetId())

    def __del__(self):
        pass


    # Virtual event handlers, overide them in your derived class
    def open_menu_click(self, event):
        event.Skip()

    def create_menu_click(self, event):
        event.Skip()

    def exit_menu_click(self, event):
        event.Skip()

    def client_menu_click(self, event):
        event.Skip()

    def proc_dato_click(self, event):
        event.Skip()

    def items_menu_click(self, event):
        event.Skip()

    def entry_menu_click(self, event):
        event.Skip()

    def mov_menu_click(self, event):
        event.Skip()

    def ventamenu_click(self, event):
        event.Skip()

    def gasto_menu_click(self, event):
        event.Skip()

    def cliente_mov_venta_click(self, event):
        event.Skip()


###########################################################################
## Class ProcDialog
###########################################################################

class ProcDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Procedencia", pos=wx.DefaultPosition,
                           size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.Size(500, -1), wx.DefaultSize)

        bSizer5 = wx.BoxSizer(wx.VERTICAL)

        self.proc_list = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                     wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.proc_list.SetMinSize(wx.Size(400, 200))

        self.proc_context = wx.Menu()
        self.add_proc = wx.MenuItem(self.proc_context, wx.ID_ANY, u"Agregar", wx.EmptyString, wx.ITEM_NORMAL)
        self.proc_context.Append(self.add_proc)

        self.edit_proc = wx.MenuItem(self.proc_context, wx.ID_ANY, u"Editar", wx.EmptyString, wx.ITEM_NORMAL)
        self.proc_context.Append(self.edit_proc)

        self.del_proc = wx.MenuItem(self.proc_context, wx.ID_ANY, u"Eliminar", wx.EmptyString, wx.ITEM_NORMAL)
        self.proc_context.Append(self.del_proc)

        self.proc_list.Bind(wx.EVT_RIGHT_DOWN, self.proc_listOnContextMenu)

        bSizer5.Add(self.proc_list, 0, wx.ALL | wx.EXPAND, 5)

        bSizer8 = wx.BoxSizer(wx.VERTICAL)

        self.ok_button = wx.Button(self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer8.Add(self.ok_button, 0, wx.ALL, 5)

        bSizer5.Add(bSizer8, 1, wx.ALIGN_RIGHT, 5)

        self.SetSizer(bSizer5)
        self.Layout()
        bSizer5.Fit(self)

        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(wx.EVT_MENU, self.add_click, id=self.add_proc.GetId())
        self.Bind(wx.EVT_MENU, self.edit_click, id=self.edit_proc.GetId())
        self.Bind(wx.EVT_MENU, self.del_click, id=self.del_proc.GetId())
        self.ok_button.Bind(wx.EVT_BUTTON, self.ok_click)

    def __del__(self):
        pass


    # Virtual event handlers, overide them in your derived class
    def add_click(self, event):
        event.Skip()

    def edit_click(self, event):
        event.Skip()

    def del_click(self, event):
        event.Skip()

    def ok_click(self, event):
        event.Skip()

    def proc_listOnContextMenu(self, event):
        self.proc_list.PopupMenu(self.proc_context, event.GetPosition())


###########################################################################
## Class ProcDatosDialog
###########################################################################

class ProcDatosDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Datos de Procedencia", pos=wx.DefaultPosition,
                           size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.Size(500, 300), wx.DefaultSize)

        bSizer6 = wx.BoxSizer(wx.VERTICAL)

        fgSizer1 = wx.FlexGridSizer(3, 2, 0, 0)
        fgSizer1.AddGrowableCol(1)
        fgSizer1.SetFlexibleDirection(wx.BOTH)
        fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.name_label = wx.StaticText(self, wx.ID_ANY, u"Nombre", wx.DefaultPosition, wx.DefaultSize, 0)
        self.name_label.Wrap(-1)

        fgSizer1.Add(self.name_label, 0, wx.ALL, 5)

        self.name_txt = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer1.Add(self.name_txt, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText6 = wx.StaticText(self, wx.ID_ANY, u"Fecha", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText6.Wrap(-1)

        fgSizer1.Add(self.m_staticText6, 0, wx.ALL, 5)

        self.date_txt = wx.adv.DatePickerCtrl(self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize,
                                              wx.adv.DP_DEFAULT)
        fgSizer1.Add(self.date_txt, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText7 = wx.StaticText(self, wx.ID_ANY, u"Detalles", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText7.Wrap(-1)

        fgSizer1.Add(self.m_staticText7, 0, wx.ALL, 5)

        self.detalle_txt = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                       wx.TE_MULTILINE)
        self.detalle_txt.SetMinSize(wx.Size(-1, 150))

        fgSizer1.Add(self.detalle_txt, 0, wx.ALL | wx.EXPAND, 5)

        bSizer6.Add(fgSizer1, 1, wx.ALL | wx.EXPAND, 5)

        bSizer7 = wx.BoxSizer(wx.HORIZONTAL)

        self.ok_button = wx.Button(self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer7.Add(self.ok_button, 0, wx.ALL, 5)

        self.cancel_bt = wx.Button(self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer7.Add(self.cancel_bt, 0, wx.ALL, 5)

        bSizer6.Add(bSizer7, 0, wx.ALIGN_RIGHT, 5)

        self.SetSizer(bSizer6)
        self.Layout()
        bSizer6.Fit(self)

        self.Centre(wx.BOTH)

        # Connect Events
        self.ok_button.Bind(wx.EVT_BUTTON, self.ok_click)
        self.cancel_bt.Bind(wx.EVT_BUTTON, self.cancel_click)

    def __del__(self):
        pass


    # Virtual event handlers, overide them in your derived class
    def ok_click(self, event):
        event.Skip()

    def cancel_click(self, event):
        event.Skip()


###########################################################################
## Class ItemsDialog
###########################################################################

class ItemsDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Articulos", pos=wx.DefaultPosition,
                           size=wx.Size(548, 324), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.Size(500, -1), wx.DefaultSize)
        self.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Sans"))

        bSizer9 = wx.BoxSizer(wx.VERTICAL)

        self.item_list = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                     wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.item_list.SetFont(
            wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Sans"))
        self.item_list.SetMinSize(wx.Size(-1, 200))

        self.m_menu5 = wx.Menu()
        self.add_item_menu = wx.MenuItem(self.m_menu5, wx.ID_ANY, u"Agregar", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu5.Append(self.add_item_menu)

        self.edit_item_menu = wx.MenuItem(self.m_menu5, wx.ID_ANY, u"Editar", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu5.Append(self.edit_item_menu)

        self.del_item_menu = wx.MenuItem(self.m_menu5, wx.ID_ANY, u"Eliminar", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu5.Append(self.del_item_menu)

        self.item_list.Bind(wx.EVT_RIGHT_DOWN, self.item_listOnContextMenu)

        bSizer9.Add(self.item_list, 1, wx.ALL | wx.EXPAND, 5)

        bSizer10 = wx.BoxSizer(wx.HORIZONTAL)

        self.ok_button = wx.Button(self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer10.Add(self.ok_button, 0, wx.ALL, 5)

        bSizer9.Add(bSizer10, 0, wx.ALIGN_RIGHT, 5)

        self.SetSizer(bSizer9)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.item_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.item_clicked)
        self.Bind(wx.EVT_MENU, self.add_click, id=self.add_item_menu.GetId())
        self.Bind(wx.EVT_MENU, self.edit_click, id=self.edit_item_menu.GetId())
        self.Bind(wx.EVT_MENU, self.del_click, id=self.del_item_menu.GetId())
        self.ok_button.Bind(wx.EVT_BUTTON, self.ok_click)

    def __del__(self):
        pass


    # Virtual event handlers, overide them in your derived class
    def item_clicked(self, event):
        event.Skip()

    def add_click(self, event):
        event.Skip()

    def edit_click(self, event):
        event.Skip()

    def del_click(self, event):
        event.Skip()

    def ok_click(self, event):
        event.Skip()

    def item_listOnContextMenu(self, event):
        self.item_list.PopupMenu(self.m_menu5, event.GetPosition())


###########################################################################
## Class ItemsDataDialog
###########################################################################

class ItemsDataDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Datos articulos", pos=wx.DefaultPosition,
                           size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.Size(500, 300), wx.DefaultSize)

        bSizer11 = wx.BoxSizer(wx.VERTICAL)

        fgSizer3 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer3.AddGrowableCol(1)
        fgSizer3.SetFlexibleDirection(wx.BOTH)
        fgSizer3.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText9 = wx.StaticText(self, wx.ID_ANY, u"Nombre", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText9.Wrap(-1)

        fgSizer3.Add(self.m_staticText9, 0, wx.ALL, 5)

        self.name_txt = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer3.Add(self.name_txt, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText10 = wx.StaticText(self, wx.ID_ANY, u"Marca", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText10.Wrap(-1)

        fgSizer3.Add(self.m_staticText10, 0, wx.ALL, 5)

        self.marca_txt = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer3.Add(self.marca_txt, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText11 = wx.StaticText(self, wx.ID_ANY, u"Foto", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText11.Wrap(-1)

        fgSizer3.Add(self.m_staticText11, 0, wx.ALL, 5)

        self.photo_txt = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer3.Add(self.photo_txt, 0, wx.ALL | wx.EXPAND, 5)

        bSizer11.Add(fgSizer3, 1, wx.ALL | wx.EXPAND, 5)

        bSizer12 = wx.BoxSizer(wx.HORIZONTAL)

        self.ok_button = wx.Button(self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer12.Add(self.ok_button, 0, wx.ALL, 5)

        self.cancel_button = wx.Button(self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer12.Add(self.cancel_button, 0, wx.ALL, 5)

        bSizer11.Add(bSizer12, 0, wx.ALIGN_RIGHT, 5)

        self.SetSizer(bSizer11)
        self.Layout()
        bSizer11.Fit(self)

        self.Centre(wx.BOTH)

        # Connect Events
        self.ok_button.Bind(wx.EVT_BUTTON, self.ok_click)
        self.cancel_button.Bind(wx.EVT_BUTTON, self.cancel_click)

    def __del__(self):
        pass


    # Virtual event handlers, overide them in your derived class
    def ok_click(self, event):
        event.Skip()

    def cancel_click(self, event):
        event.Skip()


###########################################################################
## Class ItemEntryDialog
###########################################################################

class ItemEntryDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Entrada de Articulos", pos=wx.DefaultPosition,
                           size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.Size(700, 500), wx.DefaultSize)

        bSizer13 = wx.BoxSizer(wx.VERTICAL)

        fgSizer5 = wx.FlexGridSizer(0, 4, 0, 0)
        fgSizer5.AddGrowableCol(1)
        fgSizer5.AddGrowableCol(3)
        fgSizer5.SetFlexibleDirection(wx.BOTH)
        fgSizer5.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText12 = wx.StaticText(self, wx.ID_ANY, u"Articulo", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText12.Wrap(-1)

        fgSizer5.Add(self.m_staticText12, 0, wx.ALL, 5)

        bSizer15 = wx.BoxSizer(wx.HORIZONTAL)

        item_choiceChoices = []
        self.item_choice = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, item_choiceChoices, 0)
        self.item_choice.SetSelection(0)
        bSizer15.Add(self.item_choice, 1, wx.ALL | wx.EXPAND, 5)

        self.add_item_button = wx.Button(self, wx.ID_ANY, u"+", wx.DefaultPosition, wx.Size(30, 30), 0)
        bSizer15.Add(self.add_item_button, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)

        fgSizer5.Add(bSizer15, 0, wx.EXPAND, 5)

        self.m_staticText13 = wx.StaticText(self, wx.ID_ANY, u"Procedencia", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText13.Wrap(-1)

        fgSizer5.Add(self.m_staticText13, 0, wx.ALL, 5)

        bSizer16 = wx.BoxSizer(wx.HORIZONTAL)

        proc_choiceChoices = []
        self.proc_choice = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, proc_choiceChoices, 0)
        self.proc_choice.SetSelection(0)
        bSizer16.Add(self.proc_choice, 1, wx.ALL | wx.EXPAND, 5)

        self.add_proc_button = wx.Button(self, wx.ID_ANY, u"+", wx.DefaultPosition, wx.Size(30, 30), 0)
        bSizer16.Add(self.add_proc_button, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)

        fgSizer5.Add(bSizer16, 1, wx.EXPAND, 5)

        self.m_staticText14 = wx.StaticText(self, wx.ID_ANY, u"Cantidad", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText14.Wrap(-1)

        fgSizer5.Add(self.m_staticText14, 0, wx.ALL, 5)

        self.cantidad_txt = wx.SpinCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                        wx.SP_ARROW_KEYS, 0, 10, 0)
        fgSizer5.Add(self.cantidad_txt, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText15 = wx.StaticText(self, wx.ID_ANY, u"Costo", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText15.Wrap(-1)

        fgSizer5.Add(self.m_staticText15, 0, wx.ALL, 5)

        self.cost_txt = wx.SpinCtrlDouble(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                          wx.SP_ARROW_KEYS, 0, 100, 0, 1)
        self.cost_txt.SetDigits(2)
        fgSizer5.Add(self.cost_txt, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText16 = wx.StaticText(self, wx.ID_ANY, u"Precio", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText16.Wrap(-1)

        fgSizer5.Add(self.m_staticText16, 0, wx.ALL, 5)

        self.price_txt = wx.SpinCtrlDouble(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                           wx.SP_ARROW_KEYS, 0, 100, 0, 1)
        self.price_txt.SetDigits(2)
        fgSizer5.Add(self.price_txt, 0, wx.ALL | wx.EXPAND, 5)

        self.add_button = wx.Button(self, wx.ID_ANY, u"Agregar", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer5.Add(self.add_button, 0, wx.ALL, 5)

        bSizer13.Add(fgSizer5, 1, wx.ALL | wx.EXPAND, 5)

        self.item_list = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                     wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.item_list.SetMinSize(wx.Size(-1, 300))

        self.m_menu7 = wx.Menu()
        self.eliminar_menu = wx.MenuItem(self.m_menu7, wx.ID_ANY, u"Eliminar", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu7.Append(self.eliminar_menu)

        self.item_list.Bind(wx.EVT_RIGHT_DOWN, self.item_listOnContextMenu)

        bSizer13.Add(self.item_list, 0, wx.ALL | wx.EXPAND, 5)

        bSizer14 = wx.BoxSizer(wx.HORIZONTAL)

        self.ok_button = wx.Button(self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer14.Add(self.ok_button, 0, wx.ALL, 5)

        self.cancel_button = wx.Button(self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer14.Add(self.cancel_button, 0, wx.ALL, 5)

        bSizer13.Add(bSizer14, 0, wx.ALIGN_RIGHT, 5)

        self.SetSizer(bSizer13)
        self.Layout()
        bSizer13.Fit(self)

        self.Centre(wx.BOTH)

        # Connect Events
        self.add_item_button.Bind(wx.EVT_BUTTON, self.add_item_button_click)
        self.add_proc_button.Bind(wx.EVT_BUTTON, self.add_proc_button_click)
        self.add_button.Bind(wx.EVT_BUTTON, self.add_click)
        self.Bind(wx.EVT_MENU, self.eliminar_click, id=self.eliminar_menu.GetId())
        self.ok_button.Bind(wx.EVT_BUTTON, self.ok_click)
        self.cancel_button.Bind(wx.EVT_BUTTON, self.cancel_click)

    def __del__(self):
        pass


    # Virtual event handlers, overide them in your derived class
    def add_item_button_click(self, event):
        event.Skip()

    def add_proc_button_click(self, event):
        event.Skip()

    def add_click(self, event):
        event.Skip()

    def eliminar_click(self, event):
        event.Skip()

    def ok_click(self, event):
        event.Skip()

    def cancel_click(self, event):
        event.Skip()

    def item_listOnContextMenu(self, event):
        self.item_list.PopupMenu(self.m_menu7, event.GetPosition())


###########################################################################
## Class DetailDialog
###########################################################################

class DetailDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                           size=wx.Size(500, 500), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer17 = wx.BoxSizer(wx.VERTICAL)

        self.item_label = wx.StaticText(self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0)
        self.item_label.Wrap(-1)

        bSizer17.Add(self.item_label, 0, wx.ALL, 5)

        self.item_list = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, 300),
                                     wx.LC_REPORT | wx.LC_SINGLE_SEL)
        bSizer17.Add(self.item_list, 1, wx.ALL | wx.EXPAND, 5)

        self.ok_button = wx.Button(self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer17.Add(self.ok_button, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.SetSizer(bSizer17)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.item_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.item_activated)
        self.ok_button.Bind(wx.EVT_BUTTON, self.ok_button_click)

    def __del__(self):
        pass


    # Virtual event handlers, overide them in your derived class
    def item_activated(self, event):
        event.Skip()

    def ok_button_click(self, event):
        event.Skip()


###########################################################################
## Class MovementDialog
###########################################################################

class MovementDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Movimientos", pos=wx.DefaultPosition,
                           size=wx.Size(1200, 700), style=wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer19 = wx.BoxSizer(wx.VERTICAL)

        bSizer20 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText18 = wx.StaticText(self, wx.ID_ANY, u"Cliente", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText18.Wrap(-1)

        bSizer20.Add(self.m_staticText18, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        client_cbChoices = []
        self.client_cb = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, client_cbChoices, 0)
        self.client_cb.SetSelection(0)
        bSizer20.Add(self.client_cb, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.m_button17 = wx.Button(self, wx.ID_ANY, u"+", wx.DefaultPosition, wx.Size(30, 30), 0)
        bSizer20.Add(self.m_button17, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        bSizer19.Add(bSizer20, 0, wx.ALL | wx.EXPAND, 5)

        self.m_notebook3 = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.salida_panel = wx.Panel(self.m_notebook3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer21 = wx.BoxSizer(wx.HORIZONTAL)

        self.item_left_list = wx.ListCtrl(self.salida_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                          wx.LC_REPORT | wx.LC_SINGLE_SEL)
        bSizer21.Add(self.item_left_list, 1, wx.ALL | wx.EXPAND, 5)

        bSizer22 = wx.BoxSizer(wx.VERTICAL)

        self.salida_right_bt = wx.Button(self.salida_panel, wx.ID_ANY, u">", wx.DefaultPosition, wx.Size(30, 30), 0)
        bSizer22.Add(self.salida_right_bt, 0, wx.ALL, 5)

        self.salida_left_bt = wx.Button(self.salida_panel, wx.ID_ANY, u"<", wx.DefaultPosition, wx.Size(30, 30), 0)
        bSizer22.Add(self.salida_left_bt, 0, wx.ALL, 5)

        bSizer21.Add(bSizer22, 0, wx.ALIGN_CENTER_VERTICAL, 5)

        self.item_client_take = wx.ListCtrl(self.salida_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                            wx.LC_REPORT | wx.LC_SINGLE_SEL)
        bSizer21.Add(self.item_client_take, 1, wx.ALL | wx.EXPAND, 5)

        self.salida_panel.SetSizer(bSizer21)
        self.salida_panel.Layout()
        bSizer21.Fit(self.salida_panel)
        self.m_notebook3.AddPage(self.salida_panel, u"Salida", False)
        self.dev_panel = wx.Panel(self.m_notebook3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer24 = wx.BoxSizer(wx.HORIZONTAL)

        self.item_dev_list = wx.ListCtrl(self.dev_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                         wx.LC_REPORT | wx.LC_SINGLE_SEL)
        bSizer24.Add(self.item_dev_list, 1, wx.ALL | wx.EXPAND, 5)

        bSizer25 = wx.BoxSizer(wx.VERTICAL)

        self.dev_left_bt = wx.Button(self.dev_panel, wx.ID_ANY, u"<", wx.DefaultPosition, wx.Size(30, 30), 0)
        bSizer25.Add(self.dev_left_bt, 0, wx.ALL, 5)

        self.dev_right_bt = wx.Button(self.dev_panel, wx.ID_ANY, u">", wx.DefaultPosition, wx.Size(30, 30), 0)
        bSizer25.Add(self.dev_right_bt, 0, wx.ALL, 5)

        bSizer24.Add(bSizer25, 0, wx.ALIGN_CENTER_VERTICAL, 5)

        self.item_client_has = wx.ListCtrl(self.dev_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                           wx.LC_REPORT | wx.LC_SINGLE_SEL)
        bSizer24.Add(self.item_client_has, 1, wx.ALL | wx.EXPAND, 5)

        self.dev_panel.SetSizer(bSizer24)
        self.dev_panel.Layout()
        bSizer24.Fit(self.dev_panel)
        self.m_notebook3.AddPage(self.dev_panel, u"Devolucion", True)

        bSizer19.Add(self.m_notebook3, 1, wx.EXPAND | wx.ALL, 5)

        bSizer23 = wx.BoxSizer(wx.HORIZONTAL)

        self.on_button = wx.Button(self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer23.Add(self.on_button, 0, wx.ALL, 5)

        self.cancel_button = wx.Button(self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer23.Add(self.cancel_button, 0, wx.ALL, 5)

        bSizer19.Add(bSizer23, 0, wx.ALIGN_RIGHT, 5)

        self.SetSizer(bSizer19)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.client_cb.Bind(wx.EVT_CHOICE, self.client_cb_change)
        self.item_left_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.salida_add_click)
        self.salida_right_bt.Bind(wx.EVT_BUTTON, self.salida_add_click)
        self.salida_left_bt.Bind(wx.EVT_BUTTON, self.salida_del_click)
        self.item_client_take.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.item_client_take_click)
        self.item_dev_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.item_dev_list_click)
        self.dev_left_bt.Bind(wx.EVT_BUTTON, self.dev_add_click)
        self.dev_right_bt.Bind(wx.EVT_BUTTON, self.dev_del_click)
        self.item_client_has.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.dev_add_click)
        self.on_button.Bind(wx.EVT_BUTTON, self.ok_click)
        self.cancel_button.Bind(wx.EVT_BUTTON, self.cancel_click)

    def __del__(self):
        pass


    # Virtual event handlers, overide them in your derived class
    def client_cb_change(self, event):
        event.Skip()

    def salida_add_click(self, event):
        event.Skip()

    def salida_del_click(self, event):
        event.Skip()

    def item_client_take_click(self, event):
        event.Skip()

    def item_dev_list_click(self, event):
        event.Skip()

    def dev_add_click(self, event):
        event.Skip()

    def dev_del_click(self, event):
        event.Skip()

    def ok_click(self, event):
        event.Skip()

    def cancel_click(self, event):
        event.Skip()


###########################################################################
## Class EntityMove
###########################################################################

class EntityMove(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Cantidad", pos=wx.DefaultPosition,
                           size=wx.Size(500, 300), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer26 = wx.BoxSizer(wx.VERTICAL)

        fgSizer4 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer4.AddGrowableCol(1)
        fgSizer4.SetFlexibleDirection(wx.BOTH)
        fgSizer4.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText19 = wx.StaticText(self, wx.ID_ANY, u"Articulo", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText19.Wrap(-1)

        fgSizer4.Add(self.m_staticText19, 0, wx.ALL, 5)

        self.article_label = wx.StaticText(self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0)
        self.article_label.Wrap(-1)

        fgSizer4.Add(self.article_label, 1, wx.ALL | wx.EXPAND, 5)

        self.m_staticText21 = wx.StaticText(self, wx.ID_ANY, u"Procedencia", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText21.Wrap(-1)

        fgSizer4.Add(self.m_staticText21, 0, wx.ALL, 5)

        self.proc_label = wx.StaticText(self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0)
        self.proc_label.Wrap(-1)

        fgSizer4.Add(self.proc_label, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText23 = wx.StaticText(self, wx.ID_ANY, u"Cantidad", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText23.Wrap(-1)

        fgSizer4.Add(self.m_staticText23, 0, wx.ALL, 5)

        self.cant_txt = wx.SpinCtrl(self, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 10,
                                    0)
        fgSizer4.Add(self.cant_txt, 0, wx.ALL, 5)

        self.m_staticText24 = wx.StaticText(self, wx.ID_ANY, u"Observaciones", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText24.Wrap(-1)

        fgSizer4.Add(self.m_staticText24, 0, wx.ALL, 5)

        self.observaciones_txt = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                             wx.TE_MULTILINE)
        self.observaciones_txt.SetMinSize(wx.Size(-1, 100))

        fgSizer4.Add(self.observaciones_txt, 1, wx.ALL | wx.EXPAND, 5)

        bSizer26.Add(fgSizer4, 1, wx.ALL | wx.EXPAND, 5)

        bSizer27 = wx.BoxSizer(wx.HORIZONTAL)

        self.ok_button = wx.Button(self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer27.Add(self.ok_button, 0, wx.ALL, 5)

        self.cancel_button = wx.Button(self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer27.Add(self.cancel_button, 0, wx.ALL, 5)

        bSizer26.Add(bSizer27, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.SetSizer(bSizer26)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.ok_button.Bind(wx.EVT_BUTTON, self.ok_button_click)
        self.cancel_button.Bind(wx.EVT_BUTTON, self.cancel_button_click)

    def __del__(self):
        pass


    # Virtual event handlers, overide them in your derived class
    def ok_button_click(self, event):
        event.Skip()

    def cancel_button_click(self, event):
        event.Skip()


###########################################################################
## Class VentaDialog
###########################################################################

class VentaDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Venta", pos=wx.DefaultPosition, size=wx.Size(777, 700),
                           style=wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer27 = wx.BoxSizer(wx.VERTICAL)

        bSizer28 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText24 = wx.StaticText(self, wx.ID_ANY, u"Cliente", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText24.Wrap(-1)

        bSizer28.Add(self.m_staticText24, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        client_cbChoices = []
        self.client_cb = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, client_cbChoices, 0)
        self.client_cb.SetSelection(0)
        bSizer28.Add(self.client_cb, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.add_client_button = wx.Button(self, wx.ID_ANY, u"+", wx.DefaultPosition, wx.Size(30, 30), 0)
        bSizer28.Add(self.add_client_button, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.date_cb = wx.adv.DatePickerCtrl(self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize,
                                             wx.adv.DP_DEFAULT)
        bSizer28.Add(self.date_cb, 1, wx.ALL, 5)

        bSizer27.Add(bSizer28, 0, wx.ALL | wx.EXPAND, 5)

        bSizer30 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer31 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText28 = wx.StaticText(self, wx.ID_ANY, u"Articulo", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText28.Wrap(-1)

        bSizer31.Add(self.m_staticText28, 0, wx.ALL, 5)

        self.item_tabs = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.tiene_panel = wx.Panel(self.item_tabs, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer35 = wx.BoxSizer(wx.VERTICAL)

        self.list_client_has = wx.ListCtrl(self.tiene_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                           wx.LC_REPORT | wx.LC_SINGLE_SEL)
        bSizer35.Add(self.list_client_has, 1, wx.ALL | wx.EXPAND, 5)

        self.tiene_panel.SetSizer(bSizer35)
        self.tiene_panel.Layout()
        bSizer35.Fit(self.tiene_panel)
        self.item_tabs.AddPage(self.tiene_panel, u"Stock Cliente", True)
        self.left_panel = wx.Panel(self.item_tabs, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer36 = wx.BoxSizer(wx.VERTICAL)

        self.list_item_left = wx.ListCtrl(self.left_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                          wx.LC_REPORT | wx.LC_SINGLE_SEL)
        bSizer36.Add(self.list_item_left, 1, wx.ALL | wx.EXPAND, 5)

        self.left_panel.SetSizer(bSizer36)
        self.left_panel.Layout()
        bSizer36.Fit(self.left_panel)
        self.item_tabs.AddPage(self.left_panel, u"Stock Almacen", False)

        bSizer31.Add(self.item_tabs, 1, wx.EXPAND | wx.ALL, 5)

        bSizer30.Add(bSizer31, 1, wx.EXPAND, 5)

        bSizer38 = wx.BoxSizer(wx.VERTICAL)

        self.add_sale_button = wx.Button(self, wx.ID_ANY, u">", wx.DefaultPosition, wx.Size(30, 30), 0)
        bSizer38.Add(self.add_sale_button, 0, wx.ALL, 5)

        self.del_sale_button = wx.Button(self, wx.ID_ANY, u"<", wx.DefaultPosition, wx.Size(30, 30), 0)
        bSizer38.Add(self.del_sale_button, 0, wx.ALL, 5)

        bSizer30.Add(bSizer38, 0, wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer32 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText29 = wx.StaticText(self, wx.ID_ANY, u"A Pagar", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText29.Wrap(-1)

        bSizer32.Add(self.m_staticText29, 0, wx.ALL, 5)

        self.list_client_paid = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT)
        bSizer32.Add(self.list_client_paid, 1, wx.ALL | wx.EXPAND, 5)

        bSizer34 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText30 = wx.StaticText(self, wx.ID_ANY, u"Total:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText30.Wrap(-1)

        bSizer34.Add(self.m_staticText30, 0, wx.ALL, 5)

        self.total_label = wx.StaticText(self, wx.ID_ANY, u"$0.00", wx.DefaultPosition, wx.DefaultSize, 0)
        self.total_label.Wrap(-1)

        bSizer34.Add(self.total_label, 1, wx.ALL, 5)

        bSizer32.Add(bSizer34, 0, wx.EXPAND, 5)

        bSizer30.Add(bSizer32, 1, wx.EXPAND, 5)

        bSizer27.Add(bSizer30, 1, wx.EXPAND, 5)

        bSizer33 = wx.BoxSizer(wx.HORIZONTAL)

        self.ok_button = wx.Button(self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer33.Add(self.ok_button, 0, wx.ALL, 5)

        self.cancel_button = wx.Button(self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer33.Add(self.cancel_button, 0, wx.ALL, 5)

        bSizer27.Add(bSizer33, 0, wx.ALIGN_RIGHT, 5)

        self.SetSizer(bSizer27)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.client_cb.Bind(wx.EVT_CHOICE, self.client_cb_change)
        self.add_client_button.Bind(wx.EVT_BUTTON, self.add_client_click)
        self.list_client_has.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.add_sale_click)
        self.list_item_left.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.add_sale_click)
        self.add_sale_button.Bind(wx.EVT_BUTTON, self.add_sale_click)
        self.del_sale_button.Bind(wx.EVT_BUTTON, self.del_sale_click)
        self.list_client_paid.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.edit_sale_click)
        self.ok_button.Bind(wx.EVT_BUTTON, self.ok_button_click)
        self.cancel_button.Bind(wx.EVT_BUTTON, self.cancel_button_click)

    def __del__(self):
        pass


    # Virtual event handlers, overide them in your derived class
    def client_cb_change(self, event):
        event.Skip()

    def add_client_click(self, event):
        event.Skip()

    def add_sale_click(self, event):
        event.Skip()

    def del_sale_click(self, event):
        event.Skip()

    def edit_sale_click(self, event):
        event.Skip()

    def ok_button_click(self, event):
        event.Skip()

    def cancel_button_click(self, event):
        event.Skip()


###########################################################################
## Class VentaItemDialog
###########################################################################

class VentaItemDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Detalle", pos=wx.DefaultPosition, size=wx.Size(-1, -1),
                           style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.Size(500, -1), wx.DefaultSize)

        bSizer39 = wx.BoxSizer(wx.VERTICAL)

        fgSizer5 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer5.AddGrowableCol(1)
        fgSizer5.SetFlexibleDirection(wx.BOTH)
        fgSizer5.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText32 = wx.StaticText(self, wx.ID_ANY, u"Procedencia", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText32.Wrap(-1)

        fgSizer5.Add(self.m_staticText32, 0, wx.ALL, 5)

        self.procedencia_label = wx.StaticText(self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0)
        self.procedencia_label.Wrap(-1)

        fgSizer5.Add(self.procedencia_label, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText34 = wx.StaticText(self, wx.ID_ANY, u"Articulo", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText34.Wrap(-1)

        fgSizer5.Add(self.m_staticText34, 0, wx.ALL, 5)

        self.item_label = wx.StaticText(self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0)
        self.item_label.Wrap(-1)

        fgSizer5.Add(self.item_label, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText36 = wx.StaticText(self, wx.ID_ANY, u"Cantidad", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText36.Wrap(-1)

        fgSizer5.Add(self.m_staticText36, 0, wx.ALL, 5)

        self.cantidad_txt = wx.SpinCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                        wx.SP_ARROW_KEYS, 1, 10, 0)
        fgSizer5.Add(self.cantidad_txt, 1, wx.ALL | wx.EXPAND, 5)

        self.m_staticText37 = wx.StaticText(self, wx.ID_ANY, u"Precio", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText37.Wrap(-1)

        fgSizer5.Add(self.m_staticText37, 0, wx.ALL, 5)

        self.precio_txt = wx.SpinCtrlDouble(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                            wx.SP_ARROW_KEYS, 0.1, 100, 0, 1)
        self.precio_txt.SetDigits(2)
        fgSizer5.Add(self.precio_txt, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText38 = wx.StaticText(self, wx.ID_ANY, u"Observaciones", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText38.Wrap(-1)

        fgSizer5.Add(self.m_staticText38, 0, wx.ALL, 5)

        self.observaciones_txt = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(-1, 100),
                                             wx.TE_MULTILINE)
        fgSizer5.Add(self.observaciones_txt, 0, wx.ALL | wx.EXPAND, 5)

        bSizer39.Add(fgSizer5, 1, wx.EXPAND, 5)

        bSizer40 = wx.BoxSizer(wx.HORIZONTAL)

        self.ok_button = wx.Button(self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer40.Add(self.ok_button, 0, wx.ALL, 5)

        self.cancel_button = wx.Button(self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer40.Add(self.cancel_button, 0, wx.ALL, 5)

        bSizer39.Add(bSizer40, 0, wx.ALIGN_RIGHT, 5)

        self.SetSizer(bSizer39)
        self.Layout()
        bSizer39.Fit(self)

        self.Centre(wx.BOTH)

        # Connect Events
        self.cantidad_txt.Bind(wx.EVT_SPINCTRL, self.cantidad_change_value)
        self.cantidad_txt.Bind(wx.EVT_TEXT, self.cantidad_change_value)
        self.cantidad_txt.Bind(wx.EVT_TEXT_ENTER, self.cantidad_change_value)
        self.ok_button.Bind(wx.EVT_BUTTON, self.ok_click)
        self.cancel_button.Bind(wx.EVT_BUTTON, self.cancel_click)

    def __del__(self):
        pass


    # Virtual event handlers, overide them in your derived class
    def cantidad_change_value(self, event):
        event.Skip()

    def ok_click(self, event):
        event.Skip()

    def cancel_click(self, event):
        event.Skip()


###########################################################################
## Class GastoDialog
###########################################################################

class GastoDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Gastos", pos=wx.DefaultPosition, size=wx.DefaultSize,
                           style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.Size(500, -1), wx.DefaultSize)

        bSizer39 = wx.BoxSizer(wx.VERTICAL)

        fgSizer6 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer6.AddGrowableCol(1)
        fgSizer6.SetFlexibleDirection(wx.BOTH)
        fgSizer6.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.procedencia = wx.StaticText(self, wx.ID_ANY, u"Procedencia", wx.DefaultPosition, wx.DefaultSize, 0)
        self.procedencia.Wrap(-1)

        fgSizer6.Add(self.procedencia, 0, wx.ALL, 5)

        procedencia_txtChoices = []
        self.procedencia_txt = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, procedencia_txtChoices, 0)
        self.procedencia_txt.SetSelection(0)
        fgSizer6.Add(self.procedencia_txt, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText38 = wx.StaticText(self, wx.ID_ANY, u"cantidad", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText38.Wrap(-1)

        fgSizer6.Add(self.m_staticText38, 0, wx.ALL, 5)

        self.cantidad_txt = wx.SpinCtrlDouble(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                              wx.SP_ARROW_KEYS, 0, 100, 0, 1)
        self.cantidad_txt.SetDigits(2)
        fgSizer6.Add(self.cantidad_txt, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText39 = wx.StaticText(self, wx.ID_ANY, u"Descripcion", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText39.Wrap(-1)

        fgSizer6.Add(self.m_staticText39, 0, wx.ALL, 5)

        self.descripcion_txt = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(-1, 100),
                                           wx.TE_MULTILINE)
        fgSizer6.Add(self.descripcion_txt, 0, wx.ALL | wx.EXPAND, 5)

        bSizer39.Add(fgSizer6, 1, wx.ALL | wx.EXPAND, 5)

        bSizer40 = wx.BoxSizer(wx.HORIZONTAL)

        self.add_button = wx.Button(self, wx.ID_ANY, u"+", wx.DefaultPosition, wx.Size(30, 30), 0)
        bSizer40.Add(self.add_button, 0, wx.ALL, 5)

        self.del_button = wx.Button(self, wx.ID_ANY, u"-", wx.DefaultPosition, wx.Size(30, 30), 0)
        bSizer40.Add(self.del_button, 0, wx.ALL, 5)

        bSizer39.Add(bSizer40, 0, wx.ALIGN_CENTER, 5)

        self.gasto_list = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                      wx.LC_REPORT | wx.LC_SINGLE_SEL)
        bSizer39.Add(self.gasto_list, 0, wx.ALL | wx.EXPAND, 5)

        bSizer41 = wx.BoxSizer(wx.HORIZONTAL)

        self.ol_button = wx.Button(self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer41.Add(self.ol_button, 0, wx.ALL, 5)

        bSizer39.Add(bSizer41, 0, wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetSizer(bSizer39)
        self.Layout()
        bSizer39.Fit(self)

        self.Centre(wx.BOTH)

        # Connect Events
        self.procedencia_txt.Bind(wx.EVT_CHOICE, self.procedencia_change)
        self.add_button.Bind(wx.EVT_BUTTON, self.add_button_click)
        self.del_button.Bind(wx.EVT_BUTTON, self.del_button_click)
        self.gasto_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.gasto_list_click)
        self.ol_button.Bind(wx.EVT_BUTTON, self.ok_button_click)

    def __del__(self):
        pass


    # Virtual event handlers, overide them in your derived class
    def procedencia_change(self, event):
        event.Skip()

    def add_button_click(self, event):
        event.Skip()

    def del_button_click(self, event):
        event.Skip()

    def gasto_list_click(self, event):
        event.Skip()

    def ok_button_click(self, event):
        event.Skip()


###########################################################################
## Class ClienteMovVenta
###########################################################################

class ClienteMovVenta(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Movimientos cliente", pos=wx.DefaultPosition,
                           size=wx.Size(727, 767),
                           style=wx.CLOSE_BOX | wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER)

        self.SetSizeHints(wx.Size(500, -1), wx.DefaultSize)

        bSizer42 = wx.BoxSizer(wx.VERTICAL)

        bSizer43 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText40 = wx.StaticText(self, wx.ID_ANY, u"Cliente", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText40.Wrap(-1)

        bSizer43.Add(self.m_staticText40, 0, wx.ALL, 5)

        cliente_cbChoices = []
        self.cliente_cb = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cliente_cbChoices, 0)
        self.cliente_cb.SetSelection(0)
        bSizer43.Add(self.cliente_cb, 1, wx.ALL, 5)

        bSizer42.Add(bSizer43, 0, wx.EXPAND, 5)

        self.m_staticText41 = wx.StaticText(self, wx.ID_ANY, u"Stock Cliente", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText41.Wrap(-1)

        bSizer42.Add(self.m_staticText41, 0, wx.ALL, 5)

        self.cliente_item_list = CustomListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                                wx.LC_REPORT | wx.LC_SINGLE_SEL)
        bSizer42.Add(self.cliente_item_list, 0, wx.ALL | wx.EXPAND, 5)

        bSizer44 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText42 = wx.StaticText(self, wx.ID_ANY, u"Desde", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText42.Wrap(-1)

        bSizer44.Add(self.m_staticText42, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.from_date = wx.adv.DatePickerCtrl(self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize,
                                               wx.adv.DP_DEFAULT)
        bSizer44.Add(self.from_date, 1, wx.ALL, 5)

        self.m_staticText43 = wx.StaticText(self, wx.ID_ANY, u"Hasta", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText43.Wrap(-1)

        bSizer44.Add(self.m_staticText43, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.to_date = wx.adv.DatePickerCtrl(self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize,
                                             wx.adv.DP_DEFAULT)
        bSizer44.Add(self.to_date, 1, wx.ALL, 5)

        bSizer42.Add(bSizer44, 0, wx.EXPAND, 5)

        self.m_splitter2 = wx.SplitterWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                             wx.SP_3D | wx.SP_BORDER | wx.SP_LIVE_UPDATE)
        self.m_splitter2.SetSashGravity(0.5)
        self.m_splitter2.Bind(wx.EVT_IDLE, self.m_splitter2OnIdle)

        self.m_panel8 = wx.Panel(self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer46 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText44 = wx.StaticText(self.m_panel8, wx.ID_ANY, u"Movimientos", wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.m_staticText44.Wrap(-1)

        bSizer46.Add(self.m_staticText44, 0, wx.ALL, 5)

        self.cliente_mov_list = CustomListCtrl(self.m_panel8, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                               wx.LC_REPORT | wx.LC_SINGLE_SEL)
        bSizer46.Add(self.cliente_mov_list, 1, wx.ALL | wx.EXPAND, 5)

        self.m_panel8.SetSizer(bSizer46)
        self.m_panel8.Layout()
        bSizer46.Fit(self.m_panel8)
        self.m_panel7 = wx.Panel(self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer47 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText45 = wx.StaticText(self.m_panel7, wx.ID_ANY, u"Articulos", wx.DefaultPosition, wx.DefaultSize,
                                            0)
        self.m_staticText45.Wrap(-1)

        bSizer47.Add(self.m_staticText45, 0, wx.ALL, 5)

        self.cliente_mov_items_list = CustomListCtrl(self.m_panel7, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                                     wx.LC_REPORT | wx.LC_SINGLE_SEL)
        bSizer47.Add(self.cliente_mov_items_list, 1, wx.ALL | wx.EXPAND, 5)

        self.m_panel7.SetSizer(bSizer47)
        self.m_panel7.Layout()
        bSizer47.Fit(self.m_panel7)
        self.m_splitter2.SplitVertically(self.m_panel8, self.m_panel7, 330)
        bSizer42.Add(self.m_splitter2, 1, wx.EXPAND, 5)

        self.m_staticText451 = wx.StaticText(self, wx.ID_ANY, u"Ventas", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText451.Wrap(-1)

        bSizer42.Add(self.m_staticText451, 0, wx.ALL, 5)

        self.cliente_venta_list = CustomListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                                 wx.LC_REPORT | wx.LC_SINGLE_SEL)
        bSizer42.Add(self.cliente_venta_list, 0, wx.ALL | wx.EXPAND, 5)

        self.ok_button = wx.Button(self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer42.Add(self.ok_button, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        self.SetSizer(bSizer42)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.cliente_cb.Bind(wx.EVT_CHOICE, self.cliente_change)
        self.from_date.Bind(wx.adv.EVT_DATE_CHANGED, self.from_date_change)
        self.to_date.Bind(wx.adv.EVT_DATE_CHANGED, self.to_date_change)
        self.cliente_mov_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.cliente_mov_selected)
        self.ok_button.Bind(wx.EVT_BUTTON, self.ok_button_click)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def cliente_change(self, event):
        event.Skip()

    def from_date_change(self, event):
        event.Skip()

    def to_date_change(self, event):
        event.Skip()

    def cliente_mov_selected(self, event):
        event.Skip()

    def ok_button_click(self, event):
        event.Skip()

    def m_splitter2OnIdle(self, event):
        self.m_splitter2.SetSashPosition(330)
        self.m_splitter2.Unbind(wx.EVT_IDLE)


###########################################################################
## Class UpdateDialog
###########################################################################

class UpdateDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Actualizando", pos=wx.DefaultPosition,
                           size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE | wx.STAY_ON_TOP)

        self.SetSizeHints(wx.Size(500, 100), wx.DefaultSize)

        bSizer47 = wx.BoxSizer(wx.VERTICAL)

        bSizer48 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText46 = wx.StaticText(self, wx.ID_ANY, u"Estado:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText46.Wrap(-1)

        bSizer48.Add(self.m_staticText46, 0, wx.ALL, 5)

        self.status_label = wx.StaticText(self, wx.ID_ANY, u"Estado", wx.DefaultPosition, wx.DefaultSize, 0)
        self.status_label.Wrap(-1)

        bSizer48.Add(self.status_label, 1, wx.ALL | wx.EXPAND, 5)

        bSizer47.Add(bSizer48, 0, wx.EXPAND, 5)

        self.progress_bar = wx.Gauge(self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize,
                                     wx.GA_HORIZONTAL | wx.GA_SMOOTH)
        self.progress_bar.SetValue(50)
        bSizer47.Add(self.progress_bar, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(bSizer47)
        self.Layout()
        bSizer47.Fit(self)

        self.Centre(wx.BOTH)

    def __del__(self):
        pass

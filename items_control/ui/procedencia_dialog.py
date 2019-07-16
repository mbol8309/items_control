from items_control.ui.design_wx import items_control_wx as design_wx
from items_control.data import db
from items_control import orm
from items_control import utils
import datetime
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

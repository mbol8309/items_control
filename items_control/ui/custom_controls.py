from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
import wx


# custom classess

class CustomListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        ListCtrlAutoWidthMixin.__init__(self)

        # values to work with
        self.custom_colums = {}
        self.custom_item_id = {}
        self.data = None

    def ConfigColums(self, columns):
        self.custom_colums = columns
        self.DeleteAllColumns()

        idx = 0
        for c in columns:
            self.custom_colums[idx] = c
            self.InsertColumn(idx, c)
            idx += 1

        table_width = self.GetSize()[0]  # GetSize returns (width, height) tuple
        num_col = self.GetColumnCount()
        col_width = table_width / num_col
        for i in range(0, num_col):
            self.SetColumnWidth(i, col_width)

    def SetData(self, data, functions):
        if not isinstance(data, list) or not isinstance(functions, list) \
                or not len(functions) == self.GetColumnCount():
            return None

        # self.data = data
        self.functions = functions
        self.UpdateData(data)

    def SetLambdas(self, functions):
        if not isinstance(functions, list) \
                or not len(functions) == self.GetColumnCount():
            return None
        self.functions = functions

    def UpdateData(self, data):

        if not isinstance(data, list):
            return None

        # self.data = data
        self.DeleteAllItems()
        self.custom_item_id = {}
        functions = self.functions

        idx = 0
        for d in data:
            d.custom_id = id(d)
            index = self.InsertItem(idx, functions[0](d))
            for f in range(1, len(functions)):
                self.SetItem(index, f, functions[f](d))
            self.SetItemData(index, d.custom_id)
            self.custom_item_id[d.custom_id] = d
            idx += 1

    def GetItem(self, index):
        if index >= 0 and index < self.GetItemCount():
            return self.custom_item_id[self.GetItemData(index)]
        return None

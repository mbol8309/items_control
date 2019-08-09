from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
from wx.lib.mixins.listctrl import ColumnSorterMixin
import wx


# custom classess

class CustomChoice(wx.Choice):
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, choices=[], style=0):
        wx.Choice.__init__(self, parent, id, pos, size, choices, style)

        self.custom_item_id = {}
        self.function = None

    def SetLambda(self, l):
        self.function = l

    def UpdateData(self, data):
        if not isinstance(data, list):
            return None
        self.Clear()
        self.custom_item_id = {}
        for d in data:
            d.custom_id = id(d)
            index = self.Append(self.function(d))
            self.SetClientData(index, d.custom_id)
            self.custom_item_id[d.custom_id] = d
        self.SetSelection(0)

    def GetItems(self):
        result = []
        for i in self.custom_item_id:
            result.append(self.custom_item_id[i])
        return result

    def GetItem(self, index):
        if index >= 0 and index < self.GetCount():
            return self.custom_item_id[self.GetClientData(index)]
        return None

    def GetActiveItem(self):
        return self.custom_item_id[self.GetClientData(self.GetSelection())]

class CustomListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        ListCtrlAutoWidthMixin.__init__(self)

        # values to work with
        self.custom_colums = {}
        self.custom_item_id = {}
        self.data = None

    def ConfigColumns(self, columns):
        self.custom_colums = columns

        # ColumnSorterMixin.__init__(self, len(columns))
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

    # def SetData(self, data, functions):
    #     if not isinstance(data, list) or not isinstance(functions, list) \
    #             or not len(functions) == self.GetColumnCount():
    #         return None
    #
    #     # self.data = data
    #     self.functions = functions
    #     self.UpdateData(data)

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

    def AppendData(self, item):
        index = self.GetItemCount()
        item.custom_id = id(item)
        functions = self.functions
        index = self.InsertItem(index, functions[0](item))
        for f in range(1, len(functions)):
            self.SetItem(index, f, functions[f](item))
        self.SetItemData(index, item.custom_id)
        self.custom_item_id[item.custom_id] = item

    def GetItem(self, index):
        if index >= 0 and index < self.GetItemCount():
            return self.custom_item_id[self.GetItemData(index)]
        return None

    def GetItems(self):
        result = []
        for i in self.custom_item_id:
            result.append(self.custom_item_id[i])
        return result

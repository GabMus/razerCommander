from . import kblayouts
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gdk


class RKeyboardKey:
    label = ''
    color = Gdk.RGBA(0, 0, 0)
    isGhost = False
    x = -1
    y = -1

    def __init__(self, label, x, y):
        if label in [kblayouts.GHOST, kblayouts.INV_GHOST]:
            self.isGhost = True
        self.label = label
        self.x = x
        self.y = y

    def __str__(self):
        return self.label + self.color.to_string()


class RKeyboardRow:
    keylist = []
    rowindex = -1

    def __init__(self, rowarr, index):
        self.rowindex = index
        self.keylist = []
        cx = 0
        for key in rowarr:
            self.keylist.append(RKeyboardKey(key, cx, index))
            cx += 1

    def getKey(self, index):
        return self.keylist[index]


class RKeyboard:
    layout = 'ansi_us'
    layoutList = None
    rows = []

    def __init__(self, layout):
        # self.layout=layout
        self.layout = 'ansi_us'
        self.layoutList = kblayouts.layouts[layout]
        index = 0
        self.rows = []
        for row in self.layoutList:
            self.rows.append(RKeyboardRow(row, index))
            index += 1

    def getKey(self, x, y):
        row = self.rows[y]
        key = row.getKey(x)
        return key

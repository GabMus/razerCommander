import kblayouts


class RKeyboardKey:
    label = ''
    color = '000000'
    isGhost = False

    def __init__(self, label):
        if label in [kblayouts.GHOST, kblayouts.INV_GHOST]:
            self.isGhost = True
        self.label = label

    def __str__(self):
        return label


class RKeyboardRow:
    keylist = []
    rowindex = -1

    def __init__(self, rowarr, index):
        self.rowindex = index
        self.keylist = []
        for key in rowarr:
            self.keylist.append(RKeyboardKey(key))

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

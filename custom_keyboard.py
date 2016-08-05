import kblayouts

class RKeyboardKey:
    label=''
    color='000000'
    def __init__(self, label):
        self.label=label

    def __str__(self):
        return label

class RKeyboardRow:
    keylist=[]
    rowindex=-1
    def __init__(self, rowarr, index):

    def getKey(self, index):
        return self.keylist[index]

class RKyeboard:
    layout='ansi_us'
    layoutList=None
    rows=[]

    def populateRows(self):
        index=0
        self.rows=[]
        for row in self.layoutList:
            self.rows.append(RKeyboardRow(row, index))
            index+=1

    def __init__(self, layout):
        #self.layout=layout
        self.layout='ansi_us'
        self.layoutList=kblayouts.layouts[layout]
        self.populateRows()

    def getKey(self, x, y):
        row=self.rows[y]
        key=row.getKey(x)
        return key

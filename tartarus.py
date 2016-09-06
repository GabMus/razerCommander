import os
import json

HOME = os.environ.get('HOME')
CONFDIR = HOME+('/.config/razercommander')
TARTARUS_SHORTCTUCTS_FILE = CONFDIR+('/tartarus_shortcuts')

KEYS=[
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    '10',
    '11',
    '12',
    '13',
    '14',
    '15',
    'MODE_SWITCH',
    'THUMB',
    'UP',
    'RIGHT',
    'DOWN',
    'LEFT'
]

shortcuts = {
    '1':'',
    '2':'',
    '3':'',
    '4':'',
    '5':'',
    '6':'',
    '7':'',
    '8':'',
    '9':'',
    '10':'',
    '11':'',
    '12':'',
    '13':'',
    '14':'',
    '15':'',
    'MODE_SWITCH':'',
    'THUMB':'',
    'UP':'',
    'RIGHT':'',
    'DOWN':'',
    'LEFT':''
}


def checkPath():
    if not os.path.isdir(CONFDIR):
        os.makedirs(CONFDIR)
    if not os.path.isfile(TARTARUS_SHORTCTUCTS_FILE):
        out=open(TARTARUS_SHORTCTUCTS_FILE, 'w')
        out.write(json.dumps(shortcuts))
        out.close()

checkPath()
shortcutsF=open(TARTARUS_SHORTCTUCTS_FILE,'r')
try:
    shortcutsText=shortcutsF.read()
    shortcuts=json.loads(shortcutsText)
    shortcutsF.close()
except ValueError:
    shortcutsF.close()
    shortcutsF=open(TARTARUS_SHORTCTUCTS_FILE,'w')
    shortcutsF.write(json.dumps(shortcuts))
    shortcutsF.close()

def saveConfig():
    checkPath()
    out=open(TARTARUS_SHORTCTUCTS_FILE, 'w')
    out.write(json.dumps(shortcuts))
    out.close()

def addShortcut(key, command):
    if type(key) is int:
        key=str(key)
    if key in shortcuts.keys():
        shortcuts[key]=command
        saveConfig()

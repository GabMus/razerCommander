import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Gdk
import os
import json

HOME = os.environ.get('HOME')
CONFDIR = HOME+('/.config/razercommander')
PROFILESFILE = CONFDIR+('/profiles')

blackProfile={
    'name': 'Empty',
    'colors': [
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ]
}


profiles=[blackProfile,]

if not os.path.isdir(CONFDIR):
    os.makedirs(CONFDIR)

if not os.path.isfile(PROFILESFILE):
    out=open(PROFILESFILE, 'w')
    out.write(json.dumps(profiles))
    out.close()

profilesF=open(PROFILESFILE,'r')

try:
    profilesText=profilesF.read()
    profiles=json.loads(profilesText)
    profilesF.close()
except ValueError:
    profilesF.close()
    profilesF=open(PROFILESFILE,'w')
    profilesF.write(json.dumps(profiles))
    profilesF.close()


def makeProfile(name, rkb):
    profile={'name': name, 'colors':[]}
    for row in rkb.rows:
        for key in row.keylist:
            if not key.isGhost:
                color = Gdk.RGBA()
                color.parse('#'+key.color)
                profile['colors'].append(
                    [
                        color.red,
                        color.green,
                        color.blue
                    ]
                )
    return profile

def saveProfiles():
    profilesF=open(PROFILESFILE,'w')
    profilesF.write(json.dumps(profiles))
    profilesF.close()

def getProfile(name):
    for p in profiles:
        if p['name']==name:
            return p

def addProfile(p):
    if p['name'] and p['colors']:
        for i in profiles:
            if i['name']==p['name']:
                print('Profile '+p['name']+' already exists')
                return False
        profiles.append(p)
        saveProfiles()
        return True
    else:
        print('Invalid profile')
        return False

def removeProfile(name):
    for i in profiles:
        if i['name']==name:
            profiles.remove(i)
            saveProfiles()
            return True
    else:
        print('Profile '+name+' doesn\'t exist')
        return False

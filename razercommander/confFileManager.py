import os
import json

HOME = os.environ.get('HOME')
CONFDIR = '{0}/.config/razercommander/'.format(HOME)

if 'XDG_RUNTIME_DIR' in os.environ.keys():
    if os.path.isfile('{0}/flatpak-info'.format(os.environ['XDG_RUNTIME_DIR'])):
        CONFDIR = '{0}/razercommander/'.format(os.environ.get('XDG_CONFIG_HOME'))


def check_path(path):
    complete_path = CONFDIR+path
    if not os.path.isdir(CONFDIR):
        os.makedirs(CONFDIR)
    if not os.path.isfile(complete_path):
        out = open(complete_path, 'w')
        out.write(json.dumps({}))
        out.close()


def load_file(path, default):
    complete_path = CONFDIR+path
    mfile = open(complete_path, 'r')
    to_ret = default
    try:
        mfile_txt = mfile.read()
        to_ret = json.loads(mfile_txt)
        mfile.close()
    except ValueError:
        mfile.close()
        mfile = open(complete_path, 'w')
        mfile.write(json.dumps(default))
        mfile.close()
    finally:
        return to_ret


def save_file(path, value):
    # print(value)
    complete_path = CONFDIR + path
    check_path(path)
    out = open(complete_path, 'w')
    out.write(json.dumps(value))
    out.close()

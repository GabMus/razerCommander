CONF_FILE_PATH='macro_logic.json'
from .devicesMacroKeys import *
from . import listboxHelper
from . import confFileManager
macros_conf_loaded={}
confFileManager.check_path(CONF_FILE_PATH)
macros_conf_loaded=confFileManager.load_file(CONF_FILE_PATH, macros_conf_loaded)

class MacroDevice:
    def __init__(self, macrokey_arr, device_uid, device):
        self.macrokey_arr = macrokey_arr
        self.device_uid = device_uid
        self.device = device
        self.set_all_current_macros()

    def get_key(self, key_n):
        for k in self.macrokey_arr:
            if key_n == k.key:
                return k
        return None

    def set_macro(self, key, n_macro):
        key_obj=self.get_key(key)
        if not key_obj:
            raise ValueError("get_key() for key "+key+" returned None")
        macros_conf_loaded[self.device_uid][key]=n_macro
        key_obj._set_macro(self.device, n_macro)
        confFileManager.save_file(CONF_FILE_PATH, macros_conf_loaded)

    def set_all_current_macros(self):
        for key in self.macrokey_arr:
            key.set_current_macro(self.device)


class MacroKey:
    def __init__(self, key, macro=None):
        self.key = key
        self.macro = macro

    def _set_macro(self, device, n_macro):
        self.macro=n_macro
        if not n_macro:
            device.macro.del_macro(self.key)
            return
        script_macro=device.macro.create_script_macro_item(n_macro)
        # add macro doesn't append macros to the same key, it overwrites
        device.macro.add_macro(self.key, script_macro)

    def set_current_macro(self, device):
        self._set_macro(device, self.macro)

    def __repr__(self):
        return self.key


def make_shortcutslistbox_rows(m_dev):
    rowlist=[]
    for key in m_dev.macrokey_arr:
        rowlist.append(listboxHelper.make_2x_row(key.key, key.macro))
    return rowlist

def make_device(device_uid, device):
    if not device.name in macro_kls.keys(): # failsafe for unsupported devices
        return None
    mk_arr=[]
    if not device_uid in macros_conf_loaded.keys():
        macros_conf_loaded[device_uid] = dict()
        for key_n in macro_kls[device.name]:
            macros_conf_loaded[device_uid][key_n] = ''
        confFileManager.save_file(CONF_FILE_PATH, macros_conf_loaded)
    for key_n in macro_kls[device.name]:
        mk_arr.append(MacroKey(key_n, macros_conf_loaded[device_uid][key_n]))
    n_device = MacroDevice(mk_arr, device_uid, device)
    n_device.set_all_current_macros()
    return n_device

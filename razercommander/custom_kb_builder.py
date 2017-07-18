import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Gdk
from . import custom_keyboard as CustomKb
from . import custom_profiles

KEYCAP_SIZE = 40
rkb = None


def build_key_box(key, color, signal_handler):
    box = Gtk.EventBox()
    if not key.isGhost:
        box.get_style_context().add_class('keycap')
        key.color = color
        box.override_background_color(
            Gtk.StateType.NORMAL,
            color
        )
        label = Gtk.Label()
        label.set_text(key.label)
        box.add(label)
    box.keyx = key.x
    box.keyy = key.y
    if key.label in ['tab', 'lctrl', 'lalt', 'ralt', 'rctrl', '\\']:
        box.set_size_request(KEYCAP_SIZE * 1.5, KEYCAP_SIZE)
    elif key.label == 'capslk':
        box.set_size_request(KEYCAP_SIZE * 1.75, KEYCAP_SIZE)
    elif key.label == 'lshift':  # in ['lshift', 'ret']:
        box.set_size_request(KEYCAP_SIZE * 2.25, KEYCAP_SIZE)
    elif key.label == 'ret':
        box.set_size_request(KEYCAP_SIZE * 2.10, KEYCAP_SIZE)
    elif key.label == 'rshift':
        box.set_size_request(KEYCAP_SIZE * 2.75, KEYCAP_SIZE)
    elif key.label == 'bck\nspc':
        box.set_size_request(KEYCAP_SIZE * 2, KEYCAP_SIZE)
    elif key.label == 'spacebar':
        box.set_size_request(KEYCAP_SIZE * 6, KEYCAP_SIZE)
    elif key.label == CustomKb.kblayouts.INV_GHOST:
        box.set_size_request(0, 0)
        box.set_no_show_all(True)
        box.set_visible(False)
    elif key.label == CustomKb.kblayouts.GHOST:
        box.set_size_request(KEYCAP_SIZE, KEYCAP_SIZE)
    else:
        box.set_size_request(KEYCAP_SIZE, KEYCAP_SIZE)
    box.connect('button-press-event', signal_handler)
    return box


def build_keyrow_box(row, colors, signal_handler, prof_index):
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
    for key in row.keylist:
        if not key.isGhost:
            k_col = Gdk.RGBA(
                colors[prof_index][0],
                colors[prof_index][1],
                colors[prof_index][2]
            )
        else:
            k_col = Gdk.RGBA(0, 0, 0)
        keybox = build_key_box(
            key,
            k_col,
            signal_handler
        )
        if not key.isGhost:
            prof_index += 1
        box.pack_start(keybox, True, True, 0)
    return {'row': box, 'prof_index': prof_index}


def build_keyboard_box(box, colors, signal_handler, nrkb):
    global rkb
    rkb = nrkb
    # Empty keyboardBox
    if len(box.get_children()) >= 2:
        box.remove(box.get_children()[1])

    prof_index = 0
    kb_inner_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    for row in rkb.rows:
        rowbox_res = build_keyrow_box(row, colors, signal_handler, prof_index)
        rowbox = rowbox_res['row']
        prof_index = rowbox_res['prof_index']
        kb_inner_box.pack_start(rowbox, True, True, 0)
    box.pack_end(kb_inner_box, True, True, 0)
    kb_inner_box.show_all()
    return box

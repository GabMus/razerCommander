import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Gdk, GdkPixbuf

def make_image_row(text, img_path):
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
    label = Gtk.Label()
    label.set_text(text)
    icon = Gtk.Image()
    icon.set_from_file(img_path)
    label.set_margin_left(12)
    label.set_margin_right(12)
    box.pack_start(icon, False, False, 0)
    box.pack_start(label, False, False, 0)
    row = Gtk.ListBoxRow()
    row.add(box)
    return row

def make_row(text):
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
    label = Gtk.Label()
    label.set_text(text)
    label.set_margin_left(12)
    label.set_margin_right(12)
    box.set_margin_top(12)
    box.set_margin_bottom(12)
    box.pack_start(label, False, False, 0)
    row = Gtk.ListBoxRow()
    row.add(box)
    return row

def empty_listbox(listbox):
    while True:
        row = listbox.get_row_at_index(0)
        if row:
            listbox.remove(row)
        else:
            break

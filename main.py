#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Gdk
import os
import sys
import device
import custom_keyboard as CustomKb
import custom_profiles
import listboxHelper
import custom_kb_builder

EXEC_FOLDER = os.path.realpath(os.path.dirname(__file__)) + "/"
builder = Gtk.Builder()
builder.add_from_file(EXEC_FOLDER + "ui.glade")
HOME = os.environ.get('HOME')

popoverChooseDevice = builder.get_object('popoverChooseDevice')
popoverDevicesListBox = builder.get_object('popoverDevicesListBox')
currentDeviceLabel = builder.get_object('currentDeviceLabel')

universalApplyButton = builder.get_object('universalApplyButton')

refreshDevicesButton=builder.get_object('refreshDevicesButton')

keyboardBox = builder.get_object("keyboardBox")
gameModeSwitch = builder.get_object("gameModeSwitch")

devicesList = []

mainBox=builder.get_object('mainBox')
noDevicesLabel=builder.get_object('noDevicesLabel')

def initDevices():
    for dev in device.devlist:
        newdev = device.Device(dev)
        devicesList.append(newdev)

def fillDevicesList():
    if len(devicesList) > 0:
        for i in devicesList:
            row = listboxHelper.make_row(i.name)
            row.value = i
            popoverDevicesListBox.add(row)
        popoverDevicesListBox.select_row(
            popoverDevicesListBox.get_row_at_index(0)
        )
        currentDeviceLabel.set_text(
            popoverDevicesListBox.get_row_at_index(0).value.name
        )
    else:
        currentDeviceLabel.set_text('No devices')

def updateDevicesConnected():
    if len(devicesList)>0:
        mainBox.show_all()
        keyboardBox.hide()
        noDevicesLabel.hide()
        gameModeSwitch.set_sensitive(True)
        universalApplyButton.set_sensitive(True)
    else:
        print("no devices")
        mainBox.hide()
        noDevicesLabel.show()
        gameModeSwitch.set_sensitive(False)
        universalApplyButton.set_sensitive(False)

def refreshDevices():
    listboxHelper.empty_listbox(popoverDevicesListBox)
    initDevices()
    fillDevicesList()
    updateDevicesConnected()

refreshDevices()

settings = Gtk.Settings.get_default()
settings.set_property("gtk-application-prefer-dark-theme", True)

# init profiles and fill list
popoverProfiles=builder.get_object('popoverProfiles')
buttonSaveProfile=builder.get_object('popoverProfilesSaveButton')
profilesListBox=builder.get_object('popoverProfilesListBox')

def onRmProfile(button, smth):
    custom_profiles.removeProfile(button.preset)
    refreshProfiles()

def refreshProfiles():
    # empty list first
    for child in profilesListBox.get_children():
        profilesListBox.remove(child)

    for p in custom_profiles.profiles:
        box=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        labelName=Gtk.Label()
        labelName.set_text(p['name'])
        box.pack_start(labelName, True, True, 0)
        box.set_margin_top(6)
        box.set_margin_bottom(6)
        if not p['name']=='Empty':
            rmIcon=Gtk.Image()
            rmIcon.set_from_icon_name('gtk-delete', Gtk.IconSize.BUTTON)
            rmButton=Gtk.Button()
            rmButton.add(rmIcon)
            rmButton.preset=p['name']
            rmButton.connect("button-press-event", onRmProfile)
            box.pack_end(rmButton, False, False, 0)
        row = Gtk.ListBoxRow()
        row.add(box)
        row.value=p['name']
        profilesListBox.add(row)
    profilesListBox.unselect_all()
    if popoverProfiles.get_visible():
        popoverProfiles.show_all()

refreshProfiles()

class App(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self,
                                 application_id="org.gabmus.razercommander",
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.connect("activate", self.activateCb)

    def do_startup(self):
        # start the application
        Gtk.Application.do_startup(self)

    def activateCb(self, app):
        window = builder.get_object("window")
        window.set_wmclass("razerCommander", "razerCommander")
        window.set_title("razerCommander")
        app.add_window(window)
        appMenu = Gio.Menu()
        appMenu.append("About", "app.about")
        appMenu.append("Quit", "app.quit")
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.on_about_activate)
        builder.get_object("aboutdialog").connect(
            "delete-event", lambda *_: builder.get_object("aboutdialog").hide() or True)
        app.add_action(about_action)
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.on_quit_activate)
        app.add_action(quit_action)
        app.set_app_menu(appMenu)
        window.show_all()
        keyboardBox.hide()
        updateDevicesConnected()

    def on_about_activate(self, *agrs):
        builder.get_object("aboutdialog").show()

    def on_quit_activate(self, *args):
        self.quit()

app=App()

if len(devicesList)>0:
    myrazerkb = devicesList[0]
else:
    myrazerkb = None


gameModeIcon = builder.get_object('gameModeIcon')

brightnessScale = builder.get_object('brightnessScale')

fxListBox = builder.get_object('fxListBox')

mainStackSwitcherButtons=builder.get_object('mainStackSwitcherButtons')
mainStack=builder.get_object('mainStack')

# macro logic
macro_listbox=builder.get_object('macroShortcutsListbox')
macro_device_picture=builder.get_object('macroDevicePicture')
macro_shortcut_dialog=builder.get_object('macroShortcutDialog')
macro_shortcut_entry=builder.get_object('macroShortcutEntry')
macro_shortcut_dialog_keyname_label=builder.get_object('macroShortcutDialogKeyName')
def refresh_macro_section():
    if not myrazerkb or not myrazerkb.macro_device:
        return
    listboxHelper.empty_listbox(macro_listbox)
    rows_l = device.macro_logic.make_shortcutslistbox_rows(myrazerkb.macro_device)
    for row in rows_l:
        macro_listbox.add(row)
        row.show_all()
    macro_device_picture.set_from_file(EXEC_FOLDER + 'img/'+ myrazerkb.name +'.svg')

# TODO: polish this function
def refreshFxList():
    if not myrazerkb:
        return
    # empty list before (re)filling it
    listboxHelper.empty_listbox(fxListBox)
    # fill list with supported effects
    for i in myrazerkb.availableFX:
        if i not in ['breath_single', 'breath_dual']:
            if i == 'breath_random':
                i = 'breath'
            i = i.capitalize()

            # ~~~ start
            iconPath = EXEC_FOLDER + "img/" + i + ".svg" # !!!
            row = listboxHelper.make_image_row(
                i,
                iconPath
            )
            row.value = i
            fxListBox.add(row)
            row.show_all()
    if myrazerkb.device.has('game_mode_led'):
        gameModeSwitch.set_state(myrazerkb.device.game_mode_led)
        if gameModeSwitch.get_state():
            gameModeIcon.set_from_file(EXEC_FOLDER + "img/gameModeOn.svg")
        else:
            gameModeIcon.set_from_file(EXEC_FOLDER + "img/gameModeOff.svg")
        gameModeIcon.show()
        gameModeSwitch.show()
    else:
        gameModeIcon.hide()
        gameModeSwitch.hide()

    # selective hiding of switcher buttons
    stackButtons = mainStackSwitcherButtons.get_children()

    # if device supports macros
    if myrazerkb.macro_device:
        stackButtons[2].show()
        refresh_macro_section() # possibly move this from here
    else:
        stackButtons[2].hide()
    if myrazerkb.device.type == 'mouse' and False: # TO REMOVE no mouse support in the lib yet
        stackButtons[0].show()
    else:
        stackButtons[0].hide()
        mainStack.set_visible_child(mainStack.get_children()[1])
    # fxListBox.show_all()

refreshFxList()

breathSettingsBox = builder.get_object('breathSettingsBox')
breathRandomRadio = builder.get_object('breathRandomRadio')
breathSingleRadio = builder.get_object('breathSingleRadio')
breathDoubleRadio = builder.get_object('breathDoubleRadio')
breathRGB1 = builder.get_object('breathRGB1chooser')
breathRGB2 = builder.get_object('breathRGB2chooser')

waveSettingsBox = builder.get_object('waveSettingsBox')
waveToggleLeft = builder.get_object('waveToggleBtnLeft')
waveToggleRight = builder.get_object('waveToggleBtnRight')

staticSettingsBox = builder.get_object('staticSettingsBox')
staticRGB = builder.get_object('staticRGBchooser')

reactiveSettingsBox = builder.get_object('reactiveSettingsBox')
spinReactiveTime = builder.get_object('spinReactiveTime')
reactiveRGBchooser = builder.get_object('reactiveRGBchooser')

# keyboardBox declared at top of document
customColorPicker = builder.get_object('customColorPicker')
pipetteTBtn = builder.get_object('customPipetteToolBtn')
clearTBtn = builder.get_object('customClearToolBtn')

rippleSettingsBox = builder.get_object('rippleSettingsBox')
rippleRadioColor = builder.get_object('rippleRadioColor')
rippleRadioRandom = builder.get_object('rippleRadioRandom')
rippleColorPicker = builder.get_object('rippleColorPicker')

settingsPanes = {
    'Breath': breathSettingsBox,
    'Wave': waveSettingsBox,
    'Static': staticSettingsBox,
    'Reactive': reactiveSettingsBox,
    'Custom': keyboardBox,
    'Ripple': rippleSettingsBox,
}

rkb = CustomKb.RKeyboard('ansi_us')

def onVirtKeyClick(eventbox, eventbtn):
    key = rkb.getKey(eventbox.keyx, eventbox.keyy)
    if not key.isGhost:
        if pipetteTBtn.get_active():
            color = key.color
            customColorPicker.set_rgba(color)
            pipetteTBtn.set_active(False)
        elif clearTBtn.get_active():
            key.color = Gdk.RGBA(0,0,0)
            black_rgba = Gdk.RGBA(0,0,0)
            eventbox.override_background_color(
                Gtk.StateType.NORMAL, black_rgba)
        else:
            key.color = customColorPicker.get_rgba()
            eventbox.override_background_color(
                Gtk.StateType.NORMAL, customColorPicker.get_rgba())

KEYCAP_SIZE = 50

# drawKB is now usable multiple times and profile ready
def drawKB(profile=None):
    # Load black fake profile if none provided
    if not profile:
        profile=custom_profiles.blackProfile
    custom_kb_builder.build_keyboard_box(
        keyboardBox,
        profile['colors'],
        onVirtKeyClick,
        rkb
    )

# Any better way than specifying every case?
def enableFXwSettings(fx):
    if fx == 'Breath':
        print(breathSingleRadio.get_active())
        print(breathDoubleRadio.get_active())
        if breathRandomRadio.get_active():
            myrazerkb.enableRandomBreath()
        else:
            rgb1 = breathRGB1.get_rgba()
            r1 = getColorVal(rgb1.red)
            g1 = getColorVal(rgb1.green)
            b1 = getColorVal(rgb1.blue)
            if breathDoubleRadio.get_active():
                rgb2 = breathRGB2.get_rgba()
                r2 = getColorVal(rgb2.red)
                g2 = getColorVal(rgb2.green)
                b2 = getColorVal(rgb2.blue)
                myrazerkb.enableDoubleBreath(r1, g1, b1, r2, g2, b2)
            else:
                myrazerkb.enableSingleBreath(r1, g1, b1)
    elif fx == 'Wave':
        if waveToggleLeft.get_active():
            myrazerkb.enableWave(2)
        else:
            myrazerkb.enableWave(1)
    elif fx == 'Static':
        rgb = staticRGB.get_rgba()
        r = getColorVal(rgb.red)
        g = getColorVal(rgb.green)
        b = getColorVal(rgb.blue)
        myrazerkb.enableStatic(r, g, b)
    elif fx == 'Reactive':
        time = spinReactiveTime.get_value_as_int()
        rgb = reactiveRGBchooser.get_rgba()
        r = getColorVal(rgb.red)
        g = getColorVal(rgb.green)
        b = getColorVal(rgb.blue)
        myrazerkb.enableReactive(time, r, g, b)
    elif fx == 'Custom':
        myrazerkb.applyCustom(rkb)
    elif fx == 'Ripple':
        if rippleRadioRandom.get_active():
            myrazerkb.enableRippleRandom()
        else:
            rgb = rippleColorPicker.get_rgba()
            r = getColorVal(rgb.red)
            g = getColorVal(rgb.green)
            b = getColorVal(rgb.blue)
            myrazerkb.enableRipple(r, g, b)
    else:
        myrazerkb.enableFX(fx)


def getColorVal(n):
    return int(n * 255)

saveProfileDialog=builder.get_object('saveProfileDialog')
profileNameEntry=builder.get_object('profileNameEntry')
presetExistsInfobar=builder.get_object('presetExistsInfobar')

macro_current_keystroke_label=builder.get_object('currentKeystrokeLabel')

keystroke_shortcuts_all_mods_str=[
    'Shift_L',
    'Control_L',
    'Super_L',
    'Alt_L'
]

keystroke_shortcuts_mod_shift=builder.get_object('setShortcutKeystrokeShiftModifierCheck')
keystroke_shortcuts_mod_ctrl=builder.get_object('setShortcutKeystrokeCtrlModifierCheck')
keystroke_shortcuts_mod_super=builder.get_object('setShortcutKeystrokeSuperModifierCheck')
keystroke_shortcuts_mod_alt=builder.get_object('setShortcutKeystrokeAltModifierCheck')

keystroke_shortcuts_all_mods=[
    keystroke_shortcuts_mod_shift,
    keystroke_shortcuts_mod_ctrl,
    keystroke_shortcuts_mod_super,
    keystroke_shortcuts_mod_alt
]

set_shortcut_stack=builder.get_object('setShortcutStack')

class Handler:

    def onDeleteWindow(self, *args):
        app.quit()

    def on_refreshDevicesButton_clicked(self, button):
        refreshDevices()

    def on_customProfilesButton_clicked(self, button):
        if not popoverProfiles.get_visible():
            popoverProfiles.show_all()

    def on_popoverProfilesListBox_row_selected(self, list, row):
        if row:
            profile=custom_profiles.getProfile(row.value)
            drawKB(profile)
            popoverProfiles.hide()

    def on_popoverProfilesSaveProfile_clicked(self, button):
        saveProfileDialog.show_all()
        popoverProfiles.hide()

    def on_saveProfileDialogOk_clicked(self, button):
        name=profileNameEntry.get_text()
        if not custom_profiles.addProfile(
            custom_profiles.makeProfile(name, rkb)
        ):
            print('error')
            #presetExistsInfobar.show()
        else:
            #presetExistsInfobar.hide()
            saveProfileDialog.hide()
            refreshProfiles()

    def on_presetExistsInfobar_close(self, *args):
        presetExistsInfobar.hide()

    def on_saveProfileDialogCancel_clicked(self, button):
        saveProfileDialog.hide()
        profileNameEntry.set_text('')

    def on_deviceChooserButton_clicked(self, button):
        if popoverChooseDevice.get_visible():
            popoverChooseDevice.hide()
        else:
            popoverChooseDevice.show_all()

    def on_popoverDevicesListBox_row_selected(self, list, row):
        # TODO: move to changeDevice() function
        global myrazerkb # there must be a better way
        # myrazerkb in row below is interpreted as local
        # var if global isn't specified. this ain't good
        if row:
            myrazerkb = row.value
            currentDeviceLabel.set_text(row.value.name)
            refreshFxList()
            popoverChooseDevice.hide()

    def on_universalApplyButton_clicked(self, button):
        newVal = brightnessScale.get_value()
        myrazerkb.setBrightness(int(newVal))
        if not fxListBox.get_selected_row():
            print('No fx row selected')
            return
        currentFX = fxListBox.get_selected_row().value
        if currentFX in settingsPanes.keys():
            enableFXwSettings(currentFX)
        else:
            myrazerkb.enableFX(currentFX)

    def on_gameModeSwitch_state_set(self, *args):
        myrazerkb.toggleGameMode()
        value = gameModeSwitch.get_state()
        # the state is inverted
        if not value:
            gameModeIcon.set_from_file(EXEC_FOLDER + "img/gameModeOn.svg")
        else:
            gameModeIcon.set_from_file(EXEC_FOLDER + "img/gameModeOff.svg")

    def on_breathRadio_toggled(self, radio):
        if radio.get_state():
            rlabel = radio.get_label()
            if rlabel == "Random":
                breathRGB1.set_sensitive(False)
                breathRGB2.set_sensitive(False)
            elif rlabel == "Single color":
                breathRGB1.set_sensitive(True)
                breathRGB2.set_sensitive(False)
            elif rlabel == "Double color":
                breathRGB1.set_sensitive(True)
                breathRGB2.set_sensitive(True)

    def on_rippleRadioColor_toggled(self, radio):
        if radio.get_state():
            rippleColorPicker.set_sensitive(True)
        else:
            rippleColorPicker.set_sensitive(False)

    def on_waveToggleBtn_left(self, button):
        if waveToggleLeft.get_active():
            waveToggleRight.set_active(False)

    def on_waveToggleBtn_right(self, button):
        if waveToggleRight.get_active():
            waveToggleLeft.set_active(False)

    def on_customPipetteToolBtn_toggled(self, button):
        if clearTBtn.get_active() and button.get_active():
            clearTBtn.set_active(False)

    def on_customClearToolBtn_toggled(self, button):
        if pipetteTBtn.get_active() and button.get_active():
            pipetteTBtn.set_active(False)

    def on_customColorPicker_color_set(self, *args):
        if pipetteTBtn.get_active():
            pipetteTBtn.set_active(False)
        if clearTBtn.get_active():
            clearTBtn.set_active(False)

    def on_fxListBox_row_selected(self, list, row):
        if row:
            for pane in settingsPanes.values():
                pane.hide()
            if row.value in settingsPanes.keys():
                settingsPanes[row.value].show()
            if row.value == 'Custom':
                drawKB()

    def on_macroShortcutDialogCancel_clicked(self, btn):
        macro_shortcut_dialog.hide()
        macro_shortcut_entry.set_text('')

    def on_macroShortcutsListbox_row_activated(self, list, row):
        if row and row.value:
            # uncheck all modifier checkboxes
            for i in keystroke_shortcuts_all_mods:
                i.set_active(False)
            macro_current_keystroke_label.set_text('...')
            macro_shortcut_dialog_keyname_label.set_text(row.value['key'])
            set_shortcut_stack.set_visible_child_name('Command')
            if not row.value['val']:
                macro_shortcut_entry.set_text('')
            elif row.value['val'].startswith('xdotool key '): # is keystroke
                set_shortcut_stack.set_visible_child_name('Keystroke')
                current_keystroke=row.value['val'][12:]
                macro_current_keystroke_label.set_text(current_keystroke)
            else:
                macro_shortcut_entry.set_text(row.value['val'])
            macro_shortcut_dialog.show()

    def on_macroShortcutDialogOk_clicked(self, btn):
        if set_shortcut_stack.get_visible_child_name() == 'Keystroke':
            n_macro='xdotool key '+macro_current_keystroke_label.get_text()
        else:
            n_macro=macro_shortcut_entry.get_text()
        macro_d=myrazerkb.macro_device
        macro_d.set_macro(
            macro_shortcut_dialog_keyname_label.get_text(),
            n_macro
        )
        refresh_macro_section()
        macro_shortcut_dialog.hide()

    def on_macroShortcutDialogClear_clicked(self, btn):
        macro_d=myrazerkb.macro_device
        n_macro=''
        macro_d.set_macro(
            macro_shortcut_dialog_keyname_label.get_text(),
            n_macro
        )
        refresh_macro_section()
        macro_shortcut_dialog.hide()

    key_stroke_list=[]
    key_stroke_n=0

    def on_recordKeystrokeToggleBtn_key_press_event(self, toggle_btn, event):
        if toggle_btn.get_active():
            keyname = Gdk.keyval_name(event.keyval)
            if keyname not in self.key_stroke_list:
                self.key_stroke_list.append(keyname)
                self.key_stroke_n+=1
        else:
            self.key_stroke_n=0
            self.key_stroke_list=[]

    def on_recordKeystrokeToggleBtn_key_release_event(self, toggle_btn, event):
        if toggle_btn.get_active():
            keyname = Gdk.keyval_name(event.keyval)
            #print("Release Key %s (keycode: %d)" % (keyname, event.keyval))
            self.key_stroke_n-=1
            if not self.key_stroke_n:
                keystroke=''
                for i in range(0,4):
                    if keystroke_shortcuts_all_mods[i].get_active():
                        keystroke+=keystroke_shortcuts_all_mods_str[i]+'+'
                keystroke+='+'.join(self.key_stroke_list)
                macro_current_keystroke_label.set_text(keystroke)
                self.key_stroke_list=[]
                self.key_stroke_n=0
                toggle_btn.set_active(False)
        else:
            self.key_stroke_n=0
            self.key_stroke_list=[]

builder.connect_signals(Handler())


if __name__ == "__main__":
    keyboardBox.show_all()
    app.run(sys.argv)

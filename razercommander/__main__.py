# __main__.py
#
# Copyright (C) 2017 GabMus
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio
print('Importing device logic, waiting for daemon')

try:
    from . import device
    print('Device logic loaded, deamon is alive')
except:
    print('ERROR: the daemon is not responding!\nTry running `killall razer-service && razer-service` or rebooting. If this doesn\'t work, please fill an issue!')
#    exit(1)
from . import device
from . import custom_keyboard as CustomKb
from . import custom_profiles
from . import listboxHelper
from . import custom_kb_builder

HOME = os.environ.get('HOME')

class Application(Gtk.Application):
    def __init__(self, **kwargs):
        self.builder = Gtk.Builder()
        super().__init__(application_id='org.gabmus.razercommander', **kwargs)
        self.EXEC_FOLDER = os.path.dirname(os.path.realpath(__file__))

        self.builder.add_from_file('%s/ui.glade' % self.EXEC_FOLDER)
        self.builder.connect_signals(self)

        settings = Gtk.Settings.get_default()
        settings.set_property("gtk-application-prefer-dark-theme", True)

        self.window = self.builder.get_object('window')

        self.brightnessScale = self.builder.get_object('brightnessScale')
        self.currentDeviceLabel = self.builder.get_object('currentDeviceLabel')
        self.customColorPicker = self.builder.get_object('customColorPicker')
        self.fxListBox = self.builder.get_object('fxListBox')
        self.gameModeIcon = self.builder.get_object('gameModeIcon')
        self.gameModeSwitch = self.builder.get_object("gameModeSwitch")
        self.keyboardBox = self.builder.get_object("keyboardBox")
        self.macro_current_keystroke_label = self.builder.get_object('currentKeystrokeLabel')
        self.macro_device_picture = self.builder.get_object('macroDevicePicture')
        self.macro_shortcut_dialog = self.builder.get_object('macroShortcutDialog')
        self.macro_shortcut_entry = self.builder.get_object('macroShortcutEntry')
        self.macro_shortcut_dialog_keyname_label = self.builder.get_object('macroShortcutDialogKeyName')
        self.macro_listbox = self.builder.get_object('macroShortcutsListbox')
        self.mainBox = self.builder.get_object('mainBox')
        self.mainStack = self.builder.get_object('mainStack')
        self.mainStackSwitcherButtons = self.builder.get_object('mainStackSwitcherButtons')
        self.noDevicesLabel = self.builder.get_object('noDevicesLabel')
        self.pipetteTBtn = self.builder.get_object('customPipetteToolBtn')
        self.popoverChooseDevice = self.builder.get_object('popoverChooseDevice')
        self.popoverDevicesListBox = self.builder.get_object('popoverDevicesListBox')
        self.popoverProfiles = self.builder.get_object('popoverProfiles')
        self.profileNameEntry = self.builder.get_object('profileNameEntry')
        self.profilesListBox = self.builder.get_object('popoverProfilesListBox')
        self.saveProfileDialog = self.builder.get_object('saveProfileDialog')
        self.set_shortcut_stack = self.builder.get_object('setShortcutStack')
        self.universalApplyButton = self.builder.get_object('universalApplyButton')

        self.breathDoubleRadio = self.builder.get_object('breathDoubleRadio')
        self.breathRandomRadio = self.builder.get_object('breathRandomRadio')
        self.breathRGB1 = self.builder.get_object('breathRGB1chooser')
        self.breathRGB2 = self.builder.get_object('breathRGB2chooser')
        self.breathSingleRadio = self.builder.get_object('breathSingleRadio')
        self.reactiveRGBchooser = self.builder.get_object('reactiveRGBchooser')
        self.rippleColorPicker = self.builder.get_object('rippleColorPicker')
        self.rippleRadioColor = self.builder.get_object('rippleRadioColor')
        self.rippleRadioRandom = self.builder.get_object('rippleRadioRandom')
        self.spinReactiveTime = self.builder.get_object('spinReactiveTime')
        self.staticRGB = self.builder.get_object('staticRGBchooser')
        self.waveToggleLeft = self.builder.get_object('waveToggleBtnLeft')
        self.waveToggleRight = self.builder.get_object('waveToggleBtnRight')

        self.breathSettingsBox = self.builder.get_object('breathSettingsBox')
        self.waveSettingsBox = self.builder.get_object('waveSettingsBox')
        self.staticSettingsBox = self.builder.get_object('staticSettingsBox')
        self.reactiveSettingsBox = self.builder.get_object('reactiveSettingsBox')
        self.rippleSettingsBox = self.builder.get_object('rippleSettingsBox')
        self.clearTBtn = self.builder.get_object('customClearToolBtn')

        self.dpi1Adjustment = self.builder.get_object('mouseDpi1Adjustment')
        self.dpi2Adjustment = self.builder.get_object('mouseDpi2Adjustment')
        self.radioPollrateGroup = self.builder.get_object('radioPollrate125').get_group()

        self.radioPollrate125 = self.builder.get_object('radioPollrate125')
        self.radioPollrate500 = self.builder.get_object('radioPollrate500')
        self.radioPollrate1000 = self.builder.get_object('radioPollrate1000')

        self.settingsPanes = {
            'Breath': self.breathSettingsBox,
            'Wave': self.waveSettingsBox,
            'Static': self.staticSettingsBox,
            'Reactive': self.reactiveSettingsBox,
            'Custom': self.keyboardBox,
            'Ripple': self.rippleSettingsBox
        }

        self.rkb = CustomKb.RKeyboard('ansi_us')

        self.KEYCAP_SIZE = 50
        self.keystroke_shortcuts_all_mods_str = [
            'Shift_L',
            'Control_L',
            'Super_L',
            'Alt_L'
        ]

        self.keystroke_shortcuts_mod_shift = self.builder.get_object('setShortcutKeystrokeShiftModifierCheck')
        self.keystroke_shortcuts_mod_ctrl = self.builder.get_object('setShortcutKeystrokeCtrlModifierCheck')
        self.keystroke_shortcuts_mod_super = self.builder.get_object('setShortcutKeystrokeSuperModifierCheck')
        self.keystroke_shortcuts_mod_alt = self.builder.get_object('setShortcutKeystrokeAltModifierCheck')
        self.keystroke_shortcuts_all_mods = [
            self.keystroke_shortcuts_mod_shift,
            self.keystroke_shortcuts_mod_ctrl,
            self.keystroke_shortcuts_mod_super,
            self.keystroke_shortcuts_mod_alt
        ]

        self.devicesList = []
        self.active_razer_device = None

        self.key_stroke_n = 0
        self.key_stroke_list = []

    def initDevices(self):
        self.devicesList = []
        for dev in device.devlist:
            newdev = device.Device(dev)
            self.devicesList.append(newdev)
        if len(self.devicesList) > 0:
            self.active_razer_device = self.devicesList[0]
        else:
            self.active_razer_device = None

    def fillDevicesList(self):
        if len(self.devicesList) > 0:
            for i in self.devicesList:
                row = listboxHelper.make_row(i.name)
                row.value = i
                self.popoverDevicesListBox.add(row)
            self.popoverDevicesListBox.select_row(
                self.popoverDevicesListBox.get_row_at_index(0)
            )
            self.currentDeviceLabel.set_text(
                self.popoverDevicesListBox.get_row_at_index(0).value.name
            )
        else:
            self.currentDeviceLabel.set_text('No devices')

    def updateDevicesConnected(self):
        if len(self.devicesList) > 0:
            self.mainBox.show_all()
            self.keyboardBox.hide()
            self.noDevicesLabel.hide()
            self.gameModeSwitch.set_sensitive(True)
            self.universalApplyButton.set_sensitive(True)
        else:
            print("no devices")
            self.mainBox.hide()
            self.noDevicesLabel.show()
            self.gameModeSwitch.set_sensitive(False)
            self.universalApplyButton.set_sensitive(False)

    def refreshDevices(self):
        listboxHelper.empty_listbox(self.popoverDevicesListBox)
        self.initDevices()
        self.fillDevicesList()
        self.updateDevicesConnected()

    def refreshProfiles(self):
        # empty list first
        for child in self.profilesListBox.get_children():
            self.profilesListBox.remove(child)

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
                rmButton.connect("button-press-event", self.onRmProfile)
                box.pack_end(rmButton, False, False, 0)
            row = Gtk.ListBoxRow()
            row.add(box)
            row.value=p['name']
            self.profilesListBox.add(row)
        self.profilesListBox.unselect_all()
        if self.popoverProfiles.get_visible():
            self.popoverProfiles.show_all()

    def onRmProfile(self, button, smth):
        custom_profiles.removeProfile(button.preset)
        self.refreshProfiles()

    def refresh_macro_section(self):
        if not self.active_razer_device or not self.active_razer_device.macro_device:
            return
        listboxHelper.empty_listbox(self.macro_listbox)
        rows_l = device.macro_logic.make_shortcutslistbox_rows(self.active_razer_device.macro_device)
        for row in rows_l:
            self.macro_listbox.add(row)
            row.show_all()
        self.macro_device_picture.set_from_file(
            self.EXEC_FOLDER +
            self.active_razer_device.name
            + '.svg'
        )

    def refreshFxList(self):
        if not self.active_razer_device:
            return
        # empty list before (re)filling it
        listboxHelper.empty_listbox(self.fxListBox)
        # fill list with supported effects
        for i in self.active_razer_device.availableFX:
            if i not in ['breath_single', 'breath_dual']:
                if i == 'breath_random':
                    i = 'breath'
                i = i.capitalize()

                iconPath = '%s/%s.svg' % (self.EXEC_FOLDER, i)
                row = listboxHelper.make_image_row(
                    i,
                    iconPath
                )
                row.value = i
                self.fxListBox.add(row)
                row.show_all()
        if self.active_razer_device.device.has('game_mode_led'):
            self.gameModeSwitch.set_state(self.active_razer_device.device.game_mode_led)
            if self.gameModeSwitch.get_state():
                self.gameModeIcon.set_from_file('%s/gameModeOn.svg' % self.EXEC_FOLDER)
            else:
                self.gameModeIcon.set_from_file('%s/gameModeOff.svg' % self.EXEC_FOLDER)
            self.gameModeIcon.show()
            self.gameModeSwitch.show()
        else:
            self.gameModeIcon.hide()
            self.gameModeSwitch.hide()

        # selective hiding of switcher buttons
        stackButtons = self.mainStackSwitcherButtons.get_children()

        # if device supports macros
        if self.active_razer_device.macro_device:
            stackButtons[2].show()
            self.refresh_macro_section() # possibly move this from here
        else:
            stackButtons[2].hide()
        if self.active_razer_device.device.type == 'mouse':
            stackButtons[0].show()
            self.builder.get_object(
                'mouseDpi1Adjustment'
                ).set_upper(self.active_razer_device.get_max_dpi())
            self.builder.get_object(
                'mouseDpi2Adjustment'
                ).set_upper(self.active_razer_device.get_max_dpi())
            currentDpi=self.active_razer_device.get_dpi()
            print(currentDpi[1])
            self.builder.get_object(
                'mouseDpi1Adjustment'
                ).set_value(currentDpi[0])
            self.builder.get_object(
                'mouseDpi2Adjustment'
                ).set_value(currentDpi[1])
            if self.active_razer_device.get_poll_rate() == 125:
                self.radioPollrate125.set_active(True)
            elif self.active_razer_device.get_poll_rate() == 500:
                self.radioPollrate500.set_active(True)
            elif self.active_razer_device.get_poll_rate() == 1000:
                self.radioPollrate1000.set_active(True)
            else:
                self.radioPollrate500.set_active(True)
        else:
            stackButtons[0].hide()
            self.mainStack.set_visible_child(self.mainStack.get_children()[1])
        # fxListBox.show_all()

    def onVirtKeyClick(self, eventbox, eventbtn):
        key = self.rkb.getKey(eventbox.keyx, eventbox.keyy)
        if not key.isGhost:
            if self.pipetteTBtn.get_active():
                color = key.color
                self.customColorPicker.set_rgba(color)
                self.pipetteTBtn.set_active(False)
            elif self.clearTBtn.get_active():
                key.color = Gdk.RGBA(0,0,0)
                black_rgba = Gdk.RGBA(0,0,0)
                eventbox.override_background_color(
                    Gtk.StateType.NORMAL,
                    black_rgba
                )
            else:
                key.color = self.customColorPicker.get_rgba()
                eventbox.override_background_color(
                    Gtk.StateType.NORMAL,
                    self.customColorPicker.get_rgba()
                )

    def drawKB(self, profile = None):
        # Load black fake profile if none provided
        if not profile:
            profile = custom_profiles.blackProfile
        custom_kb_builder.build_keyboard_box(
            self.keyboardBox,
            profile['colors'],
            self.onVirtKeyClick,
            self.rkb
        )

    def getColorVal(self, n):
        return int(n * 255)

    def enableFXwSettings(self, fx):
        if fx == 'Breath':
            print(self.breathSingleRadio.get_active())
            print(self.breathDoubleRadio.get_active())
            if self.breathRandomRadio.get_active():
                self.active_razer_device.enableRandomBreath()
            else:
                rgb1 = self.breathRGB1.get_rgba()
                r1 = self.getColorVal(rgb1.red)
                g1 = self.getColorVal(rgb1.green)
                b1 = self.getColorVal(rgb1.blue)
                if self.breathDoubleRadio.get_active():
                    rgb2 = self.breathRGB2.get_rgba()
                    r2 = self.getColorVal(rgb2.red)
                    g2 = self.getColorVal(rgb2.green)
                    b2 = self.getColorVal(rgb2.blue)
                    self.active_razer_device.enableDoubleBreath(r1, g1, b1, r2, g2, b2)
                else:
                    self.active_razer_device.enableSingleBreath(r1, g1, b1)
        elif fx == 'Wave':
            if self.waveToggleLeft.get_active():
                self.active_razer_device.enableWave(2)
            else:
                self.active_razer_device.enableWave(1)
        elif fx == 'Static':
            rgb = self.staticRGB.get_rgba()
            r = self.getColorVal(rgb.red)
            g = self.getColorVal(rgb.green)
            b = self.getColorVal(rgb.blue)
            self.active_razer_device.enableStatic(r, g, b)
        elif fx == 'Reactive':
            r_time = self.spinReactiveTime.get_value_as_int()
            rgb = self.reactiveRGBchooser.get_rgba()
            r = self.getColorVal(rgb.red)
            g = self.getColorVal(rgb.green)
            b = self.getColorVal(rgb.blue)
            self.active_razer_device.enableReactive(r_time, r, g, b)
        elif fx == 'Custom':
            self.active_razer_device.applyCustom(self.rkb)
        elif fx == 'Ripple':
            if self.rippleRadioRandom.get_active():
                self.active_razer_device.enableRippleRandom()
            else:
                rgb = self.rippleColorPicker.get_rgba()
                r = self.getColorVal(rgb.red)
                g = self.getColorVal(rgb.green)
                b = self.getColorVal(rgb.blue)
                self.active_razer_device.enableRipple(r, g, b)
        else:
            self.active_razer_device.enableFX(fx)



    def do_activate(self):
        window = self.builder.get_object('window')
        self.add_window(window)
        window.set_wmclass('razerCommander', 'razerCommander')
        window.set_title('razerCommander')

        appMenu = Gio.Menu()
        appMenu.append("About", "app.about")
        appMenu.append("Quit", "app.quit")
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.on_about_activate)
        self.builder.get_object("aboutdialog").connect(
            "delete-event", lambda *_: builder.get_object("aboutdialog").hide() or True)
        self.add_action(about_action)
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.on_quit_activate)
        self.add_action(quit_action)
        self.set_app_menu(appMenu)

        # initialization protocols
        self.refreshDevices()
        self.refreshProfiles()
        self.keyboardBox.hide()
        self.updateDevicesConnected()
        self.refreshFxList()

        window.show_all()
        self.keyboardBox.hide()

    def on_about_activate(self, *agrs):
        self.builder.get_object("aboutdialog").show()

    def on_quit_activate(self, *args):
        self.quit()

    def onDeleteWindow(self, *args):
        self.quit()

    # Handler functions START

    def on_refreshDevicesButton_clicked(self, button):
        self.refreshDevices()

    def on_customProfilesButton_clicked(self, button):
        if not self.popoverProfiles.get_visible():
            self.popoverProfiles.show_all()

    def on_popoverProfilesListBox_row_selected(self, list, row):
        if row:
            profile = custom_profiles.getProfile(row.value)
            self.drawKB(profile)
            self.popoverProfiles.hide()

    def on_popoverProfilesSaveProfile_clicked(self, button):
        self.saveProfileDialog.show_all()
        self.popoverProfiles.hide()

    def on_saveProfileDialogOk_clicked(self, button):
        name = self.profileNameEntry.get_text()
        if not custom_profiles.addProfile(
            custom_profiles.makeProfile(name, self.rkb)
        ):
            print('error')
            #presetExistsInfobar.show()
        else:
            #presetExistsInfobar.hide()
            self.profileNameEntry.set_text('')
            self.saveProfileDialog.hide()
            self.refreshProfiles()

    def on_presetExistsInfobar_close(self, btn, infobar):
        infobar.hide()

    def on_saveProfileDialogCancel_clicked(self, button):
        self.saveProfileDialog.hide()
        self.profileNameEntry.set_text('')

    def on_deviceChooserButton_clicked(self, button):
        if self.popoverChooseDevice.get_visible():
            self.popoverChooseDevice.hide()
        else:
            self.popoverChooseDevice.show_all()

    def on_popoverDevicesListBox_row_selected(self, list, row):
        # TODO_NO?: move to changeDevice() function
        if row:
            self.active_razer_device = row.value
            self.currentDeviceLabel.set_text(row.value.name)
            self.refreshFxList()
            self.popoverChooseDevice.hide()

    def on_universalApplyButton_clicked(self, button):
        if self.mainStack.get_visible_child_name() == 'Mouse':
            self.active_razer_device.set_dpi(
                int(self.dpi1Adjustment.get_value()),
                int(self.dpi2Adjustment.get_value()),
            )
            currentPollRate=500
            if self.radioPollrate125.get_active():
                currentPollRate=125
            elif self.radioPollrate500.get_active():
                currentPollRate=500
            elif self.radioPollrate1000.get_active():
                currentPollRate=1000
            self.active_razer_device.set_poll_rate(currentPollRate)
            return
        newVal = self.brightnessScale.get_value()
        self.active_razer_device.setBrightness(int(newVal))
        if not self.fxListBox.get_selected_row():
            print('No fx row selected')
            return
        currentFX = self.fxListBox.get_selected_row().value
        if currentFX in self.settingsPanes.keys():
            self.enableFXwSettings(currentFX)
        else:
            self.active_razer_device.enableFX(currentFX)

    def on_gameModeSwitch_state_set(self, *args):
        self.active_razer_device.toggleGameMode()
        value = self.gameModeSwitch.get_state()
        # the state is inverted
        if not value:
            self.gameModeIcon.set_from_file('%s/gameModeOn.svg' % self.EXEC_FOLDER)
        else:
            self.gameModeIcon.set_from_file('%s/gameModeOff.svg' % self.EXEC_FOLDER)

    def on_breathRadio_toggled(self, radio):
        if radio.get_state():
            rlabel = radio.get_label()
            if rlabel == "Random":
                self.breathRGB1.set_sensitive(False)
                self.breathRGB2.set_sensitive(False)
            elif rlabel == "Single color":
                self.breathRGB1.set_sensitive(True)
                self.breathRGB2.set_sensitive(False)
            elif rlabel == "Double color":
                self.breathRGB1.set_sensitive(True)
                self.breathRGB2.set_sensitive(True)

    def on_rippleRadioColor_toggled(self, radio):
        if radio.get_state():
            self.rippleColorPicker.set_sensitive(True)
        else:
            self.rippleColorPicker.set_sensitive(False)

    def on_waveToggleBtn_left(self, button):
        if self.waveToggleLeft.get_active():
            self.waveToggleRight.set_active(False)

    def on_waveToggleBtn_right(self, button):
        if self.waveToggleRight.get_active():
            self.waveToggleLeft.set_active(False)

    def on_customPipetteToolBtn_toggled(self, button):
        if self.clearTBtn.get_active() and button.get_active():
            self.clearTBtn.set_active(False)

    def on_customClearToolBtn_toggled(self, button):
        if self.pipetteTBtn.get_active() and button.get_active():
            self.pipetteTBtn.set_active(False)

    def on_customColorPicker_color_set(self, *args):
        if self.pipetteTBtn.get_active():
            self.pipetteTBtn.set_active(False)
        if self.clearTBtn.get_active():
            self.clearTBtn.set_active(False)

    def on_fxListBox_row_selected(self, list, row):
        if row:
            for pane in self.settingsPanes.values():
                pane.hide()
            if row.value in self.settingsPanes.keys():
                self.settingsPanes[row.value].show()
            if row.value == 'Custom':
                self.drawKB()

    def on_macroShortcutDialogCancel_clicked(self, btn):
        self.macro_shortcut_dialog.hide()
        self.macro_shortcut_entry.set_text('')

    def on_macroShortcutsListbox_row_activated(self, list, row):
        if row and row.value:
            # uncheck all modifier checkboxes
            for i in self.keystroke_shortcuts_all_mods:
                i.set_active(False)
            self.macro_current_keystroke_label.set_text('...')
            self.macro_shortcut_dialog_keyname_label.set_text(row.value['key'])
            self.set_shortcut_stack.set_visible_child_name('Command')
            if not row.value['val']:
                self.macro_shortcut_entry.set_text('')
            elif row.value['val'].startswith('xdotool key '): # is keystroke
                self.set_shortcut_stack.set_visible_child_name('Keystroke')
                current_keystroke=row.value['val'][12:]
                self.macro_current_keystroke_label.set_text(current_keystroke)
            else:
                self.macro_shortcut_entry.set_text(row.value['val'])
            self.macro_shortcut_dialog.show()

    def on_macroShortcutDialogOk_clicked(self, btn):
        if set_shortcut_stack.get_visible_child_name() == 'Keystroke':
            n_macro = 'xdotool key %s' % self.macro_current_keystroke_label.get_text()
        else:
            n_macro = self.macro_shortcut_entry.get_text()
        macro_d = self.active_razer_device.macro_device
        macro_d.set_macro(
            self.macro_shortcut_dialog_keyname_label.get_text(),
            n_macro
        )
        self.refresh_macro_section()
        self.macro_shortcut_dialog.hide()

    def on_macroShortcutDialogClear_clicked(self, btn):
        macro_d = self.active_razer_device.macro_device
        n_macro = ''
        macro_d.set_macro(
            self.macro_shortcut_dialog_keyname_label.get_text(),
            n_macro
        )
        self.refresh_macro_section()
        self.macro_shortcut_dialog.hide()

    def on_recordKeystrokeToggleBtn_key_press_event(self, toggle_btn, event):
        if toggle_btn.get_active():
            keyname = Gdk.keyval_name(event.keyval)
            if keyname not in self.key_stroke_list:
                self.key_stroke_list.append(keyname)
                self.key_stroke_n += 1
        else:
            self.key_stroke_n = 0
            self.key_stroke_list = []

    def on_recordKeystrokeToggleBtn_key_release_event(self, toggle_btn, event):
        if toggle_btn.get_active():
            keyname = Gdk.keyval_name(event.keyval)
            #print("Release Key %s (keycode: %d)" % (keyname, event.keyval))
            self.key_stroke_n -= 1
            if not self.key_stroke_n:
                keystroke = ''
                for i in range(0,4):
                    if self.keystroke_shortcuts_all_mods[i].get_active():
                        keystroke += self.keystroke_shortcuts_all_mods_str[i]+'+'
                keystroke += '+'.join(self.key_stroke_list)
                self.macro_current_keystroke_label.set_text(keystroke)
                self.key_stroke_list = []
                self.key_stroke_n = 0
                toggle_btn.set_active(False)
        else:
            self.key_stroke_n = 0
            self.key_stroke_list = []

    # Handler functions END



def main():
    application = Application()

    try:
        ret = application.run(sys.argv)
    except SystemExit as e:
        ret = e.code

    sys.exit(ret)


if __name__ == '__main__':
    main()

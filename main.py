#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio
import os
import sys
import device

builder = Gtk.Builder()
builder.add_from_file("ui.glade")
HOME=os.environ.get('HOME')

devicesUIDs=[]
devicesList=[]

comboChooseDevice=builder.get_object("comboChooseDevice")

def initDevices():
	devicesUIDs=[]
	cont=os.listdir(device.Device.DRIVER_PATH)
	for i in cont:
		if i[0]=="0":
			devicesUIDs.append(i)
	for i in devicesUIDs:
		devicesList.append(device.Device(i))

def fillComboBox():
	for i in devicesList:
		comboChooseDevice.append_text(i.name)
	comboChooseDevice.set_active(0)

initDevices()
fillComboBox()

#liststoreCombo=builder.get_object("liststoreCombo")

settings = Gtk.Settings.get_default()
settings.set_property("gtk-application-prefer-dark-theme", True)

class App(Gtk.Application):
	def __init__(self):
		Gtk.Application.__init__(self, application_id="org.gabmus.razercommander", flags=Gio.ApplicationFlags.FLAGS_NONE)
		self.connect("activate", self.activateCb)

	def do_startup(self):
	# start the application
		Gtk.Application.do_startup(self)

	def activateCb(self, app):
		window = builder.get_object("window")
		window.set_wmclass("razerCommander", "razerCommander")
		app.add_window(window)
		appMenu=Gio.Menu()
		appMenu.append("About", "app.about")
		appMenu.append("Quit", "app.quit")
		about_action = Gio.SimpleAction.new("about", None)
		about_action.connect("activate", self.on_about_activate)
		builder.get_object("aboutdialog").connect("delete-event", lambda *_: builder.get_object("aboutdialog").hide() or True)
		app.add_action(about_action)
		quit_action = Gio.SimpleAction.new("quit", None)
		quit_action.connect("activate", self.on_quit_activate)
		app.add_action(quit_action)
		app.set_app_menu(appMenu)
		window.show_all()


	def on_about_activate(self, *agrs):
		builder.get_object("aboutdialog").show()

	def on_quit_activate(self, *args):
		self.quit()

myrazerkb=devicesList[0]


gameModeIcon=builder.get_object("gameModeIcon")
gameModeSwitch=builder.get_object("gameModeSwitch")

brightnessScale=builder.get_object("brightnessScale")

fxListBox=builder.get_object("fxListBox")

def refreshFxList():
	# empty list before (re)filling it
	while True:
		row=fxListBox.get_row_at_index(0)
		if row:
			fxListBox.remove(row)
		else:
			break
	#fill list with supported effects
	for i in myrazerkb.lightFXList:
		# checks if the mode buffer is supported
		if myrazerkb.KNOWN_MODE_BUFFERS[i.upper()] in myrazerkb.mode_buffers:
			box=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
			labelName= Gtk.Label()
			labelName.set_text(i)
			iconPath="img/"+i+".svg"
			# check if icon file exists before creating the icon
			if os.path.isfile(iconPath):
				fxIcon=Gtk.Image()
				fxIcon.set_from_file(iconPath)
				box.pack_start(fxIcon, False, False, 0)
			box.pack_start(labelName, True, True, 0)
			row=Gtk.ListBoxRow()
			row.add(box)
			row.value=i
			fxListBox.add(row)

refreshFxList()

breathSettingsBox=builder.get_object('breathSettingsBox')
breathRandomRadio=builder.get_object('breathRandomRadio')
breathSingleRadio=builder.get_object('breathSingleRadio')
breathDoubleRadio=builder.get_object('breathDoubleRadio')
breathRGB1=builder.get_object('breathRGB1chooser')
breathRGB2=builder.get_object('breathRGB2chooser')

waveSettingsBox=builder.get_object('waveSettingsBox')

staticSettingsBox=builder.get_object('staticSettingsBox')
staticRGB=builder.get_object('staticRGBchooser')

reactiveSettingsBox=builder.get_object('reactiveSettingsBox')
spinReactiveTime=builder.get_object('spinReactiveTime')
reactiveRGBchooser=builder.get_object('reactiveRGBchooser')

settingsPanes= {
	'Breath':breathSettingsBox,
	'Wave':waveSettingsBox,
	'Static':staticSettingsBox,
	'Reactive':reactiveSettingsBox,
}

def double2hex(n):
	return format(int(n)*255, '#04x')[2:]

class Handler:

	def onDeleteWindow(self, *args):
		Gtk.main_quit(*args)

	def on_gameModeSwitch_state_set(self, *args):
		value=gameModeSwitch.get_state()
		# the state is inverted
		if not value:
			myrazerkb.setGameMode(1)
			gameModeIcon.set_from_file("img/gameModeOn.svg")
		else:
			myrazerkb.setGameMode(0)
			gameModeIcon.set_from_file("img/gameModeOff.svg")

	def on_brightnessScale_value_set(self, *args):
		newVal=brightnessScale.get_value()
		myrazerkb.setBrightness(int(newVal))

	def on_breathApplyButton_clicked(self, *args):
		if breathRandomRadio.get_active():
			myrazerkb.enableRandomBreath()
		else:
			rgb1=breathRGB1.get_rgba()
			r1=double2hex(rgb1.red)
			g1=double2hex(rgb1.green)
			b1=double2hex(rgb1.blue)
			if breathDoubleRadio.get_active:
				rgb2=breathRGB2.get_rgba()
				r2=double2hex(rgb2.red)
				g2=double2hex(rgb2.green)
				b2=double2hex(rgb2.blue)
				myrazerkb.enableDoubleBreath(r1,g1,b1,r2,g2,b2)
			else:
				myrazerkb.enableSingleBreath(r1,g1,b1)

	def on_breathRadio_toggled(self, radio):
		if radio.get_state():
			rlabel=radio.get_label()
			if rlabel=="Random":
				breathRGB1.set_sensitive(False)
				breathRGB2.set_sensitive(False)
			elif rlabel=="Single color":
				breathRGB1.set_sensitive(True)
				breathRGB2.set_sensitive(False)
			elif rlabel=="Double color":
				breathRGB1.set_sensitive(True)
				breathRGB2.set_sensitive(True)

	def on_waveButtonRight_clicked(self, *args):
		myrazerkb.enableWave(1)

	def on_waveButtonLeft_clicked(self, *args):
		myrazerkb.enableWave(2)

	def on_staticApplyButton_clicked(self, *args):
		rgb=staticRGB.get_rgba()
		r=double2hex(rgb.red)
		g=double2hex(rgb.green)
		b=double2hex(rgb.blue)
		myrazerkb.enableStatic(r,g,b)

	def on_fxListBox_row_selected(self, list, row):
		myrazerkb.enableFX(row.value)
		for pane in settingsPanes.values():
			pane.hide()
		if row.value in settingsPanes.keys():
			settingsPanes[row.value].show()

	def on_comboChooseDevice_changed(self, combo):
		kb=combo.get_active_text()
		for i in devicesList:
			if i.name==kb:
				myrazerkb=i
				break

	def on_reactiveApplyButton_clicked(self, button):
		time=spinReactiveTime.get_value_as_int()
		rgb=reactiveRGBchooser.get_rgba()
		r=double2hex(rgb.red)
		g=double2hex(rgb.green)
		b=double2hex(rgb.blue)
		myrazerkb.enableReactive(time, r, g, b)

builder.connect_signals(Handler())


if __name__ == "__main__":
	app= App()
	app.run(sys.argv)

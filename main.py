#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Gdk
import os
import sys
import device
import custom_keyboard as CustomKb

if not os.path.isdir(device.Device.DRIVER_PATH):
	print("Fatal error: looks like you don't have razer_chroma_drivers installed on your system. Please install it before using this application.")
	exit(1)

EXEC_FOLDER=os.path.realpath(os.path.dirname(__file__))+"/"
builder = Gtk.Builder()
builder.add_from_file(EXEC_FOLDER+"ui.glade")
HOME=os.environ.get('HOME')

popoverChooseDevice=builder.get_object('popoverChooseDevice')
popoverDevicesListBox=builder.get_object('popoverDevicesListBox')
currentDeviceLabel=builder.get_object('currentDeviceLabel')

universalApplyButton=builder.get_object('universalApplyButton')

universalApplyButton.modify_bg(Gtk.StateFlags.NORMAL, Gdk.Color.parse('#4884cb').color)
universalApplyButton.modify_bg(Gtk.StateFlags.PRELIGHT, Gdk.Color.parse('#5294E2').color)
universalApplyButton.modify_bg(Gtk.StateFlags.ACTIVE, Gdk.Color.parse('#454A57').color)

devicesUIDs=[]
devicesList=[]

def initDevices():
	devicesUIDs=[]
	cont=os.listdir(device.Device.DRIVER_PATH)
	for i in cont:
		if i[0]=="0":
			devicesUIDs.append(i)
	for i in devicesUIDs:
		devicesList.append(device.Device(i))

def fillDevicesList():
	if devicesList[0] != None:
		for i in devicesList:
			box=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
			labelName=Gtk.Label()
			labelName.set_text(i.name)
			box.pack_start(labelName, True, True, 0)
			box.set_margin_top(12)
			box.set_margin_bottom(12)
			row=Gtk.ListBoxRow()
			row.add(box)
			row.value=i
			popoverDevicesListBox.add(row)
		popoverDevicesListBox.select_row(
			popoverDevicesListBox.get_row_at_index(0)
		)
		currentDeviceLabel.set_text(
			popoverDevicesListBox.get_row_at_index(0).value.name
		)
	else:
		print("Fatal error: looks like you don't have a supported device. Sorry for the inconvenience, the app will crash.")
		exit(1)


initDevices()
fillDevicesList()

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
		keyboardBox.hide()



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
			iconPath=EXEC_FOLDER+"img/"+i+".svg"
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
waveToggleLeft=builder.get_object('waveToggleBtnLeft')
waveToggleRight=builder.get_object('waveToggleBtnRight')

staticSettingsBox=builder.get_object('staticSettingsBox')
staticRGB=builder.get_object('staticRGBchooser')

reactiveSettingsBox=builder.get_object('reactiveSettingsBox')
spinReactiveTime=builder.get_object('spinReactiveTime')
reactiveRGBchooser=builder.get_object('reactiveRGBchooser')

keyboardBox=builder.get_object("keyboardBox")
customColorPicker=builder.get_object('customColorPicker')
pipetteTBtn=builder.get_object('customPipetteToolBtn')
clearTBtn=builder.get_object('customClearToolBtn')

settingsPanes= {
	'Breath':breathSettingsBox,
	'Wave':waveSettingsBox,
	'Static':staticSettingsBox,
	'Reactive':reactiveSettingsBox,
	'Custom':keyboardBox,
}

rkb=CustomKb.RKeyboard('ansi_us')

def rgba_to_hex(color):
	return "{0:02x}{1:02x}{2:02x}".format(int(color.red  * 255),
		int(color.green * 255),
		int(color.blue * 255))

def onVirtKeyClick(eventbox, eventbtn):
	key=rkb.getKey(eventbox.keyx, eventbox.keyy)
	if not key.isGhost:
		if pipetteTBtn.get_active():
			color=Gdk.RGBA()
			color.parse('#'+key.color)
			customColorPicker.set_rgba(color)
			pipetteTBtn.set_active(False)
		elif clearTBtn.get_active():
			key.color='000000'
			black_rgba=Gdk.RGBA()
			black_rgba.parse('#000000')
			eventbox.override_background_color(Gtk.StateType.NORMAL, black_rgba)
		else:
			key.color=rgba_to_hex(customColorPicker.get_rgba())
			eventbox.override_background_color(Gtk.StateType.NORMAL, customColorPicker.get_rgba())

KEYCAP_SIZE=50

def drawKB():
	keyy=0
	kbcont=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
	for row in rkb.rows:
		keyx=0
		rowbox=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		for key in row.keylist:
			box=Gtk.EventBox()
			if not key.isGhost:
				box.get_style_context().add_class('keycap')
				box.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(0,0,0))
				label=Gtk.Label()
				label.set_text(key.label)
				box.add(label)
			box.keyx=keyx
			box.keyy=keyy

			if key.label in ['tab', 'lctrl', 'lalt', 'ralt', 'rctrl', '\\']:
				box.set_size_request(KEYCAP_SIZE*1.5,KEYCAP_SIZE)
			elif key.label=='capslk':
				box.set_size_request(KEYCAP_SIZE*1.75,KEYCAP_SIZE)
			elif key.label in ['lshift', 'ret']:
				box.set_size_request(KEYCAP_SIZE*2.25,KEYCAP_SIZE)
			elif key.label=='rshift':
				box.set_size_request(KEYCAP_SIZE*2.75,KEYCAP_SIZE)
			elif key.label=='bckspc':
				box.set_size_request(KEYCAP_SIZE*2,KEYCAP_SIZE)
			elif key.label=='spacebar':
				box.set_size_request(KEYCAP_SIZE*6,KEYCAP_SIZE)
			elif key.label==CustomKb.kblayouts.INV_GHOST:
				box.set_size_request(0,0)
			else:
				box.set_size_request(KEYCAP_SIZE,KEYCAP_SIZE)
			box.connect("button-press-event", onVirtKeyClick)
			rowbox.pack_start(box, True, True, 0)
			keyx+=1
		kbcont.pack_start(rowbox, True, True, 0)
		keyy+=1
	keyboardBox.pack_end(kbcont, True, True, 0)

drawKB()

# Any better way than specifying every case?
def enableFXwSettings(fx):
	if fx=='Breath':
		print(breathSingleRadio.get_active())
		print(breathDoubleRadio.get_active())
		if breathRandomRadio.get_active():
			myrazerkb.enableRandomBreath()
		else:
			rgb1=breathRGB1.get_rgba()
			r1=double2hex(rgb1.red)
			g1=double2hex(rgb1.green)
			b1=double2hex(rgb1.blue)
			if breathDoubleRadio.get_active():
				rgb2=breathRGB2.get_rgba()
				r2=double2hex(rgb2.red)
				g2=double2hex(rgb2.green)
				b2=double2hex(rgb2.blue)
				myrazerkb.enableDoubleBreath(r1,g1,b1,r2,g2,b2)
			else:
				myrazerkb.enableSingleBreath(r1,g1,b1)
	elif fx=='Wave':
		if waveToggleLeft.get_active():
			myrazerkb.enableWave(2)
		else:
			myrazerkb.enableWave(1)
	elif fx=='Static':
		rgb=staticRGB.get_rgba()
		r=double2hex(rgb.red)
		g=double2hex(rgb.green)
		b=double2hex(rgb.blue)
		myrazerkb.enableStatic(r,g,b)
	elif fx=='Reactive':
		time=spinReactiveTime.get_value_as_int()
		rgb=reactiveRGBchooser.get_rgba()
		r=double2hex(rgb.red)
		g=double2hex(rgb.green)
		b=double2hex(rgb.blue)
		myrazerkb.enableReactive(time, r, g, b)
	elif fx=='Custom':
		myrazerkb.applyCustom(rkb)
	else:
		myrazerkb.enableFX(fx)

def double2hex(n):
	return format(int(n*255), '#04x')[2:]

class Handler:

	def onDeleteWindow(self, *args):
		Gtk.main_quit(*args)

	def on_deviceChooserButton_clicked(self, button):
		if popoverChooseDevice.get_visible():
			popoverChooseDevice.hide()
		else:
			popoverChooseDevice.show_all()

	def on_popoverDevicesListBox_row_selected(self, list, row):
		myrazerkb=row.value
		currentDeviceLabel.set_text(row.value.name)
		popoverChooseDevice.hide()

	def on_universalApplyButton_clicked(self, button):
		newVal=brightnessScale.get_value()
		myrazerkb.setBrightness(int(newVal))
		currentFX=fxListBox.get_selected_row().value
		if currentFX in settingsPanes.keys():
			enableFXwSettings(currentFX)
		else:
			myrazerkb.enableFX(currentFX)

	def on_gameModeSwitch_state_set(self, *args):
		value=gameModeSwitch.get_state()
		# the state is inverted
		if not value:
			myrazerkb.setGameMode(1)
			gameModeIcon.set_from_file(EXEC_FOLDER+"img/gameModeOn.svg")
		else:
			myrazerkb.setGameMode(0)
			gameModeIcon.set_from_file(EXEC_FOLDER+"img/gameModeOff.svg")

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
		for pane in settingsPanes.values():
			pane.hide()
		if row.value in settingsPanes.keys():
			settingsPanes[row.value].show()

builder.connect_signals(Handler())


if __name__ == "__main__":
	app= App()
	app.run(sys.argv)

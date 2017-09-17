# probably not necessary vvvv
import os
import io
import logging
logging.basicConfig(level=logging.DEBUG)
from . import macro_logic

import openrazer.client as rclient
#import razer.client.constants as razer_constants

device_manager = rclient.DeviceManager()
devlist = []
for device in device_manager.devices:
    devlist.append(device)

def getSyncFX():
    return bool(device_manager.sync_effects)

def setSyncFX(value):
    if type(value) != bool:
        print('ERROR: device: setSyncFX: the value passed is not a boolean!')
        return False
    # print('SyncFX set to %s' % value)
    device_manager.sync_effects = value

# This class represents a single device (ie: a keyboard)
class Device:

    def __init__(self, device):
        self.device = device
        self.availableFX = []

        if self.device.type == 'mouse':
            for fx in self.mouse_scroll_uFXList:
                if self.device.fx.misc.has('scroll'):
                    if self.device.fx.misc.scroll_wheel.has(fx):
                        self.availableFX.append(fx)
            for fx in self.mouse_logo_uFXList:
                if self.device.fx.misc.has('logo'):
                    if self.device.fx.misc.logo.has(fx):
                        self.availableFX.append(fx)
        for fx in self.uFXList:
            if self.device.fx.has(fx):
                self.availableFX.append(fx)

        if self.device.has('lighting_led_matrix') and self.device.type == 'keyboard':
            self.availableFX.append('custom')
        if self.device.has('macro_logic'):  # unsupported dev failsafe in macro_logic.make_device()
            self.macro_device = macro_logic.make_device(
                str(self.device.serial),
                self.device)
        else:
            self.macro_device = None
        self.name = str(device.name)


    # unfriendly fx list
    uFXList = [
        'breath_single',
        'breath_dual',
        'breath_random',
        'reactive',
        'spectrum',
        'pulsate',
        'wave',
        'ripple',
        'static',
        'none',
    ]

    mouse_scroll_uFXList = [
        'scroll_blinking',
        'scroll_pulsate',
        'scroll_breath_single',
        'scroll_breath_dual',
        'scroll_breath_random',
        'scroll_spectrum',
        'scroll_reactive',
        'scroll_static',
        'scroll_none',
    ]

    mouse_logo_uFXList = [
        'logo_blinking',
        'logo_pulsate',
        'logo_breath_single',
        'logo_breath_dual',
        'logo_breath_random',
        'logo_spectrum',
        'logo_reactive',
        'logo_static',
        'logo_none',
    ]

    MSG_PROBLEM_ENABLING = 'There was an error enabling the FX '

    # Breathing effect mode
    def enableRandomBreath(self):
        # check if breathe is available for the current device
        if 'breath_random' in self.availableFX:
            if not self.device.fx.breath_random():
                logging.error(self.MSG_PROBLEM_ENABLING + 'Breath Random')
        else:
            logging.warning('The Breath Random FX is not available')

    def enableSingleBreath(self, R, G, B):
        # check if breathe is available for the current device
        if 'breath_single' in self.availableFX:
            if not self.device.fx.breath_single(R, G, B):
                logging.error(self.MSG_PROBLEM_ENABLING + 'Breath Single')
        else:
            logging.warning('The Breath Single FX is not available')

    def enableDoubleBreath(self, R1, G1, B1, R2, G2, B2):
        # check if breathe is available for the current device
        if 'breath_dual' in self.availableFX:
            if not self.device.fx.breath_dual(R1, G1, B1, R2, G2, B2):
                logging.error(self.MSG_PROBLEM_ENABLING + 'Breath Double')
        else:
            logging.warning('The Breath Double FX is not available')

    # Reactive effect mode
    # this method takes 3 arguments, the values for red, green and blue
    def enableReactive(self, time, R, G, B):  # time can be only 1, 2 or 3
        # check if reactive is available for the current device
        if 'reactive' in self.availableFX:
            if not self.device.fx.reactive(R, G, B, time):
                logging.error(self.MSG_PROBLEM_ENABLING + 'Reactive')
        else:
            logging.warning('The Reactive FX is not available')

    # Static effect mode
    # this method takes 3 arguments, the values for red, green and blue
    def enableStatic(self, R, G, B):
        # check if static is available for the current device
        if 'static' in self.availableFX:
            if not self.device.fx.static(R, G, B):
                logging.error(self.MSG_PROBLEM_ENABLING + 'Static')
        else:
            logging.warning('The Static FX is not available')

    # Wave effect mode
    # direction is an int: 1 is right, 2 is left
    def enableWave(self, direction):
        # check if wave is available for the current device
        if 'wave' in self.availableFX:
            if direction not in [1, 2]:
                logging.warning(
                    'Error when enabling Wave: value is not 1 or 2')
            elif not self.device.fx.wave(direction):
                logging.error(self.MSG_PROBLEM_ENABLING + 'Wave')
        else:
            logging.warning('The Wave FX is not available')

    # NOTE: starlight mode FX temporarely disabled since it's not supported by the lib
    # Starlight mode effect
    # This is pretty easy but undocumented in the driver wiki, so
    # just be aware of that
    # def enableStarlight(self):
        # check if starlight is available for the current device
    #    if self.KNOWN_MODE_BUFFERS['STARLIGHT'] in self.mode_buffers:
    #        command='echo -n \'1\' > '+self.DRIVER_PATH+self.escaped_uid+'/'+self.KNOWN_MODE_BUFFERS['STARLIGHT']
    #        self.__gksu_run__(command)
    #        return 0
    #    else:
    #        self.__dbug_print__("Starlight not available on this device")
    #        return 1

    # None effect mode
    # Practically disables lighting effects
    def enableNone(self):
        # check if none is available for the current device
        if 'none' in self.availableFX:
            if not self.device.fx.none():
                logging.error(self.MSG_PROBLEM_ENABLING + 'None')
        else:
            logging.warning('The None FX is not available')

    # Turns on or off game mode (it disables the <Super> key)
    # Value has to be 0 to disable or 1 to enable game mode
    def toggleGameMode(self):
        # check if game is available for the current device
        if self.device.has('game_mode_led'):
            # toggles game mode
            self.device.game_mode_led = not self.device.game_mode_led
        else:
            logging.warning('The Game Mode LED is not available')

    # Spectrum mode effect
    # This should only be supported in RGB keyboards
    def enableSpectrum(self):
        # check if spectrum is available for the current device
        if 'spectrum' in self.availableFX:
            if not self.device.fx.spectrum():
                logging.error(self.MSG_PROBLEM_ENABLING + 'Spectrum')
        else:
            logging.warning('The Spectrum FX is not available')

    def enableRipple(self, R, G, B):
        if 'ripple' in self.availableFX:
            if not self.device.fx.ripple(
                R, G, B, rclient.constants.RIPPLE_REFRESH_RATE):
                logging.error(self.MSG_PROBLEM_ENABLING + 'Ripple')
        else:
            logging.warning('The Ripple FX is not available')

    def enableRippleRandom(self):
        if 'ripple' in self.availableFX:
            if not self.device.fx.ripple_random(rclient.constants.RIPPLE_REFRESH_RATE):
                logging.error(self.MSG_PROBLEM_ENABLING + 'Ripple')
        else:
            logging.warning('The Ripple FX is not available')

    # Pulsate mode effect
    # This should only be supported in the Razer BlackWidow Ultimate 2013
    # and should be similar if not the same as breath effect
    def enablePulsate(self):
        # check if pulsate is available for the current device
        if 'pulsate' in self.availableFX:
            if not self.device.fx.pulsate():
                logging.error(self.MSG_PROBLEM_ENABLING + 'Pulsate')
        else:
            logging.warning('The Pulsate FX is not available')


    def getBrightness(self):
        # check if brightness is available for the current device
        if self.device.has('brightness'):
            return self.device.brightness
        else:
            return -1
            logging.warning('Brightness is not available')

    # Set birghtness for backlight
    # gets values between 0 and 255
    def setBrightness(self, value):
        # check if brightness is available for the current device
        if self.device.has('brightness'):
            self.device.brightness = value
        else:
            logging.warning('Brightness is not available')

    def getKbBrightness(self):
        if self.device.has('brightness'):
            return int(self.device.brightness)
        else:
            logging.warning('Brightness is not available')

    def getScrollBrightness(self):
        # check if brightness is available for the current device
        if self.device.fx.has('scroll_brightness'):
            return self.device.fx.misc.scroll_wheel.brightness
        else:
            logging.warning('Scroll Brightness is not available')
            return -1

    def getLogoBrightness(self):
        # check if brightness is available for the current device
        if self.device.fx.has('logo_brightness'):
            return self.device.fx.misc.logo.brightness
        else:
            logging.warning('Logo Brightness is not available')
            return -1

    def setScrollBrightness(self, value):
        # check if brightness is available for the current device
        if self.device.fx.has('scroll_brightness'):
            self.device.fx.misc.scroll_wheel.brightness = value
        else:
            logging.warning('Scroll Brightness is not available')

    def setLogoBrightness(self, value):
        # check if brightness is available for the current device
        if self.device.fx.has('logo_brightness'):
            self.device.fx.misc.logo.brightness = value
        else:
            logging.warning('Logo Brightness is not available')

    def enableFX(self, fx):
        if fx == "None":
            self.enableNone()
            return 0
        elif fx == "Spectrum":
            self.enableSpectrum()
            return 0
        elif fx == "Pulsate":
            self.enablePulsate()
            return 0
        elif fx == 'Scroll spectrum':
            self.enableScrollSpectrum()
        elif fx == 'Logo spectrum':
            self.enableLogoSpectrum()
        elif fx == 'Scroll none':
            self.enableScrollNone()
        elif fx == 'Logo none':
            self.enableLogoNone()
        else:
            logging.error("FX not listed")
            return 1

    def enableScrollBlinking(self, R, G, B):
        if self.device.fx.misc.scroll_wheel.has('scroll_blinking'):
            if not self.device.fx.misc.scroll_wheel.blinking(R, G, B):
                logging.error('%sBlinking' % self.MSG_PROBLEM_ENABLING)
        else:
            logging.warning('The Scroll Blinking FX is not available')

    def enableScrollPulsate(self, R, G, B):
        if self.device.fx.misc.scroll_wheel.has('scroll_pulsate'):
            if not self.device.fx.misc.scroll_wheel.pulsate(R, G, B):
                logging.error('%sPulsate' % self.MSG_PROBLEM_ENABLING)
        else:
            logging.warning('The Scroll Pulsate FX is not available')

    def enableScrollBreathSingle(self, R, G, B):
        if self.device.fx.misc.scroll_wheel.has('scroll_breath_single'):
            if not self.device.fx.misc.scroll_wheel.breath_single(R, G, B):
                logging.error('%sBreath Single' % self.MSG_PROBLEM_ENABLING)
        else:
            logging.warning('The Breath Single FX is not available')

    def enableScrollBreathDual(self, R, G, B, R1, G1, B1):
        if self.device.fx.misc.scroll_wheel.has('scroll_breath_dual'):
            if not self.device.fx.misc.scroll_wheel.breath_dual(R, G, B, R1, G1, B1):
                logging.error('%sBreath Dual' % self.MSG_PROBLEM_ENABLING)
        else:
            logging.warning('The Breath Dual FX is not available')

    def enableScrollBreathRandom(self):
        if self.device.fx.misc.scroll_wheel.has('scroll_breath_random'):
            if not self.device.fx.misc.scroll_wheel.breath_random():
                logging.error('%sBreath Random' % self.MSG_PROBLEM_ENABLING)
        else:
            logging.warning('The Breath Random FX is not available')

    def enableScrollSpectrum(self):
        if self.device.fx.misc.scroll_wheel.has('scroll_spectrum'):
            if not self.device.fx.misc.scroll_wheel.spectrum():
                logging.error('%sSpectrum' % self.MSG_PROBLEM_ENABLING)
        else:
            logging.warning('The Spectrum FX is not available')

    def enableScrollReactive(self, R, G, B, time):
        if self.device.fx.misc.scroll_wheel.has('scroll_reactive'):
            if not self.device.fx.misc.scroll_wheel.reactive(R, G, B, time):
                logging.error('%sReactive' % self.MSG_PROBLEM_ENABLING)
        else:
            logging.warning('The Reactive FX is not available')

    def enableScrollStatic(self, R, G, B):
        if self.device.fx.misc.scroll_wheel.has('scroll_static'):
            if not self.device.fx.misc.scroll_wheel.static(R, G, B):
                logging.error('%sStatic' % self.MSG_PROBLEM_ENABLING)
        else:
            logging.warning('The Static FX is not available')

    def enableScrollNone(self):
        if self.device.fx.misc.scroll_wheel.has('scroll_none'):
            if not self.device.fx.misc.scroll_wheel.none():
                logging.error('%sNone' % self.MSG_PROBLEM_ENABLING)
        else:
            logging.warning('The None FX is not available')

    def enableLogoBlinking(self, R, G, B):
        if self.device.fx.misc.logo.has('logo_blinking'):
            if not self.device.fx.misc.logo.blinking(R, G, B):
                logging.error('%sBlinking' % self.MSG_PROBLEM_ENABLING)
        else:
            logging.warning('The Logo Blinking FX is not available')

    def enableLogoPulsate(self, R, G, B):
        if self.device.fx.misc.logo.has('logo_pulsate'):
            if not self.device.fx.misc.logo.pulsate(R, G, B):
                logging.error('%sPulsate' % self.MSG_PROBLEM_ENABLING)
        else:
            logging.warning('The Logo Pulsate FX is not available')

    def enableLogoBreathSingle(self, R, G, B):
        if self.device.fx.misc.logo.has('logo_breath_single'):
            if not self.device.fx.misc.logo.breath_single(R, G, B):
                logging.error('%sBreath Single' % self.MSG_PROBLEM_ENABLING)
        else:
            logging.warning('The Breath Single FX is not available')

    def enableLogoBreathDual(self, R, G, B, R1, G1, B1):
        if self.device.fx.misc.logo.has('logo_breath_dual'):
            if not self.device.fx.misc.logo.breath_dual(R, G, B, R1, G1, B1):
                logging.error('%sBreath Dual' % self.MSG_PROBLEM_ENABLING)
        else:
            logging.warning('The Breath Dual FX is not available')

    def enableLogoBreathRandom(self):
        if self.device.fx.misc.logo.has('logo_breath_random'):
            if not self.device.fx.misc.logo.breath_random():
                logging.error('%sBreath Random' % self.MSG_PROBLEM_ENABLING)
        else:
            logging.warning('The Breath Random FX is not available')

    def enableLogoSpectrum(self):
        if self.device.fx.misc.logo.has('logo_spectrum'):
            if not self.device.fx.misc.logo.spectrum():
                logging.error('%sSpectrum' % self.MSG_PROBLEM_ENABLING)
        else:
            logging.warning('The Spectrum FX is not available')

    def enableLogoReactive(self, R, G, B, time):
        if self.device.fx.misc.logo.has('logo_reactive'):
            if not self.device.fx.misc.logo.reactive(R, G, B, time):
                logging.error('%sReactive' % self.MSG_PROBLEM_ENABLING)
        else:
            logging.warning('The Reactive FX is not available')

    def enableLogoStatic(self, R, G, B):
        if self.device.fx.misc.logo.has('logo_static'):
            if not self.device.fx.misc.logo.static(R, G, B):
                logging.error('%sStatic' % self.MSG_PROBLEM_ENABLING)
        else:
            logging.warning('The Static FX is not available')

    def enableLogoNone(self):
        if self.device.fx.misc.logo.has('logo_none'):
            if not self.device.fx.misc.logo.none():
                logging.error('%sNone' % self.MSG_PROBLEM_ENABLING)
        else:
            logging.warning('The None FX is not available')

    def _make_color_tuple(self, mcol):
    	return (int(mcol.red*255), int(mcol.green*255), int(mcol.blue*255))

    def set_macro(self, key, command):
        if not self.macro_device:
            print("ERROR: device "+self.name+" doesn't implement macro logic")
            return
        self.macro_device.set_macro(key, command)

    #legacy
    def assignMacro(self, key, command):
        script_macro=self.device.macro.create_script_macro_item(command)
        self.device.macro.add_macro(key, script_macro)

    def applyCustom(self, customKb):
        rindex = 0
        for row in customKb.rows:
            cindex=0
            for key in row.keylist:
                # print(self._make_color_tuple(key.color))
                self.device.fx.advanced.matrix.set(
                    rindex, cindex, self._make_color_tuple(key.color)
                )
                cindex+=1
            rindex += 1
        self.device.fx.advanced.draw()

    def get_poll_rate(self):
        if self.device.has('poll_rate'):
            return self.device.poll_rate
        else:
            return -1

    def set_poll_rate(self, value):
        # the poll rate value can only be 125, 500 or 1000
        if not value in [125,500,1000]:
            print('ERROR: Poll rate can only be one of 125, 500 or 1000')
            return
        if not self.device.has('poll_rate'):
            print('ERROR: device %s doesn\'t support poll_rate' % self.device.name)
            return
        self.device.poll_rate = value

    def get_dpi(self):
        if self.device.has('dpi'):
            return self.device.dpi
        else:
            return -1

    def get_max_dpi(self):
        if self.device.has('dpi'):
            return self.device.max_dpi
        else:
            return -1

    def set_dpi(self, dpi1, dpi2):
        if not self.device.has('dpi'):
            print('ERROR: device %s doesn\'t support dpi' % self.device.name)
            return
        if dpi1 > self.device.max_dpi or dpi2 > self.device.max_dpi:
            print('ERROR: the dpi value(s) provided are over the maximum dpi supported by the device')
            return
        self.device.dpi = (dpi1, dpi2)

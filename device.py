# probably not necessary vvvv
import os
import io
import logging
logging.basicConfig(level=logging.DEBUG)

import razer.client as rclient
#import razer.client.constants as razer_constants

device_manager = rclient.DeviceManager()
devlist = []
for device in device_manager.devices:
    if device.type in ['keyboard', 'tartarus', 'mouse']:
        devlist.append(device)


def is_two_digit_hex(s):
    try:
        int(s, 16)
        if len(s) == 2:
            return True
        else:
            return False
    except:
        return False


# This class represents a single device (ie: a keyboard)
class Device:

    def __init__(self, device):
        self.device = device
        self.availableFX = []
        for fx in self.uFXList:
            if self.device.fx.has(fx):
                self.availableFX.append(fx)
        self.availableFX.append('custom')
        self.name = str(device.name)

    friendlyFXList = [
        'Breath',
        'Reactive',
        'Spectrum',
        'Pulsate',
        'Wave',
        'Ripple'
        #'Starlight',
        'Static',
        'None',
        #'Custom'
    ]

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

    MSG_PROBLEM_ENABLING = 'There was an error enabling the FX '

    # legacy:
    def __gksu_run__(self, command):
        toRun = command
        logging.info("running " + toRun)
        os.system(toRun)

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

    # NOTE: removed for future use
    # Enables macro keys
    # M1 generates keycode 191, M5 generates code 195
    # There isn't an explicit option to disable macro,
    # probably you'd want to call reset
    # def enableMacro(self):
    #    # check if macro is available for the current device
    #    if self.KNOWN_OTHER_BUFFERS['MACRO'] in self.other_buffers:
    #        command='echo -n \'1\' > '+self.DRIVER_PATH+self.escaped_uid+'/'+self.KNOWN_OTHER_BUFFERS['MACRO']
    #        self.__gksu_run__(command)
    #        return 0
    #    else:
    #        self.__dbug_print__("Macro keys not available on this device")
    #        return 1

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

    # Set birghtness for backlight
    # gets values between 0 and 255
    def setBrightness(self, value):
        # check if brightness is available for the current device
        if self.device.has('brightness'):
            self.device.brightness = value
        else:
            logging.warning('Brightness is not available')

    def enableFX(self, fx):
        if fx in self.friendlyFXList:
            if fx == "None":
                self.enableNone()
            elif fx == "Spectrum":
                self.enableSpectrum()
            elif fx == "Pulsate":
                self.enablePulsate()
            return 0
        else:
            logging.error("FX not listed")
            return 1

    def _hex2rgb(self, mhex):
        return tuple(int(mhex[i:i+2], 16) for i in (0, 2 ,4))

    def assignMacro(self, key, command):

        script_macro=self.device.macro.create_script_macro_item(command)
        self.device.macro.add_macro(key, script_macro)

    def applyCustom(self, customKb):
        rindex = 0
        for row in customKb.rows:
            cindex=0
            for key in row.keylist:
                self.device.fx.advanced.matrix.set(
                    rindex, cindex, self._hex2rgb(key.color)
                )
                cindex+=1
            rindex += 1
        self.device.fx.advanced.draw()

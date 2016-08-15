#probably not necessary vvvv
import os
import io

import razer.client as rclient
#import razer.client.constants as razer_constants

device_manager = rclient.DeviceManager()
devlist=[]
for device in device_manager.devices:
    if device.type=='keyboard':
        devlist.append(device)

def is_two_digit_hex(s):
    try:
        int (s, 16)
        if len(s)==2:
            return True
        else:
            return False
    except:
        return False


# This class represents a single device (ie: a keyboard)
class Device:

    def __init__(self, device):
        self.device=device
        self.availableFX=[]
        for fx in self.uFXList:
            if self.device.fx.has(fx):
                self.availableFX.append(fx)
        self.name=str(device.name)
        #the following vars are legacy for using the driver directly, the old way
        ddircont=os.listdir(self.DRIVER_PATH)
        for i in ddircont:
            if i[0]=='0':
                with open(self.DRIVER_PATH+i+'/get_serial') as f:
                    s=f.read()
                s.strip()
                if s==str(self.device.serial):
                    self.uid=i
                    self.escaped_uid=self.uid.replace(":", "\\:")
                    break

    # legacy
    DRIVER_PATH='/sys/bus/hid/drivers/razerkbd/'
    HEXPREFIX='\\x'
    KNOWN_MODE_BUFFERS={
        'CUSTOM' : 'mode_custom'
    }
    KNOWN_SET_BUFFERS = {
        'KEYROW' : 'set_key_row'
    }

    # the seemingly duplicate list is needed to distinguish
    # light effects from other mode buffers
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
        'breath_single'
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

    MSG_PROBLEM_ENABLING='There was an error enabling the FX '

    def __dbug_print__(self, message):
        print("DEBUG -> ", message)

    def __gksu_run__(self, command):
        #NOTE: 'or True' is a temp override for GKSU: as udev rules have been implemented in the driver, running the program as root is no longer needed.
        if self.user=='root' or True:
            toRun=command
        else:
            toRun='gksu -m \"razerCommander needs an administrator password to write changes to your device\" \"'+command+'\"'
        self.__dbug_print__("running "+toRun)
        os.system(toRun)

    # below are methods for known buffers

    # Mode buffers

    # Breathing effect mode
    # (only "random mode" (as described here
    # https://github.com/pez2001/razer_chroma_drivers/wiki/Using-the-keyboard-driver)
    # for now)
    def enableRandomBreath(self):
        # check if breathe is available for the current device
        if 'breath_random' in self.availableFX:
            if not self.device.fx.breath_random():
                self.__dbug_print__(self.MSG_PROBLEM_ENABLING+'Breath Random')
        else:
            self.__dbug_print__('The Breath Random FX is not available')

    def enableSingleBreath(self, R, G, B):
        # check if breathe is available for the current device
        if 'breath_single' in self.availableFX:
            if not self.device.fx.breath_single(R, G, B):
                self.__dbug_print__(self.MSG_PROBLEM_ENABLING+'Breath Single')
        else:
            self.__dbug_print__('The Breath Single FX is not available')
            return 1

    def enableDoubleBreath(self, R1, G1, B1, R2, G2, B2):
        # check if breathe is available for the current device
        if 'breath_dual' in self.availableFX:
            if not self.device.fx.breath_single(R1, G1, B1, R2, G2, B2):
                self.__dbug_print__(self.MSG_PROBLEM_ENABLING+'Breath Double')
        else:
            self.__dbug_print__('The Breath Double FX is not available')

    # Reactive effect mode
    # this method takes 3 arguments, the values for red, green and blue
    def enableReactive(self, time, R, G, B): # time can be only 1, 2 or 3
        # check if reactive is available for the current device
        if 'reactive' in self.availableFX:
            if not self.device.fx.reactive(time, R, G, B):
                self.__dbug_print__(self.MSG_PROBLEM_ENABLING+'Reactive')
        else:
            self.__dbug_print__('The Reactive FX is not available')


    # Static effect mode
    # this method takes 3 arguments, the values for red, green and blue
    def enableStatic(self, R, G, B):
        # check if static is available for the current device
        if 'static' in self.availableFX:
            if not self.device.fx.static(R, G, B):
                self.__dbug_print__(self.MSG_PROBLEM_ENABLING+'Static')
        else:
            self.__dbug_print__('The Static FX is not available')

    # Wave effect mode
    # direction is an int: 1 is right, 2 is left
    def enableWave(self, direction):
        # check if wave is available for the current device
        if 'wave' in self.availableFX:
            if direction not in [1, 2]:
                self.__dbug_print__('Error when enabling Wave: value is not 1 or 2')
            elif not self.device.fx.wave(direction):
                self.__dbug_print__(self.MSG_PROBLEM_ENABLING+'Wave')
        else:
            self.__dbug_print__('The Wave FX is not available')

    # NOTE: starlight mode FX temporarely disabled since it's not supported by the lib
    # Starlight mode effect
    # This is pretty easy but undocumented in the driver wiki, so
    # just be aware of that
    #def enableStarlight(self):
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
                self.__dbug_print__(self.MSG_PROBLEM_ENABLING+'None')
        else:
            self.__dbug_print__('The None FX is not available')

    # Turns on or off game mode (it disables the <Super> key)
    # Value has to be 0 to disable or 1 to enable game mode
    def toggleGameMode(self):
        # check if game is available for the current device
        if self.device.has('game_mode_led'):
            #toggles game mode
            self.device.game_mode_led=not self.device.game_mode_led
        else:
            self.__dbug_print__('The Game Mode LED is not available')

    #NOTE: removed for future use
    # Enables macro keys
    # M1 generates keycode 191, M5 generates code 195
    # There isn't an explicit option to disable macro,
    # probably you'd want to call reset
    #def enableMacro(self):
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
                self.__dbug_print__(self.MSG_PROBLEM_ENABLING+'Spectrum')
        else:
            self.__dbug_print__('The Spectrum FX is not available')

    # Pulsate mode effect
    # This should only be supported in the Razer BlackWidow Ultimate 2013
    # and should be similar if not the same as breath effect
    def enablePulsate(self):
        # check if pulsate is available for the current device
        if 'pulsate' in self.availableFX:
            if not self.device.fx.pulsate():
                self.__dbug_print__(self.MSG_PROBLEM_ENABLING+'Pulsate')
        else:
            self.__dbug_print__('The Pulsate FX is not available')

    # Set birghtness for backlight
    # gets values between 0 and 255
    def setBrightness(self, value):
        # check if brightness is available for the current device
        if self.device.has('brightness'):
            self.device.brightness=value
        else:
            self.__dbug_print__('Brightness is not available')

    def enableFX(self, fx):
        if fx in self.lightFXList:
            if fx == "None":
                self.enableNone()
            elif fx == "Spectrum":
                self.enableSpectrum()
            elif fx == "Pulsate":
                self.enablePulsate()
            return 0
        else:
            self.__dbug_print__("FX not listed")
            return 1

    def applyCustom(self, customKb):
        rindex=0
        for row in customKb.rows:
            rowstring=self.HEXPREFIX+'0'+str(rindex)
            for key in row.keylist:
                rowstring+=self.HEXPREFIX+key.color[0:2]+self.HEXPREFIX+key.color[2:4]+self.HEXPREFIX+key.color[4:6]
            command="echo -e -n \""+rowstring+"\" > "+self.DRIVER_PATH+self.escaped_uid+"/"+self.KNOWN_SET_BUFFERS['KEYROW']
            self.__gksu_run__(command)
            rindex+=1
        command="echo -n \"1\" > "+self.DRIVER_PATH+self.escaped_uid+"/"+self.KNOWN_MODE_BUFFERS['CUSTOM']
        self.__gksu_run__(command)

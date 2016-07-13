import os
import io

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
    __DEBUG_PREIFX__='DEBUG (Device): '
    DRIVER_PATH='/sys/bus/hid/drivers/razerkbd/'
    DEVICE_TYPE_NAME='/device_type'
    uid=''
    escaped_uid='' # scripts need to read ":" as "\:"
    name=''
    mode_buffers=[]

    # the seemingly duplicate list is needed to distinguish
    # light effects from other mode buffers
    lightFXList = [
        'Breath',
        'Reactive',
        'Spectrum',
        'Pulsate',
        'Wave',
        'Starlight',
        'Static',
        'None',
    ]
    KNOWN_MODE_BUFFERS={
        'BREATH' : 'mode_breath', # done
        'GAME' : 'mode_game', # done
        'NONE' : 'mode_none', # done
        'REACTIVE' : 'mode_reactive', # done
        'SPECTRUM' : 'mode_spectrum', # WARNING! THIS IS UNTESTED!
        'PULSATE' : 'mode_pulsate', # WARNING! THIS IS UNTESTED!
        'STATIC' : 'mode_static', # done
        'WAVE' : 'mode_wave', # done
        'STARLIGHT' : 'mode_starlight',
    }
    KNOWN_SET_BUFFERS={
        'BRIGHTNESS' : 'set_brightness', # done
    }
    KNOWN_OTHER_BUFFERS={
        'RESET' : 'reset', # done
        'MACRO' : 'macro_keys', # WARNING! THIS IS UNTESTED!
    }
    get_buffers=[]
    set_buffers=[]
    other_buffers=[]
    dir_cont=[]
    user=''

    def __dbug_print__(self, message):
        print(self.__DEBUG_PREIFX__+message)

    def __gksu_run__(self, command):
        if self.user=='root':
            toRun=command
        else:
            toRun='gksu -m \"razerCommander needs an administrator password to write changes to your device\" \"'+command+'\"'
        self.__dbug_print__("running "+toRun)
        os.system(toRun)

    def __init__(self, uid):
        self.user=os.environ['USER']
        self.uid=uid
        self.escaped_uid=uid.replace(":", "\\:")
        # list content of a device's folder
        self.dir_cont=os.listdir(self.DRIVER_PATH+self.uid)
        # initialize known buffers lists
        for i in self.dir_cont:
            if i[:5] == 'mode_':
                self.mode_buffers.append(i)
            elif i[:4] == 'set_':
                self.set_buffers.append(i)
            elif i[:4] == 'get_':
                self.get_buffers.append(i)
            elif i in self.KNOWN_OTHER_BUFFERS.values():
                self.other_buffers.append(i)
        # read the device name from the stream, then close it
        with io.open(self.DRIVER_PATH+self.uid+self.DEVICE_TYPE_NAME, 'r') as devType:
            self.name=devType.read().strip()
            devType.close()

    # below are methods for known buffers

    # Mode buffers

    # Breathing effect mode
    # (only "random mode" (as described here
    # https://github.com/pez2001/razer_chroma_drivers/wiki/Using-the-keyboard-driver)
    # for now)
    def enableRandomBreath(self):
        # check if breathe is available for the current device
        if self.KNOWN_MODE_BUFFERS['BREATH'] in self.mode_buffers:
            command='echo -n \'1\' > '+self.DRIVER_PATH+self.escaped_uid+'/'+self.KNOWN_MODE_BUFFERS['BREATH']
            self.__gksu_run__(command)
            return 0
        else:
            self.__dbug_print__("Breathe not available on this device")
            return 1

    def enableSingleBreath(self, R, G, B):
        # check if breathe is available for the current device
        if self.KNOWN_MODE_BUFFERS['BREATH'] in self.mode_buffers:
            if is_two_digit_hex(R) and is_two_digit_hex(G) and is_two_digit_hex(B):
                command='echo -n -e \'\\x'+R+'\\x'+G+'\\x'+B+'\' > '+self.DRIVER_PATH+self.escaped_uid+'/'+self.KNOWN_MODE_BUFFERS['BREATH']
                self.__gksu_run__(command)
                return 0
            else:
                self.__dbug_print__("R, G and B values are not two digit hexes")
                return 1
        else:
            self.__dbug_print__("Breathe not available on this device")
            return 1

    def enableDoubleBreath(self, R1, G1, B1, R2, G2, B2):
        # check if breathe is available for the current device
        if self.KNOWN_MODE_BUFFERS['BREATH'] in self.mode_buffers:
            if is_two_digit_hex(R1) and is_two_digit_hex(G1) and is_two_digit_hex(B1) \
            and is_two_digit_hex(R2) and is_two_digit_hex(G2) and is_two_digit_hex(B2):
                command='echo -n -e \'\\x'+R1+'\\x'+G1+'\\x'+B1+'\\x'+R2+'\\x'+G2+'\\x'+B2+'\' > '+self.DRIVER_PATH+self.escaped_uid+'/'+self.KNOWN_MODE_BUFFERS['BREATH']
                self.__gksu_run__(command)
                return 0
            else:
                self.__dbug_print__("R, G and B values are not two digit hexes")
                return 1
        else:
            self.__dbug_print__("Breathe not available on this device")
            return 1

    # Reactive effect mode
    # this method takes 3 arguments, the values for red, green and blue
    # default: #FFFFFF (useful when device has only one color)
    def enableReactive(self, time, R="FF", G="FF", B="FF"): # time can be only 1, 2 or 3
        # check if reactive is available for the current device
        if self.KNOWN_MODE_BUFFERS['REACTIVE'] in self.mode_buffers:
            # check if time value is correct
            if time in [1,2,3]:
                # check if R, G, B values are valid
                if is_two_digit_hex(R) and is_two_digit_hex(G) and is_two_digit_hex(B):
                    command='echo -n -e \'\\x0'+str(time)+'\\x'+R+'\\x'+G+'\\x'+B+'\' > '+self.DRIVER_PATH+self.escaped_uid+'/'+self.KNOWN_MODE_BUFFERS['REACTIVE']
                    self.__gksu_run__(command)
                    return 0
                else:
                    self.__dbug_print__("R, G and B values are not two digit hexes")
                    return 1
            else:
                self.__dbug_print__("Time value out of range (possible values are 1, 2 or 3)")
        else:
            self.__dbug_print__("Reactive not available on this device")
            return 1

    # Static effect mode
    # this method takes 3 arguments, the values for red, green and blue
    # default: #FFFFFF (useful when device has only one color)
    def enableStatic(self, R="FF", G="FF", B="FF"):
        # check if static is available for the current device
        if self.KNOWN_MODE_BUFFERS['STATIC'] in self.mode_buffers:
            # check if R, G, B values are valid
            if is_two_digit_hex(R) and is_two_digit_hex(G) and is_two_digit_hex(B):
                command='echo -n -e \'\\x'+R+'\\x'+G+'\\x'+B+'\' > '+self.DRIVER_PATH+self.escaped_uid+'/'+self.KNOWN_MODE_BUFFERS['STATIC']
                self.__gksu_run__(command)
                return 0
            else:
                self.__dbug_print__("R, G and B values are not two digit hexes")
                return 1
        else:
            self.__dbug_print__("Static not available on this device")
            return 1

    # Wave effect mode
    # direction is an int: 1 is right, 2 is left
    def enableWave(self, direction):
        # check if wave is available for the current device
        if self.KNOWN_MODE_BUFFERS['WAVE'] in self.mode_buffers:
            # check if direction is 1 or 2
            if direction in [1,2]:
                command='echo -n \''+str(direction)+'\' > '+self.DRIVER_PATH+self.escaped_uid+'/'+self.KNOWN_MODE_BUFFERS['WAVE']
                self.__gksu_run__(command)
                return 0
            else:
                self.__dbug_print__("Direction value is out of range (possible values: 1 for right or 2 for left)")
                return 1
        else:
            self.__dbug_print__("Wave not available on this device")
            return 1

    # Starlight mode effect
    # This is pretty easy but undocumented in the driver wiki, so
    # just be aware of that
    def enableStarlight(self):
        # check if starlight is available for the current device
        if self.KNOWN_MODE_BUFFERS['STARLIGHT'] in self.mode_buffers:
            command='echo -n \'1\' > '+self.DRIVER_PATH+self.escaped_uid+'/'+self.KNOWN_MODE_BUFFERS['STARLIGHT']
            self.__gksu_run__(command)
            return 0
        else:
            self.__dbug_print__("Starlight not available on this device")
            return 1

    # None effect mode
    # Practically disables lighting effects
    def enableNone(self):
        # check if none is available for the current device
        if self.KNOWN_MODE_BUFFERS['NONE'] in self.mode_buffers:
            command='echo -n \'1\' > '+self.DRIVER_PATH+self.escaped_uid+'/'+self.KNOWN_MODE_BUFFERS['NONE']
            self.__gksu_run__(command)
            return 0
        else:
            self.__dbug_print__("None not available on this device\nWhich is pretty weird, you should probably file a bug report to the developer")
            return 1

    # Turns on or off game mode (it disables the <Super> key)
    # Value has to be 0 to disable or 1 to enable game mode
    def setGameMode(self, value):
        # check if game is available for the current device
        if self.KNOWN_MODE_BUFFERS['GAME'] in self.mode_buffers:
            if value in [0,1]:
                command='echo -n \''+str(value)+'\' > '+self.DRIVER_PATH+self.escaped_uid+'/'+self.KNOWN_MODE_BUFFERS['GAME']
                self.__gksu_run__(command)
                return 0
            else:
                self.__dbug_print__("Value out of range (possible values: 0 to disable, 1 to enable game mode)")
                return 1
        else:
            self.__dbug_print__("Game mode not available on this device")
            return 1

    # Resets the keyboard...?
    # Honestly I don't know what's this for...
    def reset(self):
        # check if none is available for the current device
        if self.KNOWN_OTHER_BUFFERS['RESET'] in self.other_buffers:
            command='echo -n \'1\' > '+self.DRIVER_PATH+self.escaped_uid+'/'+self.KNOWN_OTHER_BUFFERS['RESET']
            self.__gksu_run__(command)
            return 0
        else:
            self.__dbug_print__("Reset not available on this device")
            return 1

    # Enables macro keys
    # M1 generates keycode 191, M5 generates code 195
    # There isn't an explicit option to disable macro,
    # probably you'd want to call reset
    def enableMacro(self):
        # check if macro is available for the current device
        if self.KNOWN_OTHER_BUFFERS['MACRO'] in self.other_buffers:
            command='echo -n \'1\' > '+self.DRIVER_PATH+self.escaped_uid+'/'+self.KNOWN_OTHER_BUFFERS['MACRO']
            self.__gksu_run__(command)
            return 0
        else:
            self.__dbug_print__("Macro keys not available on this device")
            return 1

    # Spectrum mode effect
    # This should only be supported in RGB keyboards
    def enableSpectrum(self):
        # check if spectrum is available for the current device
        if self.KNOWN_MODE_BUFFERS['SPECTRUM'] in self.mode_buffers:
            command='echo -n \'1\' > '+self.DRIVER_PATH+self.escaped_uid+'/'+self.KNOWN_OTHER_BUFFERS['SPECTRUM']
            self.__gksu_run__(command)
            return 0
        else:
            self.__dbug_print__("Spectrum not available on this device")
            return 1

    # Pulsate mode effect
    # This should only be supported in the Razer BlackWidow Ultimate 2013
    # and should be similar if not the same as breath effect
    def enablePulsate(self):
        # check if pulsate is available for the current device
        if self.KNOWN_MODE_BUFFERS['PULSATE'] in self.mode_buffers:
            command='echo -n \'1\' > '+self.DRIVER_PATH+self.escaped_uid+'/'+self.KNOWN_OTHER_BUFFERS['PULSATE']
            self.__gksu_run__(command)
            return 0
        else:
            self.__dbug_print__("Pulsate not available on this device")
            return 1

    # Set birghtness for backlight
    # gets values between 0 and 255
    def setBrightness(self, value):
        # check if brightness is available for the current device
        if self.KNOWN_SET_BUFFERS['BRIGHTNESS'] in self.set_buffers:
            if value in range(0, 256):
                command='echo -n \''+str(value)+'\' > '+self.DRIVER_PATH+self.escaped_uid+'/'+self.KNOWN_SET_BUFFERS['BRIGHTNESS']
                self.__gksu_run__(command)
                return 0
            else:
                self.__dbug_print__("Value out of range (range 0 to 255)")
                return 1
        else:
            self.__dbug_print__("Spectrum not available on this device")
            return 1

    def enableFX(self, fx):
        if fx in self.lightFXList:
            if fx == "Breath":
                self.enableSingleBreath("00","FF","00")
            elif fx == "Reactive":
                self.enableReactive(3)
            elif fx == "Wave":
                self.enableWave(1)
            elif fx == "Starlight":
                self.enableStarlight()
            elif fx == "Static":
                self.enableStatic()
            elif fx == "None":
                self.enableNone()
            elif fx == "Spectrum":
                self.enableSpectrum()
            elif fx == "Pulsate":
                self.enablePulsate()

            return 0
        else:
            self.__dbug_print__("FX not listed")
            return 1

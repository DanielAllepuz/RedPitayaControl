"""
redpitaya_control.py

Daniel Allepuz Requena 2018

daniel.allepuz@icfo.eu
daniel.allepuz@gmail.com

TODO:
-Arbitrary generatoin doesn't work
-Duty cycle doesn't seem to work
"""

import redpitaya_scpi as scpi
from time import sleep
import numpy as np

class RedPitaya(object):
    """
    This class represents a RedPitaya.
    The port defaults to 5000.
    """
    def __init__(self, ip, port = 5000):
        super(RedPitaya, self).__init__()
        #RedPitaya server implemented in redpitaya_scpi.py (code from RedPitaya docs)
        self.rp_server = scpi.scpi(ip, port = port)

    def send_txt(self, cmd):
        """
        Sends text to the RP
        """
        print(str(">> ") + cmd)
        self.rp_server.tx_txt(cmd)

    def set_led(self, led, state):
        """
        Sets the state of one of the LEDs on the RP.
        -led: integer from 0 to 7. (LEDs are labeled on the board)
        -state: boolean True or False, integer 0 or 1
        """
        if led not in range(0, 8):
            print("# WARNING: " + str(led) + "is not a valid LED number, must be between 0 and 7")
        else:
            self.send_txt("DIG:PIN LED" + str(led) + "," + str(int(state)))

    def set_output_signal(self, channel, state, freq = 1000, func = "SINE", amplitude = 1, offset = 0, phase = 0, dcyc = 50, waveform = None):
        """
        Sets a continuous wave form.
        -channel: integer, 1 or 2
        -state: boolean, True (ON) or False (OFF)
        -freq: float in Hz, from 0 to 62.5e6
        -func: string, options are:
            SINE
            SQUARE
            TRIANGLE
            SAWU
            SAWD
            PWM
            ARBITRARY (in this case, a list has to be passed in argument waveform)
        -amplitude: float in volts. From -1V to 1V
        -offset: float in volts. From -1V to 1V
        -phase: float in degrees. From -360º to +360º
        -dcyc: duty cycle, float from 0% to a 100%
        -waveform: list with float values of the custom waveform.
        """
        if channel not in [1, 2]:
            print("# WARNING: channel " + str(channel) + " is not valid, it should be 1 or 2")
            return

        #This is used a lot in the commands
        src = "SOUR" + str(channel)
        if state:
            #Resets waveform generator
            self.send_txt("GEN:RST")
            #Sets frequency
            self.send_txt(src + ":FREQ:FIX " + str(freq))
            #Sets waveform
            self.send_txt(src + ":FUNC " + func.upper())

            wf = list(waveform)
            if func.upper() == "ARBITRARY" and wf!= None:
                self.send_txt(src + ":TRAC:DATA:DATA " + str(list(wf))[1:-1].replace(" ", ""))

            #sets amplitude
            self.send_txt(src + ":VOLT " + str(amplitude))
            #sets offset
            self.send_txt(src + ":VOLT:OFFS " + str(offset))
            #sets phase
            self.send_txt(src + ":PHAS " + str(phase))
            #sets dutycycle
            self.send_txt(src + ":DCYC " + str(dcyc))
            #sets the output ON
            self.send_txt("OUTPUT" + str(channel) + ":STATE ON")
        else:
            #sets the output OFF
            self.send_txt("OUTPUT" + str(channel) + ":STATE OFF")



if __name__ == '__main__':
    rp = RedPitaya("10.9.1.132")
    x = np.linspace(0, 2*np.pi, 100)
    rp.set_output_signal(1, True, freq = 1e6, func = "ARBITRARY", waveform = list(x))
    #sleep(5)
    #rp.set_output_signal(1, False)

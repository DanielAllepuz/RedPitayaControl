"""
Daniel Allepuz Requena 2018

daniel.allepuz@icfo.eu
daniel.allepuz@gmail.com

To install kivy: https://kivy.org/docs/installation
"""
#kivy imports
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, NumericProperty

#Red Pitaya imports
from redpitaya_control import RedPitaya

class RPControlScreen(BoxLayout):
    """
    The beahavior of the GUI is defined here
    """
    #Widget objects
    ip_input = ObjectProperty()
    port_input = ObjectProperty()
    connect_button = ObjectProperty()
    status_label = ObjectProperty()

    redpitaya = None

    channel = 1
    freq = 1000
    func = "SINE"
    amplitude = 1
    offset = 0
    phase = 0
    dcyc = 50

    def __init__(self, *args, **kwargs):
        super(RPControlScreen, self).__init__(*args, *kwargs)

    def connect_to_redpitaya(self):
        self.connect_button.disabled = True
        exceptions = []
        redpitaya = RedPitaya(self.ip_input.text, int(self.port_input.text), exceptions = exceptions)

        self.connect_button.disabled = False

        if len(exceptions) == 0:
            self.set_status("connected")
        elif type(exceptions[0]) is TimeoutError:
            self.set_status("timed out", (1.0, 0, 0, 1.0))
        elif type(exceptions[0]) is ConnectionRefusedError:
            self.set_status("connection refused\n(start SCPI server)", (1.0, 0, 0, 1.0))


    def set_status(self, status, color = [1.0, 1.0, 1.0, 1.0]):
        """
        State is text and color is an array of 4 floats
        """
        if status == "connected":
            color = (0, 1, 0, 1)
        elif status == "disconnected":
            color = (1, 1, 0, 1)

        self.status_label.color = color
        self.status_label.text = "Status: " + status

    def set_channel(self, channel):
        print("Hey")
        self.channel = channel

    def set_func(self, func):
        self.func = func

class RPControlApp(App):
    def build(self):
        screen = RPControlScreen()
        return screen

if __name__ == "__main__":
    app = RPControlApp()
    app.run()

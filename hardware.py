import spidev
import os
from time import sleep
import RPi.GPIO as GPIO
from pidev.stepper import stepper
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty

spi = spidev.SpiDev()

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'

s0 = stepper(port=0, micro_steps=32, hold_current=20, run_current=20, accel_current=20, deaccel_current=20,
             steps_per_unit=200, speed=8)

class ProjectNameGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER


Window.clearcolor = (1, 1, 1, 1)  # White


class MainScreen(Screen):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.count = 0
        self.motor = False

    def pressed(self):
        self.motor = not self.motor

        if self.motor:
            s0.run(0,20)
        else self.motor:


    def shutdown():

    os.system("sudo shutdown now")


Builder.load_file('main.kv')

SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))

if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()

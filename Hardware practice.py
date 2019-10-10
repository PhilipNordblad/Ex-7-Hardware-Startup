import os

import pygame
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.uix.slider import Slider
from pidev.Joystick import Joystick
from kivy.animation import Animation
from pygame import joystick
from threading import Thread


from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton


MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'


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
    """
    Class to handle the main screen and its associated touch events
    """
    string_count = StringProperty()
    condition = ObjectProperty()

    joystick = Joystick(0, True)
    x_axis = ObjectProperty(0,0)
    y_axis = ObjectProperty(0,0)



    def joystick_thread(self):

        while 1:
            self.joystick.refresh()
            self.x_axis = self.joystick.get_axis('x')
            self.y_axis = self.joystick.get_axis('y')
            self.ids.dog.text = str(self.joystick.get_button_state(0))



    def start_Joystick_Thread(self):
        Thread(target=self.joystick_thread).start()


    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.count = 0
        self.condition = False



    def pressed(self):

        self.count = self.count+1
        self.string_count = str(self.count)

    def press(self):

        PauseScreen.pause(pause_scene_name='pauseScene', transition_back_scene=FARMYARD_SCREEN_NAME, text="Weeeeeee!", pause_duration=1)




    def motor_pressed(self):

        self.condition = not self.condition

    def admin_action(self):
        """
        Hidden admin button touch event. Transitions to passCodeScreen.
        This method is called from pidev/kivy/PassCodeScreen.kv
        :return: None
        """
        SCREEN_MANAGER.current = 'passCode'




class farmyard(Screen):

    def __init__(self, **kwargs):
        Builder.load_file('farmyard.kv')

        PassCodeScreen.set_transition_back_screen(MAIN_SCREEN_NAME)

        super(farmyard, self).__init__(**kwargs)


    def go_back(self):
            SCREEN_MANAGER.current = MAIN_SCREEN_NAME


    def animate(self):

        self.anim = Animation(x = .5, y = .5) & Animation(size = (200,200)) + Animation(x = -50, y = -50) & Animation(size = (100,100))

        self.anim.start(self.ids.another_logo)

class AdminScreen(Screen):
    """
    Class to handle the AdminScreen and its functionality
    """

    def __init__(self, **kwargs):
        """
        Load the AdminScreen.kv file. Set the necessary names of the screens for the PassCodeScreen to transition to.
        Lastly super Screen's __init__
        :param kwargs: Normal kivy.uix.screenmanager.Screen attributes
        """
        Builder.load_file('AdminScreen.kv')

        PassCodeScreen.set_admin_events_screen(ADMIN_SCREEN_NAME)  # Specify screen name to transition to after correct password
        PassCodeScreen.set_transition_back_screen(MAIN_SCREEN_NAME)  # set screen name to transition to if "Back to Game is pressed"

        super(AdminScreen, self).__init__(**kwargs)


    @staticmethod
    def transition_back():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def shutdown():
        """
        Shutdown the system. This should free all steppers and do any cleanup necessary
        :return: None
        """
        os.system("sudo shutdown now")

    @staticmethod
    def exit_program():
        """
        Quit the program. This should free all steppers and do any cleanup necessary
        :return: None
        """
        quit()
"""
Widget additions
"""

Builder.load_file('main.kv')

SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(PassCodeScreen(name='passCode'))
SCREEN_MANAGER.add_widget(PauseScreen(name='pauseScene'))
SCREEN_MANAGER.add_widget(AdminScreen(name=ADMIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(farmyard(name=FARMYARD_SCREEN_NAME))

"""
MixPanel
"""


def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()

"""
This module is the GUI module and contains the application logic.
This module necessarily needs the "thesisscanner.kv" file,
because there is the "Kvlang-Code" written, which contains the interface design of the GUI.
The .kv file will be automatically loaded.

Required packages:

    Kivy with Python3.8:
    python -m pip install --upgrade pip wheel setuptools
    python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew --extra-index-url https://kivy.org/downloads/packages/simple
    pip install kivy[base] kivy_examples --pre --extra-index-url https://kivy.org/downloads/simple/

    Kivy with Python3 < 3.8:
    python -m pip install docutils pygments pypiwin32 kivy_deps.sdl2 kivy_deps.glew
    python -m pip install kivy

    By Alexander Bayerlein
"""

import threading
import time
# import kivy
from kivy.clock import Clock
# kivy.require('1.10.0')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen

from thesis_scanner import thesis_scanner_run

# Settings / by Daniel Rindin
timeout_limit = 60  # in sec

# Settings / by Alexander Bayerlein
# set windowsize to maximum or in fullscreen mode
# Window.maximize()
Window.fullscreen = "auto"  # closable by pressing Alt+F4
# set the background color of the window (r, g, b, alpha) -> (alpha can be understood as opacity)
# FHWS Colors: rgb= (236, 116, 3) or hexcode= #ec7403
Window.clearcolor = (.925, .455, .012, 1)


class LeftSideButton(Button):
    pass


class RightSideButton(Button):
    pass


# start screen
class FirstScreen(Screen):
    source = "..\data\paper_input.zip"


# camera screen / by Daniel Rindin
class SecondScreen(Screen):

    def on_enter(self, *args):
        # go back to the start screen after timeout_limit is reached
        Clock.schedule_once(self.switch_back, timeout_limit)

    def switch_back(self, _):
        # only goes back to first screen if the current screen is the camera screen
        if self.manager.current == "second":
            self.manager.current = "first"
            self.manager.transition.direction = "right"

    def take_photo(self):
        # print("saving...")
        self.ids.cam.export_to_png("thesis.png")


# show image screen
class ThirdScreen(Screen):
    source = "thesis.png"

    def on_pre_enter(self, *args):
        img = self.ids["image"]
        img.reload()


# loading screen
class FourthScreen(Screen):
    analyze_thread_running = True
    count = 0

    def on_enter(self, *args):
        self.analyze_thread_running = True

        analyzing_thread = threading.Thread(target=self.analyze_thesis)
        label_thread = threading.Thread(target=self.update_label)

        analyzing_thread.daemon = True
        label_thread.daemon = True

        analyzing_thread.start()
        label_thread.start()

    def update_label(self):
        label = self.ids["animation_label"]

        while self.analyze_thread_running:
            for x in range(4):
                time.sleep(0.5)
                label.text += "."
            self.count += 1

            if self.count == 1:
                label.text = "Name of the Author\n"
            elif self.count == 2:
                label.text = "Date of the Thesis\n"
            elif self.count == 3:
                label.text = "Title of the Thesis\n"
                self.count = 0

    def analyze_thesis(self):
        app = App.get_running_app()

        try:
            analyzed_author, analyzed_thesis = thesis_scanner_run.main()
            app.analyzed_author_and_thesis = ("Analyzed Author:\n" + str(analyzed_author) +
                                              "\n\n\nAnalyzed Thesis-Name:\n" + str(analyzed_thesis))
        except:

            app.analyzed_author_and_thesis = ">> Author and Thesis-Name could not be analyzed. Please try again! <<\n\n" \
                                             ">> If the problem occures again, please contact an employee of the FHWS <<"
        self.manager.current = "fifth"
        self.analyze_thread_running = False


# screen for analyzed data
class FifthScreen(Screen):

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        self.ids.a_name.text = app.analyzed_author_and_thesis


class ThesisScannerApp(App):
    analyzed_author_and_thesis = ""

    def build(self):
        return ScreenManager()


if __name__ == '__main__':
    ThesisScannerApp().run()

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout

from kivy.uix.camera import Camera

#import thesis_scanner.take_picture
#import thesis_scanner.thesis_scanner_run

# RGB, Opacity
from thesis_scanner import thesis_scanner_run

# sets the background of every page r,g,b,alpha/opacity
Window.clearcolor = (1, .58, 0, 1)

Window.maximize()  # for develop process
# Window.fullscreen = ("auto") # for final use


# Create all Pages / Screens of the GUI
# Every class represents one Page
class Page1(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create label for informations
        info = Label(text="[b]1. Insert your thesis in the scanner\n\n"
                          "Please make sure the cover page is facing up\n\n"
                          "2. press \"START\"[/b]", markup=True, font_size=35, halign="center",
                     pos_hint={"center_x": 0.5, "center_y": 0.8})
        # add label to the screen, otherwise it will not be displayed
        self.add_widget(info)

        # create and add info-image to screen
        source = "../data/paper_input.png"
        self.img = Image(source=source, pos_hint={'center_x': .5, 'center_y': .5}, size_hint=(.4, .4))
        self.add_widget(self.img)

        # create button
        self.start = Button(text="[b]START[/b]", markup=True, pos_hint={'center_x': .5, 'y': .1}, size_hint=(.25, .15),
                            font_size=35)
        # bind function to button
        self.start.bind(on_release=self.push_button_start)
        # add button to screen
        self.add_widget(self.start)

    def push_button_start(self, _):
        thesis_scanner_app.screenmanager.current = "camera"


# class CameraClass(App):
#     def build(self):
#         layout = BoxLayout(orientation='vertical')
#
#         # Create a camera object
#         self.cameraObject=Camera(play=True)
#         self.cameraObject.resolution = (1080,720) # Specify the resolution
#
#         # Create a button for taking photograph
#         self.camaraClick = Button(text="Take Photo")
#         self.camaraClick.size_hint=(.5, .2)
#         self.camaraClick.pos_hint={'x': .25, 'y':.75}
#
#         # bind the button's on_press to onCameraClick
#         self.camaraClick.bind(on_press=self.onCameraClick)
#
#         # add camera and button to the layout
#         layout.add_widget(self.cameraObject)
#         layout.add_widget(self.camaraClick)
#
#         # return the root widget
#         return layout
#
#     # Take the current frame of the video as the photo graph
#     def onCameraClick(self, *args):
#         print("saving")
#         self.cameraObject.export_to_png('thesis.png')
#         self.cameraObject.play=False
#         thesis_scanner_app.screenManager.current = "second"
#
# class Cam(FloatLayout):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)

class CameraClass(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create a camera object
        self.cameraObject = Camera(play=True)
        self.cameraObject.resolution = (1080, 720)  # Specify the resolution

        # Create a button for taking photograph
        self.camaraClick = Button(text="Take Photo")
        self.camaraClick.size_hint = (.5, .2)
        self.camaraClick.pos_hint = {'x': .25, 'y': .75}

        # bind the button's on_press to onCameraClick
        self.camaraClick.bind(on_release=self.onCameraClick)

        # add camera and button to the layout
        self.add_widget(self.cameraObject)
        self.add_widget(self.camaraClick)

    def openCamera(self):
        self.cameraObject = Camera(play=True)
        self.cameraObject.resolution = (1080, 720)  # Specify the resolution

    # Take the current frame of the video as the photo graph
    def onCameraClick(self, *args):
        print("saving")
        self.cameraObject.export_to_png('thesis.png')
        self.cameraObject.play = True
        thesis_scanner_app.page2.show_scan()
        thesis_scanner_app.screenmanager.current = "second"


class Page2(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.again = Button(text="Try Again", size_hint=(.15, .15), pos_hint={'center_x': .25, 'y': .1})
        self.again.bind(on_release=self.push_button_try_again)
        self.add_widget(self.again)

        self.next = Button(text="Next Step", size_hint=(.15, .15), pos_hint={'center_x': .75, 'y': .1})
        self.next.bind(on_release=self.push_button_next_step)
        self.add_widget(self.next)

    def show_scan(self):
        source = "thesis.png"
        self.img = Image(source=source, pos_hint={'center_x': .5, 'y': .1})
        self.img.reload()  # reloads the new image from disk if user try again
        self.add_widget(self.img)

    def push_button_try_again(self, _):
        thesis_scanner_app.screenmanager.current = "camera"


    def push_button_next_step(_):
        thesis_scanner_app.page3.analyze_thesis()
        thesis_scanner_app.page3.show_analyzed_data()
        thesis_scanner_app.screenmanager.current = "third"


class Page3(FloatLayout):
    analyzed_name = None
    analyzed_thesis = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.again = Button(text="Try Again", font_size=30, size_hint=(.25, .15),
                            pos_hint={'center_x': .25, 'y': .1})
        self.again.bind(on_release=self.push_button_try_again)
        self.add_widget(self.again)

        self.save = Button(text="Save", font_size=30, size_hint=(.25, .15), pos_hint={'center_x': .75, 'y': .1})
        self.save.bind(on_release=self.push_button_save)
        self.add_widget(self.save)

    def analyze_thesis(self):
        self.analyzed_name, self.analyzed_thesis = thesis_scanner_run.main()

    def show_analyzed_data(self):
        info = Label(text="Name: {}\n\nThesis: {}".format(self.analyzed_name, self.analyzed_thesis),
                     font_size=30,
                     halign="center",
                     pos_hint={"center_x": 0.5, "center_y": 0.8})
        self.add_widget(info)

    def push_button_try_again(self, _):
        thesis_scanner_app.screenmanager.current = "camera"

    def push_button_save(self, _):
        thesis_scanner_app.screenmanager.current = "start"


class ThesisScannerApp(App):
    def build(self):
        self.screenmanager = ScreenManager()

        self.page1 = Page1()
        screen = Screen(name="start")
        screen.add_widget(self.page1)
        self.screenmanager.add_widget(screen)

        self.camera = CameraClass()
        screen = Screen(name="camera")
        screen.add_widget(self.camera)
        self.screenmanager.add_widget(screen)

        self.page2 = Page2()
        screen = Screen(name="second")
        screen.add_widget(self.page2)
        self.screenmanager.add_widget(screen)

        self.page3 = Page3()
        screen = Screen(name="third")
        screen.add_widget(self.page3)
        self.screenmanager.add_widget(screen)

        return self.screenmanager


if __name__ == "__main__":
    thesis_scanner_app = ThesisScannerApp()
    thesis_scanner_app.run()

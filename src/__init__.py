from .assistant import Assistant
from .screen.configWindow import ConfigWindow
from .util.sound import play_sound
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon, QPixmap
import os

class App(object):

    __config_ui_filename = os.path.join("ui", "config_window.ui")
    __listening_sound_filename = os.path.join("sounds", "listening.mp3")

    def __init__(self, app_name, args = []):
        self.__app_name = app_name
        self.__application = QApplication(args)
        self.__icon = QIcon(QPixmap(os.path.join("images", "icon.ico")))

    def __create_config_window(self, title):
        self.__config_window = ConfigWindow(self.__config_ui_filename, title, self.__icon)
        self.__config_window.connect_start_button(self.__start)

    def __create_assistant(self, name, language):
        self.__assistant_name = name
        self.__assistant = Assistant(language)
        self.__assistant.add_event("on_speak", play_sound)
        self.__assistant.add_event("on_listen", lambda *args: play_sound(self.__listening_sound_filename))

    def __start(self):
        assistant_name = self.__config_window.get_name()
        language = self.__config_window.get_language()

        if assistant_name and not assistant_name.isspace():
            self.__config_window.close()
            self.__create_assistant(assistant_name, language)

    def run(self):
        self.__create_config_window("{} - Settings".format(self.__app_name))
        self.__config_window.show()
        return self.__application.exec_()

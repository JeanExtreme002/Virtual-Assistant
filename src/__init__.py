from .assistant import Assistant
from .screen.configWindow import ConfigWindow
from .util.keyboard import on_press_hotkeys
from .util.sound import play_sound
from .util.qtoaster import show_message
from PyQt5.QtWidgets import QApplication
import os

class App(object):

    __config_ui_filename = os.path.join("ui", "config_window.ui")
    __icon_filename = os.path.join("images", "icon.ico")
    __listening_sound_filename = os.path.join("sounds", "listening.mp3")
    __talking = False
    __listener = None

    def __init__(self, app_name, args = []):
        self.__application = QApplication(args)
        self.__app_name = app_name

    def __create_assistant(self, name, language):
        self.__assistant = Assistant(language)
        self.__assistant_name = name
        self.__set_assistant_events()

    def __create_config_window(self, title):
        self.__config_window = ConfigWindow(self.__config_ui_filename, title, self.__icon_filename)
        self.__config_window.connect_start_button(self.__start)

    def __get_config(self):
        assistant_name = self.__config_window.get_name()
        language = self.__config_window.get_language()
        hotkey = self.__config_window.get_hotkey()
        return assistant_name, language, hotkey

    def __set_assistant_events(self):
        self.__assistant.add_event("on_speak", play_sound)
        self.__assistant.add_event("on_chat", self.__show_message)
        self.__assistant.add_event("on_listen", lambda *args: play_sound(self.__listening_sound_filename))
        self.__assistant.add_event("on_recognition", lambda *args: play_sound(self.__listening_sound_filename))

    def __show_message(self, text):
        message = "{}: {}".format(assistant_name, text)
        show_message(message, duration = len(text) * 120 , closable = False)

    def __start(self):
        if self.__listener and self.__listener.is_alive():
            self.__listener.stop()

        assistant_name, language, hotkey = self.__get_config()

        if assistant_name and not assistant_name.isspace() and hotkey:
            self.__config_window.close()
            self.__create_assistant(assistant_name, language)
            self.__listener = on_press_hotkeys({hotkey: self.__talk})

    def __talk(self):
        if not self.__talking and not self.__config_window.is_active():
            self.__talking = True
            self.__assistant.talk()

    def run(self):
        self.__create_config_window("{} - Settings".format(self.__app_name))
        self.__config_window.show()
        return self.__application.exec_()

    def stop(self):
        if self.__listener: self.__listener.stop()
        self.__assistant.stop()
        self.__config_window.close()

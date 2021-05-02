from .assistant import Assistant
from .gui.screens.configWindow import ConfigWindow
from .gui.toaster import show_message
from .gui.trayIcon import QTrayIcon
from .util.keyboard import on_press_hotkeys
from .util.sound import play_sound
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal
import os

class App(QApplication):

    __config_ui_filename = os.path.join("ui", "config_window.ui")
    __icon_filename = os.path.join("images", "icon.ico")
    __listening_sound_filename = os.path.join("sounds", "listening.mp3")

    __talk_signal = pyqtSignal()
    __assistant = None
    __listener = None
    __press_to_talk = None

    def __init__(self, app_name, args = []):
        super().__init__(args)
        self.setQuitOnLastWindowClosed(False)

        self.__talk_signal.connect(self.__talk)
        self.__app_name = app_name

    def __change_config(self):
        self.__stop_listener()
        self.__trayIcon.set_title(self.__app_name)
        self.__config_window.show()

    def __create_assistant(self, name, language):
        self.__assistant = Assistant(language)
        self.__assistant_name = name
        self.__set_assistant_events()

    def __create_config_window(self, title):
        self.__config_window = ConfigWindow(self.__config_ui_filename, title, self.__icon_filename)
        self.__config_window.connect_start_button(self.__start_assistant)

    def __create_tray_icon(self, title):
        self.__trayIcon = QTrayIcon(title, self.__icon_filename, self)
        self.__trayIcon.add_option("Settings", self.__change_config)
        self.__trayIcon.add_option("Quit", self.quit)

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
        message, duration = "{}: {}".format(self.__assistant_name, text), len(text) * 120
        show_message(message, duration = duration, closable = False)

    def __start_assistant(self):
        assistant_name, language, hotkey = self.__get_config()

        if assistant_name and not assistant_name.isspace() and hotkey:
            self.__config_window.close()
            self.__trayIcon.set_title("{} ({})".format(self.__app_name, language.upper()))

            self.__create_assistant(assistant_name, language)
            self.__start_listener(hotkey)

    def __start_listener(self, hotkey = None):
        hotkey = hotkey if hotkey else self.__press_to_talk
        self.__listener = on_press_hotkeys({hotkey: self.__talk_signal.emit})
        self.__press_to_talk = hotkey

    def __stop_listener(self):
        if self.__listener and self.__listener.is_alive():
            self.__listener.stop()

    def __talk(self):
        self.__stop_listener()
        self.__assistant.talk()
        self.__start_listener()

    def exec(self):
        return self.exec_()

    def exec_(self):
        self.__create_tray_icon(self.__app_name)
        self.__create_config_window("{} - Settings".format(self.__app_name))
        self.__change_config()
        return super().exec_()

    def quit(self):
        if self.__listener: self.__listener.stop()
        if self.__assistant: self.__assistant.stop()
        self.__config_window.close()
        super().quit()

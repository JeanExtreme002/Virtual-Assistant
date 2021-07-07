from ..util.system.keyboard import on_press_hotkeys
from .assistantEvents import AssistantEvents
from .commandListEvents import CommandListEvents
from .controller import Controller
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

class ApplicationController(Controller, QWidget):

    __talk_signal = pyqtSignal()

    def __init__(self, application):
        Controller.__init__(self, application)
        QWidget.__init__(self)

        self.__listener = None
        self.__talk_signal.connect(self.__talk)

        self.__assistant_events = AssistantEvents(application)
        self.__command_list_events = CommandListEvents(application)

    def __talk(self):
        self.stop_listener()
        self.get_application().disable_command_list()
        self.get_application().disable_config_window()

        self.get_assistant().talk()

        self.get_application().enable_command_list()
        self.get_application().enable_config_window()
        self.start_listener()

    def set_assistant(self, assistant):
        super().set_assistant(assistant)
        self.__assistant_events.set_assistant(assistant)
        self.__command_list_events.set_assistant(assistant)

    def set_command_list(self, command_list_window):
        self.__command_list_events.set_command_list(command_list_window)

    def start_listener(self):
        hotkey = self.get_application().get_config()["press_to_talk"]
        self.__listener = on_press_hotkeys({hotkey: self.__talk_signal.emit})

    def stop_listener(self):
        if self.__listener and self.__listener.is_alive(): self.__listener.stop()

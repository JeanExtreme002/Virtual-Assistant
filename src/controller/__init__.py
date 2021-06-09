from ..util.system.keyboard import on_press_hotkeys
from .assistantController import AssistantController
from .commandListController import CommandListController
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

        self.__assistant_controller = AssistantController(application)
        self.__command_list_controller = CommandListController(application)

    def __talk(self):
        self.stop_listener()
        self.__assistant_controller.talk()
        self.start_listener()

    def set_assistant(self, assistant):
        super().set_assistant(assistant)
        self.__assistant_controller.set_assistant(assistant)
        self.__command_list_controller.set_assistant(assistant)

    def set_command_list(self, command_list_window):
        self.__command_list_controller.set_command_list(command_list_window)

    def start_listener(self):
        hotkey = self.get_application().get_config()["press_to_talk"]
        self.__listener = on_press_hotkeys({hotkey: self.__talk_signal.emit})

    def stop_listener(self):
        if self.__listener and self.__listener.is_alive(): self.__listener.stop()

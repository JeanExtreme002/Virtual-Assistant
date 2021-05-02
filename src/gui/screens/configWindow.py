from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi

class ConfigWindow(object):

    __active = False

    def __init__(self, ui_filename, title = "", icon = None):
        self.__config_window = loadUi(ui_filename)
        self.__config_window.setWindowTitle(title)
        self.__config_window.setWindowIcon(QIcon(icon))

    def close(self):
        self.__config_window.close()
        self.__active = False

    def connect_start_button(self, function):
        self.__config_window.startButton.clicked.connect(function)

    def get_language(self):
        if self.__config_window.englishSelector.isChecked(): return "en-us"
        if self.__config_window.portugueseSelector.isChecked(): return "pt-br"

    def get_name(self):
        return self.__config_window.assistantName.text()

    def get_hotkey(self):
        key = self.__config_window.pressToTalk.text().lower()
        return "<alt>+" + (key if key else self.__config_window.pressToTalk.placeholderText())

    def is_active(self):
        return self.__active

    def show(self):
        self.__active = True
        self.__config_window.show()

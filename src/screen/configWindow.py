from PyQt5.uic import loadUi

class ConfigWindow(object):

    def __init__(self, ui_filename, title = "", icon = None):
        self.__config_window = loadUi(ui_filename)
        self.__config_window.setWindowTitle(title)
        self.__config_window.setWindowIcon(icon)

    def close(self):
        self.__config_window.close()

    def connect_start_button(self, function):
        self.__config_window.startButton.clicked.connect(function)

    def get_language(self):
        if self.__config_window.englishSelector.isChecked(): return "en-us"
        if self.__config_window.portugueseSelector.isChecked(): return "pt-br"

    def get_name(self):
        return self.__config_window.assistantNameEntry.text()

    def show(self):
        self.__config_window.show()

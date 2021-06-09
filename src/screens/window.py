from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi

class Window(object):

    __active = False

    def __init__(self, ui_filename, title = "", icon = None, on_close = None):
        self._window = loadUi(ui_filename)
        self._window.setWindowTitle(title)
        self._window.setWindowIcon(QIcon(icon))

        if callable(on_close): self._window.closeEvent = lambda event: on_close()

    def close(self):
        self._window.close()
        self.__active = False

    def hide(self):
        self._window.hide()
        self.__active = False

    def is_active(self):
        return self.__active

    def show(self):
        self.__active = True
        self._window.show()

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMenu, QSystemTrayIcon

class QTrayIcon(object):

    __options = []

    def __init__(self, title = None, icon = None, parent = None):
        self.__trayIcon = QSystemTrayIcon(parent = parent)
        self.__context_menu = QMenu()
        self.__trayIcon.setContextMenu(self.__context_menu)

        self.set_icon(icon)
        self.set_title(title)

    def __add_option(self, text, function):
        option = QAction(text)
        option.triggered.connect(function)
        self.__context_menu.addAction(option)
        self.__options.append(option)

    def add_options(self, options):
        for option, function in options.items():
            self.__add_option(option, function)

    def disable_option(self, index):
        self.__options[index].setEnabled(False)

    def enable_option(self, index):
        self.__options[index].setEnabled(True)

    def set_icon(self, icon):
        self.__icon = QIcon(icon)
        self.__trayIcon.setIcon(self.__icon)
        self.__trayIcon.setVisible(True)

    def set_title(self, title):
        self.__trayIcon.setToolTip(title)

    def show_message(self, title, message, duration = 5000, icon = None):
        icon = QIcon(icon) if icon else self.__icon
        self.__trayIcon.showMessage(title, message, self.__icon, duration)

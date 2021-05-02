from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMenu, QSystemTrayIcon

class QTrayIcon(object):

    __options = []

    def __init__(self, title, icon, parent = None):
        self.__trayIcon = QSystemTrayIcon(parent = parent)
        self.__context_menu = QMenu()
        self.__trayIcon.setContextMenu(self.__context_menu)

        self.set_icon(icon)
        self.set_title(title)

    def add_option(self, text, function):
        option = QAction(text)
        option.triggered.connect(function)
        self.__context_menu.addAction(option)
        self.__options.append(option)

    def set_icon(self, icon):
        self.__icon = QIcon(icon)
        self.__trayIcon.setIcon(self.__icon)
        self.__trayIcon.setVisible(True)

    def set_title(self, title):
        self.__trayIcon.setToolTip(title)

    def show_message(self, title, message, duration = 5000, icon = None):
        icon = QIcon(icon) if icon else self.__icon
        self.__trayIcon.showMessage(title, message, self.__icon, duration)

from .assistant import Assistant
from .controller import ApplicationController
from .paths import paths
from .screens import CommandListWindow, ConfigWindow
from .util.gui import toaster
from .util.gui.trayIcon import QTrayIcon
from PyQt5.QtWidgets import QApplication

class Application(QApplication):

    __config = dict()

    def __init__(self, application_name, args = []):
        super().__init__(args)
        self.__application_name = application_name
        self.__controller = ApplicationController(self)

    def __build(self):
        self.__create_command_list_window("{} - Commands".format(self.__application_name), paths["icon"])
        self.__create_config_window("{} - Settings".format(self.__application_name), paths["icon"])
        self.__create_tray_icon(paths["icon"])

    def __change_config(self):
        self.disable_command_list()
        self.__controller.stop_listener()
        self.__reset_assistant()
        self.__show_config_window()

    def __create_assistant(self, name, language):
        self.__assistant = Assistant(name, language)
        self.__controller.set_assistant(self.__assistant)
        self.set_tray_icon_title(language = language)

    def __create_command_list_window(self, title, icon):
        self.__command_list_window = CommandListWindow(
            paths["command_list_ui"], title, icon, on_close = self.__controller.start_listener
        )
        self.__controller.set_command_list(self.__command_list_window)

    def __create_config_window(self, title, icon):
        self.__config_window = ConfigWindow(paths["config_ui"], title, icon, on_close = self.quit)
        self.__config_window.connect_start_button(self.__start_assistant)

    def __create_tray_icon(self, icon):
        self.__tray_icon = QTrayIcon(icon = icon, parent = self)
        self.__tray_icon.add_options(self.__get_tray_icon_options())

    def __get_tray_icon_options(self):
        return {"Show Commands": self.__show_command_list, "Settings": self.__change_config, "Quit": self.quit}

    def __hide_config_window(self):
        self.setQuitOnLastWindowClosed(False)
        self.__config_window.hide()

    def __reset_assistant(self):
        self.__assistant = None
        self.set_tray_icon_title()

    def __set_config(self, **config):
        self.__config.update(config)

    def __show_command_list(self):
        self.__controller.stop_listener()
        self.update_command_list()
        self.__command_list_window.show()

    def __show_config_window(self):
        self.setQuitOnLastWindowClosed(True)
        self.__config_window.show()

    def __start_assistant(self):
        assistant_name, language, hotkey, style = self.__config_window.get_all()

        if assistant_name and not assistant_name.isspace() and hotkey:
            self.__hide_config_window()
            self.__create_assistant(assistant_name, language)
            self.__start_listener(hotkey, style)
            self.enable_command_list()

    def __start_listener(self, press_to_talk, message_style):
        self.__set_config(message_style = message_style, press_to_talk = press_to_talk)
        self.__controller.start_listener()

    def disable_command_list(self):
        self.__tray_icon.disable_option(0)
        self.__command_list_window.hide()

    def disable_config_window(self):
        self.__tray_icon.disable_option(1)
        self.__config_window.hide()

    def enable_command_list(self):
        self.__tray_icon.enable_option(0)

    def enable_config_window(self):
        self.__tray_icon.enable_option(1)

    def exec(self):
        return self.exec_()

    def exec_(self):
        self.__build()
        self.__change_config()
        return super().exec_()

    def get_config(self):
        return self.__config.copy()

    def quit(self):
        self.__controller.stop_listener()
        super().quit()

    def set_tray_icon_title(self, language = "", status = ""):
        language = "({})".format(language.upper() if language and not language.isspace() else "")
        self.__tray_icon.set_title("{} {} {}".format(self.__application_name, language, status))

    def show_message(self, message, duration):
        if self.__config["message_style"] == self.__config_window.MODERN_STYLE:
            toaster.show_message("{}: {}".format(self.__assistant.get_name(), message), duration = duration)
        else:
            self.__tray_icon.show_message(self.__assistant.get_name(), message, duration)

    def update_command_list(self):
        command_list = self.__assistant.get_command_list()
        self.__command_list_window.set_command_list(command_list)

from ..paths import paths
from ..util.system.sound import play_sound
from .controller import Controller

class AssistantController(Controller):

    def __on_listen(self, *args):
        play_sound(paths["listening_sound"])
        self.__set_tray_icon_title(language = self.get_assistant().get_language(), status = "listening...")

    def __on_recognition(self, *args):
        play_sound(paths["listening_sound"])
        self.__set_tray_icon_title(language = self.get_assistant().get_language(), status = "recognizing...")

    def __on_recognition_end(self, *args):
        self.__set_tray_icon_title(language = self.get_assistant().get_language())

    def __set_assistant_events(self):
        assistant = self.get_assistant()
        assistant.set_event("on_speak", play_sound)
        assistant.set_event("on_chat", self.__show_message)
        assistant.set_event("on_listen", self.__on_listen)
        assistant.set_event("on_recognition", self.__on_recognition)
        assistant.set_event("on_recognition_end", self.__on_recognition_end)

    def __set_tray_icon_title(self, language = "", status = ""):
        self.get_application().set_tray_icon_title(language = language, status = status)

    def __show_message(self, text):
        self.get_application().show_message(message = text, duration = len(text) * 120)

    def set_assistant(self, assistant):
        super().set_assistant(assistant)
        self.__set_assistant_events()

    def talk(self):
        self.get_application().disable_command_list()
        self.get_application().disable_config_window()

        self.get_assistant().talk()

        self.get_application().enable_command_list()
        self.get_application().enable_config_window()

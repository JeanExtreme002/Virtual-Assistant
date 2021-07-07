from .controller import Controller

class CommandListEvents(Controller):

    def __on_remove_command(self, voice_command):
        if not self.__validate_voice_command(voice_command):
            return "This is a reserved command and cannot be removed"

        if not self.__has_voice_command(voice_command):
            return "This command does not exist".format(voice_command)

        self.get_assistant().remove_user_command(voice_command)
        self.get_application().update_command_list()

    def __on_set_user_command(self, data):
        if not self.__validate_voice_command(data["voice_command"]):
            return "This is a reserved command and cannot be changed"

        self.get_assistant().set_user_command(
            data["voice_command"], data["terminal_command"], data["info"], data["exec_message"],
            data["success_message"], data["error_message"], data["error_code"]
        )
        self.get_application().update_command_list()

    def __has_voice_command(self, voice_command):
        return voice_command in self.get_assistant().get_command_list()

    def __validate_voice_command(self, voice_command):
        return self.get_assistant().get_command_list().is_user_command(voice_command)

    def set_command_list(self, command_list_window):
        command_list_window.on_set_command(self.__on_set_user_command)
        command_list_window.on_remove_command(self.__on_remove_command)

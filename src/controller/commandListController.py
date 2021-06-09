from .controller import Controller

class CommandListController(Controller):

    def __on_remove_command(self, command):
        try:
            self.get_assistant().remove_user_command(command)
            self.get_application().update_command_list()
        except KeyError: pass # KeyError is raised if the user command does not exist.

    def __on_set_user_command(self, data):
        self.get_assistant().set_user_command(
            data["voice_command"], data["terminal_command"], data["info"], data["exec_message"],
            data["success_message"], data["error_message"], data["error_code"]
        )
        self.get_application().update_command_list()

    def set_command_list(self, command_list_window):
        command_list_window.on_set_command(self.__on_set_user_command)
        command_list_window.on_remove_command(self.__on_remove_command)

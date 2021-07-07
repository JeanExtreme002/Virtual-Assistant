class Command(object):

    def __init__(self, **kwargs):
        """
        Keyword arguments:
        - system_command
        - terminal_command (required if system_command is None)
        - info
        - exec_message
        - success_message
        - error_message
        - error_code
        """

        self.__system_command = kwargs.get("system_command", "")

        if not self.__system_command and not "terminal_command" in kwargs:
            raise TypeError("__init__() missing 1 required argument: 'terminal_command'")

        self.__terminal_command = kwargs.get("terminal_command", "")
        self.__args = kwargs.get("args", "")
        self.__info = kwargs.get("info", "")
        self.__exec_message = kwargs.get("exec_message", "")
        self.__success_message = kwargs.get("success_message", "")
        self.__error_message = kwargs.get("error_message", "")
        self.__error_code = kwargs.get("error_code", 1)

    def is_system_command(self):
        return bool(self.__system_command)

    def to_dict(self):
        return {
            "system_command": self.__system_command,
            "terminal_command": self.__terminal_command,
            "args": self.__args,
            "info": self.__info,
            "exec_message": self.__exec_message,
            "success_message": self.__success_message,
            "error_message": self.__error_message,
            "error_code": self.__error_code
        }

    @property
    def system_command(self):
        return self.__system_command

    @property
    def terminal_command(self):
        return self.__terminal_command

    @property
    def args(self):
        return self.__args

    @property
    def info(self):
        return self.__info

    @property
    def exec_message(self):
        return self.__exec_message

    @property
    def success_message(self):
        return self.__success_message

    @property
    def error_message(self):
        return self.__error_message

    @property
    def error_code(self):
        return self.__error_code

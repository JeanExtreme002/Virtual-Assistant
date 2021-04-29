from .core import default_commands
from .command import CommandParser

def is_default_command(user_command, language = "en-us"):
    user_command = user_command.lower()
    language = language.lower()

    for commands in default_commands[language.lower()]:
        if user_command in commands: return True

import os, sys
sys.path.append(os.getcwd())

from src.assistant.exec.parser import CommandParser, default_commands

user_commands = {
    "do something to that": {
        "command": "#user_command", "terminal_cmd": "execute something to that target", "info": "Just a test"
    },
    "do something": {
        "command": "#user_command2", "terminal_cmd": "execute something", "info": "Just a second test"
    }
}

def test_command_parser():
    command_parser = CommandParser(user_commands, language = "en-us")
    voice_command1, target_args1 = "Search", "something..."
    voice_command2, target_args2 = "Do something", "args..."
    voice_command3, target_args3 = "Do something to that", "args..."
    voice_command4, target_args4 = "This command does not exist", "args..."

    command, terminal_cmd, args, info = command_parser.parse("{} {}".format(voice_command1, target_args1))[:4]
    assert command == default_commands["en-us"][voice_command1.lower()]["command"]
    assert not terminal_cmd
    assert args == target_args1.lower()
    assert info == default_commands["en-us"][command]["info"]

    command, terminal_cmd, args, info = command_parser.parse("{} {}".format(voice_command2, target_args2))[:4]
    assert command == user_commands["do something"]["command"]
    assert terminal_cmd == user_commands["do something"]["terminal_cmd"]
    assert args == target_args2.lower()
    assert info == user_commands["do something"]["info"]

    command, terminal_cmd, args, info = command_parser.parse("{} {}".format(voice_command3, target_args3))[:4]
    assert command == user_commands["do something to that"]["command"]
    assert terminal_cmd == user_commands["do something to that"]["terminal_cmd"]
    assert args == target_args3.lower()
    assert info == user_commands["do something to that"]["info"]

    # Each value must be None because the command does not exist.
    command, terminal_cmd, args, info = command_parser.parse("{} {}".format(voice_command4, target_args4))[:4]
    assert [command, terminal_cmd, args, info].count(None) == 4

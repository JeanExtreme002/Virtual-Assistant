import os, sys, util
sys.path.append(os.getcwd())

from src.assistant.exec.commandList import CommandList
from src.assistant.exec.parser import VoiceCommandParser

command_list = CommandList("EN-US")
parser = VoiceCommandParser(command_list)

def test_parse_system_command():
    command_instance = parser.parse("repeat hello world")
    target_command = command_list.get_command_instance_by_voice_command("repeat")

    assert command_instance.system_command.lower() == "repeat"
    assert command_instance.args.lower() == "hello world"
    assert command_instance.info == target_command.info

def test_parse_user_command():
    voice_command, terminal_command = util.generate_random_user_command()
    command_list.set_user_command(voice_command, {"terminal_command": terminal_command})

    other_voice_command = voice_command + " and something more"
    other_terminal_command = terminal_command + " and something more"
    command_list.set_user_command(other_voice_command, {"terminal_command": other_terminal_command})

    argument1, argument2 = "a docile dog eating meet", "a cute cat sleeping"
    command_instance = parser.parse(voice_command + " " + argument1)
    other_command_instance = parser.parse(other_voice_command + " " + argument2)

    assert command_instance.terminal_command == terminal_command
    assert command_instance.args.lower() == argument1
    assert other_command_instance.terminal_command == other_terminal_command
    assert other_command_instance.args.lower() == argument2

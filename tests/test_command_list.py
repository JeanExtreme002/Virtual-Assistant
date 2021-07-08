import os, sys, util
sys.path.append(os.getcwd())

from src.assistant.exec.commandList import CommandList
from src.assistant.exec.commandList.errors import IncompatibleLanguageException, ReservedCommandException
from src.assistant.exec.parser.command import Command

def test_set_user_command():
    command_list = CommandList("EN-US")
    voice_command, terminal_command = util.generate_random_user_command()

    command_list.set_user_command(voice_command, {"terminal_command": terminal_command})
    command_instance = command_list.get_command_instance_by_voice_command(voice_command)

    assert isinstance(command_instance, Command)
    assert command_instance.terminal_command == terminal_command
    assert not command_instance.is_system_command()

def test_merge_command_lists():
    command_list = CommandList("EN-US")
    other_command_list = CommandList("EN-US")

    voice_command, terminal_command = util.generate_random_user_command()
    other_command_list.set_user_command(voice_command, {"terminal_command": terminal_command})

    assert not voice_command in command_list
    command_list += other_command_list
    assert voice_command in command_list

def test_prevent_merging_imcompatible_command_list():
    try:
        english_command_list = CommandList("EN-US")
        english_command_list += CommandList("PT-BR")
        raise AssertionError("Two different language command lists has been merged")
    except IncompatibleLanguageException: pass

def test_prevent_setting_illegal_command():
    try:
        CommandList("EN-US").set_user_command("repeat", {"terminal_command": "..."})
        raise AssertionError("A reserved command has been accepted to the command list")
    except ReservedCommandException: pass

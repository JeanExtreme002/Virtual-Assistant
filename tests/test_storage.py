import os, sys, util
sys.path.append(os.getcwd())

from src.assistant.storage import UserCommandStorage
from src.assistant.exec.commandList import CommandList

def test_user_command_storage():
    user_command_storage = UserCommandStorage("EN-US")
    user_command_filename = user_command_storage.get_user_command_filename()

    # Saves the stored command list so as not to lose any previously stored user command.
    stored_command_list = user_command_storage.get_command_list()
    user_command_storage.delete_user_commands()
    command_list = user_command_storage.get_command_list()

    assert not os.path.exists(user_command_filename)
    assert not command_list.get_user_commands()

    voice_command, terminal_command = util.generate_random_user_command()
    command_list.set_user_command(voice_command, {"terminal_command": terminal_command})
    user_command_storage.save_user_commands(command_list)

    assert os.path.exists(user_command_filename)

    other_user_command_storage_instance = UserCommandStorage("EN-US")
    loaded_command_list = other_user_command_storage_instance.get_command_list()

    # It must be another instance, have the same user command filename, and the loaded command list
    # must have the user command saved before.
    assert not user_command_storage is other_user_command_storage_instance
    assert user_command_filename == other_user_command_storage_instance.get_user_command_filename()
    assert voice_command in loaded_command_list

    # Restore the old user command storage.
    user_command_storage.delete_user_commands()
    user_command_storage.save_user_commands(stored_command_list)

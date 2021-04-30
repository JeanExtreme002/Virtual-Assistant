import os, sys
sys.path.append(os.getcwd())

from src.assistant.core import errors as assistant_errors
from src.assistant.core.userConfig import UserConfig

language1, language2 = "en-us", "pt-br"

user_config1 = UserConfig(language = language1)
user_config2 = UserConfig(language = language2)

invalid_user_commands1 = {"command_1": "...", "search": "...", "command_2": "..."}    # "search" is a default command
invalid_user_commands2 = {"comando_1": "...", "pesquisar": "...", "comando_2": "..."} # "pesquisar" is a default command

user_commands1 = {"command_1": "...", "command_2": "...", "command_3": "..."}
user_commands2 = {"comando_1": "...", "comando_2": "...", "comando_3": "..."}

def test_set_user_commands():
    user_config1.set_user_commands(user_commands1)
    user_config2.set_user_commands(user_commands2)

def test_load_user_commands():
    new_user_config1 = UserConfig(language = "en-us")
    new_user_config2 = UserConfig(language = "pt-br")

    assert user_config1.get_user_commands() == new_user_config1.get_user_commands()
    assert user_config2.get_user_commands() == new_user_config2.get_user_commands()

def test_delete_user_commands():
    user_config1.delete_user_commands()
    user_config2.delete_user_commands()

    assert not user_config1.get_user_commands()
    assert not user_config2.get_user_commands()

def test_block_illegal_commands():
    try:
        user_config1.set_user_commands(invalid_user_commands1)
        raise AssertionError("A illegal command ({}) has been accepted".format(language1))
    except assistant_errors.IllegalCommandException: pass

    try:
        user_config2.set_user_commands(invalid_user_commands2)
        raise AssertionError("A illegal command ({}) has been accepted".format(language2))
    except assistant_errors.IllegalCommandException: pass

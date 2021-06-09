from os.path import join

image_directory = "images"
sound_directory = "sounds"
ui_directory = "ui"

paths = {
    "command_list_ui": join(ui_directory, "command_list_window.ui"),
    "config_ui": join(ui_directory, "config_window.ui"),
    "listening_sound": join(sound_directory, "listening.mp3"),
    "icon": join(image_directory, "icon.ico")
}

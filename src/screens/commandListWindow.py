from PyQt5.QtWidgets import QHeaderView, QPushButton, QTableWidgetItem
from .window import Window

class CommandListWindow(Window):

    def __init__(self, ui_filename, title = "", icon = None, on_close = None):
        super().__init__(ui_filename = ui_filename, title = title, icon = icon, on_close = on_close)

        self._window.commandList.selectionModel().selectionChanged.connect(self.__on_change_selection)
        self._window.commandList.verticalHeader().hide()
        self._window.commandList.horizontalHeader().hide()
        self._window.commandList.horizontalHeader().setStretchLastSection(True)
        self._window.commandList.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self._window.setButton.clicked.connect(self.__set_command)
        self._window.removeButton.clicked.connect(self.__remove_command)

    def __on_change_selection(self, selected, deselected):
        indexes = selected.indexes()
        if not indexes: return

        voice_command = self._window.commandList.item(indexes[0].row(), 0).text()
        command_data = self.__command_list[voice_command]

        self._window.voiceCommand.setText(voice_command)
        self._window.terminalCommand.setText(command_data.get("terminal_command", ""))
        self._window.info.setText(command_data.get("info", ""))
        self._window.execMessage.setText(command_data.get("exec_message", ""))
        self._window.successMessage.setText(command_data.get("success_message", ""))
        self._window.errorMessage.setText(command_data.get("error_message", ""))
        self._window.errorCode.setValue(command_data.get("error_code", 0))

    def __remove_command(self):
        voice_command = self._window.voiceCommand.text()
        if voice_command.replace(" ", ""): self.__remove_function(voice_command)

    def __set_command(self):
        voice_command = self._window.voiceCommand.text()
        terminal_command = self._window.terminalCommand.text()

        if voice_command.replace(" ", "") and terminal_command.replace(" ", ""):
            self.__set_function({
                "voice_command": voice_command,
                "terminal_command": terminal_command,
                "info": self._window.info.text(),
                "exec_message": self._window.execMessage.text(),
                "success_message": self._window.successMessage.text(),
                "error_message": self._window.errorMessage.text(),
                "error_code": self._window.errorCode.value()
            })

    def on_set_command(self, function):
        if callable(function): self.__set_function = function

    def on_remove_command(self, function):
        if callable(function): self.__remove_function = function

    def set_command_list(self, command_list: dict):
        self.__command_list = command_list
        self._window.commandList.setRowCount(len(self.__command_list))
        self._window.commandList.setColumnCount(2)

        current_row = 0

        for command, data in self.__command_list.items():
            self._window.commandList.setItem(current_row, 0, QTableWidgetItem(command))
            self._window.commandList.setItem(current_row, 1, QTableWidgetItem(data["info"]))
            current_row += 1

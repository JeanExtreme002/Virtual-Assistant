from .window import Window

class ConfigWindow(Window):

    DEFAULT_STYLE = 0
    MODERN_STYLE = 1

    def connect_start_button(self, function):
        self._window.startButton.clicked.connect(function)

    def get_all(self):
        return self.get_name(), self.get_language(), self.get_hotkey(), self.get_style()

    def get_hotkey(self):
        key = self._window.pressToTalk.text().lower()
        return "<alt>+" + (key if key else self._window.pressToTalk.placeholderText())

    def get_language(self):
        if self._window.englishSelector.isChecked(): return "en-us"
        if self._window.portugueseSelector.isChecked(): return "pt-br"

    def get_name(self):
        return self._window.assistantName.text()

    def get_style(self):
        if self._window.defaultStyleSelector.isChecked(): return self.DEFAULT_STYLE
        if self._window.modernStyleSelector.isChecked(): return self.MODERN_STYLE

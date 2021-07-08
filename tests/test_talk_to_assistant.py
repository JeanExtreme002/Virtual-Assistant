import os, sys
sys.path.append(os.getcwd())

from src.assistant import Assistant
audio_filename = os.path.join("tests", "audio", "en_repeat_hello_world.wav")

def check_echo(text, language):
    text, language = text.lower(), language.lower()
    if language == "en-us": assert text == "hello world"

def test_assistant():
    assistant = Assistant(language = "EN-US")
    assistant.set_event("on_chat", lambda text: check_echo(text, "en-us"))
    assistant.talk(audio_filename)

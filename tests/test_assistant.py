import os, sys
sys.path.append(os.getcwd())

from src.assistant import Assistant

english_audio_filename = "tests/audio/repeat_hello_world_en.wav"
portuguese_audio_filename = "tests/audio/repeat_hello_world_pt.wav"

def check_echo(text, language):
    text = text.lower()
    assert language == "pt-br" and text == "olá mundo"
    assert language == "en-us" and text == "hello world"

def test_english_assistant():
    assistant = Assistant(language = "EN-US")
    assistant.set_event("on_chat", lambda text: check_echo(text, "en-us"))
    assistant.talk(english_audio_filename)

def test_portuguese_assistant():
    assistant = Assistant(language = "PT-BR")
    assistant.set_event("on_chat", lambda text: check_echo(text, "pt-br"))
    assistant.talk(portuguese_audio_filename)

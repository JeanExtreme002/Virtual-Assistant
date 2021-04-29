import os, sys
sys.path.append(os.getcwd())

from src.assistant.speech import Speech

testing_audio_filename = os.path.join("tests", "audio", "hello_world.wav")
speech = Speech()

def test_speech_to_text():
    result = speech.get_text_from_audio(testing_audio_filename)
    assert result.lower() == "hello world"

def test_text_to_speech():
    bytesIO = speech.text_to_speech("Hello World!", language = "en-us")
    assert len(bytesIO.read()) > 5000

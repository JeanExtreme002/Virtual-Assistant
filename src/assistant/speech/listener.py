from speech_recognition import AudioFile, Microphone, Recognizer

class Listener(object):

    def __init__(self):
        self.__recognizer = Recognizer()

    def __get_audio_from_file(self, filename, timeout = None, on_listen = None):
        with AudioFile(filename) as source:
            return self.__get_audio_from_source(source, timeout = timeout, on_listen = on_listen)

    def __get_audio_from_microphone(self, timeout = None, on_listen = None):
        with Microphone() as source:
            self.__recognizer.adjust_for_ambient_noise(source, duration = 1.0)
            return self.__get_audio_from_source(source, timeout = timeout, on_listen = on_listen)

    def __get_audio_from_source(self, source, timeout = None, on_listen = None):
        if callable(on_listen): on_listen()
        return self.__recognizer.listen(source, timeout = timeout)

    def get_text_from_audio(self, filename, language = "en-us", timeout = None, on_listen = None, on_recognition = None):
        try:
            audio = self.__get_audio_from_file(filename, timeout = None, on_listen = None)
            if callable(on_recognition): on_recognition()
            return self.__recognizer.recognize_google(audio, language = language)
        except FileNotFoundError as error:
            raise error
        except:
            return str()

    def speech_to_text(self, language = "en-us", timeout = None, on_listen = None, on_recognition = None):
        try:
            audio = self.__get_audio_from_microphone(timeout = timeout, on_listen = on_listen)
            if callable(on_recognition): on_recognition()
            return self.__recognizer.recognize_google(audio, language = language)
        except:
            return str()

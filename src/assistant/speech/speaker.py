from gtts import gTTS, gTTSError
from io import BytesIO

class Speaker(object):

    def __get_bytes(self, gtts):
        fp = BytesIO()

        try:
            gtts.write_to_fp(fp)
            fp.seek(0)
            return fp
        except gTTSError: return None

    def text_to_speech(self, text, language = "en"):
        gtts = gTTS(text = text, lang = language.split("-")[0], slow = False)
        return self.__get_bytes(gtts)

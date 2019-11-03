from pygame import mixer
import os

class Sounds(object):

    sounds_path = os.path.join("assistant","sounds","effects")
    listening_fn = os.path.join(sounds_path,"listening.mp3")
    message_fn = os.path.join(sounds_path,"message.mp3")

    def __init__(self,buffer=64):
        mixer.init(buffer=buffer)
    
    def play_sound(self,fn):
        mixer.music.load(fn)
        mixer.music.play()
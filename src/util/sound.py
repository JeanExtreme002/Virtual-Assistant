from pygame import mixer

mixer.init(buffer = 512)

def play_sound(filename_or_fp):
    mixer.music.load(filename_or_fp)
    mixer.music.play()

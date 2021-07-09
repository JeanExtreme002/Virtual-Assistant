from pygame import mixer

__all__ = ("init_mixer", "play_sound")

is_mixer_initialized = False

def init_mixer(buffer = 64):
    mixer.init(buffer = buffer)
    is_mixer_initialized = True

def play_sound(filename_or_fp):
    if not is_mixer_initialized: init_mixer()
    mixer.music.load(filename_or_fp)
    mixer.music.play()

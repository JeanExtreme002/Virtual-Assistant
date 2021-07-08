import random

def generate_random_user_command():
    voice_command = "test-" + "".join([chr(random.randint(97, 122)) for i in range(100)])
    terminal_command = "test-" + "".join([chr(random.randint(97, 122)) for i in range(100)])
    return voice_command, terminal_command

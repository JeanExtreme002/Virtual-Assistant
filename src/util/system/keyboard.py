from pynput import keyboard

def on_press_hotkeys(hotkeys = {}):
    if not hotkeys: return
    
    thread = keyboard.GlobalHotKeys(hotkeys)
    thread.start()
    return thread

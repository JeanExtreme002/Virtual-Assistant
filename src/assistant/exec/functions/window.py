import pygetwindow

class WindowNotFoundError(Exception): pass

def close_active_window():
    pygetwindow.getActiveWindow().close()

def close_window_by_title(window_title):
    window = find_window_by_title(window_title)
    window.close()

def find_window_by_title(window_title):
    window_title = window_title.lower()
    windows = pygetwindow.getWindowsWithTitle(window_title)
    titles = [window.title for window in windows]

    if window_title in titles:
        for window in windows:
            if window.title.lower() == window_title: return window

    for window in windows:
        if window.title.lower().startswith(window_title): return window

    if windows: return windows[0]
    else: raise WindowNotFoundError(window_title)

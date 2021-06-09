from .environment import paths
from subprocess import getstatusoutput
from threading import Thread
import os

def dir_exists(directory):
    return os.path.exists(directory) and os.path.isdir(directory)

def exec_command(command):
    return getstatusoutput(command)

def file_exists(filename):
    return os.path.exists(filename) and os.path.isfile(filename)

def get_filename_by_name(filename, path, only_ext = []):

    for found in os.listdir(path):
        abs_path = os.path.abspath(os.path.join(path, found))

        if file_exists(abs_path) and found.lower().startswith(filename.lower()):
            if not only_ext or os.path.splitext(found)[-1].lower() in only_ext:
                return abs_path

def open(path):
    exec_command('start "" "{}"'.format(path))

def open_program(name):
    Thread(target = lambda: exec_command(name)).start()

def open_directory(directory):
    for path in paths.split(";"):
        path = os.path.join(path, directory)
        abs_path = os.path.abspath(path).lower()

        if dir_exists(abs_path): return open(abs_path)
    raise NotADirectoryError(directory)

def open_file(filename, only_ext = []):
    file_ext = os.path.splitext(filename)[-1]

    for path in paths.split(";"):
        if file_ext and not only_ext:
            abs_path = os.path.abspath(os.path.join(path, filename))
            if file_exists(abs_path): return Thread(target = lambda: open(abs_path)).start()
        else:
            found = get_filename_by_name(filename, os.path.abspath(path), only_ext)
            if found: return Thread(target = lambda: open(found)).start()

    raise FileNotFoundError(filename)

def run_program(name):
    if name == "calculator": open_program("calc")
    elif name == "explorer": open_program("explorer")
    else: open_file(name, [".exe", ".lnk"])

from PyQt5.QtWidgets import QFileDialog

def get_save_filename():
    return QFileDialog.getSaveFileName()[0]

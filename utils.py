import cmd
import os
import json

from PyQt5 import QtCore


# https://opentdb.com/api.php?amount=50&category=18&difficulty=medium&type=multiple

def read_colors_from_file(file_path):
    with open(file_path, 'r') as file:
        colors_data = json.load(file)
    return colors_data


def buttonClicked():
    os.system(cmd)
    QtCore.QCoreApplication.instance().quit()

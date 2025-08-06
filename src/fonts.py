import os
import threading

from src.qt import *


repo_dir = os.path.dirname(os.path.dirname(__file__))
fonts_dir = os.path.join(repo_dir, "resources", "fonts")


def paths_in_dir_recursive(base):
    paths = []
    for name in os.listdir(base):
        path = os.path.join(base, name)
        if os.path.isdir(path):
            paths.extend(paths_in_dir_recursive(path))
        else:
            paths.append(path)
    return paths


def load_fonts():
    for path in paths_in_dir_recursive(fonts_dir):
        QFontDatabase.addApplicationFont(path)


font_loading_thread = threading.Thread(target=load_fonts)
font_loading_thread.start()


def app_icon_font(icon_size):
    font_loading_thread.join()
    font_size = int(round(3.0 * icon_size / 4.0))
    font = QFont(
        "Cardo",
        font_size,
        QFont.Weight.Bold,
    )
    font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
    return font

import os
import traceback

import natsort

from src import settings

repo_dir = os.path.dirname(os.path.dirname(__file__))
themes_dir = os.path.join(repo_dir, "resources", "themes")
os.makedirs(settings.app_user_added_themes_dir, exist_ok=True)


def get_available_themes():
    themes = []
    for file_name in os.listdir(themes_dir):
        theme, ext = os.path.splitext(file_name)
        if ext.lower() == ".qss":
            themes.append(theme)
    for file_name in os.listdir(settings.app_user_added_themes_dir):
        theme, ext = os.path.splitext(file_name)
        if ext.lower() == ".qss":
            themes.append(theme)
    return natsort.natsorted(themes)


style_sheet = None


def load_theme():
    global style_sheet
    try:
        with open(
            os.path.join(themes_dir, f"{settings.app_theme}.qss"),
            mode="r",
            encoding="utf-8",
        ) as file:
            style_sheet = file.read()
    except FileNotFoundError:
        try:
            with open(
                os.path.join(
                    settings.app_user_added_themes_dir,
                    f"{settings.app_theme}.qss",
                ),
                mode="r",
                encoding="utf-8",
            ) as file:
                style_sheet = file.read()
        except FileNotFoundError:
            print(traceback.format_exc())
            settings.app_theme = settings.defaults["app_theme"]
            settings.save()
            load_theme()
            return


load_theme()

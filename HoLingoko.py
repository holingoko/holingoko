from src import fonts
from src import settings
from src import system
from src import tools
from src.log import log

if not system.running_built_app:
    fonts.font_loading_thread.join()
    tools.update_source_code_resource()


def run():
    from src import app
    from src import dict_window
    from src import main_window
    from src import state
    from src import window

    if settings.app_startup_window == settings.StartupWindow.NEW_TEXT_EDITOR:
        main_window.MainWindow().show()
    elif (
        settings.app_startup_window
        == settings.StartupWindow.MOST_RECENTLY_CLOSED
    ):
        prev_close_time = None
        for close_time, window_state in sorted(
            state.windows.values(),
            reverse=True,
        ):
            if (
                prev_close_time is None
                or prev_close_time - close_time
                < settings.app_close_time_tolerance
            ):
                main_window.MainWindow(window_state).show()
                prev_close_time = close_time
        if not window.Window.windows:
            main_window.MainWindow().show()
    elif (
        settings.app_startup_window == settings.StartupWindow.DICTIONARY_WINDOW
    ):
        dict_window.DictWindow().show()
    app.exec()


if settings.app_enable_logging:
    log(run)
else:
    run()

import os

from src import app_info
from src import dict_database
from src import dict_entry_window
from src import dict_template_entry_window
from src import dict_template_window
from src import dict_settings_window
from src import language
from src import settings
from src import state
from src import text_editor
from src import utils
from src.language import tr
from src.qt import *


def no_state_change(f):
    def wrapped_function(*args, **kwargs):
        last_selected_dict = state.last_selected_dict
        f(*args, **kwargs)
        state.last_selected_dict = last_selected_dict

    return wrapped_function


def create_new_dict_path_with_non_existing_name(name):
    path = os.path.join(settings.dict_dir, f"{name}{app_info.db_ext}")
    if not os.path.exists(path):
        return path, name
    name_template = f"{name} {{}}"
    i = 1
    while True:
        path = os.path.join(
            settings.dict_dir, f"{name_template.format(i)}{app_info.db_ext}"
        )
        if os.path.exists(path):
            i = i + 1
        else:
            return path, os.path.splitext(os.path.basename(path))[0]


def open_dict_settings_window(name):
    dict_settings_window_ = dict_settings_window.DictSettingsWindow()
    dict_settings_window_.dict_combo_box.set_name(name)
    dict_settings_window_.show()
    return dict_settings_window_


@no_state_change
def open_windows_for_create_entry_example(
    name,
    db,
    entry_id,
):
    open_dict_settings_window(name)
    dict_entry_window_ = dict_entry_window.DictEntryWindow(db, entry_id)
    dict_entry_window_.show()
    dict_entry_window_.on_data_change()


@no_state_change
def open_windows_for_create_templates_example(
    name,
    db,
    entry_id,
    template_name,
    row_data,
):
    open_dict_settings_window(name)
    dict_template_window_ = dict_template_window.DictTemplateWindow(
        db,
        entry_id,
    )
    dict_template_window_.test_list_edit.set_row_data(row_data)
    dict_template_window_.on_data_change()
    dict_template_window_.on_save(close_if_success=False)
    dict_template_window_.show()
    dict_entry_window_ = dict_entry_window.DictEntryWindow(db)
    template_entry_window = dict_template_entry_window.DictTemplateEntryWindow(
        dict_entry_window_.db,
        dict_entry_window_.on_dict_template_entry_window_save,
    )
    template_entry_window.template_combo_box.setCurrentText(template_name)
    template_entry_window.stem_list_edit.set_row_data(row_data)
    template_entry_window.on_save(close_if_success=False)
    dict_entry_window_.on_save(close_if_success=False)
    dict_entry_window_.add_child_window(template_entry_window)
    dict_entry_window_.show()
    dict_entry_window_.on_data_change()
    template_entry_window.show()
    dict_template_window_.raise_()
    dict_template_window_.on_data_change()


@no_state_change
def open_windows_for_set_format_example(
    name,
    db,
    entry_id,
):
    dict_settings_window_ = open_dict_settings_window(name)
    dict_entry_window_ = dict_entry_window.DictEntryWindow(db, entry_id)
    dict_entry_window_.on_save(close_if_success=False)
    dict_entry_window_.show()
    dict_settings_window_.raise_()


def create_dictionary_english():
    name = tr("English Example")
    path, name = create_new_dict_path_with_non_existing_name(name)
    db = dict_database.DictDatabase(path)
    db.info.set_long_entry_format(
        f"<b>{{{tr("English")}}}</b><br>"
        f'{{{tr("Part Of Speech")}}}<br>'
        "{"
        + tr("{0} of <b>{1}</b>:").format(
            f"{{{tr("Inflection")}}}", f"{{{tr("Base Form")}}}"
        )
        + "}"
        f"{{{tr("Definitions")}}}"
    )
    db.info.set_entry_joiner("<hr>")
    db.tags.create_tag(tr("English"), True, "{{},... {}}", "", 0)
    db.tags.create_tag(tr("Part Of Speech"), False, "{{},... {}}", "", 1)
    db.tags.create_tag(tr("Inflection"), False, "{{},... {}}", "", 2)
    db.tags.create_tag(tr("Base Form"), False, "{{},... {}}", "", 3)
    db.tags.create_tag(
        tr("Definitions"),
        False,
        "{<ol><li>{}</li>...<li>{}</li></ol>}",
        "",
        4,
    )
    return name, db


def create_dictionary_mandarin_chinese():
    name = tr("Mandarin Chinese Example")
    path, name = create_new_dict_path_with_non_existing_name(name)
    db = dict_database.DictDatabase(path)
    db.info.set_long_entry_format(
        f"{{{tr("Traditional")}}}<br>"
        f"{{{tr("Simplified")}}}<br>"
        f"{{{tr("Pinyin")}}}<br>"
        f"{{{tr("Zhuyin")}}}<br>"
        f"{{{tr("Part Of Speech")}}}"
        f"{{{tr("Definitions")}}}"
    )
    db.info.set_entry_joiner("<hr>")
    db.tags.create_tag(tr("Traditional"), True, "{{},... {}}", "", 0)
    db.tags.create_tag(tr("Simplified"), True, "{{},... {}}", "", 1)
    db.tags.create_tag(tr("Pinyin"), True, "{{},... {}}", "", 2)
    db.tags.create_tag(tr("Zhuyin"), True, "{{},... {}}", "", 3)
    db.tags.create_tag(tr("Part Of Speech"), False, "{{},... {}}", "", 4)
    db.tags.create_tag(
        tr("Definitions"),
        False,
        "{<ol><li>{}</li>...<li>{}</li></ol>}",
        "",
        5,
    )
    return name, db


def create_dictionary_hindi():
    name = tr("Hindi Example")
    path, name = create_new_dict_path_with_non_existing_name(name)
    db = dict_database.DictDatabase(path)
    db.info.set_long_entry_format(
        f"<b>{{{tr("Hindi")}}}</b>"
        f"<p>{{{tr("Urdu")}}}</p>"
        f"{{{tr("Part Of Speech")}}}"
        "{"
        + tr("{0} of <b>{1}</b> /[{2}/]:").format(
            f"{{{tr("Inflection")}}}",
            f"{{{tr("Base Form Hindi")}}}",
            f"{{{tr("Base Form Urdu With Diacritics")}}}",
        )
        + "}"
        f"{{{tr("Definitions")}}}"
    )
    db.info.set_entry_joiner("<hr>")
    db.tags.create_tag(tr("Hindi"), True, "{{},... {}}", "", 0)
    db.tags.create_tag(tr("Urdu"), True, "{{},... {}}", "", 1)
    db.tags.create_tag(tr("Part Of Speech"), False, "{{},... {}}", "", 2)
    db.tags.create_tag(
        tr("Inflection"),
        False,
        "{<ul><li>{}</li>...<li>{}</li></ul>}",
        "",
        3,
    )
    db.tags.create_tag(
        tr("Base Form Hindi"),
        False,
        "{{},... {}}",
        "",
        4,
    )
    db.tags.create_tag(
        tr("Base Form Urdu With Diacritics"),
        True,
        "{{},... {}}",
        "",
        5,
    )
    db.tags.create_tag(
        tr("Definitions"),
        False,
        "{<ol><li>{}</li>...<li>{}</li></ol>}",
        "",
        6,
    )
    return name, db


def create_dictionary_spanish():
    name = tr("Spanish Example")
    path, name = create_new_dict_path_with_non_existing_name(name)
    db = dict_database.DictDatabase(path)
    db.info.set_long_entry_format(
        f"<b>{{{tr("Spanish")}}}</b><br>"
        f'{{{tr("Part Of Speech")}}}<br>'
        "{"
        + tr("{0} of <b>{1}</b>:").format(
            f"{{{tr("Inflection")}}}", f"{{{tr("Base Form")}}}"
        )
        + "}"
        f"{{{tr("Definitions")}}}"
    )
    db.info.set_entry_joiner("<hr>")
    db.tags.create_tag(tr("Spanish"), True, "{{},... {}}", "", 0)
    db.tags.create_tag(tr("Part Of Speech"), False, "{{},... {}}", "", 1)
    db.tags.create_tag(tr("Inflection"), False, "{{},... {}}", "", 2)
    db.tags.create_tag(tr("Base Form"), False, "{{},... {}}", "", 3)
    db.tags.create_tag(
        tr("Definitions"),
        False,
        "{<ol><li>{}</li>...<li>{}</li></ol>}",
        "",
        4,
    )
    return name, db


def create_dictionary_arabic():
    name = tr("Arabic Example")
    path, name = create_new_dict_path_with_non_existing_name(name)
    db = dict_database.DictDatabase(path)
    db.info.set_long_entry_format(
        f"<p><b>{{{tr("Arabic")}}}</b></p>"
        f"{{{tr("Part Of Speech")}}}"
        f"{{{tr("Definitions")}}}"
    )
    db.info.set_entry_joiner("<hr>")
    db.tags.create_tag(tr("Arabic"), True, "{{},... {}}", "", 0)
    db.tags.create_tag(tr("Part Of Speech"), True, "{{},... {}}", "", 1)
    db.tags.create_tag(
        tr("Definitions"),
        False,
        "{<ol><li>{}</li>...<li>{}</li></ol>}",
        "",
        2,
    )
    return name, db


def create_dictionary_french():
    name = tr("French Example")
    path, name = create_new_dict_path_with_non_existing_name(name)
    db = dict_database.DictDatabase(path)
    db.info.set_long_entry_format(
        f"<b>{{{tr("French")}}}</b><br>"
        f'{{{tr("Part Of Speech")}}}<br>'
        "{"
        + tr("{0} of <b>{1}</b>:").format(
            f"{{{tr("Inflection")}}}", f"{{{tr("Base Form")}}}"
        )
        + "}"
        f"{{{tr("Definitions")}}}"
    )
    db.info.set_entry_joiner("<hr>")
    db.tags.create_tag(tr("French"), True, "{{},... {}}", "", 0)
    db.tags.create_tag(tr("Part Of Speech"), False, "{{},... {}}", "", 1)
    db.tags.create_tag(tr("Inflection"), False, "{{},... {}}", "", 2)
    db.tags.create_tag(tr("Base Form"), False, "{{},... {}}", "", 3)
    db.tags.create_tag(
        tr("Definitions"),
        False,
        "{<ol><li>{}</li>...<li>{}</li></ol>}",
        "",
        4,
    )
    return name, db


def create_dictionary_bangla():
    name = tr("Bangla Example")
    path, name = create_new_dict_path_with_non_existing_name(name)
    db = dict_database.DictDatabase(path)
    db.info.set_long_entry_format(
        f"<b>{{{tr("Bangla")}}}</b><br>"
        f"{{{tr("Part Of Speech")}}}"
        f"{{{tr("Definitions")}}}"
    )
    db.info.set_entry_joiner("<hr>")
    db.tags.create_tag(tr("Bangla"), True, "{{},... {}}", "", 0)
    db.tags.create_tag(tr("Part Of Speech"), False, "{{},... {}}", "", 1)
    db.tags.create_tag(
        tr("Definitions"),
        False,
        "{<ol><li>{}</li>...<li>{}</li></ol>}",
        "",
        2,
    )
    return name, db


def create_dictionary_portuguese():
    name = tr("Portuguese Example")
    path, name = create_new_dict_path_with_non_existing_name(name)
    db = dict_database.DictDatabase(path)
    db.info.set_long_entry_format(
        f"<b>{{{tr("Portuguese")}}}</b><br>"
        f'{{{tr("Part Of Speech")}}}<br>'
        "{"
        + tr("{0} of <b>{1}</b>:").format(
            f"{{{tr("Inflection")}}}", f"{{{tr("Base Form")}}}"
        )
        + "}"
        f"{{{tr("Definitions")}}}"
    )
    db.info.set_entry_joiner("<hr>")
    db.tags.create_tag(tr("Portuguese"), True, "{{},... {}}", "", 0)
    db.tags.create_tag(tr("Part Of Speech"), False, "{{},... {}}", "", 1)
    db.tags.create_tag(tr("Inflection"), False, "{{},... {}}", "", 2)
    db.tags.create_tag(tr("Base Form"), False, "{{},... {}}", "", 3)
    db.tags.create_tag(
        tr("Definitions"),
        False,
        "{<ol><li>{}</li>...<li>{}</li></ol>}",
        "",
        4,
    )
    return name, db


def create_dictionary_russian():
    name = tr("Russian Example")
    path, name = create_new_dict_path_with_non_existing_name(name)
    db = dict_database.DictDatabase(path)
    db.info.set_long_entry_format(
        f"<b>{{{tr("Russian With Stress Marks")}}}</b><br>"
        f'{{{tr("Part Of Speech")}}}'
        "{"
        + tr("{0} of <b>{1}</b>:").format(
            f"{{{tr("Inflection")}}}",
            f"{{{tr("Base Form With Stress Marks")}}}",
        )
        + "}"
        f"{{{tr("Definitions")}}}"
    )
    db.info.set_entry_joiner("<hr>")
    db.tags.create_tag(tr("Russian"), True, "{{},... {}}", "", 0)
    db.tags.create_tag(
        tr("Russian With Stress Marks"),
        True,
        "{{},... {}}",
        "",
        1,
    )
    db.tags.create_tag(tr("Part Of Speech"), False, "{{},... {}}", "", 2)
    db.tags.create_tag(
        tr("Inflection"),
        False,
        "{<ul><li>{}</li>...<li>{}</li></ul>}",
        "",
        3,
    )
    db.tags.create_tag(
        tr("Base Form With Stress Marks"),
        False,
        "{{},... {}}",
        "",
        4,
    )
    db.tags.create_tag(
        tr("Definitions"),
        False,
        "{<ol><li>{}</li>...<li>{}</li></ol>}",
        "",
        5,
    )
    return name, db


def create_dictionary_indonesian():
    name = tr("Indonesian Example")
    path, name = create_new_dict_path_with_non_existing_name(name)
    db = dict_database.DictDatabase(path)
    db.info.set_long_entry_format(
        f"<b>{{{tr("Indonesian")}}}</b><br>"
        f"{{{tr("Part Of Speech")}}}"
        f"{{{tr("Definitions")}}}"
    )
    db.info.set_entry_joiner("<hr>")
    db.tags.create_tag(tr("Indonesian"), True, "{{},... {}}", "", 0)
    db.tags.create_tag(tr("Part Of Speech"), False, "{{},... {}}", "", 1)
    db.tags.create_tag(
        tr("Definitions"),
        False,
        "{<ol><li>{}</li>...<li>{}</li></ol>}",
        "",
        2,
    )
    return name, db


def create_dictionary_urdu():
    name = tr("Urdu Example")
    path, name = create_new_dict_path_with_non_existing_name(name)
    db = dict_database.DictDatabase(path)
    db.info.set_long_entry_format(
        f"<p><b>{{{tr("Urdu")}}}</b></p>"
        f"{{{tr("Hindi")}}}<br>"
        f"{{{tr("Part Of Speech")}}}"
        f"{{{tr("Definitions")}}}"
    )
    db.info.set_entry_joiner("<hr>")
    db.tags.create_tag(tr("Urdu"), True, "{{},... {}}", "", 0)
    db.tags.create_tag(tr("Hindi"), True, "{{},... {}}", "", 1)
    db.tags.create_tag(tr("Part Of Speech"), True, "{{},... {}}", "", 2)
    db.tags.create_tag(
        tr("Definitions"),
        False,
        "{<ol><li>{}</li>...<li>{}</li></ol>}",
        "",
        3,
    )
    return name, db


def create_dictionary_german():
    name = tr("German Example")
    path, name = create_new_dict_path_with_non_existing_name(name)
    db = dict_database.DictDatabase(path)
    db.info.set_long_entry_format(
        f"<b>{{{tr("German")}}}</b><br>"
        f'{{{tr("Part Of Speech")}}}'
        "{"
        + tr("{0} of <b>{1}</b>:").format(
            f"{{{tr("Inflection")}}}", f"{{{tr("Base Form")}}}"
        )
        + "}"
        f"{{{tr("Definitions")}}}"
    )
    db.info.set_entry_joiner("<hr>")
    db.tags.create_tag(tr("German"), True, "{{},... {}}", "", 0)
    db.tags.create_tag(tr("Part Of Speech"), False, "{{},... {}}", "", 1)
    db.tags.create_tag(
        tr("Inflection"),
        False,
        "{<ul><li>{}</li>...<li>{}</li></ul>}",
        "",
        2,
    )
    db.tags.create_tag(tr("Base Form"), False, "{{},... {}}", "", 3)
    db.tags.create_tag(
        tr("Definitions"),
        False,
        "{<ol><li>{}</li>...<li>{}</li></ol>}",
        "",
        4,
    )
    return name, db


def create_dictionary_japanese():
    name = tr("Japanese Example")
    path, name = create_new_dict_path_with_non_existing_name(name)
    db = dict_database.DictDatabase(path)
    db.info.set_long_entry_format(
        "{"
        + f"{{{tr("Kanji")}}}<br>"
        + "}{"
        + f"{{{tr("Hiragana")}}}<br>"
        + "}{"
        f"{{{tr("Katakana")}}}<br>"
        + "}"
        + f"{{{tr("Part Of Speech")}}}"
        + f"{{{tr("Definitions")}}}"
    )
    db.info.set_entry_joiner("<hr>")
    db.tags.create_tag(tr("Kanji"), True, "{{},... {}}", "", 0)
    db.tags.create_tag(tr("Hiragana"), True, "{{},... {}}", "", 1)
    db.tags.create_tag(tr("Katakana"), True, "{{},... {}}", "", 2)
    db.tags.create_tag(tr("Part Of Speech"), False, "{{},... {}}", "", 3)
    db.tags.create_tag(
        tr("Definitions"),
        False,
        "{<ol><li>{}</li>...<li>{}</li></ol>}",
        "",
        4,
    )
    return name, db


def create_dictionary_latin():
    name = tr("Latin Example")
    path, name = create_new_dict_path_with_non_existing_name(name)
    db = dict_database.DictDatabase(path)
    db.info.set_long_entry_format(
        f"<b>{{{tr("Latin With Long Vowel Marks")}}}</b><br>"
        f"{{{tr("Part Of Speech")}}}"
        "{"
        + tr("{0} of <b>{1}</b>:").format(
            f"{{{tr("Inflection")}}}",
            f"{{{tr("Base Form With Long Vowel Marks")}}}",
        )
        + "}"
        f"{{{tr("Definitions")}}}"
    )
    db.info.set_entry_joiner("<hr>")
    db.tags.create_tag(tr("Latin"), True, "{{},... {}}", "", 0)
    db.tags.create_tag(
        tr("Latin With Long Vowel Marks"),
        True,
        "{{},... {}}",
        "",
        1,
    )
    db.tags.create_tag(tr("Part Of Speech"), False, "{{},... {}}", "", 2)
    db.tags.create_tag(
        tr("Inflection"),
        False,
        "{<ul><li>{}</li>...<li>{}</li></ul>}",
        "",
        3,
    )
    db.tags.create_tag(
        tr("Base Form With Long Vowel Marks"),
        False,
        "{{},... {}}",
        "",
        4,
    )
    db.tags.create_tag(
        tr("Definitions"),
        False,
        "{<ol><li>{}</li>...<li>{}</li></ol>}",
        "",
        5,
    )
    return name, db


def create_dictionary_latin_short():
    name = tr("Latin")
    path, name = create_new_dict_path_with_non_existing_name(name)
    db = dict_database.DictDatabase(path)
    db.info.set_short_entry_format(
        '<div style="font-family:Cardo; font-size:12pt">'
        f"{{{tr("Latin")}}} {{{tr("Info")}}}{{{tr("Definitions")}}}"
        "</div>"
    )
    db.info.set_entry_joiner("<hr>")
    db.tags.create_tag(tr("Latin"), True, "", "{{},... {}}", 0)
    db.tags.create_tag(tr("Info"), False, "", "{{},... {}}", 1)
    db.tags.create_tag(
        tr("Definitions"),
        False,
        "",
        "{<ol><li>{}</li>...<li>{}</li></ol>}",
        2,
    )
    return name, db


def create_dictionary_latin_long():
    name = tr("Latin")
    path, name = create_new_dict_path_with_non_existing_name(name)
    db = dict_database.DictDatabase(path)
    db.info.set_long_entry_format(
        '<div style="font-family:Cardo; font-size:12pt">'
        f"<b>{{{tr("Latin With Long Vowel Marks")}}}</b><br>"
        f"{{{tr("Part Of Speech")}}}"
        "{"
        + tr("{0} of <b>{1}</b>:").format(
            f"{{{tr("Inflection")}}}",
            f"{{{tr("Base Form With Long Vowel Marks")}}}",
        )
        + "}"
        f"{{{tr("Definitions")}}}"
        "</div>"
    )
    db.info.set_entry_joiner("<hr>")
    db.tags.create_tag(tr("Latin"), True, "{{},... {}}", "", 0)
    db.tags.create_tag(
        tr("Latin With Long Vowel Marks"),
        True,
        "{{},... {}}",
        "",
        1,
    )
    db.tags.create_tag(tr("Part Of Speech"), False, "{{},... {}}", "", 2)
    db.tags.create_tag(
        tr("Inflection"),
        False,
        "{<ul><li>{}</li>...<li>{}</li></ul>}",
        "",
        3,
    )
    db.tags.create_tag(
        tr("Base Form With Long Vowel Marks"),
        False,
        "{{},... {}}",
        "",
        4,
    )
    db.tags.create_tag(
        tr("Definitions"),
        False,
        "{<ol><li>{}</li>...<li>{}</li></ol>}",
        "",
        5,
    )
    return name, db


def create_entry_english():
    name, db = create_dictionary_english()
    entry_id = db.entries.create_entry()
    form_id = db.forms.create_form(entry_id, 0)
    tag_values_list = [
        (
            form_id,
            db.tags.get_tag_id(tr("English")),
            ["example"],
            True,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Part Of Speech")),
            [tr("noun")],
            False,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Inflection")),
            [tr("singular")],
            False,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Base Form")),
            ["example"],
            False,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Definitions")),
            ["example"],
            False,
            False,
        ),
    ]
    for tag_values in tag_values_list:
        db.tag_rows.set_tag_values(*tag_values)
    open_windows_for_create_entry_example(name, db, entry_id)


def create_entry_mandarin_chinese():
    name, db = create_dictionary_mandarin_chinese()
    entry_id = db.entries.create_entry()
    form_id = db.forms.create_form(entry_id, 0)
    tag_values_list = [
        (
            form_id,
            db.tags.get_tag_id(tr("Traditional")),
            ["例子"],
            True,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Simplified")),
            ["例子"],
            True,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Pinyin")),
            ["lìzi"],
            True,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Zhuyin")),
            ["ㄌㄧˋㄗ˙"],
            True,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Part Of Speech")),
            [tr("noun")],
            False,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Definitions")),
            ["example"],
            False,
            False,
        ),
    ]
    for tag_values in tag_values_list:
        db.tag_rows.set_tag_values(*tag_values)
    open_windows_for_create_entry_example(name, db, entry_id)


def create_entry_hindi():
    name, db = create_dictionary_hindi()
    entry_id = db.entries.create_entry()
    form_id = db.forms.create_form(entry_id, 0)
    tag_values_list = [
        (
            form_id,
            db.tags.get_tag_id(tr("Hindi")),
            ["उदाहरण"],
            True,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Urdu")),
            ["اداہرن"],
            True,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Part Of Speech")),
            [tr("masculine noun")],
            False,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Inflection")),
            [
                tr("direct singular"),
                tr("oblique singular"),
                tr("vocative singular"),
                tr("direct plural"),
            ],
            False,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Base Form Hindi")),
            ["उदाहरण"],
            False,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Base Form Urdu With Diacritics")),
            ["اُداہَرَن"],
            False,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Definitions")),
            ["example"],
            False,
            False,
        ),
    ]
    for tag_values in tag_values_list:
        db.tag_rows.set_tag_values(*tag_values)
    open_windows_for_create_entry_example(name, db, entry_id)


def create_entry_spanish():
    name, db = create_dictionary_spanish()
    entry_id = db.entries.create_entry()
    form_id = db.forms.create_form(entry_id, 0)
    tag_values_list = [
        (
            form_id,
            db.tags.get_tag_id(tr("Spanish")),
            ["ejemplo"],
            True,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Part Of Speech")),
            [tr("masculine noun")],
            False,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Inflection")),
            [tr("singular")],
            False,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Base Form")),
            ["ejemplo"],
            False,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Definitions")),
            ["example"],
            False,
            False,
        ),
    ]
    for tag_values in tag_values_list:
        db.tag_rows.set_tag_values(*tag_values)
    open_windows_for_create_entry_example(name, db, entry_id)


def create_entry_arabic():
    name, db = create_dictionary_arabic()
    entry_id = db.entries.create_entry()
    form_id = db.forms.create_form(entry_id, 0)
    tag_values_list = [
        (
            form_id,
            db.tags.get_tag_id(tr("Arabic")),
            ["مثال"],
            True,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Part Of Speech")),
            [tr("masculine noun")],
            False,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Definitions")),
            ["example"],
            False,
            False,
        ),
    ]
    for tag_values in tag_values_list:
        db.tag_rows.set_tag_values(*tag_values)
    open_windows_for_create_entry_example(name, db, entry_id)


def create_entry_french():
    name, db = create_dictionary_french()
    entry_id = db.entries.create_entry()
    form_id = db.forms.create_form(entry_id, 0)
    tag_values_list = [
        (
            form_id,
            db.tags.get_tag_id(tr("French")),
            ["exemple"],
            True,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Part Of Speech")),
            [tr("masculine noun")],
            False,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Inflection")),
            [tr("singular")],
            False,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Base Form")),
            ["exemple"],
            False,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Definitions")),
            ["example"],
            False,
            False,
        ),
    ]
    for tag_values in tag_values_list:
        db.tag_rows.set_tag_values(*tag_values)
    open_windows_for_create_entry_example(name, db, entry_id)


def create_entry_bangla():
    name, db = create_dictionary_bangla()
    entry_id = db.entries.create_entry()
    form_id = db.forms.create_form(entry_id, 0)
    tag_values_list = [
        (
            form_id,
            db.tags.get_tag_id(tr("Bangla")),
            ["উদাহরণ"],
            True,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Part Of Speech")),
            [tr("masculine noun")],
            False,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Definitions")),
            ["example"],
            False,
            False,
        ),
    ]
    for tag_values in tag_values_list:
        db.tag_rows.set_tag_values(*tag_values)
    open_windows_for_create_entry_example(name, db, entry_id)


def create_entry_portuguese():
    name, db = create_dictionary_portuguese()
    entry_id = db.entries.create_entry()
    form_id = db.forms.create_form(entry_id, 0)
    tag_values_list = [
        (
            form_id,
            db.tags.get_tag_id(tr("Portuguese")),
            ["exemplo"],
            True,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Part Of Speech")),
            [tr("masculine noun")],
            False,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Inflection")),
            [tr("singular")],
            False,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Base Form")),
            ["exemplo"],
            False,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Definitions")),
            ["example"],
            False,
            False,
        ),
    ]
    for tag_values in tag_values_list:
        db.tag_rows.set_tag_values(*tag_values)
    open_windows_for_create_entry_example(name, db, entry_id)


def create_entry_russian():
    name, db = create_dictionary_russian()
    entry_id = db.entries.create_entry()
    form_id = db.forms.create_form(entry_id, 0)
    tag_values_list = [
        (
            form_id,
            db.tags.get_tag_id(tr("Russian")),
            ["пример"],
            True,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Russian With Stress Marks")),
            ["приме́р"],
            True,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Part Of Speech")),
            [tr("masculine noun")],
            False,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Inflection")),
            [
                tr("nominative singular"),
                tr("accusative singular"),
            ],
            False,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Base Form With Stress Marks")),
            ["приме́р"],
            False,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Definitions")),
            ["example"],
            False,
            False,
        ),
    ]
    for tag_values in tag_values_list:
        db.tag_rows.set_tag_values(*tag_values)
    open_windows_for_create_entry_example(name, db, entry_id)


def create_entry_indonesian():
    name, db = create_dictionary_indonesian()
    entry_id = db.entries.create_entry()
    form_id = db.forms.create_form(entry_id, 0)
    tag_values_list = [
        (
            form_id,
            db.tags.get_tag_id(tr("Indonesian")),
            ["contoh"],
            True,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Part Of Speech")),
            [tr("noun")],
            False,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Definitions")),
            ["example"],
            False,
            False,
        ),
    ]
    for tag_values in tag_values_list:
        db.tag_rows.set_tag_values(*tag_values)
    open_windows_for_create_entry_example(name, db, entry_id)


def create_entry_urdu():
    name, db = create_dictionary_urdu()
    entry_id = db.entries.create_entry()
    form_id = db.forms.create_form(entry_id, 0)
    tag_values_list = [
        (
            form_id,
            db.tags.get_tag_id(tr("Urdu")),
            ["مثال"],
            True,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Hindi")),
            ["मिसाल"],
            True,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Part Of Speech")),
            [tr("masculine noun")],
            False,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Definitions")),
            ["example"],
            False,
            False,
        ),
    ]
    for tag_values in tag_values_list:
        db.tag_rows.set_tag_values(*tag_values)
    open_windows_for_create_entry_example(name, db, entry_id)


def create_entry_german():
    name, db = create_dictionary_german()
    entry_id = db.entries.create_entry()
    form_id = db.forms.create_form(entry_id, 0)
    tag_values_list = [
        (
            form_id,
            db.tags.get_tag_id(tr("German")),
            ["Beispiel"],
            True,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Part Of Speech")),
            [tr("neuter noun")],
            False,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Inflection")),
            [
                tr("nominative singular"),
                tr("dative singular"),
                tr("accusative singular"),
            ],
            False,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Base Form")),
            ["Beispiel"],
            False,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Definitions")),
            ["example"],
            False,
            False,
        ),
    ]
    for tag_values in tag_values_list:
        db.tag_rows.set_tag_values(*tag_values)
    open_windows_for_create_entry_example(name, db, entry_id)


def create_entry_japanese():
    name, db = create_dictionary_japanese()
    entry_id = db.entries.create_entry()
    form_id = db.forms.create_form(entry_id, 0)
    tag_values_list = [
        (
            form_id,
            db.tags.get_tag_id(tr("Kanji")),
            ["例"],
            True,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Hiragana")),
            ["れい"],
            True,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Katakana")),
            [""],
            True,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Part Of Speech")),
            [tr("noun")],
            False,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Definitions")),
            ["example"],
            False,
            False,
        ),
    ]
    for tag_values in tag_values_list:
        db.tag_rows.set_tag_values(*tag_values)
    open_windows_for_create_entry_example(name, db, entry_id)


def create_entry_latin():
    name, db = create_dictionary_latin()
    entry_id = db.entries.create_entry()
    form_id = db.forms.create_form(entry_id, 0)
    tag_values_list = [
        (
            form_id,
            db.tags.get_tag_id(tr("Latin")),
            ["exemplum"],
            True,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Latin With Long Vowel Marks")),
            ["exemplum"],
            True,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Part Of Speech")),
            [tr("2nd declension neuter noun")],
            False,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Inflection")),
            [
                tr("nominative singular"),
                tr("accusative singular"),
                tr("vocative singular"),
            ],
            False,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Base Form With Long Vowel Marks")),
            ["exemplum"],
            False,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Definitions")),
            ["example"],
            False,
            False,
        ),
    ]
    for tag_values in tag_values_list:
        db.tag_rows.set_tag_values(*tag_values)
    open_windows_for_create_entry_example(name, db, entry_id)


def create_template_english():
    name, db = create_dictionary_english()
    entry_id = db.entries.create_entry()
    template_name = tr("Create Template Example")
    db.entries.set_template_name(entry_id, template_name)
    form_ids = [db.forms.create_form(entry_id, i) for i in range(2)]
    tag_values_list = [
        (
            form_ids[0],
            db.tags.get_tag_id(tr("English")),
            ["{}"],
            True,
            False,
        ),
        (
            form_ids[1],
            db.tags.get_tag_id(tr("English")),
            ["{}s"],
            True,
            False,
        ),
        *[
            (
                form_id,
                db.tags.get_tag_id(tr("Part Of Speech")),
                [tr("noun")],
                False,
                False,
            )
            for form_id in form_ids
        ],
        (
            form_ids[0],
            db.tags.get_tag_id(tr("Inflection")),
            [tr("singular")],
            False,
            False,
        ),
        (
            form_ids[1],
            db.tags.get_tag_id(tr("Inflection")),
            [tr("plural")],
            False,
            False,
        ),
        *[
            (
                form_id,
                db.tags.get_tag_id(tr("Base Form")),
                ["{}"],
                False,
                False,
            )
            for form_id in form_ids
        ],
        *[
            (
                form_id,
                db.tags.get_tag_id(tr("Definitions")),
                ["{}"],
                False,
                False,
            )
            for form_id in form_ids
        ],
    ]
    for tag_values in tag_values_list:
        db.tag_rows.set_tag_values(*tag_values)
    row_data = [
        (
            None,
            [
                (
                    db.tags.get_tag_id(tr("English")),
                    tr("English"),
                    ["example"],
                ),
                (
                    db.tags.get_tag_id(tr("Part Of Speech")),
                    tr("Part Of Speech"),
                    [""],
                ),
                (
                    db.tags.get_tag_id(tr("Inflection")),
                    tr("Inflection"),
                    [""],
                ),
                (
                    db.tags.get_tag_id(tr("Base Form")),
                    tr("Base Form"),
                    ["example"],
                ),
                (
                    db.tags.get_tag_id(tr("Definitions")),
                    tr("Definitions"),
                    ["example"],
                ),
            ],
        )
    ]
    open_windows_for_create_templates_example(
        name,
        db,
        entry_id,
        template_name,
        row_data,
    )


def create_template_hindi():
    name, db = create_dictionary_hindi()
    entry_id = db.entries.create_entry()
    template_name = tr("Create Template Example")
    db.entries.set_template_name(entry_id, template_name)
    form_ids = [db.forms.create_form(entry_id, i) for i in range(3)]
    tag_values_list = [
        (
            form_ids[0],
            db.tags.get_tag_id(tr("Hindi")),
            ["{}ण"],
            True,
            False,
        ),
        (
            form_ids[1],
            db.tags.get_tag_id(tr("Hindi")),
            ["{}णों"],
            True,
            False,
        ),
        (
            form_ids[2],
            db.tags.get_tag_id(tr("Hindi")),
            ["{}णो"],
            True,
            False,
        ),
        (
            form_ids[0],
            db.tags.get_tag_id(tr("Urdu")),
            ["{}ن"],
            True,
            False,
        ),
        (
            form_ids[1],
            db.tags.get_tag_id(tr("Urdu")),
            ["{}نوں"],
            True,
            False,
        ),
        (
            form_ids[2],
            db.tags.get_tag_id(tr("Urdu")),
            ["{}نو"],
            True,
            False,
        ),
        *[
            (
                form_id,
                db.tags.get_tag_id(tr("Part Of Speech")),
                [tr("masculine noun")],
                False,
                False,
            )
            for form_id in form_ids
        ],
        (
            form_ids[0],
            db.tags.get_tag_id(tr("Inflection")),
            [
                tr("direct singular"),
                tr("oblique singular"),
                tr("vocative singular"),
                tr("direct plural"),
            ],
            False,
            False,
        ),
        (
            form_ids[1],
            db.tags.get_tag_id(tr("Inflection")),
            [tr("oblique plural")],
            False,
            False,
        ),
        (
            form_ids[2],
            db.tags.get_tag_id(tr("Inflection")),
            [tr("vocative plural")],
            False,
            False,
        ),
        *[
            (
                form_id,
                db.tags.get_tag_id(tr("Base Form Hindi")),
                ["{}"],
                False,
                False,
            )
            for form_id in form_ids
        ],
        *[
            (
                form_id,
                db.tags.get_tag_id(tr("Base Form Urdu With Diacritics")),
                ["{}"],
                False,
                False,
            )
            for form_id in form_ids
        ],
        *[
            (
                form_id,
                db.tags.get_tag_id(tr("Definitions")),
                ["{}"],
                False,
                False,
            )
            for form_id in form_ids
        ],
    ]
    for tag_values in tag_values_list:
        db.tag_rows.set_tag_values(*tag_values)
    row_data = [
        (
            None,
            [
                (
                    db.tags.get_tag_id(tr("Hindi")),
                    tr("Hindi"),
                    ["उदाहर"],
                ),
                (
                    db.tags.get_tag_id(tr("Urdu")),
                    tr("Urdu"),
                    ["اداہر"],
                ),
                (
                    db.tags.get_tag_id(tr("Part Of Speech")),
                    tr("Part Of Speech"),
                    [""],
                ),
                (
                    db.tags.get_tag_id(tr("Inflection")),
                    tr("Inflection"),
                    [""],
                ),
                (
                    db.tags.get_tag_id(tr("Base Form Hindi")),
                    tr("Base Form Hindi"),
                    ["उदाहरण"],
                ),
                (
                    db.tags.get_tag_id(tr("Base Form Urdu With Diacritics")),
                    tr("Base Form Urdu With Diacritics"),
                    ["اُداہَرَن"],
                ),
                (
                    db.tags.get_tag_id(tr("Definitions")),
                    tr("Definitions"),
                    ["example"],
                ),
            ],
        )
    ]
    open_windows_for_create_templates_example(
        name,
        db,
        entry_id,
        template_name,
        row_data,
    )


def create_template_spanish():
    name, db = create_dictionary_spanish()
    entry_id = db.entries.create_entry()
    template_name = tr("Create Template Example")
    db.entries.set_template_name(entry_id, template_name)
    form_ids = [db.forms.create_form(entry_id, i) for i in range(2)]
    tag_values_list = [
        (
            form_ids[0],
            db.tags.get_tag_id(tr("Spanish")),
            ["{}"],
            True,
            False,
        ),
        (
            form_ids[1],
            db.tags.get_tag_id(tr("Spanish")),
            ["{}s"],
            True,
            False,
        ),
        *[
            (
                form_id,
                db.tags.get_tag_id(tr("Part Of Speech")),
                [tr("masculine noun")],
                False,
                False,
            )
            for form_id in form_ids
        ],
        (
            form_ids[0],
            db.tags.get_tag_id(tr("Inflection")),
            [tr("singular")],
            False,
            False,
        ),
        (
            form_ids[1],
            db.tags.get_tag_id(tr("Inflection")),
            [tr("plural")],
            False,
            False,
        ),
        *[
            (
                form_id,
                db.tags.get_tag_id(tr("Base Form")),
                ["{}"],
                False,
                False,
            )
            for form_id in form_ids
        ],
        *[
            (
                form_id,
                db.tags.get_tag_id(tr("Definitions")),
                ["{}"],
                False,
                False,
            )
            for form_id in form_ids
        ],
    ]
    for tag_values in tag_values_list:
        db.tag_rows.set_tag_values(*tag_values)
    row_data = [
        (
            None,
            [
                (
                    db.tags.get_tag_id(tr("Spanish")),
                    tr("Spanish"),
                    ["ejemplo"],
                ),
                (
                    db.tags.get_tag_id(tr("Part Of Speech")),
                    tr("Part Of Speech"),
                    [""],
                ),
                (
                    db.tags.get_tag_id(tr("Inflection")),
                    tr("Inflection"),
                    [""],
                ),
                (
                    db.tags.get_tag_id(tr("Base Form")),
                    tr("Base Form"),
                    ["ejemplo"],
                ),
                (
                    db.tags.get_tag_id(tr("Definitions")),
                    tr("Definitions"),
                    ["example"],
                ),
            ],
        )
    ]
    open_windows_for_create_templates_example(
        name,
        db,
        entry_id,
        template_name,
        row_data,
    )


def create_template_french():
    name, db = create_dictionary_french()
    entry_id = db.entries.create_entry()
    template_name = tr("Create Template Example")
    db.entries.set_template_name(entry_id, template_name)
    form_ids = [db.forms.create_form(entry_id, i) for i in range(2)]
    tag_values_list = [
        (
            form_ids[0],
            db.tags.get_tag_id(tr("French")),
            ["{}"],
            True,
            False,
        ),
        (
            form_ids[1],
            db.tags.get_tag_id(tr("French")),
            ["{}s"],
            True,
            False,
        ),
        *[
            (
                form_id,
                db.tags.get_tag_id(tr("Part Of Speech")),
                [tr("masculine noun")],
                False,
                False,
            )
            for form_id in form_ids
        ],
        (
            form_ids[0],
            db.tags.get_tag_id(tr("Inflection")),
            [tr("singular")],
            False,
            False,
        ),
        (
            form_ids[1],
            db.tags.get_tag_id(tr("Inflection")),
            [tr("plural")],
            False,
            False,
        ),
        *[
            (
                form_id,
                db.tags.get_tag_id(tr("Base Form")),
                ["{}"],
                False,
                False,
            )
            for form_id in form_ids
        ],
        *[
            (
                form_id,
                db.tags.get_tag_id(tr("Definitions")),
                ["{}"],
                False,
                False,
            )
            for form_id in form_ids
        ],
    ]
    for tag_values in tag_values_list:
        db.tag_rows.set_tag_values(*tag_values)
    row_data = [
        (
            None,
            [
                (
                    db.tags.get_tag_id(tr("French")),
                    tr("French"),
                    ["exemple"],
                ),
                (
                    db.tags.get_tag_id(tr("Part Of Speech")),
                    tr("Part Of Speech"),
                    [""],
                ),
                (
                    db.tags.get_tag_id(tr("Inflection")),
                    tr("Inflection"),
                    [""],
                ),
                (
                    db.tags.get_tag_id(tr("Base Form")),
                    tr("Base Form"),
                    ["exemple"],
                ),
                (
                    db.tags.get_tag_id(tr("Definitions")),
                    tr("Definitions"),
                    ["example"],
                ),
            ],
        )
    ]
    open_windows_for_create_templates_example(
        name,
        db,
        entry_id,
        template_name,
        row_data,
    )


def create_template_portuguese():
    name, db = create_dictionary_portuguese()
    entry_id = db.entries.create_entry()
    template_name = tr("Create Template Example")
    db.entries.set_template_name(entry_id, template_name)
    form_ids = [db.forms.create_form(entry_id, i) for i in range(2)]
    tag_values_list = [
        (
            form_ids[0],
            db.tags.get_tag_id(tr("Portuguese")),
            ["{}"],
            True,
            False,
        ),
        (
            form_ids[1],
            db.tags.get_tag_id(tr("Portuguese")),
            ["{}s"],
            True,
            False,
        ),
        *[
            (
                form_id,
                db.tags.get_tag_id(tr("Part Of Speech")),
                [tr("masculine noun")],
                False,
                False,
            )
            for form_id in form_ids
        ],
        (
            form_ids[0],
            db.tags.get_tag_id(tr("Inflection")),
            [tr("singular")],
            False,
            False,
        ),
        (
            form_ids[1],
            db.tags.get_tag_id(tr("Inflection")),
            [tr("plural")],
            False,
            False,
        ),
        *[
            (
                form_id,
                db.tags.get_tag_id(tr("Base Form")),
                ["{}"],
                False,
                False,
            )
            for form_id in form_ids
        ],
        *[
            (
                form_id,
                db.tags.get_tag_id(tr("Definitions")),
                ["{}"],
                False,
                False,
            )
            for form_id in form_ids
        ],
    ]
    for tag_values in tag_values_list:
        db.tag_rows.set_tag_values(*tag_values)
    row_data = [
        (
            None,
            [
                (
                    db.tags.get_tag_id(tr("Portuguese")),
                    tr("Portuguese"),
                    ["exemplo"],
                ),
                (
                    db.tags.get_tag_id(tr("Part Of Speech")),
                    tr("Part Of Speech"),
                    [""],
                ),
                (
                    db.tags.get_tag_id(tr("Inflection")),
                    tr("Inflection"),
                    [""],
                ),
                (
                    db.tags.get_tag_id(tr("Base Form")),
                    tr("Base Form"),
                    ["exemplo"],
                ),
                (
                    db.tags.get_tag_id(tr("Definitions")),
                    tr("Definitions"),
                    ["example"],
                ),
            ],
        )
    ]
    open_windows_for_create_templates_example(
        name,
        db,
        entry_id,
        template_name,
        row_data,
    )


def create_template_russian():
    name, db = create_dictionary_russian()
    entry_id = db.entries.create_entry()
    template_name = tr("Create Template Example")
    db.entries.set_template_name(entry_id, template_name)
    form_ids = [db.forms.create_form(entry_id, i) for i in range(10)]
    tag_values_list = [
        (
            form_ids[0],
            db.tags.get_tag_id(tr("Russian")),
            ["{}"],
            True,
            False,
        ),
        (
            form_ids[1],
            db.tags.get_tag_id(tr("Russian")),
            ["{}а"],
            True,
            False,
        ),
        (
            form_ids[2],
            db.tags.get_tag_id(tr("Russian")),
            ["{}у"],
            True,
            False,
        ),
        (
            form_ids[3],
            db.tags.get_tag_id(tr("Russian")),
            ["{}ом"],
            True,
            False,
        ),
        (
            form_ids[4],
            db.tags.get_tag_id(tr("Russian")),
            ["{}е"],
            True,
            False,
        ),
        (
            form_ids[5],
            db.tags.get_tag_id(tr("Russian")),
            ["{}ы"],
            True,
            False,
        ),
        (
            form_ids[6],
            db.tags.get_tag_id(tr("Russian")),
            ["{}ов"],
            True,
            False,
        ),
        (
            form_ids[7],
            db.tags.get_tag_id(tr("Russian")),
            ["{}ам"],
            True,
            False,
        ),
        (
            form_ids[8],
            db.tags.get_tag_id(tr("Russian")),
            ["{}ами"],
            True,
            False,
        ),
        (
            form_ids[9],
            db.tags.get_tag_id(tr("Russian")),
            ["{}ах"],
            True,
            False,
        ),
        (
            form_ids[0],
            db.tags.get_tag_id(tr("Russian With Stress Marks")),
            ["{}"],
            True,
            False,
        ),
        (
            form_ids[1],
            db.tags.get_tag_id(tr("Russian With Stress Marks")),
            ["{}а"],
            True,
            False,
        ),
        (
            form_ids[2],
            db.tags.get_tag_id(tr("Russian With Stress Marks")),
            ["{}у"],
            True,
            False,
        ),
        (
            form_ids[3],
            db.tags.get_tag_id(tr("Russian With Stress Marks")),
            ["{}ом"],
            True,
            False,
        ),
        (
            form_ids[4],
            db.tags.get_tag_id(tr("Russian With Stress Marks")),
            ["{}е"],
            True,
            False,
        ),
        (
            form_ids[5],
            db.tags.get_tag_id(tr("Russian With Stress Marks")),
            ["{}ы"],
            True,
            False,
        ),
        (
            form_ids[6],
            db.tags.get_tag_id(tr("Russian With Stress Marks")),
            ["{}ов"],
            True,
            False,
        ),
        (
            form_ids[7],
            db.tags.get_tag_id(tr("Russian With Stress Marks")),
            ["{}ам"],
            True,
            False,
        ),
        (
            form_ids[8],
            db.tags.get_tag_id(tr("Russian With Stress Marks")),
            ["{}ами"],
            True,
            False,
        ),
        (
            form_ids[9],
            db.tags.get_tag_id(tr("Russian With Stress Marks")),
            ["{}ах"],
            True,
            False,
        ),
        *[
            (
                form_id,
                db.tags.get_tag_id(tr("Part Of Speech")),
                [tr("masculine noun")],
                False,
                False,
            )
            for form_id in form_ids
        ],
        (
            form_ids[0],
            db.tags.get_tag_id(tr("Inflection")),
            [
                tr("nominative singular"),
                tr("accusative singular"),
            ],
            False,
            False,
        ),
        (
            form_ids[1],
            db.tags.get_tag_id(tr("Inflection")),
            [tr("genitive singular")],
            False,
            False,
        ),
        (
            form_ids[2],
            db.tags.get_tag_id(tr("Inflection")),
            [tr("dative singular")],
            False,
            False,
        ),
        (
            form_ids[3],
            db.tags.get_tag_id(tr("Inflection")),
            [tr("instrumental singular")],
            False,
            False,
        ),
        (
            form_ids[4],
            db.tags.get_tag_id(tr("Inflection")),
            [tr("prepositional singular")],
            False,
            False,
        ),
        (
            form_ids[5],
            db.tags.get_tag_id(tr("Inflection")),
            [
                tr("nominative plural"),
                tr("accusative plural"),
            ],
            False,
            False,
        ),
        (
            form_ids[6],
            db.tags.get_tag_id(tr("Inflection")),
            [tr("genitive plural")],
            False,
            False,
        ),
        (
            form_ids[7],
            db.tags.get_tag_id(tr("Inflection")),
            [tr("dative plural")],
            False,
            False,
        ),
        (
            form_ids[8],
            db.tags.get_tag_id(tr("Inflection")),
            [tr("instrumental plural")],
            False,
            False,
        ),
        (
            form_ids[9],
            db.tags.get_tag_id(tr("Inflection")),
            [tr("prepositional plural")],
            False,
            False,
        ),
        *[
            (
                form_id,
                db.tags.get_tag_id(tr("Base Form With Stress Marks")),
                ["{}"],
                False,
                False,
            )
            for form_id in form_ids
        ],
        *[
            (
                form_id,
                db.tags.get_tag_id(tr("Definitions")),
                ["{}"],
                False,
                False,
            )
            for form_id in form_ids
        ],
    ]
    for tag_values in tag_values_list:
        db.tag_rows.set_tag_values(*tag_values)
    row_data = [
        (
            None,
            [
                (
                    db.tags.get_tag_id(tr("Russian")),
                    tr("Russian"),
                    ["пример"],
                ),
                (
                    db.tags.get_tag_id(tr("Russian With Stress Marks")),
                    tr("Russian With Stress Marks"),
                    ["приме́р"],
                ),
                (
                    db.tags.get_tag_id(tr("Part Of Speech")),
                    tr("Part Of Speech"),
                    [""],
                ),
                (
                    db.tags.get_tag_id(tr("Inflection")),
                    tr("Inflection"),
                    [""],
                ),
                (
                    db.tags.get_tag_id(tr("Base Form With Stress Marks")),
                    tr("Base Form With Stress Marks"),
                    ["приме́р"],
                ),
                (
                    db.tags.get_tag_id(tr("Definitions")),
                    tr("Definitions"),
                    ["example"],
                ),
            ],
        )
    ]
    open_windows_for_create_templates_example(
        name,
        db,
        entry_id,
        template_name,
        row_data,
    )


def create_template_german():
    name, db = create_dictionary_german()
    entry_id = db.entries.create_entry()
    template_name = tr("Create Template Example")
    db.entries.set_template_name(entry_id, template_name)
    form_ids = [db.forms.create_form(entry_id, i) for i in range(5)]
    tag_values_list = [
        (
            form_ids[0],
            db.tags.get_tag_id(tr("German")),
            ["{}"],
            True,
            False,
        ),
        (
            form_ids[1],
            db.tags.get_tag_id(tr("German")),
            ["{}s"],
            True,
            False,
        ),
        (
            form_ids[2],
            db.tags.get_tag_id(tr("German")),
            ["{}es"],
            True,
            False,
        ),
        (
            form_ids[3],
            db.tags.get_tag_id(tr("German")),
            ["{}e"],
            True,
            False,
        ),
        (
            form_ids[4],
            db.tags.get_tag_id(tr("German")),
            ["{}en"],
            True,
            False,
        ),
        *[
            (
                form_id,
                db.tags.get_tag_id(tr("Part Of Speech")),
                [tr("neuter noun")],
                False,
                False,
            )
            for form_id in form_ids
        ],
        (
            form_ids[0],
            db.tags.get_tag_id(tr("Inflection")),
            [
                tr("nominative singular"),
                tr("dative singular"),
                tr("accusative singular"),
            ],
            False,
            False,
        ),
        (
            form_ids[1],
            db.tags.get_tag_id(tr("Inflection")),
            [tr("genitive singular")],
            False,
            False,
        ),
        (
            form_ids[2],
            db.tags.get_tag_id(tr("Inflection")),
            [tr("genitive singular")],
            False,
            False,
        ),
        (
            form_ids[3],
            db.tags.get_tag_id(tr("Inflection")),
            [
                tr("nominative plural"),
                tr("genitive plural"),
                tr("accusative plural"),
                tr("dative singular"),
            ],
            False,
            False,
        ),
        (
            form_ids[4],
            db.tags.get_tag_id(tr("Inflection")),
            [tr("dative plural")],
            False,
            False,
        ),
        *[
            (
                form_id,
                db.tags.get_tag_id(tr("Base Form")),
                ["{}"],
                False,
                False,
            )
            for form_id in form_ids
        ],
        *[
            (
                form_id,
                db.tags.get_tag_id(tr("Definitions")),
                ["{}"],
                False,
                False,
            )
            for form_id in form_ids
        ],
    ]
    for tag_values in tag_values_list:
        db.tag_rows.set_tag_values(*tag_values)
    row_data = [
        (
            None,
            [
                (
                    db.tags.get_tag_id(tr("German")),
                    tr("German"),
                    ["Beispiel"],
                ),
                (
                    db.tags.get_tag_id(tr("Part Of Speech")),
                    tr("Part Of Speech"),
                    [""],
                ),
                (
                    db.tags.get_tag_id(tr("Inflection")),
                    tr("Inflection"),
                    [""],
                ),
                (
                    db.tags.get_tag_id(tr("Base Form")),
                    tr("Base Form"),
                    ["Beispiel"],
                ),
                (
                    db.tags.get_tag_id(tr("Definitions")),
                    tr("Definitions"),
                    ["example"],
                ),
            ],
        )
    ]
    open_windows_for_create_templates_example(
        name,
        db,
        entry_id,
        template_name,
        row_data,
    )


def create_template_latin():
    name, db = create_dictionary_latin()
    entry_id = db.entries.create_entry()
    template_name = tr("Create Template Example")
    db.entries.set_template_name(entry_id, template_name)
    form_ids = [db.forms.create_form(entry_id, i) for i in range(6)]
    tag_values_list = [
        (
            form_ids[0],
            db.tags.get_tag_id(tr("Latin")),
            ["{}um"],
            True,
            False,
        ),
        (
            form_ids[1],
            db.tags.get_tag_id(tr("Latin")),
            ["{}i"],
            True,
            False,
        ),
        (
            form_ids[2],
            db.tags.get_tag_id(tr("Latin")),
            ["{}o"],
            True,
            False,
        ),
        (
            form_ids[3],
            db.tags.get_tag_id(tr("Latin")),
            ["{}a"],
            True,
            False,
        ),
        (
            form_ids[4],
            db.tags.get_tag_id(tr("Latin")),
            ["{}orum"],
            True,
            False,
        ),
        (
            form_ids[5],
            db.tags.get_tag_id(tr("Latin")),
            ["{}is"],
            True,
            False,
        ),
        (
            form_ids[0],
            db.tags.get_tag_id(tr("Latin With Long Vowel Marks")),
            ["{}um"],
            True,
            False,
        ),
        (
            form_ids[1],
            db.tags.get_tag_id(tr("Latin With Long Vowel Marks")),
            ["{}ī"],
            True,
            False,
        ),
        (
            form_ids[2],
            db.tags.get_tag_id(tr("Latin With Long Vowel Marks")),
            ["{}ō"],
            True,
            False,
        ),
        (
            form_ids[3],
            db.tags.get_tag_id(tr("Latin With Long Vowel Marks")),
            ["{}a"],
            True,
            False,
        ),
        (
            form_ids[4],
            db.tags.get_tag_id(tr("Latin With Long Vowel Marks")),
            ["{}ōrum"],
            True,
            False,
        ),
        (
            form_ids[5],
            db.tags.get_tag_id(tr("Latin With Long Vowel Marks")),
            ["{}īs"],
            True,
            False,
        ),
        *[
            (
                form_id,
                db.tags.get_tag_id(tr("Part Of Speech")),
                [tr("2nd declension neuter noun")],
                False,
                False,
            )
            for form_id in form_ids
        ],
        (
            form_ids[0],
            db.tags.get_tag_id(tr("Inflection")),
            [
                tr("nominative singular"),
                tr("accusative singular"),
                tr("vocative singular"),
            ],
            False,
            False,
        ),
        (
            form_ids[1],
            db.tags.get_tag_id(tr("Inflection")),
            [
                tr("genitive singular"),
            ],
            False,
            False,
        ),
        (
            form_ids[2],
            db.tags.get_tag_id(tr("Inflection")),
            [
                tr("dative singular"),
                tr("ablative singular"),
            ],
            False,
            False,
        ),
        (
            form_ids[3],
            db.tags.get_tag_id(tr("Inflection")),
            [
                tr("nominative plural"),
                tr("accusative plural"),
                tr("vocative plural"),
            ],
            False,
            False,
        ),
        (
            form_ids[4],
            db.tags.get_tag_id(tr("Inflection")),
            [
                tr("genitive plural"),
            ],
            False,
            False,
        ),
        (
            form_ids[5],
            db.tags.get_tag_id(tr("Inflection")),
            [
                tr("dative plural"),
                tr("ablative plural"),
            ],
            False,
            False,
        ),
        *[
            (
                form_id,
                db.tags.get_tag_id(tr("Base Form With Long Vowel Marks")),
                ["{}"],
                False,
                False,
            )
            for form_id in form_ids
        ],
        *[
            (
                form_id,
                db.tags.get_tag_id(tr("Definitions")),
                ["{}"],
                False,
                False,
            )
            for form_id in form_ids
        ],
    ]
    for tag_values in tag_values_list:
        db.tag_rows.set_tag_values(*tag_values)
    row_data = [
        (
            None,
            [
                (
                    db.tags.get_tag_id(tr("Latin")),
                    tr("Latin"),
                    ["exempl"],
                ),
                (
                    db.tags.get_tag_id(tr("Latin With Long Vowel Marks")),
                    tr("Latin With Long Vowel Marks"),
                    ["exempl"],
                ),
                (
                    db.tags.get_tag_id(tr("Part Of Speech")),
                    tr("Part Of Speech"),
                    [""],
                ),
                (
                    db.tags.get_tag_id(tr("Inflection")),
                    tr("Inflection"),
                    [""],
                ),
                (
                    db.tags.get_tag_id(tr("Base Form With Long Vowel Marks")),
                    tr("Base Form With Long Vowel Marks"),
                    ["exemplum"],
                ),
                (
                    db.tags.get_tag_id(tr("Definitions")),
                    tr("Definitions"),
                    ["example"],
                ),
            ],
        )
    ]
    open_windows_for_create_templates_example(
        name,
        db,
        entry_id,
        template_name,
        row_data,
    )


def set_entry_format_simple():
    name = tr("Simple Example")
    path, name = create_new_dict_path_with_non_existing_name(name)
    db = dict_database.DictDatabase(path)
    db.info.set_long_entry_format(
        tr("{0}: {1}").format(
            f"{{{tr("Tag 1")}}}",
            f"{{{tr("Tag 2")}}}",
        )
    )
    db.info.set_entry_joiner("<hr>")
    db.tags.create_tag(tr("Tag 1"), True, "{{},... {}}", "", 0)
    db.tags.create_tag(tr("Tag 2"), False, "{{},... {}}", "", 1)

    entry_id = db.entries.create_entry()
    form_id = db.forms.create_form(entry_id, 0)
    tag_values_list = [
        (
            form_id,
            db.tags.get_tag_id(tr("Tag 1")),
            [tr("value 1")],
            True,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Tag 2")),
            [tr("value 2")],
            False,
            False,
        ),
    ]
    for tag_values in tag_values_list:
        db.tag_rows.set_tag_values(*tag_values)
    open_windows_for_set_format_example(name, db, entry_id)


def set_entry_format_conditional_statements():
    name = tr("Conditional Statements Example")
    path, name = create_new_dict_path_with_non_existing_name(name)
    db = dict_database.DictDatabase(path)
    condition1 = tr("Both {0} and {1} are present.").format(
        f"{{{tr("Tag 1")}}}",
        f"{{{tr("Tag 2")}}}",
    )
    condition2 = tr("Only {} is present.").format(
        f"{{{tr("Tag 1")}}}",
    )
    condition3 = tr("Only {} is present.").format(
        f"{{{tr("Tag 2")}}}",
    )
    db.info.set_long_entry_format(
        f"{{{condition1}}}|{{{condition2}}}|{{{condition3}}}"
    )
    db.info.set_entry_joiner("<hr>")
    db.tags.create_tag(tr("Tag 1"), True, "{{},... {}}", "", 0)
    db.tags.create_tag(tr("Tag 2"), False, "{{},... {}}", "", 1)
    entry_id = db.entries.create_entry()
    form_id1 = db.forms.create_form(entry_id, 0)
    form_id2 = db.forms.create_form(entry_id, 1)
    form_id3 = db.forms.create_form(entry_id, 2)
    tag_values_list = [
        (
            form_id1,
            db.tags.get_tag_id(tr("Tag 1")),
            [tr("value 1")],
            True,
            False,
        ),
        (
            form_id1,
            db.tags.get_tag_id(tr("Tag 2")),
            [tr("value 2")],
            False,
            False,
        ),
        (
            form_id2,
            db.tags.get_tag_id(tr("Tag 1")),
            [tr("value 1")],
            True,
            False,
        ),
        (
            form_id2,
            db.tags.get_tag_id(tr("Tag 2")),
            [""],
            False,
            False,
        ),
        (
            form_id3,
            db.tags.get_tag_id(tr("Tag 1")),
            [""],
            True,
            False,
        ),
        (
            form_id3,
            db.tags.get_tag_id(tr("Tag 2")),
            [tr("value 2")],
            False,
            False,
        ),
    ]
    for tag_values in tag_values_list:
        db.tag_rows.set_tag_values(*tag_values)
    open_windows_for_set_format_example(name, db, entry_id)


def set_entry_format_html():
    name = tr("HTML Example")
    path, name = create_new_dict_path_with_non_existing_name(name)
    db = dict_database.DictDatabase(path)
    db.info.set_long_entry_format(
        '<b>{0}</b><br><i>{1}</i><div style="color:#EE1111; background-color:#1111EE; font-family:Cardo; font-size:{3}pt"><b>{2}</b></div>'.format(
            f"{{{tr("Tag 1")}}}",
            f"{{{tr("Tag 2")}}}",
            f"{{{tr("Tag 3")}}}",
            settings.dict_font_size * 3,
        )
    )
    db.info.set_entry_joiner("<hr>")
    db.tags.create_tag(tr("Tag 1"), True, "{{},... {}}", "", 0)
    db.tags.create_tag(tr("Tag 2"), True, "{{},... {}}", "", 1)
    db.tags.create_tag(tr("Tag 3"), True, "{{},... {}}", "", 2)
    entry_id = db.entries.create_entry()
    form_id = db.forms.create_form(entry_id, 0)
    tag_values_list = [
        (
            form_id,
            db.tags.get_tag_id(tr("Tag 1")),
            [tr("This tag is bold.")],
            True,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Tag 2")),
            [tr("This tag is italic.")],
            True,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Tag 3")),
            [tr("This tag is stylish.")],
            True,
            False,
        ),
    ]
    for tag_values in tag_values_list:
        db.tag_rows.set_tag_values(*tag_values)
    open_windows_for_set_format_example(name, db, entry_id)


def set_entry_format_escaped_curly_braces():
    name = tr("Escaped Curly Braces Example")
    path, name = create_new_dict_path_with_non_existing_name(name)
    db = dict_database.DictDatabase(path)
    db.info.set_long_entry_format(
        tr("{}").format(r"\{" + f"{{{tr("Tag")}}}" + r"\}")
    )
    db.info.set_entry_joiner("<hr>")
    db.tags.create_tag(tr("Tag"), True, "{{},... {}}", "", 0)
    entry_id = db.entries.create_entry()
    form_id = db.forms.create_form(entry_id, 0)
    tag_values_list = [
        (
            form_id,
            db.tags.get_tag_id(tr("Tag")),
            [tr("This tag is surrounded by escaped curly braces.")],
            True,
            False,
        ),
    ]
    for tag_values in tag_values_list:
        db.tag_rows.set_tag_values(*tag_values)
    open_windows_for_set_format_example(name, db, entry_id)


def set_tag_values_format_simple():
    name = tr("Simple Example")
    path, name = create_new_dict_path_with_non_existing_name(name)
    db = dict_database.DictDatabase(path)
    db.info.set_long_entry_format(f"{{{tr("Tag")}}}")
    db.info.set_entry_joiner("<hr>")
    db.tags.create_tag(
        tr("Tag"),
        True,
        "{{},... {}}" + language.rtl_tag_or_empty_string,
        "",
        0,
    )
    entry_id = db.entries.create_entry()
    form_id1 = db.forms.create_form(entry_id, 0)
    form_id2 = db.forms.create_form(entry_id, 1)
    form_id3 = db.forms.create_form(entry_id, 2)
    tag_values_list = [
        (
            form_id1,
            db.tags.get_tag_id(tr("Tag")),
            [tr("value 1")],
            True,
            False,
        ),
        (
            form_id2,
            db.tags.get_tag_id(tr("Tag")),
            [
                tr("value 1"),
                tr("value 2"),
            ],
            False,
            False,
        ),
        (
            form_id3,
            db.tags.get_tag_id(tr("Tag")),
            [
                tr("value 1"),
                tr("value 2"),
                tr("value 3"),
            ],
            False,
            False,
        ),
    ]
    for tag_values in tag_values_list:
        db.tag_rows.set_tag_values(*tag_values)
    open_windows_for_set_format_example(name, db, entry_id)


def set_tag_values_format_conditional_statements():
    name = tr("Conditional Statements Example")
    path, name = create_new_dict_path_with_non_existing_name(name)
    db = dict_database.DictDatabase(path)
    db.info.set_long_entry_format(f"{{{tr("Tag")}}}")
    db.info.set_entry_joiner("<hr>")
    db.tags.create_tag(
        tr("Tag"),
        True,
        tr("{}|{{} and {}}|{{},... {}, and {}}")
        + language.rtl_tag_or_empty_string,
        "",
        0,
    )
    entry_id = db.entries.create_entry()
    form_id1 = db.forms.create_form(entry_id, 0)
    form_id2 = db.forms.create_form(entry_id, 1)
    form_id3 = db.forms.create_form(entry_id, 2)
    form_id4 = db.forms.create_form(entry_id, 3)
    tag_values_list = [
        (
            form_id1,
            db.tags.get_tag_id(tr("Tag")),
            [tr("value 1")],
            True,
            False,
        ),
        (
            form_id2,
            db.tags.get_tag_id(tr("Tag")),
            [
                tr("value 1"),
                tr("value 2"),
            ],
            False,
            False,
        ),
        (
            form_id3,
            db.tags.get_tag_id(tr("Tag")),
            [
                tr("value 1"),
                tr("value 2"),
                tr("value 3"),
            ],
            False,
            False,
        ),
        (
            form_id4,
            db.tags.get_tag_id(tr("Tag")),
            [
                tr("value 1"),
                tr("value 2"),
                tr("value 3"),
                tr("value 4"),
            ],
            False,
            False,
        ),
    ]
    for tag_values in tag_values_list:
        db.tag_rows.set_tag_values(*tag_values)
    open_windows_for_set_format_example(name, db, entry_id)


def set_tag_values_format_html():
    name = tr("HTML Example")
    path, name = create_new_dict_path_with_non_existing_name(name)
    db = dict_database.DictDatabase(path)
    db.info.set_long_entry_format(f"{{{tr("Tag")}}}")
    db.info.set_entry_joiner("<hr>")
    db.tags.create_tag(
        tr("Tag"),
        True,
        "{<ol><li>{}</li>...<li>{}</li></ol>}",
        "",
        0,
    )
    entry_id = db.entries.create_entry()
    form_id1 = db.forms.create_form(entry_id, 0)
    form_id2 = db.forms.create_form(entry_id, 1)
    form_id3 = db.forms.create_form(entry_id, 2)
    tag_values_list = [
        (
            form_id1,
            db.tags.get_tag_id(tr("Tag")),
            [tr("value 1")],
            True,
            False,
        ),
        (
            form_id2,
            db.tags.get_tag_id(tr("Tag")),
            [
                tr("value 1"),
                tr("value 2"),
            ],
            False,
            False,
        ),
        (
            form_id3,
            db.tags.get_tag_id(tr("Tag")),
            [
                tr("value 1"),
                tr("value 2"),
                tr("value 3"),
            ],
            False,
            False,
        ),
    ]
    for tag_values in tag_values_list:
        db.tag_rows.set_tag_values(*tag_values)
    open_windows_for_set_format_example(name, db, entry_id)


def set_tag_values_format_escaped_ellipsis():
    name = tr("Escaped Ellipsis Example")
    path, name = create_new_dict_path_with_non_existing_name(name)
    db = dict_database.DictDatabase(path)
    db.info.set_long_entry_format(f"{{{tr("Tag")}}}")
    db.info.set_entry_joiner("<hr>")
    db.tags.create_tag(
        tr("Tag"),
        True,
        r"{{},... {}\...}" + language.rtl_tag_or_empty_string,
        "",
        0,
    )
    entry_id = db.entries.create_entry()
    form_id = db.forms.create_form(entry_id, 0)
    tag_values_list = [
        (
            form_id,
            db.tags.get_tag_id(tr("Tag")),
            [
                tr("value 1"),
                tr("value 2"),
                tr("value 3"),
            ],
            False,
            False,
        ),
    ]
    for tag_values in tag_values_list:
        db.tag_rows.set_tag_values(*tag_values)
    open_windows_for_set_format_example(name, db, entry_id)


def set_tag_values_format_right_to_left_language():
    name = tr("Right To Left Language Example")
    path, name = create_new_dict_path_with_non_existing_name(name)
    db = dict_database.DictDatabase(path)
    db.info.set_long_entry_format(f"{{{tr("Tag")}}}")
    db.info.set_entry_joiner("<hr>")
    db.tags.create_tag(
        tr("Tag"),
        True,
        "{{},... {}}{<-}",
        "",
        0,
    )
    entry_id = db.entries.create_entry()
    form_id1 = db.forms.create_form(entry_id, 0)
    form_id2 = db.forms.create_form(entry_id, 1)
    form_id3 = db.forms.create_form(entry_id, 2)
    tag_values_list = [
        (
            form_id1,
            db.tags.get_tag_id(tr("Tag")),
            [tr("value 1")],
            True,
            False,
        ),
        (
            form_id2,
            db.tags.get_tag_id(tr("Tag")),
            [
                tr("value 1"),
                tr("value 2"),
            ],
            False,
            False,
        ),
        (
            form_id3,
            db.tags.get_tag_id(tr("Tag")),
            [
                tr("value 1"),
                tr("value 2"),
                tr("value 3"),
            ],
            False,
            False,
        ),
    ]
    for tag_values in tag_values_list:
        db.tag_rows.set_tag_values(*tag_values)
    open_windows_for_set_format_example(name, db, entry_id)


# https://www.thelatinlibrary.com/caesar/gallic/gall1.shtml
COMMENTARII_DE_BELLO_GALLICO_LIBER_I = """[1] Gallia est omnis divisa in partes tres, quarum unam incolunt Belgae, aliam Aquitani, tertiam qui ipsorum lingua Celtae, nostra Galli appellantur. Hi omnes lingua, institutis, legibus inter se differunt. Gallos ab Aquitanis Garumna flumen, a Belgis Matrona et Sequana dividit. Horum omnium fortissimi sunt Belgae, propterea quod a cultu atque humanitate provinciae longissime absunt, minimeque ad eos mercatores saepe commeant atque ea quae ad effeminandos animos pertinent important, proximique sunt Germanis, qui trans Rhenum incolunt, quibuscum continenter bellum gerunt. Qua de causa Helvetii quoque reliquos Gallos virtute praecedunt, quod fere cotidianis proeliis cum Germanis contendunt, cum aut suis finibus eos prohibent aut ipsi in eorum finibus bellum gerunt. Eorum una, pars, quam Gallos obtinere dictum est, initium capit a flumine Rhodano, continetur Garumna flumine, Oceano, finibus Belgarum, attingit etiam ab Sequanis et Helvetiis flumen Rhenum, vergit ad septentriones. Belgae ab extremis Galliae finibus oriuntur, pertinent ad inferiorem partem fluminis Rheni, spectant in septentrionem et orientem solem. Aquitania a Garumna flumine ad Pyrenaeos montes et eam partem Oceani quae est ad Hispaniam pertinet; spectat inter occasum solis et septentriones.

[2] Apud Helvetios longe nobilissimus fuit et ditissimus Orgetorix. Is M. Messala, [et P.] M. Pisone consulibus regni cupiditate inductus coniurationem nobilitatis fecit et civitati persuasit ut de finibus suis cum omnibus copiis exirent: perfacile esse, cum virtute omnibus praestarent, totius Galliae imperio potiri. Id hoc facilius iis persuasit, quod undique loci natura Helvetii continentur: una ex parte flumine Rheno latissimo atque altissimo, qui agrum Helvetium a Germanis dividit; altera ex parte monte Iura altissimo, qui est inter Sequanos et Helvetios; tertia lacu Lemanno et flumine Rhodano, qui provinciam nostram ab Helvetiis dividit. His rebus fiebat ut et minus late vagarentur et minus facile finitimis bellum inferre possent; qua ex parte homines bellandi cupidi magno dolore adficiebantur. Pro multitudine autem hominum et pro gloria belli atque fortitudinis angustos se fines habere arbitrabantur, qui in longitudinem milia passuum CCXL, in latitudinem CLXXX patebant.

[3] His rebus adducti et auctoritate Orgetorigis permoti constituerunt ea quae ad proficiscendum pertinerent comparare, iumentorum et carrorum quam maximum numerum coemere, sementes quam maximas facere, ut in itinere copia frumenti suppeteret, cum proximis civitatibus pacem et amicitiam confirmare. Ad eas res conficiendas biennium sibi satis esse duxerunt; in tertium annum profectionem lege confirmant. Ad eas res conficiendas Orgetorix deligitur. Is sibi legationem ad civitates suscipit. In eo itinere persuadet Castico, Catamantaloedis filio, Sequano, cuius pater regnum in Sequanis multos annos obtinuerat et a senatu populi Romani amicus appellatus erat, ut regnum in civitate sua occuparet, quod pater ante habuerit; itemque Dumnorigi Haeduo, fratri Diviciaci, qui eo tempore principatum in civitate obtinebat ac maxime plebi acceptus erat, ut idem conaretur persuadet eique filiam suam in matrimonium dat. Perfacile factu esse illis probat conata perficere, propterea quod ipse suae civitatis imperium obtenturus esset: non esse dubium quin totius Galliae plurimum Helvetii possent; se suis copiis suoque exercitu illis regna conciliaturum confirmat. Hac oratione adducti inter se fidem et ius iurandum dant et regno occupato per tres potentissimos ac firmissimos populos totius Galliae sese potiri posse sperant.

[4] Ea res est Helvetiis per indicium enuntiata. Moribus suis Orgetoricem ex vinculis causam dicere coegerunt; damnatum poenam sequi oportebat, ut igni cremaretur. Die constituta causae dictionis Orgetorix ad iudicium omnem suam familiam, ad hominum milia decem, undique coegit, et omnes clientes obaeratosque suos, quorum magnum numerum habebat, eodem conduxit; per eos ne causam diceret se eripuit. Cum civitas ob eam rem incitata armis ius suum exequi conaretur multitudinemque hominum ex agris magistratus cogerent, Orgetorix mortuus est; neque abest suspicio, ut Helvetii arbitrantur, quin ipse sibi mortem consciverit.

[5] Post eius mortem nihilo minus Helvetii id quod constituerant facere conantur, ut e finibus suis exeant. Ubi iam se ad eam rem paratos esse arbitrati sunt, oppida sua omnia, numero ad duodecim, vicos ad quadringentos, reliqua privata aedificia incendunt; frumentum omne, praeter quod secum portaturi erant, comburunt, ut domum reditionis spe sublata paratiores ad omnia pericula subeunda essent; trium mensum molita cibaria sibi quemque domo efferre iubent. Persuadent Rauracis et Tulingis et Latobrigis finitimis, uti eodem usi consilio oppidis suis vicisque exustis una cum iis proficiscantur, Boiosque, qui trans Rhenum incoluerant et in agrum Noricum transierant Noreiamque oppugnabant, receptos ad se socios sibi adsciscunt.

[6] Erant omnino itinera duo, quibus itineribus domo exire possent: unum per Sequanos, angustum et difficile, inter montem Iuram et flumen Rhodanum, vix qua singuli carri ducerentur, mons autem altissimus impendebat, ut facile perpauci prohibere possent; alterum per provinciam nostram, multo facilius atque expeditius, propterea quod inter fines Helvetiorum et Allobrogum, qui nuper pacati erant, Rhodanus fluit isque non nullis locis vado transitur. Extremum oppidum Allobrogum est proximumque Helvetiorum finibus Genava. Ex eo oppido pons ad Helvetios pertinet. Allobrogibus sese vel persuasuros, quod nondum bono animo in populum Romanum viderentur, existimabant vel vi coacturos ut per suos fines eos ire paterentur. Omnibus rebus ad profectionem comparatis diem dicunt, qua die ad ripam Rhodani omnes conveniant. Is dies erat a. d. V. Kal. Apr. L. Pisone, A. Gabinio consulibus.

[7] Caesari cum id nuntiatum esset, eos per provinciam nostram iter facere conari, maturat ab urbe proficisci et quam maximis potest itineribus in Galliam ulteriorem contendit et ad Genavam pervenit. Provinciae toti quam maximum potest militum numerum imperat (erat omnino in Gallia ulteriore legio una), pontem, qui erat ad Genavam, iubet rescindi. Ubi de eius adventu Helvetii certiores facti sunt, legatos ad eum mittunt nobilissimos civitatis, cuius legationis Nammeius et Verucloetius principem locum obtinebant, qui dicerent sibi esse in animo sine ullo maleficio iter per provinciam facere, propterea quod aliud iter haberent nullum: rogare ut eius voluntate id sibi facere liceat. Caesar, quod memoria tenebat L. Cassium consulem occisum exercitumque eius ab Helvetiis pulsum et sub iugum missum, concedendum non putabat; neque homines inimico animo, data facultate per provinciam itineris faciundi, temperaturos ab iniuria et maleficio existimabat. Tamen, ut spatium intercedere posset dum milites quos imperaverat convenirent, legatis respondit diem se ad deliberandum sumpturum: si quid vellent, ad Id. April. reverterentur.

[8] Interea ea legione quam secum habebat militibusque, qui ex provincia convenerant, a lacu Lemanno, qui in flumen Rhodanum influit, ad montem Iuram, qui fines Sequanorum ab Helvetiis dividit, milia passuum XVIIII murum in altitudinem pedum sedecim fossamque perducit. Eo opere perfecto praesidia disponit, castella communit, quo facilius, si se invito transire conentur, prohibere possit. Ubi ea dies quam constituerat cum legatis venit et legati ad eum reverterunt, negat se more et exemplo populi Romani posse iter ulli per provinciam dare et, si vim facere conentur, prohibiturum ostendit. Helvetii ea spe deiecti navibus iunctis ratibusque compluribus factis, alii vadis Rhodani, qua minima altitudo fluminis erat, non numquam interdiu, saepius noctu si perrumpere possent conati, operis munitione et militum concursu et telis repulsi, hoc conatu destiterunt.

[9] Relinquebatur una per Sequanos via, qua Sequanis invitis propter angustias ire non poterant. His cum sua sponte persuadere non possent, legatos ad Dumnorigem Haeduum mittunt, ut eo deprecatore a Sequanis impetrarent. Dumnorix gratia et largitione apud Sequanos plurimum poterat et Helvetiis erat amicus, quod ex ea civitate Orgetorigis filiam in matrimonium duxerat, et cupiditate regni adductus novis rebus studebat et quam plurimas civitates suo beneficio habere obstrictas volebat. Itaque rem suscipit et a Sequanis impetrat ut per fines suos Helvetios ire patiantur, obsidesque uti inter sese dent perficit: Sequani, ne itinere Helvetios prohibeant, Helvetii, ut sine maleficio et iniuria transeant.

[10] Caesari renuntiatur Helvetiis esse in animo per agrum Sequanorum et Haeduorum iter in Santonum fines facere, qui non longe a Tolosatium finibus absunt, quae civitas est in provincia. Id si fieret, intellegebat magno cum periculo provinciae futurum ut homines bellicosos, populi Romani inimicos, locis patentibus maximeque frumentariis finitimos haberet. Ob eas causas ei munitioni quam fecerat T. Labienum legatum praeficit; ipse in Italiam magnis itineribus contendit duasque ibi legiones conscribit et tres, quae circum Aquileiam hiemabant, ex hibernis educit et, qua proximum iter in ulteriorem Galliam per Alpes erat, cum his quinque legionibus ire contendit. Ibi Ceutrones et Graioceli et Caturiges locis superioribus occupatis itinere exercitum prohibere conantur. Compluribus his proeliis pulsis ab Ocelo, quod est oppidum citerioris provinciae extremum, in fines Vocontiorum ulterioris provinciae die septimo pervenit; inde in Allobrogum fines, ab Allobrogibus in Segusiavos exercitum ducit. Hi sunt extra provinciam trans Rhodanum primi.

[11] Helvetii iam per angustias et fines Sequanorum suas copias traduxerant et in Haeduorum fines pervenerant eorumque agros populabantur. Haedui, cum se suaque ab iis defendere non possent, legatos ad Caesarem mittunt rogatum auxilium: ita se omni tempore de populo Romano meritos esse ut paene in conspectu exercitus nostri agri vastari, liberi [eorum] in servitutem abduci, oppida expugnari non debuerint. Eodem tempore quo Haedui Ambarri, necessarii et consanguinei Haeduorum, Caesarem certiorem faciunt sese depopulatis agris non facile ab oppidis vim hostium prohibere. Item Allobroges, qui trans Rhodanum vicos possessionesque habebant, fuga se ad Caesarem recipiunt et demonstrant sibi praeter agri solum nihil esse reliqui. Quibus rebus adductus Caesar non expectandum sibi statuit dum, omnibus, fortunis sociorum consumptis, in Santonos Helvetii pervenirent.

[12] Flumen est Arar, quod per fines Haeduorum et Sequanorum in Rhodanum influit, incredibili lenitate, ita ut oculis in utram partem fluat iudicari non possit. Id Helvetii ratibus ac lintribus iunctis transibant. Ubi per exploratores Caesar certior factus est tres iam partes copiarum Helvetios id flumen traduxisse, quartam vero partem citra flumen Ararim reliquam esse, de tertia vigilia cum legionibus tribus e castris profectus ad eam partem pervenit quae nondum flumen transierat. Eos impeditos et inopinantes adgressus magnam partem eorum concidit; reliqui sese fugae mandarunt atque in proximas silvas abdiderunt. Is pagus appellabatur Tigurinus; nam omnis civitas Helvetia in quattuor pagos divisa est. Hic pagus unus, cum domo exisset, patrum nostrorum memoria L. Cassium consulem interfecerat et eius exercitum sub iugum miserat. Ita sive casu sive consilio deorum immortalium quae pars civitatis Helvetiae insignem calamitatem populo Romano intulerat, ea princeps poenam persolvit. Qua in re Caesar non solum publicas, sed etiam privatas iniurias ultus est, quod eius soceri L. Pisonis avum, L. Pisonem legatum, Tigurini eodem proelio quo Cassium interfecerant.

[13] Hoc proelio facto, reliquas copias Helvetiorum ut consequi posset, pontem in Arari faciendum curat atque ita exercitum traducit. Helvetii repentino eius adventu commoti cum id quod ipsi diebus XX aegerrime confecerant, ut flumen transirent, illum uno die fecisse intellegerent, legatos ad eum mittunt; cuius legationis Divico princeps fuit, qui bello Cassiano dux Helvetiorum fuerat. Is ita cum Caesare egit: si pacem populus Romanus cum Helvetiis faceret, in eam partem ituros atque ibi futuros Helvetios ubi eos Caesar constituisset atque esse voluisset; sin bello persequi perseveraret, reminisceretur et veteris incommodi populi Romani et pristinae virtutis Helvetiorum. Quod improviso unum pagum adortus esset, cum ii qui flumen transissent suis auxilium ferre non possent, ne ob eam rem aut suae magnopere virtuti tribueret aut ipsos despiceret. Se ita a patribus maioribusque suis didicisse, ut magis virtute contenderent quam dolo aut insidiis niterentur. Quare ne committeret ut is locus ubi constitissent ex calamitate populi Romani et internecione exercitus nomen caperet aut memoriam proderet.

[14] His Caesar ita respondit: eo sibi minus dubitationis dari, quod eas res quas legati Helvetii commemorassent memoria teneret, atque eo gravius ferre quo minus merito populi Romani accidissent; qui si alicuius iniuriae sibi conscius fuisset, non fuisse difficile cavere; sed eo deceptum, quod neque commissum a se intellegeret quare timeret neque sine causa timendum putaret. Quod si veteris contumeliae oblivisci vellet, num etiam recentium iniuriarum, quod eo invito iter per provinciam per vim temptassent, quod Haeduos, quod Ambarros, quod Allobrogas vexassent, memoriam deponere posse? Quod sua victoria tam insolenter gloriarentur quodque tam diu se impune iniurias tulisse admirarentur, eodem pertinere. Consuesse enim deos immortales, quo gravius homines ex commutatione rerum doleant, quos pro scelere eorum ulcisci velint, his secundiores interdum res et diuturniorem impunitatem concedere. Cum ea ita sint, tamen, si obsides ab iis sibi dentur, uti ea quae polliceantur facturos intellegat, et si Haeduis de iniuriis quas ipsis sociisque eorum intulerint, item si Allobrogibus satis faciunt, sese cum iis pacem esse facturum. Divico respondit: ita Helvetios a maioribus suis institutos esse uti obsides accipere, non dare, consuerint; eius rem populum Romanum esse testem. Hoc responso dato discessit.

[15] Postero die castra ex eo loco movent. Idem facit Caesar equitatumque omnem, ad numerum quattuor milium, quem ex omni provincia et Haeduis atque eorum sociis coactum habebat, praemittit, qui videant quas in partes hostes iter faciant. Qui cupidius novissimum agmen insecuti alieno loco cum equitatu Helvetiorum proelium committunt; et pauci de nostris cadunt. Quo proelio sublati Helvetii, quod quingentis equitibus tantam multitudinem equitum propulerant, audacius subsistere non numquam et novissimo agmine proelio nostros lacessere coeperunt. Caesar suos a proelio continebat, ac satis habebat in praesentia hostem rapinis, pabulationibus populationibusque prohibere. Ita dies circiter XV iter fecerunt uti inter novissimum hostium agmen et nostrum primum non amplius quinis aut senis milibus passuum interesset.

[16] Interim cotidie Caesar Haeduos frumentum, quod essent publice polliciti, flagitare. Nam propter frigora [quod Gallia sub septentrionibus, ut ante dictum est, posita est,] non modo frumenta in agris matura non erant, sed ne pabuli quidem satis magna copia suppetebat; eo autem frumento quod flumine Arari navibus subvexerat propterea uti minus poterat quod iter ab Arari Helvetii averterant, a quibus discedere nolebat. Diem ex die ducere Haedui: conferri, comportari, adesse dicere. Ubi se diutius duci intellexit et diem instare quo die frumentum militibus metiri oporteret, convocatis eorum principibus, quorum magnam copiam in castris habebat, in his Diviciaco et Lisco, qui summo magistratui praeerat, quem vergobretum appellant Haedui, qui creatur annuus et vitae necisque in suos habet potestatem, graviter eos accusat, quod, cum neque emi neque ex agris sumi possit, tam necessario tempore, tam propinquis hostibus ab iis non sublevetur, praesertim cum magna ex parte eorum precibus adductus bellum susceperit; multo etiam gravius quod sit destitutus queritur.

[17] Tum demum Liscus oratione Caesaris adductus quod antea tacuerat proponit: esse non nullos, quorum auctoritas apud plebem plurimum valeat, qui privatim plus possint quam ipsi magistratus. Hos seditiosa atque improba oratione multitudinem deterrere, ne frumentum conferant quod debeant: praestare, si iam principatum Galliae obtinere non possint, Gallorum quam Romanorum imperia perferre, neque dubitare [debeant] quin, si Helvetios superaverint Romani, una cum reliqua Gallia Haeduis libertatem sint erepturi. Ab isdem nostra consilia quaeque in castris gerantur hostibus enuntiari; hos a se coerceri non posse. Quin etiam, quod necessariam rem coactus Caesari enuntiarit, intellegere sese quanto id cum periculo fecerit, et ob eam causam quam diu potuerit tacuisse.

[18] Caesar hac oratione Lisci Dumnorigem, Diviciaci fratrem, designari sentiebat, sed, quod pluribus praesentibus eas res iactari nolebat, celeriter concilium dimittit, Liscum retinet. Quaerit ex solo ea quae in conventu dixerat. Dicit liberius atque audacius. Eadem secreto ab aliis quaerit; reperit esse vera: ipsum esse Dumnorigem, summa audacia, magna apud plebem propter liberalitatem gratia, cupidum rerum novarum. Complures annos portoria reliquaque omnia Haeduorum vectigalia parvo pretio redempta habere, propterea quod illo licente contra liceri audeat nemo. His rebus et suam rem familiarem auxisse et facultates ad largiendum magnas comparasse; magnum numerum equitatus suo sumptu semper alere et circum se habere, neque solum domi, sed etiam apud finitimas civitates largiter posse, atque huius potentiae causa matrem in Biturigibus homini illic nobilissimo ac potentissimo conlocasse; ipsum ex Helvetiis uxorem habere, sororum ex matre et propinquas suas nuptum in alias civitates conlocasse. Favere et cupere Helvetiis propter eam adfinitatem, odisse etiam suo nomine Caesarem et Romanos, quod eorum adventu potentia eius deminuta et Diviciacus frater in antiquum locum gratiae atque honoris sit restitutus. Si quid accidat Romanis, summam in spem per Helvetios regni obtinendi venire; imperio populi Romani non modo de regno, sed etiam de ea quam habeat gratia desperare. Reperiebat etiam in quaerendo Caesar, quod proelium equestre adversum paucis ante diebus esset factum, initium eius fugae factum a Dumnorige atque eius equitibus (nam equitatui, quem auxilio Caesari Haedui miserant, Dumnorix praeerat): eorum fuga reliquum esse equitatum perterritum.

[19] Quibus rebus cognitis, cum ad has suspiciones certissimae res accederent, quod per fines Sequanorum Helvetios traduxisset, quod obsides inter eos dandos curasset, quod ea omnia non modo iniussu suo et civitatis sed etiam inscientibus ipsis fecisset, quod a magistratu Haeduorum accusaretur, satis esse causae arbitrabatur quare in eum aut ipse animadverteret aut civitatem animadvertere iuberet. His omnibus rebus unum repugnabat, quod Diviciaci fratris summum in populum Romanum studium, summum in se voluntatem, egregiam fidem, iustitiam, temperantiam cognoverat; nam ne eius supplicio Diviciaci animum offenderet verebatur. Itaque prius quam quicquam conaretur, Diviciacum ad se vocari iubet et, cotidianis interpretibus remotis, per C. Valerium Troucillum, principem Galliae provinciae, familiarem suum, cui summam omnium rerum fidem habebat, cum eo conloquitur; simul commonefacit quae ipso praesente in concilio [Gallorum] de Dumnorige sint dicta, et ostendit quae separatim quisque de eo apud se dixerit. Petit atque hortatur ut sine eius offensione animi vel ipse de eo causa cognita statuat vel civitatem statuere iubeat.

[20] Diviciacus multis cum lacrimis Caesarem complexus obsecrare coepit ne quid gravius in fratrem statueret: scire se illa esse vera, nec quemquam ex eo plus quam se doloris capere, propterea quod, cum ipse gratia plurimum domi atque in reliqua Gallia, ille minimum propter adulescentiam posset, per se crevisset; quibus opibus ac nervis non solum ad minuendam gratiam, sed paene ad perniciem suam uteretur. Sese tamen et amore fraterno et existimatione vulgi commoveri. Quod si quid ei a Caesare gravius accidisset, cum ipse eum locum amicitiae apud eum teneret, neminem existimaturum non sua voluntate factum; qua ex re futurum uti totius Galliae animi a se averterentur. Haec cum pluribus verbis flens a Caesare peteret, Caesar eius dextram prendit; consolatus rogat finem orandi faciat; tanti eius apud se gratiam esse ostendit uti et rei publicae iniuriam et suum dolorem eius voluntati ac precibus condonet. Dumnorigem ad se vocat, fratrem adhibet; quae in eo reprehendat ostendit; quae ipse intellegat, quae civitas queratur proponit; monet ut in reliquum tempus omnes suspiciones vitet; praeterita se Diviciaco fratri condonare dicit. Dumnorigi custodes ponit, ut quae agat, quibuscum loquatur scire possit.

[21] Eodem die ab exploratoribus certior factus hostes sub monte consedisse milia passuum ab ipsius castris octo, qualis esset natura montis et qualis in circuitu ascensus qui cognoscerent misit. Renuntiatum est facilem esse. De tertia vigilia T. Labienum, legatum pro praetore, cum duabus legionibus et iis ducibus qui iter cognoverant summum iugum montis ascendere iubet; quid sui consilii sit ostendit. Ipse de quarta vigilia eodem itinere quo hostes ierant ad eos contendit equitatumque omnem ante se mittit. P. Considius, qui rei militaris peritissimus habebatur et in exercitu L. Sullae et postea in M. Crassi fuerat, cum exploratoribus praemittitur.

[22] Prima luce, cum summus mons a [Lucio] Labieno teneretur, ipse ab hostium castris non longius mille et quingentis passibus abesset neque, ut postea ex captivis comperit, aut ipsius adventus aut Labieni cognitus esset, Considius equo admisso ad eum accurrit, dicit montem, quem a Labieno occupari voluerit, ab hostibus teneri: id se a Gallicis armis atque insignibus cognovisse. Caesar suas copias in proximum collem subducit, aciem instruit. Labienus, ut erat ei praeceptum a Caesare ne proelium committeret, nisi ipsius copiae prope hostium castra visae essent, ut undique uno tempore in hostes impetus fieret, monte occupato nostros expectabat proelioque abstinebat. Multo denique die per exploratores Caesar cognovit et montem a suis teneri et Helvetios castra, movisse et Considium timore perterritum quod non vidisset pro viso sibi renuntiavisse. Eo die quo consuerat intervallo hostes sequitur et milia passuum tria ab eorum castris castra ponit.

[23] Postridie eius diei, quod omnino biduum supererat, cum exercitui frumentum metiri oporteret, et quod a Bibracte, oppido Haeduorum longe maximo et copiosissimo, non amplius milibus passuum XVIII aberat, rei frumentariae prospiciendum existimavit; itaque iter ab Helvetiis avertit ac Bibracte ire contendit. Ea res per fugitivos L. Aemilii, decurionis equitum Gallorum, hostibus nuntiatur. Helvetii, seu quod timore perterritos Romanos discedere a se existimarent, eo magis quod pridie superioribus locis occupatis proelium non commisissent, sive eo quod re frumentaria intercludi posse confiderent, commutato consilio atque itinere converso nostros a novissimo agmine insequi ac lacessere coeperunt.

[24] Postquam id animum advertit, copias suas Caesar in proximum collem subduxit equitatumque, qui sustineret hostium impetum, misit. Ipse interim in colle medio triplicem aciem instruxit legionum quattuor veteranarum; in summo iugo duas legiones quas in Gallia citeriore proxime conscripserat et omnia auxilia conlocavit, ita ut supra se totum montem hominibus compleret; impedimenta sarcinasque in unum locum conferri et eum ab iis qui in superiore acie constiterant muniri iussit. Helvetii cum omnibus suis carris secuti impedimenta in unum locum contulerunt; ipsi confertissima acie, reiecto nostro equitatu, phalange facta sub primam nostram aciem successerunt.

[25] Caesar primum suo, deinde omnium ex conspectu remotis equis, ut aequato omnium periculo spem fugae tolleret, cohortatus suos proelium commisit. Milites loco superiore pilis missis facile hostium phalangem perfregerunt. Ea disiecta gladiis destrictis in eos impetum fecerunt. Gallis magno ad pugnam erat impedimento quod pluribus eorum scutis uno ictu pilorum transfixis et conligatis, cum ferrum se inflexisset, neque evellere neque sinistra impedita satis commode pugnare poterant, multi ut diu iactato bracchio praeoptarent scutum manu emittere et nudo corpore pugnare. Tandem vulneribus defessi et pedem referre et, quod mons suberit circiter mille passuum spatio, eo se recipere coeperunt. Capto monte et succedentibus nostris, Boi et Tulingi, qui hominum milibus circiter XV agmen hostium claudebant et novissimis praesidio erant, ex itinere nostros ab latere aperto adgressi circumvenire, et id conspicati Helvetii, qui in montem sese receperant, rursus instare et proelium redintegrare coeperunt. Romani conversa signa bipertito intulerunt: prima et secunda acies, ut victis ac submotis resisteret, tertia, ut venientes sustineret.

[26] Ita ancipiti proelio diu atque acriter pugnatum est. Diutius cum sustinere nostrorum impetus non possent, alteri se, ut coeperant, in montem receperunt, alteri ad impedimenta et carros suos se contulerunt. Nam hoc toto proelio, cum ab hora septima ad vesperum pugnatum sit, aversum hostem videre nemo potuit. Ad multam noctem etiam ad impedimenta pugnatum est, propterea quod pro vallo carros obiecerunt et e loco superiore in nostros venientes tela coiciebant et non nulli inter carros rotasque mataras ac tragulas subiciebant nostrosque vulnerabant. Diu cum esset pugnatum, impedimentis castrisque nostri potiti sunt. Ibi Orgetorigis filia atque unus e filiis captus est. Ex eo proelio circiter hominum milia CXXX superfuerunt eaque tota nocte continenter ierunt [nullam partem noctis itinere intermisso]; in fines Lingonum die quarto pervenerunt, cum et propter vulnera militum et propter sepulturam occisorum nostri [triduum morati] eos sequi non potuissent. Caesar ad Lingonas litteras nuntiosque misit, ne eos frumento neve alia re iuvarent: qui si iuvissent, se eodem loco quo Helvetios habiturum. Ipse triduo intermisso cum omnibus copiis eos sequi coepit.

[27] Helvetii omnium rerum inopia adducti legatos de deditione ad eum miserunt. Qui cum eum in itinere convenissent seque ad pedes proiecissent suppliciterque locuti flentes pacem petissent, atque eos in eo loco quo tum essent suum adventum expectare iussisset, paruerunt. Eo postquam Caesar pervenit, obsides, arma, servos qui ad eos perfugissent, poposcit. Dum ea conquiruntur et conferuntur, [nocte intermissa] circiter hominum milia VI eius pagi qui Verbigenus appellatur, sive timore perterriti, ne armis traditis supplicio adficerentur, sive spe salutis inducti, quod in tanta multitudine dediticiorum suam fugam aut occultari aut omnino ignorari posse existimarent, prima nocte e castris Helvetiorum egressi ad Rhenum finesque Germanorum contenderunt.

[28] Quod ubi Caesar resciit, quorum per fines ierant his uti conquirerent et reducerent, si sibi purgati esse vellent, imperavit; reductos in hostium numero habuit; reliquos omnes obsidibus, armis, perfugis traditis in deditionem accepit. Helvetios, Tulingos, Latobrigos in fines suos, unde erant profecti, reverti iussit, et, quod omnibus frugibus amissis domi nihil erat quo famem tolerarent, Allobrogibus imperavit ut iis frumenti copiam facerent; ipsos oppida vicosque, quos incenderant, restituere iussit. Id ea maxime ratione fecit, quod noluit eum locum unde Helvetii discesserant vacare, ne propter bonitatem agrorum Germani, qui trans Rhenum incolunt, ex suis finibus in Helvetiorum fines transirent et finitimi Galliae provinciae Allobrogibusque essent. Boios petentibus Haeduis, quod egregia virtute erant cogniti, ut in finibus suis conlocarent, concessit; quibus illi agros dederunt quosque postea in parem iuris libertatisque condicionem atque ipsi erant receperunt.

[29] In castris Helvetiorum tabulae repertae sunt litteris Graecis confectae et ad Caesarem relatae, quibus in tabulis nominatim ratio confecta erat, qui numerus domo exisset eorum qui arma ferre possent, et item separatim, quot pueri, senes mulieresque. [Quarum omnium rerum] summa erat capitum Helvetiorum milium CCLXIII, Tulingorum milium XXXVI, Latobrigorum XIIII, Rauracorum XXIII, Boiorum XXXII; ex his qui arma ferre possent ad milia nonaginta duo. Summa omnium fuerunt ad milia CCCLXVIII. Eorum qui domum redierunt censu habito, ut Caesar imperaverat, repertus est numerus milium C et X.

[30] Bello Helvetiorum confecto totius fere Galliae legati, principes civitatum, ad Caesarem gratulatum convenerunt: intellegere sese, tametsi pro veteribus Helvetiorum iniuriis populi Romani ab his poenas bello repetisset, tamen eam rem non minus ex usu [terrae] Galliae quam populi Romani accidisse, propterea quod eo consilio florentissimis rebus domos suas Helvetii reliquissent uti toti Galliae bellum inferrent imperioque potirentur, locumque domicilio ex magna copia deligerent quem ex omni Gallia oportunissimum ac fructuosissimum iudicassent, reliquasque civitates stipendiarias haberent. Petierunt uti sibi concilium totius Galliae in diem certam indicere idque Caesaris facere voluntate liceret: sese habere quasdam res quas ex communi consensu ab eo petere vellent. Ea re permissa diem concilio constituerunt et iure iurando ne quis enuntiaret, nisi quibus communi consilio mandatum esset, inter se sanxerunt.

[31] Eo concilio dimisso, idem princeps civitatum qui ante fuerant ad Caesarem reverterunt petieruntque uti sibi secreto in occulto de sua omniumque salute cum eo agere liceret. Ea re impetrata sese omnes flentes Caesari ad pedes proiecerunt: non minus se id contendere et laborare ne ea quae dixissent enuntiarentur quam uti ea quae vellent impetrarent, propterea quod, si enuntiatum esset, summum in cruciatum se venturos viderent. Locutus est pro his Diviciacus Haeduus: Galliae totius factiones esse duas; harum alterius principatum tenere Haeduos, alterius Arvernos. Hi cum tantopere de potentatu inter se multos annos contenderent, factum esse uti ab Arvernis Sequanisque Germani mercede arcesserentur. Horum primo circiter milia XV Rhenum transisse; postea quam agros et cultum et copias Gallorum homines feri ac barbari adamassent, traductos plures; nunc esse in Gallia ad C et XX milium numerum. Cum his Haeduos eorumque clientes semel atque iterum armis contendisse; magnam calamitatem pulsos accepisse, omnem nobilitatem, omnem senatum, omnem equitatum amisisse. Quibus proeliis calamitatibusque fractos, qui et sua virtute et populi Romani hospitio atque amicitia plurimum ante in Gallia potuissent, coactos esse Sequanis obsides dare nobilissimos civitatis et iure iurando civitatem obstringere sese neque obsides repetituros neque auxilium a populo Romano imploraturos neque recusaturos quo minus perpetuo sub illorum dicione atque imperio essent. Unum se esse ex omni civitate Haeduorum qui adduci non potuerit ut iuraret aut liberos suos obsides daret. Ob eam rem se ex civitate profugisse et Romam ad senatum venisse auxilium postulatum, quod solus neque iure iurando neque obsidibus teneretur. Sed peius victoribus Sequanis quam Haeduis victis accidisse, propterea quod Ariovistus, rex Germanorum, in eorum finibus consedisset tertiamque partem agri Sequani, qui esset optimus totius Galliae, occupavisset et nunc de altera parte tertia Sequanos decedere iuberet, propterea quod paucis mensibus ante Harudum milia hominum XXIIII ad eum venissent, quibus locus ac sedes pararentur. Futurum esse paucis annis uti omnes ex Galliae finibus pellerentur atque omnes Germani Rhenum transirent; neque enim conferendum esse Gallicum cum Germanorum agro neque hanc consuetudinem victus cum illa comparandam. Ariovistum autem, ut semel Gallorum copias proelio vicerit, quod proelium factum sit ad Magetobrigam, superbe et crudeliter imperare, obsides nobilissimi cuiusque liberos poscere et in eos omnia exempla cruciatusque edere, si qua res non ad nutum aut ad voluntatem eius facta sit. Hominem esse barbarum, iracundum, temerarium: non posse eius imperia, diutius sustineri. Nisi quid in Caesare populoque Romano sit auxilii, omnibus Gallis idem esse faciendum quod Helvetii fecerint, ut domo emigrent, aliud domicilium, alias sedes, remotas a Germanis, petant fortunamque, quaecumque accidat, experiantur. Haec si enuntiata Ariovisto sint, non dubitare quin de omnibus obsidibus qui apud eum sint gravissimum supplicium sumat. Caesarem vel auctoritate sua atque exercitus vel recenti victoria vel nomine populi Romani deterrere posse ne maior multitudo Germanorum Rhenum traducatur, Galliamque omnem ab Ariovisti iniuria posse defendere.

[32] Hac oratione ab Diviciaco habita omnes qui aderant magno fletu auxilium a Caesare petere coeperunt. Animadvertit Caesar unos ex omnibus Sequanos nihil earum rerum facere quas ceteri facerent sed tristes capite demisso terram intueri. Eius rei quae causa esset miratus ex ipsis quaesiit. Nihil Sequani respondere, sed in eadem tristitia taciti permanere. Cum ab his saepius quaereret neque ullam omnino vocem exprimere posset, idem Diviacus Haeduus respondit: hoc esse miseriorem et graviorem fortunam Sequanorum quam reliquorum, quod soli ne in occulto quidem queri neque auxilium implorare auderent absentisque Ariovisti crudelitatem, velut si cora adesset, horrerent, propterea quod reliquis tamen fugae facultas daretur, Sequanis vero, qui intra fines suos Ariovistum recepissent, quorum oppida omnia in potestate eius essent, omnes cruciatus essent perferendi.

[33] His rebus cognitis Caesar Gallorum animos verbis confirmavit pollicitusque est sibi eam rem curae futuram; magnam se habere spem et beneficio suo et auctoritate adductum Ariovistum finem iniuriis facturum. Hac oratione habita, concilium dimisit. Et secundum ea multae res eum hortabantur quare sibi eam rem cogitandam et suscipiendam putaret, in primis quod Haeduos, fratres consanguineosque saepe numero a senatu appellatos, in servitute atque [in] dicione videbat Germanorum teneri eorumque obsides esse apud Ariovistum ac Sequanos intellegebat; quod in tanto imperio populi Romani turpissimum sibi et rei publicae esse arbitrabatur. Paulatim autem Germanos consuescere Rhenum transire et in Galliam magnam eorum multitudinem venire populo Romano periculosum videbat, neque sibi homines feros ac barbaros temperaturos existimabat quin, cum omnem Galliam occupavissent, ut ante Cimbri Teutonique fecissent, in provinciam exirent atque inde in Italiam contenderent [, praesertim cum Sequanos a provincia nostra Rhodanus divideret]; quibus rebus quam maturrime occurrendum putabat. Ipse autem Ariovistus tantos sibi spiritus, tantam arrogantiam sumpserat, ut ferendus non videretur.

[34] Quam ob rem placuit ei ut ad Ariovistum legatos mitteret, qui ab eo postularent uti aliquem locum medium utrisque conloquio deligeret: velle sese de re publica et summis utriusque rebus cum eo agere. Ei legationi Ariovistus respondit: si quid ipsi a Caesare opus esset, sese ad eum venturum fuisse; si quid ille se velit, illum ad se venire oportere. Praeterea se neque sine exercitu in eas partes Galliae venire audere quas Caesar possideret, neque exercitum sine magno commeatu atque molimento in unum locum contrahere posse. Sibi autem mirum videri quid in sua Gallia, quam bello vicisset, aut Caesari aut omnino populo Romano negotii esset.

[35] His responsis ad Caesarem relatis, iterum ad eum Caesar legatos cum his mandatis mittit: quoniam tanto suo populique Romani beneficio adtectus, cum in consulatu suo rex atque amicus a senatu appellatus esset, hanc sibi populoque Romano gratiam referret ut in conloquium venire invitatus gravaretur neque de communi re dicendum sibi et cognoscendum putaret, haec esse quae ab eo postularet: primum ne quam multitudinem hominum amplius trans Rhenum in Galliam traduceret; deinde obsides quos haberet ab Haeduis redderet Sequanisque permitteret ut quos illi haberent voluntate eius reddere illis liceret; neve Haeduos iniuria lacesseret neve his sociisque eorum bellum inferret. Si [id] ita fecisset, sibi populoque Romano perpetuam gratiam atque amicitiam cum eo futuram; si non impetraret, sese, quoniam M. Messala, M. Pisone consulibus senatus censuisset uti quicumque Galliam provinciam obtineret, quod commodo rei publicae lacere posset, Haeduos ceterosque amicos populi Romani defenderet, se Haeduorum iniurias non neglecturum.

[36] Ad haec Ariovistus respondit: ius esse belli ut qui vicissent iis quos vicissent quem ad modum vellent imperarent. Item populum Romanum victis non ad alterius praescriptum, sed ad suum arbitrium imperare consuesse. Si ipse populo Romano non praescriberet quem ad modum suo iure uteretur, non oportere se a populo Romano in suo iure impediri. Haeduos sibi, quoniam belli fortunam temptassent et armis congressi ac superati essent, stipendiarios esse factos. Magnam Caesarem iniuriam facere, qui suo adventu vectigalia sibi deteriora faceret. Haeduis se obsides redditurum non esse neque his neque eorum sociis iniuria bellum inlaturum, si in eo manerent quod convenisset stipendiumque quotannis penderent; si id non fecissent, longe iis fraternum nomen populi Romani afuturum. Quod sibi Caesar denuntiaret se Haeduorum iniurias non neglecturum, neminem secum sine sua pernicie contendisse. Cum vellet, congrederetur: intellecturum quid invicti Germani, exercitatissimi in armis, qui inter annos XIIII tectum non subissent, virtute possent.

[37] Haec eodem tempore Caesari mandata referebantur et legati ab Haeduis et a Treveris veniebant: Haedui questum quod Harudes, qui nuper in Galliam transportati essent, fines eorum popularentur: sese ne obsidibus quidem datis pacem Ariovisti redimere potuisse; Treveri autem, pagos centum Sueborum ad ripas Rheni consedisse, qui Rhemum transire conarentur; his praeesse Nasuam et Cimberium fratres. Quibus rebus Caesar vehementer commotus maturandum sibi existimavit, ne, si nova manus Sueborum cum veteribus copiis Ariovisti sese coniunxisset, minus facile resisti posset. Itaque re frumentaria quam celerrime potuit comparata magnis itineribus ad Ariovistum contendit.

[38] Cum tridui viam processisset, nuntiatum est ei Ariovistum cum suis omnibus copiis ad occupandum Vesontionem, quod est oppidum maximum Sequanorum, contendere [triduique viam a suis finibus processisse]. Id ne accideret, magnopere sibi praecavendum Caesar existimabat. Namque omnium rerum quae ad bellum usui erant summa erat in eo oppido facultas, idque natura loci sic muniebatur ut magnam ad ducendum bellum daret facultatem, propterea quod flumen [alduas] Dubis ut circino circumductum paene totum oppidum cingit, reliquum spatium, quod est non amplius pedum MDC, qua flumen intermittit, mons continet magna altitudine, ita ut radices eius montis ex utraque parte ripae fluminis contingant, hunc murus circumdatus arcem efficit et cum oppido coniungit. Huc Caesar magnis nocturnis diurnisque itineribus contendit occupatoque oppido ibi praesidium conlocat.

[39] Dum paucos dies ad Vesontionem rei frumentariae commeatusque causa moratur, ex percontatione nostrorum vocibusque Gallorum ac mercatorum, qui ingenti magnitudine corporum Germanos, incredibili virtute atque exercitatione in armis esse praedicabant (saepe numero sese cum his congressos ne vultum quidem atque aciem oculorum dicebant ferre potuisse), tantus subito timor omnem exercitum occupavit ut non mediocriter omnium mentes animosque perturbaret. Hic primum ortus est a tribunis militum, praefectis, reliquisque qui ex urbe amicitiae causa Caesarem secuti non magnum in re militari usum habebant: quorum alius alia causa inlata, quam sibi ad proficiscendum necessariam esse diceret, petebat ut eius voluntate discedere liceret; non nulli pudore adducti, ut timoris suspicionem vitarent, remanebant. Hi neque vultum fingere neque interdum lacrimas tenere poterant: abditi in tabernaculis aut suum fatum querebantur aut cum familiaribus suis commune periculum miserabantur. Vulgo totis castris testamenta obsignabantur. Horum vocibus ac timore paulatim etiam ii qui magnum in castris usum habebant, milites centurionesque quique equitatui praeerant, perturbabantur. Qui se ex his minus timidos existimari volebant, non se hostem vereri, sed angustias itineris et magnitudinem silvarum quae intercederent inter ipsos atque Ariovistum, aut rem frumentariam, ut satis commode supportari posset, timere dicebant. Non nulli etiam Caesari nuntiabant, cum castra moveri ac signa ferri iussisset, non fore dicto audientes milites neque propter timorem signa laturos.

[40] Haec cum animadvertisset, convocato consilio omniumque ordinum ad id consilium adhibitis centurionibus, vehementer eos incusavit: primum, quod aut quam in partem aut quo consilio ducerentur sibi quaerendum aut cogitandum putarent. Ariovistum se consule cupidissime populi Romani amicitiam adpetisse; cur hunc tam temere quisquam ab officio discessurum iudicaret? Sibi quidem persuaderi cognitis suis poslulatis atque aequitate condicionum perspecta eum neque suam neque populi Romani gratiam repudiaturum. Quod si furore atque amentia impulsum bellum intulisset, quid tandem vererentur? Aut cur de sua virtute aut de ipsius diligentia desperarent? Factum eius hostis periculum patrum nostrorum memoria Cimbris et Teutonis a C. Mario pulsis [cum non minorem laudem exercitus quam ipse imperator meritus videbatur]; factum etiam nuper in Italia servili tumultu, quos tamen aliquid usus ac disciplina, quam a nobis accepissent, sublevarint. Ex quo iudicari posse quantum haberet in se boni constantia, propterea quod quos aliquam diu inermes sine causa timuissent hos postea armatos ac victores superassent. Denique hos esse eosdem Germanos quibuscum saepe numero Helvetii congressi non solum in suis sed etiam in illorum finibus plerumque superarint, qui tamen pares esse nostro exercitui non potuerint. Si quos adversum proelium et fuga Gallorum commoveret, hos, si quaererent, reperire posse diuturnitate belli defatigatis Gallis Ariovistum, cum multos menses castris se ac paludibus tenuisset neque sui potestatem fecisset, desperantes iam de pugna et dispersos subito adortum magis ratione et consilio quam virtute vicisse. Cui rationi contra homines barbaros atque imperitos locus fuisset, hac ne ipsum quidem sperare nostros exercitus capi posse. Qui suum timorem in rei frumentariae simulationem angustiasque itineris conferrent, facere arroganter, cum aut de officio imperatoris desperare aut praescribere viderentur. Haec sibi esse curae; frumentum Sequanos, Leucos, Lingones subministrare, iamque esse in agris frumenta matura; de itinere ipsos brevi tempore iudicaturos. Quod non fore dicto audientes neque signa laturi dicantur, nihil se ea re commoveri: scire enim, quibuscumque exercitus dicto audiens non fuerit, aut male re gesta fortunam defuisse aut aliquo facinore comperto avaritiam esse convictam. Suam innocentiam perpetua vita, felicitatem Helvetiorum bello esse perspectam. Itaque se quod in longiorem diem conlaturus fuisset repraesentaturum et proxima nocte de quarta, vigilia castra moturum, ut quam primum intellegere posset utrum apud eos pudor atque officium an timor plus valeret. Quod si praeterea nemo sequatur, tamen se cum sola decima legione iturum, de qua non dubitet, sibique eam praetoriam cohortem futuram. Huic legioni Caesar et indulserat praecipue et propter virtutem confidebat maxime.

[41] Hac oratione habita mirum in modum conversae sunt omnium mentes summaque alacritas et cupiditas belli gerendi innata est, princepsque X. legio per tribunos militum ei gratias egit quod de se optimum iudicium fecisset, seque esse ad bellum gerendum paratissimam confirmavit. Deinde reliquae legiones cum tribunis militum et primorum ordinum centurionibus egerunt uti Caesari satis facerent: se neque umquam dubitasse neque timuisse neque de summa belli suum iudicium sed imperatoris esse existimavisse. Eorum satisfactione accepta et itinere exquisito per Diviciacum, quod ex Gallis ei maximam fidem habebat, ut milium amplius quinquaginta circuitu locis apertis exercitum duceret, de quarta vigilia, ut dixerat, profectus est. Septimo die, cum iter non intermitteret, ab exploratoribus certior factus est Ariovisti copias a nostris milia passuum IIII et XX abesse.

[42] Cognito Caesaris adventu Ariovistus legatos ad eum mittit: quod antea de conloquio postulasset, id per se fieri licere, quoniam propius accessisset seque id sine periculo facere posse existimaret. Non respuit condicionem Caesar iamque eum ad sanitatem reverti arbitrabatur, cum id quod antea petenti denegasset ultro polliceretur, magnamque in spem veniebat pro suis tantis populique Romani in eum beneficiis cognitis suis postulatis fore uti pertinacia desisteret. Dies conloquio dictus est ex eo die quintus. Interim saepe cum legati ultro citroque inter eos mitterentur, Ariovistus postulavit ne quem peditem ad conloquium Caesar adduceret: vereri se ne per insidias ab eo circumveniretur; uterque cum equitatu veniret: alia ratione sese non esse venturum. Caesar, quod neque conloquium interposita causa tolli volebat neque salutem suam Gallorum equitatui committere audebat, commodissimum esse statuit omnibus equis Gallis equitibus detractis eo legionarios milites legionis X., cui quam maxime confidebat, imponere, ut praesidium quam amicissimum, si quid opus facto esset, haberet. Quod cum fieret, non inridicule quidam ex militibus X. legionis dixit: plus quam pollicitus esset Caesarem facere; pollicitum se in cohortis praetoriae loco X. legionem habiturum ad equum rescribere.

[43] Planities erat magna et in ea tumulus terrenus satis grandis. Hic locus aequum fere spatium a castris Ariovisti et Caesaris aberat. Eo, ut erat dictum, ad conloquium venerunt. Legionem Caesar, quam equis devexerat, passibus CC ab eo tumulo constituit. Item equites Ariovisti pari intervallo constiterunt. Ariovistus ex equis ut conloquerentur et praeter se denos ad conloquium adducerent postulavit. Ubi eo ventum est, Caesar initio orationis sua senatusque in eum beneficia commemoravit, quod rex appellatus esset a senatu, quod amicus, quod munera amplissime missa; quam rem et paucis contigisse et pro magnis hominum officiis consuesse tribui docebat; illum, cum neque aditum neque causam postulandi iustam haberet, beneficio ac liberalitate sua ac senatus ea praemia consecutum. Docebat etiam quam veteres quamque iustae causae necessitudinis ipsis cum Haeduis intercederent, quae senatus consulta quotiens quamque honorifica in eos facta essent, ut omni tempore totius Galliae principatum Haedui tenuissent, prius etiam quam nostram amicitiam adpetissent. Populi Romani hanc esse consuetudinem, ut socios atque amicos non modo sui nihil deperdere, sed gratia, dignitate, honore auctiores velit esse; quod vero ad amicitiam populi Romani attulissent, id iis eripi quis pati posset? Postulavit deinde eadem quae legatis in mandatis dederat: ne aut Haeduis aut eorum sociis bellum inferret, obsides redderet, si nullam partem Germanorum domum remittere posset, at ne quos amplius Rhenum transire pateretur.

[44] Ariovistus ad postulata Caesaris pauca respondit, de suis virtutibus multa praedicavit: transisse Rhenum sese non sua sponte, sed rogatum et arcessitum a Gallis; non sine magna spe magnisque praemiis domum propinquosque reliquisse; sedes habere in Gallia ab ipsis concessas, obsides ipsorum voluntate datos; stipendium capere iure belli, quod victores victis imponere consuerint. Non sese Gallis sed Gallos sibi bellum intulisse: omnes Galliae civitates ad se oppugnandum venisse ac contra se castra habuisse; eas omnes copias a se uno proelio pulsas ac superatas esse. Si iterum experiri velint, se iterum paratum esse decertare; si pace uti velint, iniquum esse de stipendio recusare, quod sua voluntate ad id tempus pependerint. Amicitiam populi Romani sibi ornamento et praesidio, non detrimento esse oportere, atque se hac spe petisse. Si per populum Romanum stipendium remittatur et dediticii subtrahantur, non minus libenter sese recusaturum populi Romani amicitiam quam adpetierit. Quod multitudinem Germanorum in Galliam traducat, id se sui muniendi, non Galliae oppugnandae causa facere; eius rei testimonium esse quod nisi rogatus non venerit et quod bellum non intulerit sed defenderit. Se prius in Galliam venisse quam populum Romanum. Numquam ante hoc tempus exercitum populi Romani Galliae provinciae finibus egressum. Quid sibi vellet? Cur in suas possessiones veniret? Provinciam suam hanc esse Galliam, sicut illam nostram. Ut ipsi concedi non oporteret, si in nostros fines impetum faceret, sic item nos esse iniquos, quod in suo iure se interpellaremus. Quod fratres a senatu Haeduos appellatos diceret, non se tam barbarum neque tam imperitum esse rerum ut non sciret neque bello Allobrogum proximo Haeduos Romanis auxilium tulisse neque ipsos in iis contentionibus quas Haedui secum et cum Sequanis habuissent auxilio populi Romani usos esse. Debere se suspicari simulata Caesarem amicitia, quod exercitum in Gallia habeat, sui opprimendi causa habere. Qui nisi decedat atque exercitum deducat ex his regionibus, sese illum non pro amico sed pro hoste habiturum. Quod si eum interfecerit, multis sese nobilibus principibusque populi Romani gratum esse facturum (id se ab ipsis per eorum nuntios compertum habere), quorum omnium gratiam atque amicitiam eius morte redimere posset. Quod si decessisset et liberam possessionem Galliae sibi tradidisset, magno se illum praemio remuneraturum et quaecumque bella geri vellet sine ullo eius labore et periculo confecturum.

[45] Multa a Caesare in eam sententiam dicta sunt quare negotio desistere non posset: neque suam neque populi Romani consuetudinem pati ut optime meritos socios desereret, neque se iudicare Galliam potius esse Ariovisti quam populi Romani. Bello superatos esse Arvernos et Rutenos a Q. Fabio Maximo, quibus populus Romanus ignovisset neque in provinciam redegisset neque stipendium posuisset. Quod si antiquissimum quodque tempus spectari oporteret, populi Romani iustissimum esse in Gallia imperium; si iudicium senatus observari oporteret, liberam debere esse Galliam, quam bello victam suis legibus uti voluisset.

[46] Dum haec in conloquio geruntur, Caesari nuntiatum est equites Ariovisti propius tumulum accedere et ad nostros adequitare, lapides telaque in nostros coicere. Caesar loquendi finem fecit seque ad suos recepit suisque imperavit ne quod omnino telum in hostes reicerent. Nam etsi sine ullo periculo legionis delectae cum equitatu proelium fore videbat, tamen committendum non putabat ut, pulsis hostibus, dici posset eos ab se per fidem in conloquio circumventos. Postea quam in vulgus militum elatum est qua arrogantia in conloquio Ariovistus usus omni Gallia Romanis interdixisset, impetumque in nostros eius equites fecissent, eaque res conloquium ut diremisset, multo maior alacritas studiumque pugnandi maius exercitui iniectum est.

[47] Biduo post Ariovistus ad Caesarem legatos misit: velle se de iis rebus quae inter eos egi coeptae neque perfectae essent agere cum eo: uti aut iterum conloquio diem constitueret aut, si id minus vellet, ex suis legatis aliquem ad se mitteret. Conloquendi Caesari causa visa non est, et eo magis quod pridie eius diei Germani retineri non potuerant quin tela in nostros coicerent. Legatum ex suis sese magno cum periculo ad eum missurum et hominibus feris obiecturum existimabat. Commodissimum visum est C. Valerium Procillum, C. Valerii Caburi filium, summa virtute et humanitate adulescentem, cuius pater a C. Valerio Flacco civitate donatus erat, et propter fidem et propter linguae Gallicae scientiam, qua multa iam Ariovistus longinqua consuetudine utebatur, et quod in eo peccandi Germanis causa non esset, ad eum mittere, et una M. Metium, qui hospitio Ariovisti utebatur. His mandavit quae diceret Ariovistus cognoscerent et ad se referrent. Quos cum apud se in castris Ariovistus conspexisset, exercitu suo praesente conclamavit: quid ad se venirent? an speculandi causa? Conantes dicere prohibuit et in catenas coniecit.

[48] Eodem die castra promovit et milibus passuum VI a Caesaris castris sub monte consedit. Postridie eius diei praeter castra Caesaris suas copias traduxit et milibus passuum duobus ultra eum castra fecit eo consilio uti frumento commeatuque qui ex Sequanis et Haeduis supportaretur Caesarem intercluderet. Ex eo die dies continuos V Caesar pro castris suas copias produxit et aciem instructam habuit, ut, si vellet Ariovistus proelio contendere, ei potestas non deesset. Ariovistus his omnibus diebus exercitum castris continuit, equestri proelio cotidie contendit. Genus hoc erat pugnae, quo se Germani exercuerant: equitum milia erant VI, totidem numero pedites velocissimi ac fortissimi, quos ex omni copia singuli singulos suae salutis causa delegerant: cum his in proeliis versabantur, ad eos se equites recipiebant; hi, si quid erat durius, concurrebant, si qui graviore vulnere accepto equo deciderat, circumsistebant; si quo erat longius prodeundum aut celerius recipiendum, tanta erat horum exercitatione celeritas ut iubis sublevati equorum cursum adaequarent.

[49] Ubi eum castris se tenere Caesar intellexit, ne diutius commeatu prohiberetur, ultra eum locum, quo in loco Germani consederant, circiter passus DC ab his, castris idoneum locum delegit acieque triplici instructa ad eum locum venit. Primam et secundam aciem in armis esse, tertiam castra munire iussit. [Hic locus ab hoste circiter passus DC, uti dictum est, aberat.] Eo circiter hominum XVI milia expedita cum omni equitatu Ariovistus misit, quae copiae nostros terrerent et munitione prohiberent. Nihilo setius Caesar, ut ante constituerat, duas acies hostem propulsare, tertiam opus perficere iussit. Munitis castris duas ibi legiones reliquit et partem auxiliorum, quattuor reliquas legiones in castra maiora reduxit.

[50] Proximo die instituto suo Caesar ex castris utrisque copias suas eduxit paulumque a maioribus castris progressus aciem instruxit hostibusque pugnandi potestatem fecit. Ubi ne tum quidem eos prodire intellexit, circiter meridiem exercitum in castra reduxit. Tum demum Ariovistus partem suarum copiarum, quae castra minora oppugnaret, misit. Acriter utrimque usque ad vesperum pugnatum est. Solis occasu suas copias Ariovistus multis et inlatis et acceptis vulneribus in castra reduxit. Cum ex captivis quaereret Caesar quam ob rem Ariovistus proelio non decertaret, hanc reperiebat causam, quod apud Germanos ea consuetudo esset ut matres familiae eorum sortibus et vaticinationibus declararent utrum proelium committi ex usu esset necne; eas ita dicere: non esse fas Germanos superare, si ante novam lunam proelio contendissent.

[51] Postridie eius diei Caesar praesidio utrisque castris quod satis esse visum est reliquit, alarios omnes in conspectu hostium pro castris minoribus constituit, quod minus multitudine militum legionariorum pro hostium numero valebat, ut ad speciem alariis uteretur; ipse triplici instructa acie usque ad castra hostium accessit. Tum demum necessario Germani suas copias castris eduxerunt generatimque constituerunt paribus intervallis, Harudes, Marcomanos, Tribocos, Vangiones, Nemetes, Sedusios, Suebos, omnemque aciem suam raedis et carris circumdederunt, ne qua spes in fuga relinqueretur. Eo mulieres imposuerunt, quae ad proelium proficiscentes milites passis manibus flentes implorabant ne se in servitutem Romanis traderent.

[52] Caesar singulis legionibus singulos legatos et quaestorem praefecit, uti eos testes suae quisque virtutis haberet; ipse a dextro cornu, quod eam partem minime firmam hostium esse animadverterat, proelium commisit. Ita nostri acriter in hostes signo dato impetum fecerunt itaque hostes repente celeriterque procurrerunt, ut spatium pila in hostes coiciendi non daretur. Relictis pilis comminus gladiis pugnatum est. At Germani celeriter ex consuetudine sua phalange facta impetus gladiorum exceperunt. Reperti sunt complures nostri qui in phalanga insilirent et scuta manibus revellerent et desuper vulnerarent. Cum hostium acies a sinistro cornu pulsa atque in fugam coniecta esset, a dextro cornu vehementer multitudine suorum nostram aciem premebant. Id cum animadvertisset P. Crassus adulescens, qui equitatui praeerat, quod expeditior erat quam ii qui inter aciem versabantur, tertiam aciem laborantibus nostris subsidio misit.

[53] Ita proelium restitutum est, atque omnes hostes terga verterunt nec prius fugere destiterunt quam ad flumen Rhenum milia passuum ex eo loco circiter L pervenerunt. Ibi perpauci aut viribus confisi tranare contenderunt aut lintribus inventis sibi salutem reppererunt. In his fuit Ariovistus, qui naviculam deligatam ad ripam nactus ea profugit; reliquos omnes consecuti equites nostri interfecerunt. Duae fuerunt Ariovisti uxores, una Sueba natione, quam domo secum eduxerat, altera Norica, regis Voccionis soror, quam in Gallia duxerat a fratre missam: utraque in ea fuga periit; duae filiae: harum altera occisa, altera capta est. C. Valerius Procillus, cum a custodibus in fuga trinis catenis vinctus traheretur, in ipsum Caesarem hostes equitatu insequentem incidit. Quae quidem res Caesari non minorem quam ipsa victoria voluptatem attulit, quod hominem honestissimum provinciae Galliae, suum familiarem et hospitem, ereptum ex manibus hostium sibi restitutum videbat neque eius calamitate de tanta voluptate et gratulatione quicquam fortuna deminuerat. Is se praesente de se ter sortibus consultum dicebat, utrum igni statim necaretur an in aliud tempus reservaretur: sortium beneficio se esse incolumem. Item M. Metius repertus et ad eum reductus est.

[54] Hoc proelio trans Rhenum nuntiato, Suebi, qui ad ripas Rheni venerant, domum reverti coeperunt; quos ubi qui proximi Rhenum incolunt perterritos senserunt, insecuti magnum ex iis numerum occiderunt. Caesar una aestate duobus maximis bellis confectis maturius paulo quam tempus anni postulabat in hiberna in Sequanos exercitum deduxit; hibernis Labienum praeposuit; ipse in citeriorem Galliam ad conventus agendos profectus est.
"""


def translate_text_dictionary_popup():
    settings.dict_popup_show = True
    from src import main_window

    main_window = main_window.MainWindow(
        (
            [
                text_editor.TextEditor.default_state(),
                text_editor.TextEditor.default_state(),
            ],
            None,
            None,
        )
    )
    main_window.show()
    latin_text_editor, english_text_editor = main_window.text_editors
    latin_text_editor.path = "Commentarii de Bello Gallico, Liber I"
    latin_text_editor.set_text(COMMENTARII_DE_BELLO_GALLICO_LIBER_I)
    latin_text_editor.text_edit.font_combo_box.setCurrentText("Cardo")
    latin_text_editor.text_edit.font_size = 12
    latin_text_editor.text_edit.text_edit.clear_undo_stack()
    english_text_editor.path = "Commentaries on the Gallic War, Book 1"
    english_text_editor.set_text(
        "[1] All Gaul is divided into three parts, one of which the Balgae inhabit, another the Aquitani, the third those who in their own language are called Celts, in ours Gauls."
    )
    english_text_editor.text_edit.font_combo_box.setCurrentText("Cardo")
    english_text_editor.text_edit.font_size = 12
    english_text_editor.text_edit.text_edit.clear_undo_stack()
    name, db = create_dictionary_latin_short()
    latin_text_editor.dictionary = name
    entry_id = db.entries.create_entry()
    form_id = db.forms.create_form(entry_id, 0)
    tag_values_list = [
        (
            form_id,
            db.tags.get_tag_id(tr("Latin")),
            ["lingua"],
            True,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Info")),
            ["-ae, f."],
            False,
            False,
        ),
        (
            form_id,
            db.tags.get_tag_id(tr("Definitions")),
            [
                "a tongue",
                "speech, language",
                "a raised strip of land",
            ],
            False,
            False,
        ),
    ]
    for tag_values in tag_values_list:
        db.tag_rows.set_tag_values(*tag_values)
    cursor = latin_text_editor.text_edit.text_edit.textCursor()
    cursor.movePosition(
        QTextCursor.MoveOperation.Start,
        QTextCursor.MoveMode.MoveAnchor,
        n=1,
    )
    move_to_index = (
        COMMENTARII_DE_BELLO_GALLICO_LIBER_I.find("lingua")
        + len("lingua") // 2
    )
    cursor.movePosition(
        QTextCursor.MoveOperation.NextCharacter,
        QTextCursor.MoveMode.MoveAnchor,
        n=move_to_index,
    )
    latin_text_editor.text_edit.text_edit.prev_popup_cursor = cursor

    def fn():
        latin_text_editor.text_edit.text_edit.popup.show()
        latin_text_editor.text_edit.text_edit.pop_refresh()

    utils.run_after_current_event(fn)


def translate_text_dictionary_side_bar():
    settings.dict_side_bar_text_editor_show = True
    from src import main_window

    main_window = main_window.MainWindow(
        (
            [
                text_editor.TextEditor.default_state(),
            ],
            None,
            None,
        )
    )
    main_window.show()
    latin_text_editor = main_window.text_editors[0]
    latin_text_editor.path = "Commentarii de Bello Gallico, Liber I"
    latin_text_editor.set_text(COMMENTARII_DE_BELLO_GALLICO_LIBER_I)
    latin_text_editor.text_edit.font_combo_box.setCurrentText("Cardo")
    latin_text_editor.text_edit.font_size = 12
    latin_text_editor.text_edit.text_edit.clear_undo_stack()
    name, db = create_dictionary_latin_long()
    latin_text_editor.dictionary = name
    entry_ids = [db.entries.create_entry() for _ in range(2)]
    form_ids = [db.forms.create_form(entry_id, 0) for entry_id in entry_ids]
    tag_values_list = [
        *[
            (
                form_id,
                db.tags.get_tag_id(tr("Latin")),
                ["appellantur"],
                True,
                False,
            )
            for form_id in form_ids
        ],
        *[
            (
                form_id,
                db.tags.get_tag_id(tr("Latin With Long Vowel Marks")),
                ["appellantur"],
                True,
                False,
            )
            for form_id in form_ids
        ],
        (
            form_ids[0],
            db.tags.get_tag_id(tr("Part Of Speech")),
            ["first conjugation verb"],
            True,
            False,
        ),
        (
            form_ids[1],
            db.tags.get_tag_id(tr("Part Of Speech")),
            ["third conjugation verb"],
            True,
            False,
        ),
        (
            form_ids[0],
            db.tags.get_tag_id(tr("Inflection")),
            [
                tr("present passive indicative third-person plural"),
            ],
            False,
            False,
        ),
        (
            form_ids[1],
            db.tags.get_tag_id(tr("Inflection")),
            [
                tr("present passive subjunctive third-person plural"),
            ],
            False,
            False,
        ),
        (
            form_ids[0],
            db.tags.get_tag_id(tr("Base Form With Long Vowel Marks")),
            ["appellāre"],
            False,
            False,
        ),
        (
            form_ids[1],
            db.tags.get_tag_id(tr("Base Form With Long Vowel Marks")),
            ["appellere"],
            False,
            False,
        ),
        (
            form_ids[0],
            db.tags.get_tag_id(tr("Definitions")),
            [
                tr("to address, to speak to"),
                tr("to name, to call"),
            ],
            False,
            False,
        ),
        (
            form_ids[1],
            db.tags.get_tag_id(tr("Definitions")),
            [
                tr("to drive to, to bring to"),
                tr("to bring to land, to put ashore"),
            ],
            False,
            False,
        ),
    ]
    for tag_values in tag_values_list:
        db.tag_rows.set_tag_values(*tag_values)
    cursor = latin_text_editor.text_edit.text_edit.textCursor()
    cursor.movePosition(
        QTextCursor.MoveOperation.Start,
        QTextCursor.MoveMode.MoveAnchor,
        n=1,
    )
    move_to_index = (
        COMMENTARII_DE_BELLO_GALLICO_LIBER_I.find("appellantur")
        + len("appellantur") // 2
    )
    cursor.movePosition(
        QTextCursor.MoveOperation.NextCharacter,
        QTextCursor.MoveMode.MoveAnchor,
        n=move_to_index,
    )
    latin_text_editor.text_edit.text_edit.prev_side_bar_cursor = cursor

    def fn():
        latin_text_editor.text_edit.text_edit.side_bar_refresh()

    utils.run_after_current_event(fn)

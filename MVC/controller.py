import sys
from viwe import error_print, print_about_prog, print_menu, get_iput, menu_pause, yes_no
from model import Contact, File_phone_book, Phone_book
from config import path_to_phone_book

from pathlib import Path
import json

def get_data(path_file:str = path_to_phone_book) -> dict:
    path = Path(path_file)
    file = File_phone_book()

    if not path.exists():
        error_print(f'Фйла <{path_file}> нет в системе.')
        yes = yes_no('Создать его ?')
        if yes:
            path.touch()
            file.create_clear_file()
        else:
            error_print('В фалй config.py указан некорректный путь до файла телефонного справочника. Введите корректный путь перед следующим запуском.\nОстановка программы.')
            sys.exit(1)

    try:
        return file.read_file()
    except json.JSONDecodeError as e:
        error_print(f"Структура файла повреждена! Вы можете исправить проблему вручную перед повторным запуском или запустите очистку контактов.")
        yes = yes_no('Запустить очистку записной книжки?')
        if yes:
            file.write_file({})
            return get_data()
        else:
            error_print('Остановка программы.')
            sys.exit(1)
    except Exception as e:
        error_print(str(e))
        error_print('Программа остановленна из-за непредвиденной ошибки!')
        sys.exit(1)






def open_main_menu():
    ph_book = Phone_book(get_data())
    menu_points = [
        "Просмотр всех контактов",
        "Поиск контактов",
        "Изменение контактов",
        "Добавление контактов",
        "Удаление контактов",
        "Очистка контактов",
        "Пересчёт ID контактов",
        "О программе",
    ]
    selection = None
    while selection != "0":
        print_menu(menu_points)
        selection = get_iput()
        if not (selection.isdigit() and 0<= int(selection) <= len(menu_points)):
            error_print()
            menu_pause()

        if selection == '1':
            # view_contact()
            print()
        elif selection == '2':
            # search_menu()
            print()
        elif selection == '3':
            # edit_menu()
            print()
        elif selection == '4':
            new_contact = Contact()
            ph_book.add_contact(new_contact)
            # add_phone()
            print()
        elif selection == '5':
            # del_menu()
            pass
        elif selection == '6':
            # clean_book()
            print()
        elif selection == '7':
            # sorted_id()
            print()
        elif selection == '8':
            print_about_prog()
            menu_pause()
        


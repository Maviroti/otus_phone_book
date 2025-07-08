from viwe import error_print, print_about_prog, print_menu, get_iput, menu_pause, yes_no
from model import File_phone_book
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
            file.write_file({})
        else:
            error_print('В фалй config.py указан некорректный путь до файла телефонного справочника. Введите корректный путь перед следующим запуском.\nОстановка программы.')
            exit(1)

    try:
        return file.read_file()
    except json.JSONDecodeError as e:
        error_print(f"Структура файла повреждена! Исправьте ошибки вручную или запустите очистку контактов.")
        menu_pause()
    except Exception as e:
        error_print(e)
        error_print('Программа остановленна из-за непредвиденной ошибки!')

    




def open_main_menu():
    data = get_data()
    print(data)
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
        


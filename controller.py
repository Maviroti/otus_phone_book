import sys
from view import clear_console, custom_print, error_print, print_about_prog, print_menu, get_input, menu_pause, yes_no
from model import Contact, File_phone_book, Phone_book
from config import path_to_phone_book

from pathlib import Path
import json


def get_data(file : 'File_phone_book') -> dict:
    path = Path(file.path)

    if not path.exists():
        error_print(f'Файла <{file.path}> нет в системе.')
        yes = yes_no('Создать его ?')
        if yes:
            path.touch()
            file.create_clear_file()
        else:
            error_print('В файл config.py указан некорректный путь до файла телефонного справочника. Введите корректный путь перед следующим запуском.\nОстановка программы.')
            sys.exit(1)
    try:
        return file.read_file()
    except json.JSONDecodeError as e:
        error_print(f"Структура файла повреждена! Вы можете исправить проблему вручную перед повторным запуском или запустите очистку контактов.")
        yes = yes_no('Запустить очистку записной книжки?')
        if yes:
            file.write_file({})
            return get_data(file)
        else:
            error_print('Остановка программы.')
            sys.exit(1)
    except Exception as e:
        error_print(str(e))
        error_print('Программа остановлена из-за непредвиденной ошибки!')
        sys.exit(1)

def open_edit_menu(edit_phone_id:str, phone_book : 'Phone_book') -> None:
    menu_points = [
        'Изменить имя', 
        'Изменить телефон',
        'Изменить комментарий',
        'Просмотр контакта',
    ]
    selection = None
    while selection != "0":
        print_menu(menu_points)
        selection = get_input()
    
        if selection == '1':
            clear_console()
            name = get_input('Введите новое имя: ')
            phone_book.edit_contacts(edit_phone_id,name=name)
        elif selection == '2':
            clear_console()
            phone = get_input('Введите новый телефон: ')
            phone_book.edit_contacts(edit_phone_id,phone=phone)
        elif selection == '3':
            clear_console()
            comment = get_input('Введите новый комментарий: ')
            phone_book.edit_contacts(edit_phone_id,comment=comment)
        elif selection == '4':
            clear_console()
            view_contact_by_id(phone_book, edit_phone_id)
            menu_pause()

def open_search_menu(phone_book : 'Phone_book') -> None:
    menu_points = [
        'Поиск по имени', 
        'Поиск по номеру',
        'Поиск по комментарию',
        'Поиск по всему',
    ]
    selection = None
    while selection != "0":
        print_menu(menu_points)
        selection = get_input()
        if selection == '1':
            clear_console()
            query = get_input('Введите имя для поиска: ')
            found_contacts_list = phone_book.search_contact(query, name=True)
            menu_pause()
        elif selection == '2':
            clear_console()
            query = get_input('Введите телефон для поиска: ')
            found_contacts_list = phone_book.search_contact(query, phone=True)
            menu_pause()
        elif selection == '3':
            clear_console()
            query = get_input('Введите комментарий для поиска: ')
            found_contacts_list = phone_book.search_contact(query, comment=True)
            menu_pause()
        elif selection == '4':
            clear_console()
            query = get_input('Введите запрос для поиска: ')
            found_contacts_list = phone_book.search_contact(query, name=True, phone=True, comment=True)
            menu_pause()
        if found_contacts_list:
            for cont in found_contacts_list:
                view_contacts(cont)
        else:
            error_print('По данному запросу ничего не найдено!')

def view_contacts(ph_book: 'Phone_book') -> None:
    for cont in ph_book.contacts:
        custom_print(cont)

def view_change(ph_book: 'Phone_book') -> None:
    custom_print('Список изменений.')
    if ph_book.change_log['new']:
        custom_print('Добавлены контакты:')
        for cont in ph_book.change_log['new']: custom_print(cont)
    if ph_book.change_log['change']:
        custom_print('')
        custom_print('Изменены контакты:')
        for cont in ph_book.change_log['change']: custom_print(cont)
    if ph_book.change_log['del']:
        custom_print('')
        custom_print('Удалены контакты:')
        for cont in ph_book.change_log['del']: custom_print(cont)

def view_contact_by_id(ph_book: 'Phone_book', id: str) -> None:
        cont = ph_book.get_contact_by_id(id)
        custom_print(str(cont))

def open_main_menu() -> None:
    ph_file = File_phone_book()
    ph_book = Phone_book(get_data(ph_file))
    menu_points = [
        "Просмотр всех контактов",
        "Поиск контактов",
        "Изменение контактов",
        "Добавление контактов",
        "Удаление контактов",
        "Очистка контактов",
        "Пересчёт ID контактов",
        "Посмотреть изменения",
        "О программе",
    ]
    selection = None
    while selection != "0":
        print_menu(menu_points)
        selection = get_input()
        if not (selection.isdigit() and 0<= int(selection) <= len(menu_points)):
            error_print()
            menu_pause()

        if selection == '1':
            view_contacts(ph_book)
            menu_pause()
        elif selection == '2':
            open_search_menu(ph_book)
        elif selection == '3':
            clear_console()
            custom_print('Для изменения контакта, необходимо будет указать его ID. Если Вы не знаете ID, то можете воспользоваться "Просмотром" или "Поиском" в основном меню.')
            yes = yes_no("Продолжить?")
            if yes:
                edit_phone_id = get_input("Введите ID: ")
                if ph_book.check_contact_exist_by_id(edit_phone_id):
                    open_edit_menu(edit_phone_id, ph_book)
                else: 
                    error_print('Контакта с таким ID нет! Возможно вы его удалили.')
                    menu_pause()
        elif selection == '4':
            id = ph_book.get_new_id()
            name = get_input('Введите имя: ')
            phone = get_input('Введите телефон: ')
            comment = get_input('Введите комментарий: ')
            new_contact = Contact(id, name, phone, comment)
            ph_book.add_contact(new_contact)
        elif selection == '5':
            clear_console()
            custom_print('Для удаления контакта, необходимо будет указать его ID. Если Вы не знаете ID, то можете воспользоваться "Просмотром" или "Поиском" в основном меню.')
            yes = yes_no("Продолжить?")
            if yes:
                dell_phone_id_set = set(get_input("Введите ID (если несколько, то через пробел): ").split())
                stop_flag = False
                if not dell_phone_id_set:
                    error_print('Некорректный ввод!')
                    stop_flag = True
                else:
                    for phone_id in dell_phone_id_set:
                        if not ph_book.check_contact_exist_by_id(phone_id):
                            error_print(f'Контакта с ID <{phone_id}> нет! Возможно вы его уже удалили.')
                            stop_flag = True
                            break
                
                if stop_flag: 
                    menu_pause()
                else:
                    for phone_id in dell_phone_id_set:
                        ph_book.del_contact_by_id(phone_id)
        elif selection == '6':
            custom_print('Все контакты будут удалены и файл будет очищен без возможности отменить это действие!')
            yes = yes_no('Продолжить? ')
            if yes:
                ph_file.write_file({})
                ph_book = Phone_book(get_data(ph_file))
            custom_print('')
        elif selection == '7':
            custom_print('Будет выполнено переприсвоение ID, возможна смена ID у некоторых контактов.')
            yes = yes_no('Продолжить?')
            if yes:
                ph_book.sorted_contact_id()
        elif selection == '8':
            view_change(ph_book)
            menu_pause()
        elif selection == '9':
            print_about_prog()
            menu_pause()
    else:
        if ph_book.check_change_exist():
            clear_console()
            custom_print('Были внесены изменения в телефонную книгу.')
            view_change(ph_book)
            yes = yes_no('Сохранить изменения?')
            if yes:
                ph_book.save_change(ph_file)



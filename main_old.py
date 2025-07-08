

import json
import os
import sys

from helpers import clear_console, get_data, get_json_format, get_max_id, print_about_prog, print_dict, menu_pause, dump_data, sorted_id, yes_no
from config_old import PATH

# === [Просмотр] ===
def view_contact():
    """
    Выводит содержание книги контактов
    """
    clear_console()
    data = get_data()
    if data is None:
        menu_pause()
        return
    print_dict(data)
    menu_pause()


# === [Поиск] ===
def input_keyword() -> str:
    """
    Функция возвращает ключевое слово для поиска

    Returns:
        keyword(str): Ключевое слово, введённое в консоли
    """
    keyword = input('Введите текст для поиска: ')
    return keyword

def search(field=False) -> None:
    """
    Функция выполняет поиск и вывод контактов

    Args:
        field: Поле по которому выполняется поиск, если False поиск будет по всем полям
    """
    clear_console()
    keyword = input_keyword()
    data = get_data()
    if data is None:
        menu_pause()
        return
    found_flag = False
    for id, phone in data.items():
        try:
            # Условие на нахождение ключевого слова в одном из полей при поиске по всем полям
            find_by_all_field = not field and (keyword in phone['name'] or keyword in phone['phone'] or keyword in phone['comment'])
            # Условие на нахождение ключевого слова в переданном поле при поиске по конкретному полю
            find_by_field = field and keyword in phone[field]
            if find_by_all_field or find_by_field:
                found_flag = True
                print(f'Контакт ID: {id}')
                print_dict(phone, 4)
        except Exception as e:
            print('При поиске возникла ошибка!')
            print(e)
            exit(1)

    if not found_flag:
        print('Ничего не найдено')
    menu_pause()

def search_menu() -> None:
    """
    Функция запускает интерфактивное меню поиска по контактам
    """
    while True:
        clear_console()
        print(f'1. Поиск по имени')
        print(f'2. Поиск по номеру')
        print(f'3. Поиск по комментарияю')
        print(f'4. Поиск по всему')
        print(f'0. Выход')

        selection = input("Введите номер пункта: ")

        if selection == '1':
            search('name')
            print()
        elif selection == '2':
            search('phone')
            print()
        elif selection == '3':
            search('comment')
            print()
        elif selection == '4':
            search()
            print()
        elif selection == '0':
            clear_console()
            break
        else:
            print("Некорректный ввод!\n")
            menu_pause()


# === [Изменение] ===
def edit_phone(phone:dict, field:str) -> dict:
    """
    Функция меняет имя 

    Args:
        phone(dict): Контакт в котором будут проводиться изменения
        field(str): Название поля, которое будет изменяться
    """
    clear_console()
    new_field = input('Введите новое значение: ')
    phone[field] = new_field
    result = phone
    return result

def edit_menu() -> None:
    """
    Функция запускает интерфактивное меню по изменению контактов
    """
    clear_console()
    print('Для изменения контакта, необходимо будет указать его ID. Если Вы не знаете ID, то можете воспользоваться "Просмотром" или "Поиском" в основном меню.')
    continue_tag = input('Продолжить? (y/n): ')
    if continue_tag == 'n' or continue_tag == 'N':
        return
    elif continue_tag != 'y' and continue_tag != 'Y':
        print("Некорректный ввод!\nВы будете возвращены в основное меню")
        menu_pause()
        return

    edit_phone_id = input("Введите ID: ")
    data = get_data()
    if data is None:
        menu_pause()
        return
    phone = None

    if edit_phone_id in data:
        phone = data[edit_phone_id]
    else:
        print('Контакта с таким ID не существует!')
        menu_pause()
        return
    

    while True:
        clear_console()
        print('1. Изменить имя')
        print('2. Изменить телефон')
        print('3. Изменить комментарий')
        print('4. Просмотр контакта')
        print('0. Выход')

        selection = input("Введите номер пункта: ")

        if selection == '1':
            phone = edit_phone(phone, 'name')
            print()
        elif selection == '2':
            phone = edit_phone(phone, 'phone')
            print()
        elif selection == '3':
            phone = edit_phone(phone, 'comment')
            print()
        elif selection == '4':
            clear_console()
            print(f'Контакт ID: {edit_phone_id}')
            print_dict(phone, indent=4)
            menu_pause()
            print()
        elif selection == '0':
            clear_console()
            break
        else:
            print("Некорректный ввод!\n")
            menu_pause()

        data[edit_phone_id] = phone
        dump_data(data)


# === [Добавление] ===
def add_phone():
    """
    Функция добавляет новую запись в книгу
    """
    max_id = get_max_id()
    if max_id is not None:
        new_id = get_max_id() + 1
    else:
        return
    name = input('Введите имя: ')
    phone = input('Введите номер: ')
    comment = input('Введите комментарий: ')
    new_data = get_json_format(name, phone, comment)
    data = get_data()
    if data is None:
        menu_pause()
        return
    merge_data = {**data, str(new_id): new_data}
    dump_data(merge_data)


# === [Удаление] ===
def del_menu():
    """
    Функция запускает интерфактивное меню по удалению контакта
    """
    clear_console()
    print('Для изменения контакта, необходимо будет указать его ID. Если Вы не знаете ID, то можете воспользоваться "Просмотром" или "Поиском" в основном меню.')
    continue_tag = input('Продолжить? (y/n): ')
    if continue_tag == 'n' or continue_tag == 'N':
        return
    elif continue_tag != 'y' and continue_tag != 'Y':
        print("Некорректный ввод!\nВы будете возвращены в основное меню")
        menu_pause()
        return
    
    dell_phone_id_str = input("Введите ID (если несколько, то через пробел): ")
    del_phone_id_set = set(dell_phone_id_str.split())
    data = get_data()
    if data is None:
        menu_pause()
        return

    for phone_id in del_phone_id_set:
        if phone_id not in data:
            print(f'Контакта с таким ID ["{phone_id}"] не существует!')
            menu_pause()
            return
        
    for phone_id in del_phone_id_set:
        del data[phone_id]

    dump_data(data)


# === [Очистка] ===
def clean_book() -> None:
    yes = yes_no('Книга контактов будет полностью удалена!')
    if yes:
        dump_data({})


def menu():
    while True:
        clear_console()
        print('1. Просмотр всех контактов')
        print('2. Поиск контактов')
        print('3. Изменение контактов')
        print('4. Добавление контактов')
        print('5. Удаление контактов')
        print('6. Очистка контактов')
        print('7. Пересчёт ID контактов')
        print('8. О программе')
        print('0. Выход')

        selection = input("Введите номер пункта: ")
        if selection == '1':
            view_contact()
            print()
        elif selection == '2':
            search_menu()
            print()
        elif selection == '3':
            edit_menu()
            print()
        elif selection == '4':
            add_phone()
            print()
        elif selection == '5':
            del_menu()
        elif selection == '6':
            clean_book()
            print()
        elif selection == '7':
            sorted_id()
            print()
        elif selection == '8':
            print_about_prog()
        elif selection == '0':
            print('Остановка программы')
            sys.exit(0)
        else:
            print("Некорректный ввод!\n")
            menu_pause()

def main():
    menu()

if __name__ == "__main__":
    main()
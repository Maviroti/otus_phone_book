import json
import os

from config_old import PATH, version, copyright

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_dict(data: dict, indent:int = 0):
    """
    Функция выводит словарь в читаемом виде

    Args:
        data(dict): словарь, который нужно вывести
        indent(int): Длина отступа для верхнего уровня вложенности
    """
    for key, value in data.items():
        print(' ' * indent + str(key)+':', end=' ')
        if isinstance(value, dict):
            print()
            print_dict(value, indent=4)
        else:
            print(value)

def menu_pause():
    input('Нажмите ENTER для продолжения')

def dump_data(new_data):
    with open (PATH, 'w', encoding='UTF-8') as f:
        json.dump(new_data, f, indent=4, ensure_ascii=False)

def yes_no(text:str) -> bool:
    """
    Функция запускает меню с выбором (y/n)

    Args:
        test(str): Текст для этого приглашения

    Returns:
        yes(bool): true - cошласие, false - отказ/невернный ввод
    """
    print(text)
    continue_tag = input('Продолжить? (y/n): ')
    if continue_tag == 'n' or continue_tag == 'N':
        return False
    elif continue_tag != 'y' and continue_tag != 'Y':
        print("Некорректный ввод!\nВы будете возвращены в меню")
        menu_pause()
        return False
    return True

def get_data() -> dict:
    """
    Функция возвращает содержание книги контактов

    Returns:
        data(dict): Содержание json файла с контактами
    """
    with open (PATH, 'r', encoding='UTF-8') as f:
        try:
            data = json.load(f)
            return data
        except json.JSONDecodeError as e:
            print(f"Структура файла повреждена! Исправьте ошибки вручную или запустите очистку контактов.")
        except Exception as e:
            print(f'Операция прервана из-за непредвиденной ошибки!')

def get_max_id() -> int:
    """
    Функция возвращает самый большой ID

    Returns:
        max_id(int): Последний id из книги
    """
    data = get_data()
    if data is None:
        menu_pause()
        return
    id_list = list(data.keys())
    if not id_list:
        return 0
    try:
        max_id = max(map(int, id_list))
    except ValueError as e:
        print(f'В книге записан некорректный ID [{str(e).split()[-1]}]. Исправьте ошибку вручную или запустите очистку контактов.')
        menu_pause()
        return

    return max_id

def get_json_format(name: str, phone: str, comm: str) -> dict:
    """
    Функция возвращает подготовленный для записи в json cловарь

    Args
        name(str): Имя контакта
        phone(str): Телефонный номер
        comm(str): Комментарий

    Returns:
        data(dict): Подготовленный для записи в json словарь
    """
    data = {"name": name, "phone": phone, "comment": comm}
    return data

def sorted_id():
    """
    Функция присваивает всем контактам порядковый id
    """
    yes = yes_no('Будет выполнено переприсвоение ID, возможна смена ID у некоторых контактов.')
    if yes:
        data =get_data()
        if data is None:
            menu_pause()
            return
        new_data = {}
        for enum, key in enumerate(data):
            new_data[str(enum + 1)] = data[key]
        dump_data(new_data)

def print_about_prog():
    clear_console()
    print(f'Версия: {version}')
    print(copyright)
    menu_pause()

if __name__ == "__main__":
    pass
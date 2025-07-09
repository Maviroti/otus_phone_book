
from config import version, copyright
import os




def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_pause():
    input('Нажмите ENTER для продолжения')

def yes_no(text:str) -> bool:
    """
    Функция запускает меню с выбором (y/n)

    Args:
        test(str): Текст для этого приглашения

    Returns:
        yes(bool): true - cошласие, false - отказ/невернный ввод
    """
    continue_tag = input(f'{text} (y/n): ')
    if continue_tag == 'n' or continue_tag == 'N':
        return False
    elif continue_tag != 'y' and continue_tag != 'Y':
        print("Некорректный ввод!")
        return yes_no(text)
    return True

def print_menu(points: list, clr_cosole = True)-> None:
    if clr_cosole:
        clear_console()
    for enum, point in enumerate(points):
        print(f'{enum + 1}. {point}')
    print('0. Выход')

def get_input(msg :str = "Введите номер пункта: ") -> str:
    return input(msg)

def error_print(err_msg: str = "Некорректный ввод!"):
    print(err_msg)

def print_about_prog():
    clear_console()
    print(f'Версия: {version}')
    print(copyright)
    



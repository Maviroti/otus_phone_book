import pytest

from controller import open_edit_menu, open_main_menu, open_search_menu
from model import Phone_book


@pytest.mark.parametrize('incor_value', ['-1', '00', 'abc', '1 1'])
@pytest.mark.parametrize('menu_func', [(open_main_menu, []), (open_search_menu,['tst_phone_book']), (open_edit_menu, ['1', 'tst_phone_book'])])
@pytest.mark.parametrize('tst_phone_book', [True], indirect=True)
def test_main_menu_incor_input(incor_value:str, monkeypatch, capsys, menu_func:tuple, tst_phone_book: Phone_book) -> None:
    """Тестирование вывода ошибки о некорректном вводе во всех меню

    Args:
        incor_value (str): список некорректных значений
        monkeypatch (_type_): фикстура
        capsys (_type_): фикстура
        menu_func (tuple): кортеж с функцией и её аргументами
        tst_phone_book (Phone_book): тестовый объект класса
    """
    func = menu_func[0]
    atr_list:list = menu_func[1]
    if 'tst_phone_book' in atr_list:
        atr_list[atr_list.index('tst_phone_book')] = tst_phone_book
    inputs = iter([incor_value, '', '0'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    func(*atr_list)
    captured = capsys.readouterr()
    assert 'Некорректный ввод!' in captured.out





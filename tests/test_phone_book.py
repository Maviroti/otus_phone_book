from functools import reduce
from model import Contact, ContactNotExist, File_phone_book, Phone_book

import pytest

@pytest.fixture
def get_init_data(request) -> dict:
    """Фикстура готовит тестовые данные для проверки инициализации объектов класса Phone_book

    Args:
        request (_type_): Получение данных через параметризацию

    Returns:
        dict: Возвращает словарь, который содержит словарь сырых данных и список с объектами Contact для проверки правильности создания объекта Phone_book
    """
    data_list = request.param
    data_dict = reduce(lambda a, b: a | b, data_list)
    contact_list = []
    for contact_dict in data_list:
        contact_list.append(Contact.from_dict(contact_dict))
    return {'data_dict': data_dict, 'cont_list':contact_list}

@pytest.mark.parametrize(
        'get_init_data',
        [
            [{'1': {'name': 'tester1', 'phone': '89459999999', 'comment': 'this is comment'}}],
            [{'2': {'name': 'тестировщик2', 'phone': 'телефон', 'comment': 'это комментарий'}}],
            [{'3': {'name': 'тестер-tester-3', 'phone': 'телефон-89264567898798', 'comment': 'this IS comment на разных я зыках'}}],
            [
                {'1': {'name': 'tester1', 'phone': '89459999999', 'comment': 'this is comment'}},
                {'2': {'name': 'тестировщик2', 'phone': 'телефон', 'comment': 'это комментарий'}},
                {'3': {'name': 'тестер-tester-3', 'phone': 'телефон-89264567898798', 'comment': 'this IS comment на разных я зыках'}},
            ],
            [{'': {'name': '', 'phone': '', 'comment': ''}}],
        ],
        indirect=True
)
def test_init_phone_book(get_init_data:dict) -> None:
    """Тест для проверки инициализации объекта класса Phone_book

    Args:
        get_init_data (dict): Словарь, который содержит словарь сырых данных и список с объектами Contact для проверки правильности создания объекта Phone_book. 
        Пример: {'data_dict': {сырые данные}, 'cont_list: [Список контактов (объекты класса Contact)]}
    """
    obj = Phone_book(get_init_data['data_dict'])
    assert obj.contacts == get_init_data['cont_list']

@pytest.fixture
def tst_contact(request) -> Contact:
    """Возвращает объект класса Contact

    Args:
        request (_type_): строка с id контакта 

    Returns:
        Contact: объект сс тестовыми данными
    """
    cont_id:str = request.param
    return Contact(cont_id, f'tst_name_{cont_id}', f'+{cont_id} 000 000 00 00', f'comment_{cont_id}')

@pytest.mark.parametrize('tst_phone_book', [True, False], indirect=True)
@pytest.mark.parametrize('tst_contact', ['1'], indirect=True)
def test_add_contact(tst_phone_book: Phone_book, tst_contact: Contact) -> None:
    """Проверяет создание нового контакта в пустой и непустой книге

    Args:
        tst_phone_book (Phone_book): тестовый объект класса
        tst_contact (Contact): тестовый объект класса
    """
    ph_book = tst_phone_book
    ph_book.add_contact(tst_contact)
    assert tst_contact in ph_book.contacts
    assert tst_contact in ph_book.change_log['new']


@pytest.mark.parametrize(['tst_phone_book', 'expected'], [(True, '1'), (False, '2')], indirect=['tst_phone_book'])
def test_getting_new_id(tst_phone_book: Phone_book, expected:str) -> None:
    """Тест на определение нового ID для контакта

    Args:
        tst_phone_book (Phone_book): объект класса 
        expected (str): ожидаемое значение нового ID
    """
    ph_book = tst_phone_book
    new_id = ph_book.get_new_id()
    assert new_id == expected

@pytest.mark.parametrize(['tst_phone_book', 'tst_contact'], [(False, '2')], indirect=True)
@pytest.mark.parametrize('change', [True, False])
def test_checking_change_exist(tst_phone_book: Phone_book, change: bool, tst_contact: Contact) -> None:
    """Тестирует проверку наличия изменений в книге

    Args:
        tst_phone_book (Phone_book): тестовая книга
        change (bool): будут ли вносится изменения
        tst_contact (Contact): тестовый контакт (для внесения изменений в книгу через его добавление)
    """
    ph_book = tst_phone_book
    
    if change:
        ph_book.add_contact(tst_contact)
        assert ph_book.check_change_exist()
    else:
        assert not ph_book.check_change_exist()       

@pytest.mark.parametrize('tst_phone_book', [True, False], indirect=True)
@pytest.mark.parametrize(['tst_contact'], ['2'], indirect=True)
def test_save_change(tst_phone_book:Phone_book, tst_contact:Contact, gen_clear_file:str) -> None:
    """Тестирует сохранение изменений в файле

    Args:
        tst_phone_book (Phone_book): объект класса
        tst_contact (Contact): тестовый контакт
        gen_clear_file (str): пусть до чистого тестового файла
    """
    ph_bk_file = File_phone_book(gen_clear_file)
    ph_book = tst_phone_book
    new_cont = tst_contact
    ph_book.add_contact(new_cont)
    ph_book.save_change(ph_bk_file)
    assert not ph_book.check_change_exist()

@pytest.mark.parametrize(['tst_phone_book', 'ch_id', 'expected'], 
                         [(True, '1', False), 
                          (False, '1', True),
                          (False, '2', False)
                          ], 
                         indirect=['tst_phone_book'])
def test_checking_cont_id_exist(tst_phone_book: Phone_book, ch_id:str, expected:bool) -> None:
    """Тестирует проверку существования контакта по ID

    Args:
        tst_phone_book (Phone_book): объект класса 
        ch_id (str): проверяемый ID
        expected (bool): ожидаемый результат 
    """
    ph_book = tst_phone_book
    id_exist = ph_book.check_contact_exist_by_id(ch_id)
    assert id_exist == expected

@pytest.mark.parametrize(['tst_phone_book', 'cont_exist'], [(True, False), (False, True)], indirect=['tst_phone_book'])
def test_getting_contact_by_id(tst_phone_book: Phone_book, cont_exist: bool) -> None:
    ph_book = tst_phone_book
    cont = ph_book.get_contact_by_id('1')
    if cont_exist:
        assert cont
    else:
        assert cont is None

@pytest.mark.parametrize(['tst_phone_book', 'cont_exist'], [(True, False), (False, True)], indirect=['tst_phone_book'])
def test_deleting_cont_by_id(tst_phone_book: Phone_book, cont_exist:bool) -> None:
    """Тестирует удаление контакта из книги

    Args:
        tst_phone_book (Phone_book): объект класса
        cont_exist (bool): содержит ли книга контакт
    """
    ph_book = tst_phone_book
    if not cont_exist:
        with pytest.raises(ContactNotExist):
            ph_book.del_contact_by_id('1')
    else:
        ph_book.del_contact_by_id('1')
        assert ph_book.change_log['del']
        assert not ph_book.contacts

@pytest.mark.parametrize('tst_phone_book', [False], indirect=True)
@pytest.mark.parametrize('new_data', [{'name': 'new_test_name'},
                                      {'phone': '8 999 999 999 99'},
                                      {'comment': 'new_comm'},
                                      {'name': 'new_test_name','phone': '8 999 999 999 99'},
                                      {'name': 'new_test_name','comment': 'new_comm'},
                                      {'name': 'new_test_name','phone': '8 999 999 999 99','comment': 'new_comm'}, 
                                      {'phone': '8 999 999 999 99','comment': 'new_comm'}, 
                                      ])
def test_edit_contact(tst_phone_book:Phone_book, new_data:dict) -> None:
    """Тестирование изменения контакта

    Args:
        tst_phone_book (Phone_book): объект класса
        new_data (dict): данные которые нужно изменить
    """
    ph_book = tst_phone_book
    ph_book.edit_contacts(id='1', **new_data)
    for key in new_data:
        assert new_data[key] == getattr(ph_book.contacts[0], key)
    assert ph_book.change_log['change'] == ph_book.contacts

@pytest.mark.parametrize('tst_phone_book', [False], indirect=True)
@pytest.mark.parametrize(['search_data', 'exist'], [({'search_query': 'tester', 'name':True}, True), 
                                                    ({'search_query': 'tester', 'phone':True}, False),
                                                    ({'search_query': 'tester', 'comment':True}, False),
                                                    ({'search_query': 'tester', 'name':True, 'phone':True}, True),
                                                    ({'search_query': 'tester', 'name':True, 'comment':True}, True),
                                                    ({'search_query': 'tester', 'name':True, 'phone':True, 'comment':True}, True),
                                                    ({'search_query': 'hello', 'name':True}, False),
                                                    ({'search_query': 'hello', 'name':True, 'phone':True, 'comment':True}, False),
                                                    ])
def test_searching_contacts(tst_phone_book: Phone_book, search_data: dict, exist:bool) -> None:
    """Тестирует поиск контакта

    Args:
        tst_phone_book (Phone_book): объект класса
        search_data (dict): аргументы для вызова метода поиска контакта
        exist (bool): ожидается ли нахождение тестового контакта
    """
    ph_book = tst_phone_book
    tst_cont_list = ph_book.contacts
    search_cont = ph_book.search_contact(**search_data)
    if exist:
        assert tst_cont_list == search_cont
    else:
        assert not search_cont

@pytest.fixture
def not_sorted_ph_book() -> Phone_book:
    test_contact = {'1':{'name': 'tester', 'phone':'+79999999999', 'comment': 'test_comm'}, 
                    '5':{'name': 'tester', 'phone':'+79999999999', 'comment': 'test_comm'},
                    '10':{'name': 'tester', 'phone':'+79999999999', 'comment': 'test_comm'},
                    '3':{'name': 'tester', 'phone':'+79999999999', 'comment': 'test_comm'},
                    }
    return Phone_book(test_contact)


def test_sort_cont(not_sorted_ph_book: Phone_book) -> None:
    """Тестирует сортировку ID контактов

    Args:
        not_sorted_ph_book (Phone_book): книга с несортированными контактами
    """
    ph_book = not_sorted_ph_book
    ph_book.sorted_contact_id()
    for enum, cont in enumerate(ph_book.contacts, 1):
        assert str(enum) == cont.id
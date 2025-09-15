import pytest
import json
from model import File_phone_book, StructureError

@pytest.fixture
def get_file_ph_book(gen_test_file:dict) -> 'File_phone_book':
    """Возвращает Объект класса File_phone_book, полученный на основе файла из gen_test_file

    Args:
        gen_test_file (dict): Словарь с путём до тестового файла и данными которые в него записаны {'path': 'путь', 'data': 'данные'}

    Returns:
        File_phone_book: Объект класса
    """
    obj = File_phone_book(gen_test_file['path'])
    return obj

def test_read(gen_test_file: dict, get_file_ph_book:'File_phone_book') -> None:
    """Тест для проверки чтения из файла через класс File_phone_book

    Args:
        gen_test_file (dict): Словарь с путём до файла и его содержимым 
        get_class_obj (File_phone_book): Объект класса File_phone_book
    """
    class_obj = get_file_ph_book
    tst_data = class_obj.read_file()
    assert tst_data == gen_test_file['data']

@pytest.mark.parametrize(
          'negative_data', 
          [
               '{,}',
               'string',
               '',
               '''{"1":{"name":"tester", "phone":"123", "comment":"tst comm",}}''',
               '[1 , 3]',

          ]
)
def test_read_negative(gen_test_file: dict, get_file_ph_book: 'File_phone_book', negative_data) -> None:
    """Тест для **негативной** проверки чтения из файла через класс File_phone_book

    Args:
        gen_test_file (dict): Словарь с путём до файла и его содержимым
        get_class_obj (File_phone_book): Объект класса File_phone_book
        negative_data (_type_): Негативные данные для записи в файл перед считыванием
    """
    cls_obj = get_file_ph_book
    path = gen_test_file['path']
    with open (path, 'w', encoding='UTF-8') as f:
        f.write(negative_data)
    with pytest.raises((json.JSONDecodeError,  StructureError)):
        cls_obj.read_file()

@pytest.mark.parametrize(
        'new_data',
        [
            {
                "100":{
                    'name': 'tester1',
                    "phone": "8-925-147-89-65",
                    'comment': 'This is комментарий'
                }
            },
            {
                '':{
                    '': '',
                    '': '',
                    '': ''
                }
            },
            {},
        ],
)
def test_write(gen_test_file:dict, get_file_ph_book: 'File_phone_book', new_data: dict) -> None:
    """Тест для проверки записи в файл через класс File_phone_book

    Args:
        gen_test_file (dict): Словарь с путём до файла и его содержимым
        get_class_obj (File_phone_book): Объект класса File_phone_book
        new_data (dict): Данные для записи в файл
    """
    get_file_ph_book.write_file(new_data)
    path = gen_test_file['path']
    with open (path, 'r', encoding='UTF-8') as f:
        data = json.load(f)
    assert data == new_data

def test_create_clear_file(get_file_ph_book:File_phone_book) -> None:
    """Тест для проверки безошибочного выполнения метода create_clear_file

    Args:
        get_class_obj (File_phone_book): Объект класса File_phone_book
    """
    obj = get_file_ph_book
    obj.create_clear_file()
    
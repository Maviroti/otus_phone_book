from model import Phone_book

import pytest
import json

@pytest.fixture
def gen_clear_file(tmp_path) -> str:
      path_f = tmp_path / "test_ph_book.json"
      open(path_f, 'a', encoding='utf-8').close()
      return str(path_f)

@pytest.fixture()
def gen_test_file(gen_clear_file: str) -> dict:
    """
    Фикстура для подготовки тестового файла телефонного справочника (.json) с тестовыми данными

    Returns:
        dict: Словарь с путём до тестового файла и его содержимым в формате словаря
    """
    path = gen_clear_file
    data = {
          "1":{
                "name": "Петя",
                "phone": "8-800-555-35-35",
                "comment": "Money в долг"
          },
          "2":{
                "name": "Vasya",
                "phone": "8-800-555-35-35",
                "comment": "No comments"
          },
          "3":{
                "name": "Иванов Иван Иванович",
                "phone": "911",
                "comment": ""
          },
          "4":{
                "name": "Pedro P.",
                "phone": "+74959999999",
                "comment": "Taxi Яндекс"
          },
    }
    with open (path, 'w', encoding='UTF-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    return {'path': path, 'data': data}


@pytest.fixture()
def tst_phone_book(request) -> Phone_book:
    """Возвращает объект класса Phone_book. Либо пустой, либо с тестовым контактом

    Args:
        request (_type_): True для получения пустого объекта, False для объекта с тестовым контактом

    Returns:
        Phone_book: объект класса
    """
    clear = request.param
    test_contact = {'1':{'name': 'tester', 'phone':'+79999999999', 'comment': 'test_comm'}}
    if clear:
        ph_book =  Phone_book({})
    else:
        ph_book = Phone_book(test_contact)
    return ph_book



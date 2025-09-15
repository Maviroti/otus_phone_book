from copy import deepcopy
from dataclasses import dataclass
import json
from config import path_to_phone_book


@dataclass
class Contact():
    id: str
    name: str
    phone: str
    comment: str

    @classmethod
    def from_dict(cls, data_dict:dict) -> 'Contact':
        """Создаёт контакт из словаря

        Args:
            data_dict (dict): словарь с данными контакта 

        Raises:
            ValueError: если структура словаря не соответствует контакту 

        Returns:
            Contact: объект класса
        """
        dict_keys = list(data_dict.keys())
        if len(dict_keys) != 1:
            raise ValueError('Некорректная структура словаря')
        id = dict_keys[0]
        value_dict = data_dict[id]
        return cls(id, value_dict['name'], value_dict['phone'], value_dict['comment'])

    def __str__(self) -> str:
        result = f'Контакт: {self.id}\n' + f'\tИмя: {self.name}\n' + f'\tТелефон: {self.phone}\n' + f'\tКомментарий: {self.comment}\n'
        return result
    
    def __repr__(self) -> str:
        return f'Contact(id = {self.id}, name = {self.name}, phone = {self.phone}, comment = {self.comment})'
    
    def to_dict(self) -> dict:
        return {self.id: {'name':self.name, 'phone':self.phone, 'comment':self.comment}}

class File_phone_book():
    def __init__(self, path : str = path_to_phone_book) -> None:
        self.path = path

    def read_file(self) -> dict:
        """Считывает данные из файла записной книжки и возвращает словарь с контактами

        Raises:
            StructureError: Если в json файле записан список, то метод выбросит исключение

        Returns:
            dict: Словарь с данными из файла
        """
        with open (self.path, 'r', encoding='UTF-8') as f:
            data_dict = json.load(f)
            if isinstance(data_dict, list):
                raise StructureError()
            return data_dict
    
    def write_file(self, data: dict) -> None:
        """Метод записывает данные в файл записной книжки

        Args:
            data (dict): Данные для записи в файл
        """
        with open (self.path, 'w', encoding='UTF-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def create_clear_file(self) -> None:
        """Метод создаёт пустой файл записной книжки
        """
        self.write_file({})

class Phone_book():
    _clear_change_log = {'new': [], 'change': [], 'del': []}

    def __init__(self, data: dict) -> None:
        """Класс для работы с телефонной книгой 

        Args:
            data (dict): Словарь с данными из телефонной книги
        """
        self.contacts:list[Contact] = []
        self.change_log = deepcopy(self._clear_change_log)

        for id in data.keys():
            self.contacts.append(Contact(id, data[id]['name'], data[id]['phone'], data[id]['comment'] ))

    def add_contact(self, contact: Contact) -> None:
        """Добавляет контакт в книгу

        Args:
            contact (Contact): контакт который надо добавить
        """
        self.contacts.append(contact)
        self.change_log['new'].append(contact)

    def get_new_id(self) -> str:
        """Возвращает новый ID для нового контакта

        Returns:
            str: строка с числовым ID
        """
        if self.contacts:
            cont_with_max_id = max(self.contacts, key=lambda contact: int(contact.id))
            return str(int(cont_with_max_id.id) + 1)
        return "1"

    def check_change_exist(self) -> bool:
        """Проверяет были ли внесены изменения в книгу

        Returns:
            bool: True - есть изменения, False - изменений нет
        """
        for key in self.change_log.keys():
            if self.change_log[key]:
                return True
        return False

    def save_change(self, file:'File_phone_book') -> None:
        """Записывает книгу в файл

        Args:
            file (File_phone_book): объект класса 
        """
        dict_contacts = {}
        for cont in self.contacts:
            dict_contacts = {**dict_contacts, **cont.to_dict()}
        file.write_file(dict_contacts)
        self.change_log = deepcopy(self._clear_change_log)

    def check_contact_exist_by_id(self, id: str) -> bool:
        """Проверяет есть ли контакт с таким ID

        Args:
            id (str): проверяемый ID

        Returns:
            bool: True - контакт есть, False - такого контакта нет
        """
        for cont in self.contacts:
            if cont.id == id:
                return True
        return False

    def get_contact_by_id(self, id:str) -> 'Contact|None':
        """Возвращает контакт по ID (если есть такой)

        Args:
            id (str): id контакта 

        Returns:
            Contact|None: объект класса Contact или None, контакта с таким ID нет
        """
        for cont in self.contacts:
            if cont.id == id:
                return cont

    def del_contact_by_id(self, id : str) -> None:
        """Удаляет контакт по его id

        Args:
            id (str): id контакта

        Raises:
            ContactNotExist: если контакта с таким id нет в базе
        """
        cont = self.get_contact_by_id(id)
        if cont is None:
            raise ContactNotExist(id)
        self.contacts.remove(cont)
        if cont in self.change_log['new']:
            self.change_log['new'].remove(cont)
        else:
            self.change_log['del'].append(cont)

    def edit_contacts(self, id: str, name: 'str|None'=None, phone:'str|None'= None, comment:'str|None'= None ) -> 'bool|None':
        """Вносит изменения в контакт 

        Args:
            id (str): ID контакта, который нужно отредактировать
            name (str|None, optional): новое имя. Defaults to None.
            phone (str|None, optional): новый телефон. Defaults to None.
            comment (str|None, optional): новый комментарий. Defaults to None.

        Returns:
            bool|None: вернёт None в случае успеха и False если не найдёт контакт
        """
        cont = self.get_contact_by_id(id)
        if cont is not None:
            in_new = False
            in_change = False
            if cont in self.change_log['new']: 
                self.change_log['new'].remove(cont)
                in_new = True
            if cont in self.change_log['change']: 
                self.change_log['change'].remove(cont)
                in_change = True
            if name is not None:
                cont.name = name
            if phone is not None:
                cont.phone = phone
            if comment is not None:
                cont.comment = comment
            if in_new:
                self.change_log['new'].append(cont)
            if in_change:
                self.change_log['change'].append(cont)
            if not in_change and not in_new:
                self.change_log['change'].append(cont)
        else:
            return False

    def search_contact(self, search_query: str, name:bool = False, phone:bool = False, comment:bool = False) -> list[Contact]:
        """Ищет контакты по заданному полю

        Args:
            search_query (str): поисковая последовательность
            name (bool, optional): поиск по именам. Defaults to False.
            phone (bool, optional): поиск по телефонам. Defaults to False.
            comment (bool, optional): поиск по комментариям. Defaults to False.

        Returns:
            list[Contact]: список контактов в которых содержится поисковая строка в выбранных полях
        """
        found_contacts = []
        if name:
            for cont in self.contacts:
                if search_query in cont.name and cont not in found_contacts:
                    found_contacts.append(cont)
        if phone:
            for cont in self.contacts:
                if search_query in cont.phone and cont not in found_contacts:
                    found_contacts.append(cont)
        if comment:
            for cont in self.contacts:
                if search_query in cont.comment and cont not in found_contacts:
                    found_contacts.append(cont)

        return found_contacts

    def sorted_contact_id(self) -> None:
        """В случае необходимости изменяет ID контактов таким образом, чтобы они шли по числовому порядку
        """
        for enum, cont in enumerate(self.contacts, 1):
            if cont.id != str(enum):
                in_new = False
                in_change = False
                if cont in self.change_log['new']: 
                    self.change_log['new'].remove(cont)
                    in_new = True
                if cont in self.change_log['change']: 
                    self.change_log['change'].remove(cont)
                    in_change = True
                cont.id = str(enum)
                if in_new:
                    self.change_log['new'].append(cont)
                if in_change:
                    self.change_log['change'].append(cont)
                if not in_change and not in_new:
                    self.change_log['change'].append(cont)
    
    def __str__(self) -> str:
        return str(self.contacts)

class PhBookErr(Exception):
    pass

class ContactNotExist(PhBookErr):
    def __init__(self, cont_id:str) -> None:
        super().__init__(f'Контакта с ID {cont_id} нет в книге!')


class FilePhBookErr(Exception):
    pass

class StructureError(FilePhBookErr): 
    def __init__(self) -> None:
        super().__init__(f'Нарушена структура внутри файла')
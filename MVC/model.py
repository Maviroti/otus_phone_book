from dataclasses import dataclass
import json
from config import path_to_phone_book


@dataclass
class Contact():
    id: str
    name: str
    phone: str
    comment: str

    def __str__(self) -> str:
        result = f'Контакт: {self.id}\n' + f'\tИмя: {self.name}\n' + f'\tТелефон: {self.phone}\n' + f'\tКомментарий: {self.comment}\n'
        return result
    
    def __repr__(self) -> str:
        return f'Contact(id = {self.id}, name = {self.name}, phone = {self.phone}, comment = {self.comment})'
    
    def to_dict(self) -> dict:
        return {self.id: {'name' : self.name, 'phone': self.phone, 'comment': self.comment}}





class File_phone_book():
    def __init__(self, path : str = path_to_phone_book):
        self.path = path

    def read_file(self) -> dict:
        with open (self.path, 'r', encoding='UTF-8') as f:
            return json.load(f)
        
    
    def write_file(self, data: dict):
        try:
            with open (self.path, 'w', encoding='UTF-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(e)
            exit(1)

    def create_clear_file(self):
        self.write_file({})


class Phone_book():

    _clear_change_log = {'new': [], 'change': [], 'del': []}

    def __init__(self, data: dict) -> None:
        self.contacts = []
        self.change_log = self._clear_change_log

        for id in data.keys():
            self.contacts.append(Contact(id, data[id]['name'], data[id]['phone'], data[id]['comment'] ))

    def add_contact(self, contact: Contact) -> None:
        self.contacts.append(contact)
        self.change_log['new'].append(contact)

    def view_contacts(self) -> None:
        for contact in self.contacts:
            print(contact)

    def get_new_id(self) -> str:
        if self.contacts:
            cont_with_max_id = max(self.contacts, key=lambda contact: int(contact.id))
            return str(int(cont_with_max_id.id) + 1)
        return "1"

    def check_change_exist(self) -> bool:
        for key in self.change_log.keys():
            if self.change_log[key]:
                return True
        return False

    def view_change(self):
        print('Список изменений.')
        if self.change_log['new']:
            print('Добавлены контакты:')
            for cont in self.change_log['new']: print(cont)
        if self.change_log['change']:
            print()
            print('Изменены контакты:')
            for cont in self.change_log['change']: print(cont)
        if self.change_log['del']:
            print()
            print('Удалены контакты:')
            for cont in self.change_log['del']: print(cont)

    def save_change(self, file : 'File_phone_book') -> None:
        dict_contacts = {}
        for cont in self.contacts:
            dict_contacts = {**dict_contacts, **cont.to_dict()}
        file.write_file(dict_contacts)
        self.change_log = self._clear_change_log

    def check_contact_exist_by_id(self, id: str) -> bool:
        for cont in self.contacts:
            if cont.id == id:
                return True
        return False

    def _get_contact_by_id(self, id:str) -> 'Contact|None':
        for cont in self.contacts:
            if cont.id == id:
                return cont

    def del_contact_by_id(self, id : str) -> None:
        cont = self._get_contact_by_id(id)
        self.contacts.remove(cont)
        if cont in self.change_log['new']:
            self.change_log['new'].remove(cont)
        else:
            self.change_log['del'].append(cont)

    def edit_contacts(self, id: str, name: 'str|None' =None, phone:'str|None' = None, comment:'str|None' = None ) -> 'bool|None':
        cont = self._get_contact_by_id(id)
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

    def view_contact_by_id(self, id: str) -> None:
        cont = self._get_contact_by_id(id)
        print(cont)

    def search_and_view_contact(self, search_query: str, name:bool = False, phone:bool = False, comment:bool = False) -> None:
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

        if found_contacts:
            print('Результат поиска:')
            for cont in found_contacts:
                print(cont)
        else:
            print('По данному запросу ничего не найдено!')

    def sorted_contact_id(self) -> None:
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
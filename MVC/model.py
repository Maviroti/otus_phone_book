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
    def __init__(self, data: dict) -> None:
        self.contacts = []

        for id in data.keys():
            self.contacts.append(Contact(id, data[id]['name'], data[id]['phone'], data[id]['comment'] ))
        # self.data = data

    # def clear_book(self) -> None:
    #     self.file.write_file({})

    def add_contact(self, contact: Contact) -> None:
        self.contacts.append(contact)

    def view_contact(self) -> None:
        for contact in self.contacts:
            print(contact)

    def get_new_id(self) -> str:
        if self.contacts:
            cont_with_max_id = max(self.contacts, key=lambda contact: int(contact.id))
            return str(int(cont_with_max_id.id) + 1)
        return "1"

    def __str__(self) -> str:
        return str(self.contacts)

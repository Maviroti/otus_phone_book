from dataclasses import dataclass
import json
from config import path_to_phone_book


@dataclass
class Contact():
    def __init__(self, id, name, phone, comment):
      self.id = id
      self.name = name
      self.phone = phone
      self.comment = comment

    def __str__(self):
        pass


class Phone_book():
    pass

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


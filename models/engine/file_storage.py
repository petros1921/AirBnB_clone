#!/usr/bin/python3

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

class_mapping = {
    "Amenity": Amenity,
    "BaseModel": BaseModel,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User
}


class FileStorage:
    file_path = "file.json"
    objects_dict = {}

    def get_all_objects(self):
        return self.objects_dict

    def add_new_object(self, obj):
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.objects_dict[key] = obj

    def save_to_file(self):
        json_objects = {}
        for key, obj in self.objects_dict.items():
            json_objects[key] = obj.to_dict()
        with open(self.file_path, 'w') as file:
            json.dump(json_objects, file)

    def reload_from_file(self):
        try:
            with open(self.file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.objects_dict[key] = classes[jo[key]["__class__"]](**jo[key])
        except:
            pass

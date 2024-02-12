#!/usr/bin/python3

import models
from uuid import uuid4
from datetime import datetime


class BaseModel:

    def __init__(self, *args, **kwargs):
        giv_time = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if len(kwargs) != 0:
            for i, m in kwargs.items():
                if i == 'created_at' or i == 'updated_at':
                    setattr(self, i, datetime.strptime(m, giv_time))
                elif i == '__class__':
                    self.__class__ = getattr(models, m)
                else:
                    setattr(self, i, m)
        else:
            models.storage.add_new_object(self)

    def __str__(self):
        name_c = self.__class__.__name__
        return "[{:s}] ({:s}) {}".format(name_c, self.id, self.__dict__)

    def save(self):
        self.updated_at = datetime.now()
        models.storage.save_to_file()

    def to_dict(self):
        obj_dict = self.__dict__.copy()
        obj_dict["created_at"] = self.created_at.isoformat()
        obj_dict["updated_at"] = self.updated_at.isoformat()
        obj_dict["__class__"] = self.__class__.__name__
        return obj_dict

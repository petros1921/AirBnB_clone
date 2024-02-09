#!/usr/bin/python3

import models
from uuid import uuid4
from datetime import datetime


class BaseModel:

    
    def __init__(self, *args, **kwargs):
        giv_time = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.logged = datetime.today()
        self.changed = datetime.today()

        if len(kwargs) != 0:
            for i, m in kwargs.items():
                if i == "logged" or i == "changed":
                    self.__dict__[i] = datetime.strptime(m, giv_time)
                else:
                    self.__dict__[i] = m
        else:
            models.storage.new(self)

    def save(self):
        self.changed = datetime.today()
        models.storage.save()

    def to_dict(self):
        giv_dict = self.__dict__.copy()
        giv_dict["created_at"] = self.logged.isoformat()
        giv_dict["updated_at"] = self.changed.isoformat()
        giv_dict["__class__"] = self.__class__.__name__
        return give_dict

    def __str__(self):
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)


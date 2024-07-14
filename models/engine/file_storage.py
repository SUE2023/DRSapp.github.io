#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
import models
import os
from models.base_model import BaseModel
from models.meetings import Meeting
from models.staff import Staff
from models.user import User
from models.boards import Board
from models.directors import Director

def classes():
    """Returns dictionary of class references"""
    return {
        "Meeting": Meeting,
        "BaseModel": BaseModel,
        "Staff": Staff,
        "User": User,
        "Board": Board,
        "Director": Director
    }

class FileStorage:
    """Serializes instances to a JSON file & deserializes back to instances"""

    # string - path to the JSON file
    __file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def __init__(self):
        pass

    def all(self, cls=None):
        """Returns the dictionary __objects"""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)"""
        json_objects = {key: obj.to_dict() for key, obj in self.__objects.items()}
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """Loads storage dictionary from file"""
        if os.path.exists(self.__file_path):
            with open(self.__file_path, 'r', encoding='utf-8') as my_file:
                object_dict = json.load(my_file)
                for id, dictionary in object_dict.items():
                    class_name = dictionary['__class__']
                    self.__objects[id] = classes()[class_name].from_dict(dictionary)

    def delete(self, obj=None):
        """Delete obj from __objects if it’s inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """Call reload() method for deserializing the JSON file to objects"""
        self.reload()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes().values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if value.id == id:
                return value

        return None

    def count(self, cls=None):
        """
        Count the number of objects in storage
        """
        if not cls:
            count = sum(len(models.storage.all(clas).values()) for clas in classes().values())
        else:
            count = len(models.storage.all(cls).values())

        return count
#!/usr/bin/python3
"""
Initializes the storage system and the classes
"""

from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
from os import getenv

import os
import models

storage_type = getenv('STORAGE_TYPE')

if storage_type == 'db':
    storage = DBStorage()
else:
    storage = FileStorage()

storage.reload()
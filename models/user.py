#!/usr/bin/python3
""" holds class User"""

import os
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import column_property, declarative_base, deferred, relationship
from typing import List

Base = declarative_base()

STORAGE_TYPE = os.environ.get('DRSapp_TYPE_STORAGE')

class User(BaseModel, Base if STORAGE_TYPE == "db" else object):
    """Representation of a user"""
    if STORAGE_TYPE == "db":
        __tablename__ = 'user'
        name = Column(String(128), nullable=False)
        department = Column(String(128), nullable=False)
        # Foreign key to staff
        staff_id = Column(String(60), ForeignKey('staff.id'), nullable=True)
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=False)
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        
    else:
        name = ""
        staff_id = ""
        director_id = ""
        description = ""
        department = []
        firstname_ids = []
        lastname_ids = []
        email_ids = []
        password_ids = []

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)

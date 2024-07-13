#!/usr/bin/python3
"""
Boards Class from Models Module
"""

import os
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import declarative_base
from typing import List

Base = declarative_base()

STORAGE_TYPE = os.environ.get('DRSapp_TYPE_STORAGE')

class Board(BaseModel, Base if STORAGE_TYPE == "db" else object):
    """Representation of a board"""
    if STORAGE_TYPE == "db":
        __tablename__ = 'boards'
        name = Column(String(128), nullable=False)
        area_id = Column(String(60), nullable=False)
        profession_id = Column(String(60), nullable=False)
        advice = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        # Foreign key to meetings
        meeting_id = Column(String(60), ForeignKey('meetings.id'), nullable=False)
        # Foreign key to directors (optional, if directors are involved in meetings)
        director_id = Column(String(60), ForeignKey('directors.id'), nullable=True)
    else:
        name = ""
        area_id = ""
        profession_id = ""
        advice = ""
        description = ""
        area_ids = []
        profession_ids = []
        advice_ids = []

    @property
    def area(self):
        """
        Getter for area list, i.e., area attribute of self
        """
        return self.area_ids if hasattr(self, 'area_ids') and self.area_ids else []

    @area.setter
    def area(self, area_obj):
        """
        Setter for area_ids
        """
        if not hasattr(self, 'area_ids'):
            self.area_ids = []
        if area_obj and area_obj.id not in self.area_ids:
            self.area_ids.append(area_obj.id)

    @property
    def profession(self):
        """
        Getter for profession list, i.e., profession attribute of self
        """
        return self.profession_ids if hasattr(self, 'profession_ids') and self.profession_ids else []

    @profession.setter
    def profession(self, profession_obj):
        """
        Setter for profession_ids
        """
        if not hasattr(self, 'profession_ids'):
            self.profession_ids = []
        if profession_obj and profession_obj.id not in self.profession_ids:
            self.profession_ids.append(profession_obj.id)

    @property
    def advice(self):
        """
        Getter for advice list, i.e., advice attribute of self
        """
        return self.advice_ids if hasattr(self, 'advice_ids') and self.advice_ids else []

    @advice.setter
    def advice(self, advice_obj):
        """
        Setter for advice_ids
        """
        if not hasattr(self, 'advice_ids'):
            self.advice_ids = []
        if advice_obj and advice_obj.id not in self.advice_ids:
            self.advice_ids.append(advice_obj.id)
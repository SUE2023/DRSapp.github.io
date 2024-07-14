#!/usr/bin/python3
"""
Directors Class from Models Module
"""

import os
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import column_property, declarative_base, deferred, relationship
from typing import List

Base = declarative_base()

STORAGE_TYPE = os.environ.get('DRSapp_TYPE_STORAGE')

class Director(BaseModel, Base if STORAGE_TYPE == "db" else object):
    """Representation of a director"""
    if STORAGE_TYPE == "db":
        __tablename__ = 'directors'
        name = Column(String(128), nullable=False)
        departmental = Column(String(128), nullable=False)
        strategic = Column(String(60), nullable=False)
        board = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        # Foreign key to meetings
        meetings_id = Column(String(60), ForeignKey('meetings.id'), nullable=False)
        # Foreign key to staff
        staff_id = Column(String(60), ForeignKey('staff.id'), nullable=True)
    else:
        name = ""
        departmental_id = ""
        strategic_id = ""
        board_id = ""
        description = ""
        department_ids = []
        strategic_id = []
        board_id = []

    @property
    def departmental(self):
        """
        getter for departmentals list, i.e. departmentals attribute of self
        """
        return self.departmental_ids if hasattr(self, 'departmental_ids') and self.departmental_ids else None

    @departmental.setter
    def departmental(self, departmental_obj):
        """
        setter for departmental_ids
        """
        if hasattr(self, 'departmental_ids') and departmental_obj and departmental_obj.id not in self.departmental_ids:
            self.departmental_ids.append(departmental_obj.id)

    @property
    def strategic(self):
        """
        getter for strategic list, i.e. strategic attribute of self
        """
        return self.strategic_ids if hasattr(self, 'strategic_ids') and self.strategic_ids else None

    @strategic.setter
    def strategic(self, strategic_obj):
        """
        setter for strategic_ids
        """
        if hasattr(self, 'strategic_ids') and strategic_obj and strategic_obj.id not in self.strategic_ids:
            self.strategic_ids.append(strategic_obj.id)

    @property
    def board(self):
        """
        getter for board list, i.e. board attribute of self
        """
        return self.board_ids if hasattr(self, 'board_ids') and self.board_ids else None

    @board.setter
    def board(self, board_obj):
        """
        setter for board_ids
        """
        if hasattr(self, 'board_ids') and board_obj and board_obj.id not in self.board_ids:
            self.board_ids.append(board_obj.id)

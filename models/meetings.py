#!/usr/bin/python3
""" holds class Meeting"""

import os
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import column_property, declarative_base, deferred, relationship
from typing import List

Base = declarative_base()

STORAGE_TYPE = os.environ.get('DRSapp_TYPE_STORAGE')

class Meeting(BaseModel, Base if STORAGE_TYPE == "db" else object):
    """Representation of a meeting"""
    if STORAGE_TYPE == "db":
        __tablename__ = 'meetings'
        name = Column(String(128), nullable=False)
        # Foreign key to staff
        staff_id = Column(String(60), ForeignKey('staff.id'), nullable=False)
        # Foreign key to directors (optional, if directors are involved in meetings)
        director_id = Column(String(60), ForeignKey('directors.id'), nullable=True)
    else:
        name = ""
        staff_id = ""
        director_id = ""
        description = ""
        department_ids = []
        decision_ids = []
        level_ids = []

    @property
    def department(self) -> List[str]:
        """
        Getter for departments list, i.e., departments attribute of self
        """
        return self.department_ids if hasattr(self, 'department_ids') and self.department_ids else []

    @department.setter
    def department(self, department_obj):
        """
        Setter for department_ids
        """
        if not hasattr(self, 'department_ids'):
            self.department_ids = []
        if department_obj and department_obj.id not in self.department_ids:
            self.department_ids.append(department_obj.id)

    @property
    def decisions(self) -> List[str]:
        """
        Getter for decisions list, i.e., decisions attribute of self
        """
        return self.decision_ids if hasattr(self, 'decision_ids') and self.decision_ids else []

    @decisions.setter
    def decisions(self, decision_obj):
        """
        Setter for decision_ids
        """
        if not hasattr(self, 'decision_ids'):
            self.decision_ids = []
        if decision_obj and decision_obj.id not in self.decision_ids:
            self.decision_ids.append(decision_obj.id)

    @property
    def level(self) -> List[str]:
        """
        Getter for levels list, i.e., levels attribute of self
        """
        return self.level_ids if hasattr(self, 'level_ids') and self.level_ids else []

    @level.setter
    def level(self, level_obj):
        """
        Setter for level_ids
        """
        if not hasattr(self, 'level_ids'):
            self.level_ids = []
        if level_obj and level_obj.id not in self.level_ids:
            self.level_ids.append(level_obj.id)

    @property
    def staff(self) -> str:
        """
        Getter for staff_id, i.e., staff_id attribute of self
        """
        return self.staff_id if hasattr(self, 'staff_id') and self.staff_id else ""

    @staff.setter
    def staff(self, staff_obj):
        """
        Setter for staff_id
        """
        if staff_obj:
            self.staff_id = staff_obj.id
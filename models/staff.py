#!/usr/bin/python3
""" holds class Staff"""

import os
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import column_property, declarative_base, deferred, relationship
from typing import List

Base = declarative_base()

STORAGE_TYPE = os.environ.get('DRSapp_TYPE_STORAGE')

class Staff(BaseModel, Base if STORAGE_TYPE == "db" else object):
    """Representation of a staff"""
    if STORAGE_TYPE == "db":
        __tablename__ = 'staff'
        name = Column(String(128), nullable=False)
        staffnumber = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        reports = Column(String(str), nullable=True)
        # Foreign key to meetings
        meetings_id = Column(String(60), ForeignKey('meetings.id'), nullable=False)
        # Foreign key to directors (optional, if directors are involved in meetings)
        director_id = Column(String(60), ForeignKey('directors.id'), nullable=True)
    else:
        name = ""
        staff_id = ""
        director_id = ""
        description = ""
        reports_ids = []

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)


    @property
    def reports(self) -> List[str]:
        """
        Getter for reports list, i.e., reports attribute of self
        """
        return self.reports_ids if hasattr(self, 'reports_ids') and self.reports_ids else []

    @reports.setter
    def reports(self, reports_obj):
        """
        Setter for reports_ids
        """
        if not hasattr(self, 'reports_ids'):
            self.reports_ids = []
        if reports_obj and reports_obj.id not in self.reports_ids:
            self.reports_ids.append(reports_obj.id)
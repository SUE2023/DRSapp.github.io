#!/usr/bin/python3
""" Blueprint for API """
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.directors import *
from api.v1.views.boards import *
from api.v1.views.meetings import *
from api.v1.views.staff import *
from api.v1.views.user import *


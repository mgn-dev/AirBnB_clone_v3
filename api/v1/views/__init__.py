#!/usr/bin/python3
"""Package initializer"""

from flask import Blueprint

# Create an instance of Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Wildcard import everything in the package api.v1.views.index
from api.v1.views.index import *

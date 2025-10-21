from flask import Blueprint

users_bp = Blueprint("users", __name__)

from . import users_put
from . import users_get
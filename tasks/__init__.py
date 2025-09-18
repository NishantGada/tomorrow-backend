from flask import Blueprint

tasks_bp = Blueprint("tasks", __name__)

from . import tasks_post
from . import tasks_get
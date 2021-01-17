from flask import Blueprint

admin_blue = Blueprint('admin', __name__)

from admin import auth
from admin import tec
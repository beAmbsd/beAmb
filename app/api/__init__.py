from flask import Blueprint

from app.core import errors


bp_api = Blueprint('api', __name__, url_prefix='/api/v0.1')

from app.api import users, tokens, api_info

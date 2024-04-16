from flask import Blueprint


bp_api = Blueprint('api', __name__, url_prefix='/api/v0.1')

from app.api import users, errors, tokens, api_info

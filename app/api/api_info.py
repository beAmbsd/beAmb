from http import HTTPStatus
from flask import jsonify, url_for
from app.api import bp_api


@bp_api.route('/', methods=['GET'])
def show_version():
    return jsonify(status=HTTPStatus.OK,
                   version='0.1',
                   url_page=url_for('api.show_version'))

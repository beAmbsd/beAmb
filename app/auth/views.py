from typing import Type
from http import HTTPStatus
from flask import request, jsonify
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
from app.extensions.db import Session
from app.models import User
from app.auth import bp_auth



class UserRegister(MethodView):

    @staticmethod
    def _get_user(id: int, orm_model: Type[User], session=Session):
        """ Get user from DB if exist. """
        with Session() as session:
            user = session.get(User, id)
        if not user:
            return HTTPStatus.NOT_FOUND
        return user

    def get(self, user_id):
        user = self._get_user(user_id, User, Session)
        if user:
            return jsonify(status=HTTPStatus.OK)
        else:
            return jsonify(status=HTTPStatus.NOT_FOUND)

    def post(self):
        data = request.get_json(force=True)
        error = []

        if not data:
            error.append('Credentials is required.')
        else:
            with Session() as conn:
                try:
                    new_user = User(name=data.get('name'),
                                    password=data.get('password'),
                                    email=data.get('email'))
                    conn.add(new_user)
                    conn.commit()
                    return jsonify(status=HTTPStatus.CREATED,
                                   message=f'User {new_user.name.capitalize()} created.')

                except IntegrityError:
                    conn.rollback()
                    error.append("User is already registered.")
                    return jsonify(status=HTTPStatus.BAD_REQUEST,
                                   message=", ".join(error))

        return jsonify(status=HTTPStatus.BAD_REQUEST,
                       message=", ".join(error))

    def __repr__(self) -> str:
        return f'{self.model}: {self.model.name.capitalize()}'
    

bp_auth.add_url_rule(rule='/register',
                     view_func=UserRegister.as_view('register'),
                     methods=['GET', 'POST'])
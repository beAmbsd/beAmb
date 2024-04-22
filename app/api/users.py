from typing import Type, Optional
from http import HTTPStatus
from werkzeug.security import generate_password_hash
from flask import request, jsonify
from flask.views import MethodView
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.db import Session
from app.models import User
from app.api import bp_api
from app.core.validators import UserValidator
from app.core.service import create_hash


class UserRegister(MethodView):

    @staticmethod
    def _get_user(id: int, orm_model: Type[User], session=Session):
        """ Get user from DB if exist. """
        with Session() as session:
            user = session.get(User, id)
        if not user:
            return HTTPStatus.NOT_FOUND
        return user

    def get(self, user_id: int):
        try:
            user = self._get_user(user_id, User, Session)
            if user: 
                user_data = {
                    'id': user.id,
                    'name': user.name.capitalize(),
                    'email': user.email,
                    'registered': user.registered
                    }
                return jsonify(status=HTTPStatus.OK,
                            user=user_data)
        except AttributeError as er:
            return jsonify(status=HTTPStatus.NOT_FOUND,
                           message='User is not found or not set')

    def post(self):
        data = request.get_json(force=True)
        new_user = UserValidator(
                data.get('name'),
                data.get('email'),
                data.get('password')
                ).to_dict()
        hs_pswd = generate_password_hash(
            password=data.get('password'),
            method='scrypt:32768:8:1',
            salt_length=20
        )
        new_user['password'] = hs_pswd
        return self.add_user(data=new_user)

    def email_is_exist(self, data: str, session=Session) -> Optional[dict]:
        with session() as conn:
            stmt = select(User).filter(User.email == data.get('email'))
            email_exists = conn.scalar(stmt)
        if email_exists is not None:
            return jsonify(
                status=HTTPStatus.BAD_REQUEST,
                message='A user with the same email already exists.'
                )
        else:
            return data

    def add_user(self, data: dict):
        with Session() as conn:
            try:
                new_user = User(**data)
                conn.add(new_user)
                conn.commit()
                return jsonify(
                    status=HTTPStatus.CREATED,
                    message=f'User {new_user.name.capitalize()} created.'
                    )

            except IntegrityError as ie:
                conn.rollback()
                return jsonify(status=HTTPStatus.BAD_REQUEST,
                                error=ie.detail)

    def __repr__(self) -> str:
        return f'{self.model}: {self.model.name.capitalize()}'


# url's for apiviews
bp_api.add_url_rule(rule='/user/<int:user_id>',
                     view_func=UserRegister.as_view('manage'),
                     methods=['GET', 'PATCH', 'DELETE'])
bp_api.add_url_rule(rule='/register',
                     view_func=UserRegister.as_view('register'),
                     methods=['POST'])

from typing import Type
from http import HTTPStatus
from flask import request, jsonify, g
from flask.views import MethodView
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.db import Session, engine
from app.models import User
from app.api import bp_api



class UserRegister(MethodView):

    @staticmethod
    def _get_user(id: int, orm_model: Type[User], session=Session):
        """ Get user from DB if exist. """
        with Session() as session:
            user = session.get(User, id)
        if not user:
            return HTTPStatus.NOT_FOUND
        return user

    def get(self):
        try:
            user_id = int(request.args.get('user_id'))
            user = self._get_user(user_id, User, Session)
            print(user)
            if user: 
                user_data = {'id': user.id,
                        'name': user.name.capitalize(),
                        'email': user.email,
                        'registered': user.registered}
                return jsonify(status=HTTPStatus.OK,
                            user=user_data)
        except AttributeError as er:
            return jsonify(status=HTTPStatus.NOT_FOUND,
                           message='User is not found or not set')

    def post(self):
        data = request.get_json(force=True)

        if not data:
            if user := (select(User).where(User.email == data.get('email'))):
                return jsonify(
                    status=HTTPStatus.BAD_REQUEST,
                    message='A user with the same name already exists.'
                    )
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
                except IntegrityError as ie:
                    conn.rollback()
                    return jsonify(status=HTTPStatus.BAD_REQUEST,
                                   error=ie.detail)
        return jsonify(status=HTTPStatus.BAD_REQUEST)
                


    def __repr__(self) -> str:
        return f'{self.model}: {self.model.name.capitalize()}'


# url's for apiviews
bp_api.add_url_rule(rule='/register/<user_id:int>',
                     view_func=UserRegister.as_view('register'),
                     methods=['GET'])
bp_api.add_url_rule(rule='/register/<user_id:int>',
                     view_func=UserRegister.as_view('register'),
                     methods=['POST'])

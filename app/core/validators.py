from abc import ABC, abstractmethod
import re
from typing import List
from python_usernames import is_safe_username


class Validator(ABC):

    def __set_name__(self, owner, name):
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.private_name, value)

    @abstractmethod
    def validate(self, value):
        if not value:
            raise TypeError('Entered the empty value.')


class UsernameValidator(Validator):

    def __init__(self, minlen: int=None, maxlen: int=None) -> None:
        self.minlen = minlen
        self.maxlen = maxlen

    def validate(self, value):
        if self.minlen is not None and len(value) < self.minlen:
            raise ValueError('Name too short.')
        if self.maxlen is not None and len(value) > self.maxlen:
            raise ValueError('Name too long.')
        if not is_safe_username(value):
            raise ValueError('Username is not valid')


class EmailValidator(Validator):
    """
    Checking the validity of the specified email address.
    A valid value is checked using a regular expression.

    : params maxlen : int maximum line length
    : params minlen : int minimum line length

    """

    def __init__(self, minlen: int=None, maxlen: int=None) -> None:
        self.minlen = minlen
        self.maxlen = maxlen
        self.email_pattern = r'^\w$'

    def validate(self, value):
        if self.minlen is not None and len(value.split('@')[0]) < self.minlen:
            raise ValueError('Name too short.')
        if self.maxlen is not None and len(value.split('@')[0]) > self.maxlen:
            raise ValueError('Name too long.')
        # if not re.match(self.email_pattern, value.strip()):
        #     raise ValueError('Email is not valid.')

    
class PasswordValidator(Validator):

    def __init__(self, minlen: int=5, maxlen: int=None) -> None:
        self.minlen = minlen
        self.maxlen = maxlen

    def validate(self, value):
        if self.minlen is not None and len(value) < self.minlen:
            raise ValueError('Password too short')
        if self.maxlen is not None and len(value) > self.maxlen:
            raise ValueError('name too long')
        

class UserValidator:

    name = UsernameValidator(minlen=5, maxlen=21)
    email = EmailValidator(minlen=3, maxlen=21)
    password = PasswordValidator(maxlen=128)

    def __init__(self, name: str, email: str,
                 password: str) -> None:
        self.name = name
        self.email = email
        self.password = password

    def to_dict(self) -> dict[str, str]:
        """
        The data received from the user 
        will be returned in the form of a dictionary.
        """
        return {'name': self.name,
                'email': self.email,
                'password': self.password}
        

    def __repr__(self) -> str:
        return "Username: {}\nEmail: {}\nPassword: {}".format(
            self.name, self.email, self.password
            )

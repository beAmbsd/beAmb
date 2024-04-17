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
        self.email_pattern = r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$'

    def validate(self, value):
        if self.minlen is not None and len(value.split('@')[0]) < self.minlen:
            raise ValueError('Name too short.')
        if self.maxlen is not None and len(value.split('@')[0]) > self.maxlen:
            raise ValueError('Name too long.')
        if not re.match(self.email_pattern, value.strip()):
            raise ValueError('Email is not valid.')

    
class PasswordValidator(Validator):

    def __init__(self, forbidden_chars: List[str],
                 minlen: int=5, maxlen: int=None) -> None:
        self.minlen = minlen
        self.maxlen = maxlen
        self.forbidden_chars = ['(', ')', '\\', '\n', '\`']

    def validate(self, value):
        if self.minlen is not None and len(value) < self.minlen:
            raise ValueError('Password too short')
        if self.maxlen is not None and len(value) > self.maxlen:
            raise ValueError('name too long')
        if self.forbidden_chars in value:
            raise TypeError('Forbidden chars!')
        

class UserValidator:

    name = UsernameValidator(minlen=5, maxlen=21)
    email = EmailValidator(minlen=3, maxlen=21)
    password = PasswordValidator(maxlen=128)

    def __init__(self, name: str, email: str,
                 password: str) -> None:
        self.name = name
        self.email = email
        self.password = password


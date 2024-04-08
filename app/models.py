from datetime import datetime
from werkzeug.security import generate_password_hash
from sqlalchemy import MetaData, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_login import UserMixin


class Base(DeclarativeBase):
    metadata = MetaData()


class User(Base, UserMixin):
    """ User model. """
    def __init__(self, name, password, email):
        self.name: str = name
        self._password: str = password
        self.email: str = email

    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(256), nullable=False)
    email: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    registered: Mapped[datetime] = mapped_column(
        default=datetime.now
        )

    @property
    def password_hash(self, paswd):
        self._password = generate_password_hash(password=paswd,
                                                method='pbkdf2',
                                                salt_length=16)

    def __repr__(self):
        return f'User {self.name}'

    def get_id(self):
        return self.id

from datetime import datetime
from sqlalchemy import MetaData, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    metadata = MetaData()


class User(Base):
    """ User model. """
    def __init__(self, name, password, email):
        self.name: str = name
        self.password_hash: str = password
        self.email: str = email

    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    email: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    registered: Mapped[datetime] = mapped_column(
        default=datetime.now
        )

    def __repr__(self):
        return f'User {self.name}'
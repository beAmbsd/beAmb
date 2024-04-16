from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.config import config_by_name


def url_object(config_type: str = 'dev') -> str:
        URI = config_by_name[config_type].SQLALCHEMY_DATABASE_URI
        return URI

engine = create_engine(url_object('dev'))
Session = sessionmaker(bind=engine)
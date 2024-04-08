from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import config_by_name


def url_object(config_type: str | None, default='dev'):
    (URI := config_by_name[config_type].SQLALCHEMY_DATABASE_URI) \
        if config_type else default
    return URI


engine = create_engine(url_object('dev'),  # echo=True,
                       isolation_level="READ COMMITTED",
                       max_overflow=5,
                       pool_size=1,
                       pool_reset_on_return="rollback")
Session = sessionmaker(bind=engine,
                       autoflush=False)

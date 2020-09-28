from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base, Config as __Config
import os

class Db:

    def __init__(self):
        __engine = create_engine(os.getenv('POSTGRES_URI'))
        self.__Session = sessionmaker(bind=__engine)

    @property
    def session(self):
        session = self.__Session()
        return session


def startup():
    __engine = create_engine(os.getenv('POSTGRES_URI'))
    Base.metadata.bind = __engine
    Base.metadata.create_all(__engine)
    session = sessionmaker(bind=__engine)()

    current_values = [c.key for c in __Config.get(session)]
    default = {'prefix': '.'}
    for key in list(default.keys()):
        if key not in current_values:
            session.add(__Config(key=key, value=default[key]))
    session.commit()

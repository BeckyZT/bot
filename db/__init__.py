from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base, Config
import os

class Db:

    def __init__(self):
        self.__engine = create_engine(os.getenv('POSTGRES_URI'))
        self.__Session = sessionmaker(bind=self.__engine)

    @property
    def session(self):
        session = self.__Session()
        return session

    def startup(self,):
        Base.metadata.bind = self.__engine
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine)()

        current_values = [c.key for c in Config.get(session)]
        default = {'prefix': '.'}
        for key in list(default.keys()):
            if key not in current_values:
                session.add(Config(key=key, value=default[key]))
        session.commit()
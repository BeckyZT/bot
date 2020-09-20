from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base, Server,RoomCode


class Db():

    def __init__(self):
        self.__setup()

    def __setup(self):
        __engine = create_engine('sqlite:///database.sqlite')
        Base.metadata.bind = __engine
        Base.metadata.create_all(__engine)

        self.__Session = sessionmaker(bind=__engine)

    @property
    def session(self):
        session = self.__Session()
        session.execute('PRAGMA foreign_keys = ON')
        return session

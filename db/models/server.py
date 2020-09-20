from sqlalchemy import Column, String, BigInteger
from sqlalchemy.orm import relationship

from .base import Base


class Server(Base):
    __tablename__ = 'server'

    id = Column(BigInteger,primary_key=True)
    prefix = Column(String,server_default='.!')

    @classmethod
    def get_prefix(cls,session,id):
        return session.query(cls).filter_by(id=id).all()

    @classmethod
    def get_by_id(cls,session,id):
        return session.query(cls).filter_by(id=id).first()
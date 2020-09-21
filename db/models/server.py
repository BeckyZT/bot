from sqlalchemy import Column, String, BigInteger

from .base import Base


class Server(Base):
	__tablename__ = 'server'

	id = Column(BigInteger, primary_key=True)
	prefix = Column(String, server_default='.!')

	@classmethod
	def get_prefix(cls, session, id):
		return session.query(cls.prefix).filter_by(id=id).scalar()

	@classmethod
	def get_by_id(cls, session, id):
		return session.query(cls).filter_by(id=id).scalar()

	@classmethod
	def update_prefix_by_id(cls, session, id, prefix):
		session.query(cls).filter_by(id=id).update({cls.prefix: prefix})
		session.commit()

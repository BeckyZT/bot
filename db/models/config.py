from sqlalchemy import Column, String, Integer

from .base import Base


class Config(Base):
	__tablename__ = 'config'

	id = Column(Integer, primary_key=True)
	key = Column(String, nullable=False)
	value = Column(String, nullable=False)

	@classmethod
	def get(cls, session, key=None):
		if key is None:
			return session.query(cls.key).all()
		return session.query(cls).filter(cls.key == key).scalar()

	@classmethod
	def update(cls, session, key, value):
		session.query(cls).filter(key == key).update({cls.value: value})
		session.commit()

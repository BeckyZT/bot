from sqlalchemy import Column, BigInteger, String, ForeignKey

from .base import Base


class RoomCode(Base):
	__tablename__ = 'room_code'
	server_id = Column(BigInteger, ForeignKey('server.id', ondelete='CASCADE'), primary_key=True)

	code = Column(String)

	@classmethod
	def get_code(cls, session, server_id):
		return session.query(cls).filter_by(server_id=server_id).first()

	@classmethod
	def update_code_by_server_id(cls, session, server_id, code):
		session.query(cls).filter_by(server_id=server_id).update({cls.code: code})
		session.commit()

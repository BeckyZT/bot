from sqlalchemy import Column, BigInteger, String, ForeignKey

from .base import Base


class RoomCode(Base):
	__tablename__ = 'room_code'
	room_id = Column(BigInteger, primary_key=True,autoincrement=True)
	code = Column(String)

	@classmethod
	def add_code(cls,session,room_id,code):
		room_code = RoomCode(room_id=room_id,code=code)
		session.add(room_code)
		session.commit()

	@classmethod
	def get_code(cls, session, room_id):
		return session.query(cls).filter(cls.room_id == room_id).scalar()

	@classmethod
	def update_code(cls, session, room_id, code):
		session.query(cls).filter(cls.room_id == room_id).update({cls.code: code})
		session.commit()

	@classmethod
	def delete(cls, session, room_code):
		session.delete(room_code)
		session.commit()

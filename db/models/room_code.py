from sqlalchemy import Column, BigInteger, String, ForeignKey

from .base import Base


class RoomCode(Base):
	__tablename__ = 'room_code'
	room_id = Column(BigInteger, primary_key=True,autoincrement=True)
	code = Column(String)
	region = Column(String)

	@classmethod
	def add_code(cls,session,room_id,code,region):
		room_code = RoomCode(room_id=room_id, code=code, region=region)
		session.add(room_code)
		session.commit()

	@classmethod
	def get_code(cls, session, room_id):
		return session.query(cls).filter(cls.room_id == room_id).scalar()

	@classmethod
	def update_code(cls, session, room_id, code,region):
		update_values= {
			cls.code: code,
			cls.region: region
		}

		session.query(cls).filter(cls.room_id == room_id).update(update_values)
		session.commit()

	@classmethod
	def delete(cls, session, room_code):
		session.delete(room_code)
		session.commit()

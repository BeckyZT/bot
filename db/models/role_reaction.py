from sqlalchemy import String, Column, BigInteger, ForeignKey, Boolean

from .base import Base


class RoleReaction(Base):
	__tablename__ = 'role_reaction'

	channel_id = Column(BigInteger, primary_key=True)
	message_id = Column(BigInteger, primary_key=True)
	emoji = Column(String, primary_key=True)
	role_id = Column(BigInteger, primary_key=True)

	@classmethod
	def get(cls, session, channel_id, message_id, emoji=None, role_id=None):
		criteria = [
			cls.channel_id == channel_id,
			cls.message_id == message_id
		]

		if emoji is not None:
			criteria.append(cls.emoji == emoji)

		if role_id is not None:
			criteria.append(cls.role_id == role_id)

		return session.query(cls).filter(*criteria).all()
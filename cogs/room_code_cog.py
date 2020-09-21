from discord.ext import commands

from db import Db, RoomCode


class RoomCodeCog(commands.Cog, name='Room Code'):

	def __init__(self, bot):
		self.bot = bot
		self.session = Db().session

	@commands.command()
	async def setcode(self, ctx, code):
		code = code.upper()
		room_code = RoomCode.get_code(self.session, ctx.guild.id)
		if room_code is None:
			room_code = RoomCode(server_id=ctx.guild.id, code=code)
			self.session.add(room_code)
			self.session.commit()
			await ctx.send(f'Código definido para {room_code.code}')
		elif room_code.code == code:
			await ctx.send("Código solicitado é igual ao anterior")
		else:
			RoomCode.update_code_by_server_id(self.session, room_code.server_id, code)
			await ctx.send(f'Código definido para {room_code.code}')

	@commands.command()
	async def code(self, ctx):
		room_code = RoomCode.get_code(self.session, ctx.guild.id)
		if room_code is None:
			await ctx.send('Nenhum código definido')
		else:
			await ctx.send(f'O código é {room_code.code}')

	@commands.command()
	async def clearcode(self, ctx):
		room_code = RoomCode.get_code(self.session, ctx.guild.id)
		if room_code is None:
			await ctx.send('Não há código para redefinir')
		else:
			self.session.delete(room_code)
			self.session.commit()
			await ctx.send('Código redefinido')


def setup(bot):
	bot.add_cog(RoomCodeCog(bot))

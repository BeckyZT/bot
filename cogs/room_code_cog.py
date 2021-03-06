from discord.ext import commands
from unidecode import unidecode
from db.models import RoomCode


class RoomCodeCog(commands.Cog, name='Room Code'):

	def __init__(self, bot, session):
		self.bot = bot
		self.session = session

	@commands.command()
	async def setcode(self, ctx, code,region):
		code = unidecode(code.upper())
		if not code.isalnum():
			await ctx.send('O código deve conter apenas letras e números')
			return

		if len(code) < 4 or len(code) > 6:
			await ctx.send("O código deve conter de 4 a 6 caracteres")
			return

		region = region.upper()
		valid_regions = ['NA', 'AS', 'EU']

		if ctx.author.voice is None:
			await ctx.send("Conecte-se a um chat para que possa alterar o código")
		else:
			if region not in valid_regions:
				await ctx.send(f"Regiões inválidas, deve ser uma dessas: `{', '.join(valid_regions)}`")
				return

			room_code = RoomCode.get_code(self.session, ctx.author.voice.channel.id)

			if room_code is None:
				RoomCode.add_code(self.session,ctx.author.voice.channel.id, code,region)
			else:
				RoomCode.update_code(self.session,ctx.author.voice.channel.id, code,region)

			await ctx.send(f'Código `{code}` definido na região `{region}`')

	@setcode.error
	async def setcode_error(self,ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('O formato deve ser: `.setcode <sala> <região>`')
		else:
			raise error

	@commands.command()
	async def code(self, ctx):
		if ctx.author.voice is None:
			await ctx.send("Conecte-se a um chat para que eu envie o código")
		else:
			room_code = RoomCode.get_code(self.session, ctx.author.voice.channel.id)
			if room_code is None:
				await ctx.send('Não há códigos definidos')
			else:
				await ctx.send(f'O código é: `{room_code.code}` na região `{room_code.region}`')

	@commands.command()
	async def clearcode(self, ctx):
		if ctx.author.voice is None:
			await ctx.send("Conecte-se a um chat para que eu redefina o código")
		else:
			room_code = RoomCode.get_code(self.session, ctx.author.voice.channel.id)
			if room_code is None:
				await ctx.send('Não há código para redefinir')
			else:
				RoomCode.delete(self.session,room_code)
				await ctx.send('Código redefinido')

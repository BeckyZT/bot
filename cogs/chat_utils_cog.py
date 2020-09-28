from discord.ext import commands
from unidecode import unidecode


class ChatUtilsCog(commands.Cog, name='Chat Utils'):

	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):
		text = unidecode(message.content.lower())
		distract = ['distrai', 'distraido']

		if any(d for d in distract if d in text):
			await message.channel.send('<a:distract:757381529478496346>')

	@commands.command()
	async def pong(self, ctx):
		await ctx.send('Ué')

	@commands.command()
	async def ping(self, ctx):
		await ctx.send('Pong :ping_pong:')

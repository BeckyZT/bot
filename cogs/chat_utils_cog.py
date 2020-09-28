from discord.ext import commands
from unidecode import unidecode


class ChatUtilsCog(commands.Cog, name='Chat Utils'):

	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author==self.bot.user:
			return
		text = unidecode(message.content.lower())

		if "distrai" in text:
			await message.channel.send('<a:distract:760176755780223017>')
		elif any([text.startswith(txt) for txt in ['oi', 'eae', 'ola']]):
			if self.bot.user in message.mentions:
				await message.channel.send('Oii')

	@commands.command()
	async def pong(self, ctx):
		await ctx.send('Ué')

	@commands.command()
	async def ping(self, ctx):
		await ctx.send('Pong :ping_pong:')

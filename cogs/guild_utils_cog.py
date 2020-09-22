from discord.ext import commands

from db import Db, Config


class GuildUtilsCog(commands.Cog, name='Guild Utils'):

	def __init__(self, bot):
		self.bot = bot
		self.session = Db().session

	@commands.command()
	async def prefix(self, ctx, prefix):
		Config.update(self.session,'prefix', prefix)
		await ctx.send(f'Prefixo alterado para `{prefix}`')


def setup(bot):
	bot.add_cog(GuildUtilsCog(bot))

from discord.ext import commands

from db import Db, Server


class GuildUtilsCog(commands.Cog, name='Guild Utils'):

	def __init__(self, bot):
		self.bot = bot
		self.session = Db().session

	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		server = Server(id=guild.id)
		self.session.add(server)
		self.session.commit()

	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
		server = Server.get_by_id(self.session, guild.id)
		self.session.delete(server)
		self.session.commit()

	@commands.command()
	async def prefix(self, ctx, prefix):
		Server.update_prefix_by_id(self.session, ctx.guild.id, prefix)
		await ctx.send(f'Prefixo alterado para `{prefix}`')


def setup(bot):
	bot.add_cog(GuildUtilsCog(bot))

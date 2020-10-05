from discord.ext import commands
from db.models import Config


class GuildUtilsCog(commands.Cog, name='Guild Utils'):

	def __init__(self, bot, session):
		self.bot = bot
		self.session = session
		self.reaction_emojis = {
					'<:azul1:756368844251201576>': 759195481561366569,
					'<:vermelho:756368844041486437>': 752577427146014822,
					'<:amongas:756368109887160361>': 759198385692606474
				}
	@commands.command()
	@commands.is_owner()
	async def prefix(self, ctx, prefix):
		Config.update(self.session, 'prefix', prefix)
		await ctx.send(f'Prefixo alterado para `{prefix}`')

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if payload.channel_id == 759191967258902549:
			if payload.message_id == 759199219352338443:
				guild = self.bot.get_guild(payload.guild_id)
				if str(payload.emoji) in self.reaction_emojis:
					await payload.member.add_roles(guild.get_role(self.reaction_emojis[str(payload.emoji)]))


	@commands.Cog.listener()
	async def on_raw_reaction_remove(self, payload):
		if payload.channel_id == 759191967258902549:
			if payload.message_id == 759199219352338443:
				guild = self.bot.get_guild(payload.guild_id)
				member = guild.get_member(payload.user_id)
				if str(payload.emoji) in self.reaction_emojis:
					await member.remove_roles(guild.get_role(self.reaction_emojis[str(payload.emoji)]))
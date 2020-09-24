from discord import TextChannel, PartialEmoji, Role
from discord.ext import commands

from db import Db
from db.models import RoleReaction,Config


class GuildUtilsCog(commands.Cog, name='Guild Utils'):

	def __init__(self, bot):
		self.bot = bot
		self.session = Db().session

	@commands.command()
	@commands.is_owner()
	async def prefix(self, ctx, prefix):
		Config.update(self.session, 'prefix', prefix)
		await ctx.send(f'Prefixo alterado para `{prefix}`')

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		role_reactions = RoleReaction.get(self.session,payload.channel_id,payload.message_id,str(payload.emoji))
		roles = []
		guild = self.bot.get_guild(payload.guild_id)
		for rr in role_reactions:
			roles.append(guild.get_role(rr.role_id))

		await payload.member.add_roles(*roles)

	@commands.Cog.listener()
	async def on_raw_reaction_remove(self, payload):
		role_reactions = RoleReaction.get(self.session, payload.channel_id, payload.message_id, str(payload.emoji))
		roles = []
		guild = self.bot.get_guild(payload.guild_id)
		for rr in role_reactions:
			roles.append(guild.get_role(rr.role_id))

		await guild.get_member(payload.user_id).remove_roles(*roles)

	@commands.Cog.listener()
	async def on_raw_message_delete(self,payload):
		role_reactions = RoleReaction.get(self.session,payload.channel_id,payload.message_id)

		if len(role_reactions) > 0:
			for rr in role_reactions:
				self.session.delete(rr)
			self.session.commit()

	@commands.command()
	async def react(self, ctx, channel: TextChannel, message_id, emoji: PartialEmoji, role:Role):
		message = await channel.fetch_message(message_id)

		if len(RoleReaction.get(self.session,channel.id,message.id,str(emoji),role.id)) > 0:
			await ctx.send('Já existente')
		else:
			role_reaction = RoleReaction(channel_id=channel.id,message_id=message.id,emoji=str(emoji),role_id=role.id)
			self.session.add(role_reaction)
			self.session.commit()
			await message.add_reaction(emoji)

	@commands.command()
	async def unreact(self,ctx, channel: TextChannel, message_id,emoji: PartialEmoji=None):
		message = await channel.fetch_message(message_id)

		if emoji is not None:
			role_reactions = RoleReaction.get(self.session,channel.id,message.id,str(emoji))
		else:
			role_reactions = RoleReaction.get(self.session, channel.id, message.id)
		if len(role_reactions) == 0:
			await ctx.send('Não existente')
		else:
			for rr in role_reactions:
				self.session.delete(rr)
			self.session.commit()

			for rr in role_reactions:
				await message.remove_reaction(rr.emoji,self.bot.user)

def setup(bot):
	bot.add_cog(GuildUtilsCog(bot))

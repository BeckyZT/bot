from cogs.chat_utils_cog import ChatUtilsCog
from cogs.guild_utils_cog import GuildUtilsCog
from cogs.room_code_cog import RoomCodeCog

def init_cogs(bot,session):
	bot.add_cog(ChatUtilsCog(bot))
	bot.add_cog(GuildUtilsCog(bot,session))
	bot.add_cog(RoomCodeCog(bot,session))

import dotenv
import os
import db
from cogs import init_cogs
from db import Db
from db.models import Config
from discord.ext.commands import Bot, CommandNotFound

from keep_alive import keep_alive

dotenv.load_dotenv()
db.startup()
session = Db().session


def get_prefix(bot, message):
	return Config.get(session, 'prefix').value


bot = Bot(command_prefix=get_prefix)

init_cogs(bot, session)

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, CommandNotFound):
		return
	raise error

@bot.event
async def on_ready():
	print('Online')
	print(f'https://discord.com/oauth2/authorize?client_id={bot.user.id}&scope=bot')

keep_alive()

bot.remove_command('help')
bot.run(os.getenv("DISCORD_TOKEN"))

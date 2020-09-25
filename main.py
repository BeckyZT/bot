import dotenv
import os
import db
from db import Db
from db.models import Config
from discord.ext.commands import Bot

from kee_alive import keep_alive

dotenv.load_dotenv()
db.startup()
session = Db().session


def get_prefix(bot, message):
	return Config.get(session, 'prefix').value


bot = Bot(command_prefix=get_prefix)

for file in os.listdir('./cogs'):
	if file.endswith('.py'):
		bot.load_extension(f'cogs.{file[:-3]}')


@bot.event
async def on_ready():
	print('Online')
	print(f'https://discord.com/oauth2/authorize?client_id={bot.user.id}&scope=bot')

keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))

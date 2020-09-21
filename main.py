import dotenv
import os
from db import Db, Server
from discord.ext.commands import Bot

dotenv.load_dotenv()
session = Db().session


def get_prefix(bot, message):
	prefix = Server.get_prefix(session, message.guild.id)
	return prefix


bot = Bot(command_prefix=get_prefix)


@bot.command()
async def load(ctx, extension):
	bot.load_extension(f'cogs.{extension}')


@bot.command()
async def reload(ctx, extension):
	bot.reload_extension(f'cogs.{extension}')


@bot.command()
async def unload(ctx, extension):
	bot.unload_extension(f'cogs.{extension}')


for file in os.listdir('./cogs'):
	if file.endswith('.py'):
		bot.load_extension(f'cogs.{file[:-3]}')


@bot.event
async def on_ready():
	print('Online')
	print(f'https://discord.com/oauth2/authorize?client_id={bot.user.id}&scope=bot')


bot.run(os.getenv("DISCORD_TOKEN"))

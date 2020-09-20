import discord
import dotenv
import os
import json

from db import Db,Server,RoomCode

from discord.ext.commands import Bot

dotenv.load_dotenv()

bot = Bot(command_prefix='!')

session = Db().session

@bot.event
async def on_guild_join(guild):
    server = Server(id=guild.id)
    session.add(server)
    session.commit()

@bot.event
async def on_guild_remove(guild):
    server = Server.get_by_id(session,guild.id)
    session.delete(server)
    session.commit()

@bot.event
async def on_ready():
    print('Online')
    print(f'https://discord.com/oauth2/authorize?client_id={bot.user.id}&scope=bot')

@bot.command()
async def setcode(ctx,code):
    code = code.upper()
    room_code = RoomCode.get_code(session,ctx.guild.id)
    if room_code is None:
        room_code = RoomCode(server_id=ctx.guild.id,code=code)
        session.add(room_code)
        session.commit()
    elif room_code.code == code:
        await ctx.send("Código solicitado é igual ao anterior")
    else:
        RoomCode.update_code_by_server_id(session,ctx.guild.id,code)
        await ctx.send(f'Código definido para {room_code.code}')

@bot.command()
async def code(ctx):
    room_code = RoomCode.get_code(session,ctx.guild.id)
    if room_code is None:
        await ctx.send('Nenhum código definido')
    else:
        await ctx.send(f'O código é {room_code.code}')

@bot.command()
async def clearcode(ctx):
    room_code = RoomCode.get_code(session,ctx.guild.id)
    if room_code is None:
        await ctx.send('Não há código para redefinir')
    else:
        session.delete(room_code)
        session.commit()
        await ctx.send('Código redefinido')


bot.run(os.getenv("DISCORD_TOKEN"))

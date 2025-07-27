# main file for Aventure

# This example requires the 'message_content' intent.
#

import discord
from discord.ext import commands
from discord import app_commands
import logging
import asyncio

import aventure_config as config
import aventure_db as db
from game_driver import *
import sqlite3


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=config.COMMAND_PREFIX, intents=intents, help_command=None)

client = discord.Client(intents=intents)

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')


gameDriver: Game = Game()

# === util functions === #

# checks if a command was sent in a server or not.
# returns false if guild (server) is None. else true.
# will either take context obj for normal commands or
# interaction onj for slash commands.
# discord treats them differently, but
# the info we need from them is the same
async def is_in_guild(ctx: commands.Context) -> bool:
    if ctx.guild == None:
        return False
    else:
        return True
    
async def load(discord_id: int):
    async with sqlite3.connect(await db.getDatabasePath()) as conn:
        cursor = conn.cursor()
        print(discord_id)
        if await db.findUser(cursor, discord_id):
            print('old')
        else:
            print('new')
            await db.newUser(conn, cursor, discord_id)


async def save():
    pass

# === bot code === #

@bot.event
async def on_ready():
    await bot.tree.sync()
    #await print(f'We have logged in as {bot.user}')
    await db.initializeDB()

# ping command. really used for debugging. will be removed later
@bot.command()
async def ping(ctx: commands.Context):
    user = ctx.author
    await load(user.id)
    await ctx.send("pong")

#========= server side commands ==========#
@bot.command(name='dm')
async def dm(ctx: commands.Context):
    user = ctx.author

    await load(user.id)

    if await is_in_guild(ctx):
        # checks if the user does not have a dm channel aready
        # and makes one if needed. should rarely ever be called
        # according to docs (https://discordpy.readthedocs.io/en/stable/api.html#discord.User.create_dm)
        if user.dm_channel == None:
            await user.create_dm()
        
        await ctx.send(f'DM sent')
        await user.send(f'Hello! Type \'{config.COMMAND_PREFIX}help\' for DM commands')
        

@bot.command()
async def help(ctx: commands.Context):
    await ctx.send("TODO: Implement help")

@bot.command()
async def stats(ctx: commands.Context):
    await ctx.send("TODO: Implement stats") 

@bot.command()
async def delete(ctx: commands.Context):
    await ctx.send("TODO: Implement delete") 

#========== dm commands ============#


# run the bot
bot.run(config.TOKEN, log_handler=handler, log_level=logging.DEBUG)

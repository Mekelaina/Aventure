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
import aiosqlite


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=config.COMMAND_PREFIX, intents=intents, help_command=None)

client = discord.Client(intents=intents)

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

GUILD_HELP = f'''Command Prefix: `{config.COMMAND_PREFIX}`
---- Server Commands ----
dm -- I will send you a dm.
stats -- Share your game stats with the server!
how -- An explination on how to play.
delete -- delete your progress and records.
help -- Print this message.'''

DM_HELP = f'''TODO: DM HELP'''

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
    
async def load(discord_id: int) -> int:
    internal_id = 0
    try:
        async with aiosqlite.connect(await db.getDatabasePath()) as conn:
            cursor = await conn.cursor()
            #print(discord_id)
            if await db.findUser(cursor, discord_id):
                internal_id = await db.loadUser(conn, cursor, discord_id,
                                  gameDriver.player, gameDriver.map, gameDriver.enemy)
            else:
                await db.newUser(conn, cursor, discord_id, 
                                gameDriver.player, gameDriver.map, gameDriver.enemy)
        return internal_id
    except aiosqlite.Error as error:
                print('Error occurred -', error)
                

async def save(discord_id: int):
    try:
        async with aiosqlite.connect(await db.getDatabasePath()) as conn:
            cursor = await conn.cursor()
            await db.saveUser(conn, cursor, discord_id, 
                              gameDriver.player, gameDriver.map, gameDriver.enemy)
    except aiosqlite.Error as error:
        print('Error occurred -', error)

async def delete_user(discord_id: int, internal_id: int):
    try:
        async with aiosqlite.connect(await db.getDatabasePath()) as conn:
            cursor = await conn.cursor()
            await db.deleteUser(conn, cursor, discord_id, internal_id)
    except aiosqlite.Error as error:
        print('Error occurred -', error)

# === bot code === #

@bot.event
async def on_ready():
    #await bot.tree.sync()
    #await print(f'We have logged in as {bot.user}')
    await db.initializeDB()

# ping command. really used for debugging. will be removed later
@bot.command()
async def ping(ctx: commands.Context):
    user = ctx.author
    await load(user.id)
    await gameDriver.messageIncrement()
    await save(user.id)
    await ctx.send("pong")

#========= server side commands ==========#
@bot.command(name='dm')
async def dm(ctx: commands.Context):
    user = ctx.author
    await load(user.id)
    await gameDriver.messageIncrement()
    # game logic goes here
    await save(user.id)

    if await is_in_guild(ctx):
        # checks if the user does not have a dm channel aready
        # and makes one if needed. should rarely ever be called
        # according to docs (https://discordpy.readthedocs.io/en/stable/api.html#discord.User.create_dm)
        if user.dm_channel == None:
            await user.create_dm()
        
        await ctx.send(f'DM sent')
        await user.send(f'Hello! Type \'{config.COMMAND_PREFIX}help\' for DM commands')
    else:
        await user.send(f"We're already in DMs, {user.display_name}")
    
        

@bot.command()
async def help(ctx: commands.Context):
    user = ctx.author
    await load(user.id)
    await gameDriver.messageIncrement()
    # game logic goes here
    await save(user.id)

    if await is_in_guild(ctx):
        await ctx.send(GUILD_HELP)
    else:
        await ctx.send(DM_HELP)

@bot.command()
async def stats(ctx: commands.Context):
    user = ctx.author
    await load(user.id)
    await gameDriver.messageIncrement()
    await save(user.id)
    await ctx.send(f'''---- Stats! ----
Dungeons Cleared: {gameDriver.player.stats.dungeonsCleared}
Enemies Killed: {gameDriver.player.stats.enemiesKilled}
Deaths: {gameDriver.player.stats.deaths}
Total Gold: {gameDriver.player.stats.totalGold}
Total Items: {gameDriver.player.stats.totalItems}
Messages Sent: {gameDriver.player.stats.messagesSent}''')

@bot.command()
async def delete(ctx: commands.Context):
    if await is_in_guild(ctx):
        user = ctx.author
        internal_id = await load(user.id)
        print(internal_id)
        await delete_user(user.id, internal_id)
        await ctx.send(f'User {user.display_name} has been deleted.')

@bot.command()
async def how(ctx: commands.Context):
    await ctx.send("TODO: Implement how")

#========== dm commands ============#


# run the bot
bot.run(config.TOKEN, log_handler=handler, log_level=logging.DEBUG)

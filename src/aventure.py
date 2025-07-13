# main file for Aventure

# This example requires the 'message_content' intent.
#

import discord
from discord.ext import commands
import logging

import aventure_config as config

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=config.COMMAND_PREFIX, intents=intents)

client = discord.Client(intents=intents)

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')




# === util functions === #

# checks if a command was sent in a server or not.
# returns false if guild (server) is None. else true.
async def is_in_guild(ctx: commands.Context) -> bool:
    #print(ctx.guild)
    if ctx.guild == None:
        return False
    else:
        return True


# === bot code === #

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# ping command. really used for debugging. will be removed later
@bot.command()
async def ping(ctx: commands.Context):
    
    if await is_in_guild(ctx):
        await ctx.send('Loop')
    else:
        await ctx.send('Zoop')

# sends a DM to the user if called from a server. 
# Since the game part takes place in dms. 
@bot.command()
async def dm(ctx: commands.Context):
    # get user from context
    user = ctx.author
    
    if await is_in_guild(ctx):
        # checks if the user does not have a dm channel aready
        # and makes one if needed. should rarely ever be called
        # according to docs (https://discordpy.readthedocs.io/en/stable/api.html#discord.User.create_dm)
        if user.dm_channel == None:
            await user.create_dm()
        
        await user.send(f'Hello~ Type \'{config.COMMAND_PREFIX}help\' for getting started!')
    else:
        await user.send("We're already in DMs, silly")


# run the bot
bot.run(config.TOKEN, log_handler=handler, log_level=logging.DEBUG)

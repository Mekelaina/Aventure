# main file for Aventure

# This example requires the 'message_content' intent.
#

import discord
from discord.ext import commands
from discord import app_commands
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
# will either take context obj for normal commands or
# interaction onj for slash commands.
# discord treats them differently, but
# the info we need from them is the same
async def is_in_guild(ctx: commands.Context | discord.Interaction) -> bool:
    if ctx.guild == None:
        return False
    else:
        return True
    
async def swallow_user_input(ctx: commands.Context | discord.Interaction) -> bool:
    if await is_in_guild(ctx):
        await ctx.message.delete(delay=0.5)
    else:
        # TODO figure out permissions to delete commands in dms. 
        pass


# === bot code === #

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'We have logged in as {bot.user}')

# ping command. really used for debugging. will be removed later
@bot.command()
async def ping(ctx: commands.Context):
    await ctx.send("pong")
    swallow_user_input(ctx)


# === slash commands === #

# sends a DM to the user if called from a server. 
# Since the game part takes place in dms. 
#@bot.command()
@bot.tree.command(
        name='dm',
        description='Send a new DM from the Bot to you. \n The game is played in DMs'
)
async def dm(interaction: discord.Integration):
    # get user from context
    user = interaction.user

    if await is_in_guild():
        # checks if the user does not have a dm channel aready
        # and makes one if needed. should rarely ever be called
        # according to docs (https://discordpy.readthedocs.io/en/stable/api.html#discord.User.create_dm)
        if user.dm_channel == None:
            await user.create_dm()
        
        await user.send(f'Hello~ Type \'{config.COMMAND_PREFIX}help\' for getting started!')
    else:
        await user.send("We're already in DMs, silly")
    
    swallow_user_input(interaction)       

@bot.tree.command(
    name='help',
    description='Useful info and how to get started'
)
async def help(interaction: discord.Interaction):
    await interaction.response.send_message("TODO: implement help")
    #await swallow_user_input()

@bot.tree.command(
    name='show_stats',
    description='Share your in game stats with your friends!'
)
async def stats(interaction: discord.Interaction):
    await interaction.response.send_message("tTODO: implement stats")

@bot.tree.command(
    name='delete_info',
    description='Delete all stored progress. We\'ll miss you.. :('
)
async def delete_user(interaction: discord.Interaction):
    await interaction.response.send_message("TODO: implement delete user")


#=== normal commands ===#


# run the bot
bot.run(config.TOKEN, log_handler=handler, log_level=logging.DEBUG)

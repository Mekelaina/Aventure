# main file for Aventure

# This example requires the 'message_content' intent.

import discord
from discord.ext import commands
import logging

import aventure_config as config

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='av ', intents=intents)

client = discord.Client(intents=intents)

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    
    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')


#bot.add_command(ping2)
bot.run(config.TOKEN, log_handler=handler, log_level=logging.DEBUG)

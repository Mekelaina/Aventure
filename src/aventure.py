# main file for Aventure

# This example requires the 'message_content' intent.
#

import discord
from discord.ext import commands
from discord import app_commands
import logging

import aventure_config as config
import aventure_db as db
from game_driver import *
from aventure_player import GameState
import aiosqlite


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=config.COMMAND_PREFIX, intents=intents, help_command=None)

client = discord.Client(intents=intents)

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# game init
gameDriver: Game = Game()
NEW_PLAYER_DRIVER: Game = Game()

#defined print strings
GUILD_HELP = f'''Command Prefix: `{config.COMMAND_PREFIX}`
---- Server Commands ----
dm -- I will send you a dm.
stats -- Share your game stats with the server!
how -- An explination on how to play.
delete -- delete your progress and records.
help -- Print this message.'''

DM_HELP = f'''TODO: DM HELP'''

MAIN_MENU = '''---- Aventure ----
new -- Start a new run!
resume -- pick up where you left off
stats -- view your stats'''


KEY = '''```
---- ASCII Key ----
#   Wall
*   Open Door
-   Unlocked Door N/S
|   Unlocked Door E/W
@   You
$   Treasure/Item
%   Switch
/   Toggled Switch
!   Dungeon Key```'''


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
            inDB = await db.findUser(cursor, discord_id)
            if inDB:
                internal_id = await db.loadUser(conn, cursor, discord_id,
                                  gameDriver.player, gameDriver.map, gameDriver.enemy)
                
            else:
                await db.newUser(conn, cursor, discord_id, 
                                NEW_PLAYER_DRIVER.player, NEW_PLAYER_DRIVER.map, NEW_PLAYER_DRIVER.enemy)
                internal_id = await db.loadUser(conn, cursor, discord_id,
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

async def clearDos() -> None:
    await gameDriver.setDoNew(False)
    await gameDriver.setDoDelete(False)

async def printRoom(ctx: commands.Context):
    room = await gameDriver.getRoomAscii()
    print(f'Room: {gameDriver.player.data.room}')
    await ctx.author.send(room)


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
    #print(gameDriver.player.data)
    await clearDos()
    await save(user.id)
    await ctx.send("pong")

@bot.command()
async def debug(ctx: commands.Context):
    user = ctx.author
    await load(user.id)
    await gameDriver.messageIncrement()
    await gameDriver.setState(GameState.NORUN_MENU)
    await user.send('reset')
    await clearDos()
    await save(user.id)

#========= server side commands ==========#
@bot.command(name='dm')
async def dm(ctx: commands.Context):
    user = ctx.author
    await load(user.id)
    await gameDriver.messageIncrement()
    await clearDos()
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
    await clearDos()
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
    await clearDos()
    await save(user.id)

    if await is_in_guild(ctx):
            await ctx.send(f'''---- Stats! ----
Dungeons Cleared: {gameDriver.player.stats.dungeonsCleared}
Enemies Killed: {gameDriver.player.stats.enemiesKilled}
Deaths: {gameDriver.player.stats.deaths}
Total Gold: {gameDriver.player.stats.totalGold}
Total Items: {gameDriver.player.stats.totalItems}
Messages Sent: {gameDriver.player.stats.messagesSent}''')
    else:
        await user.send(f'''---- Stats! ----
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
        if await gameDriver.isDoDelete():
            await gameDriver.setDoDelete(False)
            await delete_user(user.id, internal_id)
            await ctx.send(f'User {user.display_name} has been deleted.')
        else:
            await gameDriver.setDoDelete(True)
            await ctx.send(f'delete will remove all your progress. If you wish to delete your data, type `{config.COMMAND_PREFIX}delete` again.')
            await save(user.id)

@bot.command()
async def how(ctx: commands.Context):
    user = ctx.author
    internal_id = await load(user.id)
    await gameDriver.messageIncrement()
    await clearDos()
    await save(user.id)
    await ctx.send("TODO: Implement how")

    

#========== dm commands ============#

@bot.command()
async def key(ctx: commands.Context):
    if not await is_in_guild(ctx):
        user = ctx.author
        await load(user.id)
        await gameDriver.messageIncrement()
        await clearDos()
        await user.send(KEY)
        await save(user.id)

@bot.command()
async def menu(ctx: commands.Context):
    if not await is_in_guild(ctx):
        user = ctx.author
        await load(user.id)
        await gameDriver.messageIncrement()
        await clearDos()
        match gameDriver.player.state:
            case GameState.NORUN_MENU | GameState.RUN_MENU:
                await user.send('Please select an option:')
                await user.send(MAIN_MENU)
            case GameState.RUN_DUNGEON:
                await user.send('Saving run...')
                await gameDriver.setState(GameState.RUN_MENU)
                await user.send('Run saved! Please choose an option')
                await user.send(MAIN_MENU)
            case GameState.RUN_COMBAT:
                await user.send('Cant save during combat!')
        await save(user.id)

@bot.command()
async def new(ctx: commands.Context):
    if not await is_in_guild(ctx):
        user = ctx.author
        await load(user.id)
        await gameDriver.messageIncrement()
        await gameDriver.setDoDelete(False)

        match gameDriver.player.state:
            case GameState.NORUN_MENU:
                await user.send('Starting a new run...')
                await gameDriver.newGame(2)
                #gameDriver.player.data.room = 1
                intro = await gameDriver.getMapIntro()
                await user.send(intro)
                await printRoom(ctx)

            case GameState.RUN_MENU:
                if await gameDriver.isDoNew():
                    #print('E')
                    await user.send('Starting a new run...')
                    await gameDriver.setDoNew(False)
                    await gameDriver.newGame(2)
                    intro = await gameDriver.getMapIntro()
                    await user.send(intro)
                    await printRoom(ctx)
                else:
                    #print('F')
                    await user.send(f'''You have a curently saved run. Starting a new one will clear any progress.\ntype `{config.COMMAND_PREFIX}new` again to overwrite your saved run.''')
                    await gameDriver.setDoNew(True)
            case _:
                pass
        #print('saving')
        #print(gameDriver.player.data.room)
        await save(user.id)

@bot.command()
async def resume(ctx: commands.Context):
    if not await is_in_guild(ctx):
        user = ctx.author
        await load(user.id)
        await gameDriver.messageIncrement()
        await clearDos()

        match gameDriver.player.state:
            case GameState.RUN_MENU:
                await user.send('Resuming run where you left off...')
                await gameDriver.setState(GameState.RUN_DUNGEON)
                await printRoom(ctx)

            case GameState.NORUN_MENU:
                await user.send('You dont have an active run. Select new to start a new run.')

        await save(user.id)

@bot.command()
async def room(ctx: commands.Context):
    if not await is_in_guild(ctx):
        user = ctx.author
        await load(user.id)
        await gameDriver.messageIncrement()
        await clearDos()
        match gameDriver.player.state:
            case GameState.RUN_DUNGEON:
                await printRoom(ctx)

        await save(user.id)

@bot.command()
async def look(ctx: commands.Context, *args):
    if not await is_in_guild(ctx):
        user = ctx.author
        await load(user.id)
        await gameDriver.messageIncrement()
        await clearDos()
    
        match gameDriver.player.state:
            case GameState.RUN_DUNGEON:
                if not args:
                    desc = await gameDriver.getRoomDesc()
                    await user.send(desc)
                else:
                    roomHasItem = await gameDriver.roomHasItem()
                    if roomHasItem:
                        itemName = ' '.join(args)
                        itemDesc = await gameDriver.lookItem(itemName)
                        await user.send(itemDesc)

                #await printRoom(ctx)
        
        await save(user.id)

@bot.command()
async def inv(ctx: commands.Context, *args):
    if not await is_in_guild(ctx):
        user = ctx.author
        await load(user.id)
        await gameDriver.messageIncrement()
        await clearDos()
        match gameDriver.player.state:
            case GameState.RUN_DUNGEON:
                itemName = ' '.join(args)
                if not args:
                    i = await gameDriver.getInv()
                    e = await gameDriver.getEquipment()
                    
                    await user.send(e)
                    await user.send(i)
                else:
                    itemName = ' '.join(args)
                    hasItem = await gameDriver.playerHasItem(itemName)
                    if hasItem:
                        message = await gameDriver.lookItem(itemName)
                        await user.send(message)
                    else:
                        await user.send(f'No item `{itemName}`')
        await save(user.id)

@bot.command()
async def equip(ctx: commands.Context, *args):
     if not await is_in_guild(ctx):
        user = ctx.author
        await load(user.id)
        await gameDriver.messageIncrement()
        await clearDos()

        match gameDriver.player.state:
            case GameState.RUN_DUNGEON:
                if args:
                    itemName = ' '.join(args)
                    hasItem = await gameDriver.playerHasItem(itemName)
                    if hasItem:
                        res, message = await gameDriver.playerEquipItem(itemName)
                        await user.send(message)
                    else:
                        await user.send(f'No item `{itemName}`')
                else:
                    await user.send('please provide an item in your inventory to equip.')
        await save(user.id)

@bot.command()
async def switch(ctx: commands.Context):
    if not await is_in_guild(ctx):
        user = ctx.author
        await load(user.id)
        await gameDriver.messageIncrement()
        await clearDos()
        match gameDriver.player.state:
            case GameState.RUN_DUNGEON:
                hasSwitch = await gameDriver.roomHasSwitch()
                if hasSwitch:
                    switchToggled = await gameDriver.roomSwitchToggled()
                    if switchToggled:
                        await user.send('The switch is wont budge from its on position.')
                    else:
                        await gameDriver.roomFlipSwitch()
                        await user.send('You flip the switch with a heavy *clunk*, you hear a door open in another room.')
                else:
                    await user.send('This room has no switch')
        await save(user.id)

@bot.command()
async def take(ctx: commands.Context, *args):
    if not await is_in_guild(ctx):
        user = ctx.author
        await load(user.id)
        await gameDriver.messageIncrement()
        await clearDos()

        if not args:
            await user.send('Please specify something to take.')
        else:
            hasItem = await gameDriver.roomHasItem()
            argName = ' '.join(args)
            if hasItem:
                itemName = await gameDriver.playerTakeItem()
                await user.send(f'You took the {itemName}')
            elif argName.lower() == 'key':
                print('a')
                hasKey = await gameDriver.roomHasKey()
                print('b')
                if hasKey:
                    print('c')
                    await gameDriver.playerTakeKey()
                    await user.send('You took the key.')
                else:
                    await user.send('What key?')
            else:
                await user.send('There\'s nothing to take in this room.')

        await save(user.id)

@bot.command()
async def enemy(ctx: commands.Context):
    if not await is_in_guild(ctx):
        user = ctx.author
        await load(user.id)
        await gameDriver.messageIncrement()
        await clearDos()

        match gameDriver.player.state:
            case GameState.RUN_DUNGEON:
                print('ewe')
                hasEnemy = await gameDriver.roomHasEnemy()
                if hasEnemy:
                    desc = await gameDriver.getRoomEnemyDesc()
                    await user.send(desc)
                    #await printRoom(ctx)
                else:
                    await user.send('You are all alone in this room.')
        
        await save(user.id)

@bot.command()
async def move(ctx: commands.Context, arg):
    if not await is_in_guild(ctx):
        user = ctx.author
        await load(user.id)
        await gameDriver.messageIncrement()
        await clearDos()

        match gameDriver.player.state:
            case GameState.RUN_DUNGEON:
                moveRes = -1
                message = ''
                match arg:
                    case 'n':
                        moveRes, message = await gameDriver.move(Direction.NORTH)
                    case 'e':
                        moveRes, message = await gameDriver.move(Direction.EAST)
                    case 's':
                        moveRes, message = await gameDriver.move(Direction.SOUTH)
                    case 'w' | _:
                        moveRes, message = await gameDriver.move(Direction.WEST)
                   
                await user.send(message)
                if moveRes == 1:
                    await printRoom(ctx)
                elif moveRes == 3:
                    await gameDriver.clearDungeonIncrement()
                    await gameDriver.setState(GameState.NORUN_MENU)
                    await user.send('Please select an option:')
                    await user.send(MAIN_MENU)
        
        await save(user.id)

        

# run the bot
bot.run(config.TOKEN, log_handler=handler, log_level=logging.DEBUG)

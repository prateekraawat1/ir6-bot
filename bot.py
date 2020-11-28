import os
import discord
import random
import pymongo
import dns

#for optional parameters / skip parameters in functions
import typing

from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DBUSER = os.getenv('MONGODB_USER')
DBPASS = os.getenv('MONGODB_PASS')

bot = commands.Bot(command_prefix = "!")

#loggin errors
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
# end of logging


#Setting up mongoDB

dbClient = pymongo.MongoClient("mongodb+srv://carlbot:prateek23@sar6.tiqn4.mongodb.net/carlbot?retryWrites=true&w=majority")
db = dbClient.test

"""
#print all available databases in the cluster
dblist = dbClient.list_database_names()
print(dblist)
"""
@bot.event 
async def on_ready():
    print(f'{bot.user.name} has connected!')

@bot.command(name='99')
async def nine_nine(self, ctx):
    #if ctx.author == self.author
        #return

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

@bot.command(aliases=['hi', 'hello'])
async def _hi(ctx):
    """
    docstring
    """
    response = "Hello!"
    await ctx.send(response)

@bot.command(name = 'ping')
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

@bot.command(name = 'delete')
@commands.has_permissions(manage_messages=True)
async def delete(ctx, amount: int):
    if amount == 0:
        await ctx.send("Nothing to delete!")
    else:
        await ctx.channel.purge(limit = amount+1)
        await ctx.send(f'{amount} messages deleted!')

@commands.command()
async def register(ctx, *, team):
    await ctx.send(f"Team {team} Registered!")
bot.add_command(register)

bot.run(TOKEN)

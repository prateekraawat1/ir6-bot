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
DISCORD_ID = "CarlJohnson#0041"

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
db = dbClient["carlbot"]
dbCol = db['teams']

"""
#print all available databases in the cluster
dblist = dbClient.list_database_names()
print(dblist)
"""


@bot.event 
async def on_ready():
    print(f'{bot.user.name} has connected!')

@bot.command(name='99')
async def nine_nine(ctx):
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



##
##To-Do Check if the team already exists in database
##
@bot.command()
async def register(ctx, country, captain, viceCaptain, *, team):
    from discord.utils import get
    async with ctx.typing():
        countries = ["india", "bangladesh", "srilanka", "pakistan"]
        country = country.lower()
        if (country not in countries):
            print("Invalid country entered!")
            await ctx.send("Invalid country! Valid countries are: `India`, `Bangladesh`, `SriLanka`, `Pakistan`")
            return 
        await ctx.send("\nRegistering Team")
        token = generateToken()
        teamDb = {
            "teamName": team,
            "country": country,
            "captain": captain,
            "viceCaptain": viceCaptain,
            "token": token
        }
        x = dbCol.insert_one(teamDb)
        print(x.inserted_id)
        #sending dm to user with their token
        await ctx.author.send(f"Your team `{team}`\'s token: `{token}`\n\nYou will need this token in case you want to delete your existing team.\nIf you face any error such as invalid token or something similar please contact `{DISCORD_ID}`")
    #give user team captain role
    ROLE = "Team Captain"
    user = ctx.author
    role = get(user.guild.roles, name = ROLE)
    print(f"Giving Captain role to {user}")
    await user.add_roles(role)
    await ctx.send(f"Team `{team}` Registered!")
    print(f"team {team} registered")

@register.error
async def register_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Missing required parameters! Usage `!register [country] [captain] [vice-captain/coach] [teamname]`')


@bot.command(name="deleteteam")
async def deleteteam(ctx, token):
    from discord.utils import get
    deleteQuery = {"token": token}
    try:
        x = dbCol.find_one(deleteQuery)
        if (x == None):
            await ctx.channel.purge(limit = 1)
            await ctx.send(f"Team not found! Ensure you are using the correct token or contact `{DISCORD_ID}`")
            return
        team = x["teamName"]
        print("Deleting team " + team)
        dbCol.delete_one(deleteQuery)
        await ctx.channel.purge(limit = 1)
        await ctx.send(f"Team {team} deleted!")
        #take user team captain role
        ROLE = "Team Captain"
        user = ctx.author
        role = get(user.guild.roles, name = ROLE)
        print(f"Removing Captain role from {user}")
        await user.remove_roles(role)
    except:
        await ctx.channel.purge(limit = 1)
        await ctx.send(f"Error! Team cannot be deleted! Contact `{DISCORD_ID}` if the problem persists.")


@bot.command(name = "listallteams")
@commands.has_permissions(manage_roles=True)
async def listallteams(ctx):
    team = ""
    country = ""
    captain = ""
    viceCaptain = ""
    for x in dbCol.find({}, {"_id": 0, "token": 0}):
        team = x["teamName"]
        country = x["country"]
        captain = x["captain"]
        viceCaptain = x["viceCaptain"]

        embeded = discord.Embed(title = team, color = 0xff0000)
        embeded.add_field(name = "Country", value = country, inline = False)
        embeded.add_field(name = "Captain", value = captain, inline = False)    
        embeded.add_field(name = "Vice Captain", value = viceCaptain, inline = False)
        await ctx.send(embed = embeded)

def generateToken():
    import string
    import secrets

    alphabet = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(alphabet) for i in range(6))
    print("Token generated: " + token)
    return token



bot.run(TOKEN)
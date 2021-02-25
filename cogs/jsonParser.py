import discord
import requests
from discord.ext import commands


class jsonPaser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print('jsonParser loaded!')


    @commands.command(name = "test",
                    usage="<usage>",
                    description = "description")
    
    async def test(self, ctx):
        await ctx.send("template command")

    @commands.command(name = "jsontest", aliases=["aliase"])
    async def  commandName(self, ctx):
        import urllib.request
        from urllib.request import Request, urlopen
        import json
        req = Request('https://starb.in/raw/zpToHm', headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as url:
            data = json.loads(url.read().decode())
            # print(data)

            
            embed=discord.Embed(title=data['title'], description="description", color=0xff0000)
            embed.set_footer(text=data["footer"]["text"], icon_url=data["footer"]["icon_url"])
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(jsonPaser(bot))


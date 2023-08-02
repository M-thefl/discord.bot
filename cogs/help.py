from typing import List
from discord.ext import commands
import discord

class tictactoe(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("help")

############################   help    #################################
    @commands.hybrid_command(name="help", with_app_command=True, description="help")
    @commands.cooldown(3, 60, commands.BucketType.member)
    async def help(self, ctx: commands.Context):
     embed = discord.Embed(title="**help command🚀**",colour= 00000)
     embed.add_field(name="General",value="`avatar`,`userinfo`,`cat`", inline=True)
     embed.add_field(name="Admin",value="`kick`,`ban`,`unbanall`,`mute`", inline=True)
     embed.add_field(name="Server",value="`lock`,`unlock`,`clear`", inline=True)
     embed.add_field(name="Info",value="`help`,`ping`,`root`", inline=True)
     embed.add_field(name="Other",value="`ticket`,`welcome`,`level`", inline=True)
     embed.set_footer(text='Perfix: e!\nsupport slash command (/)')
     await ctx.author.send(embed=embed)
     await ctx.send("**ferestade shod!**")

async def setup(bot: commands.Bot):
   await bot.add_cog(tictactoe(bot))
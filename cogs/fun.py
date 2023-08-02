import discord
from discord.ext import commands
import random
class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("fun")
    ############################   fun    #################################
    @commands.hybrid_command(name="cat", with_app_command=True, description="cat")
    @commands.cooldown(3, 60, commands.BucketType.member)
    async def cat(self, ctx: commands.Context):
        cat_tags = ["cute"]
        tag = random.choice(cat_tags)
        em = discord.Embed(colour = 000000)
        em.set_image(url = f"https://cataas.com/cat/{tag}")
        await ctx.send(embed=em)  


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Fun(bot))
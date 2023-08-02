import discord
from discord import app_commands
from discord.ext import commands
import asyncio
from datetime import timedelta
from discord.ext.commands import guild_only

############################   unabn all    #################################
class unbanallConfirm(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "بله", style = discord.ButtonStyle.green)
    async def unbanall_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        for ban_entry in bans:
            await interaction.guild.unban(user = ban_entry.user)
        unbanall_embed = discord.Embed(title = "Unban All", description = f"{author.mention} همه کسایی که بن بودن آن بن شدن {len(bans)})", colour = discord.Colour.green())
        await interaction.followup.send(embed = unbanall_embed)

class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    @commands.Cog.listener()
    async def on_ready(self):
        print("Mod")


############################   clear    #################################
    @commands.hybrid_command(name="clear", with_app_command=True, description="clear-message")
    @commands.cooldown(3, 60, commands.BucketType.member)
    @commands.has_permissions(administrator = True)
    async def clear(self, ctx: commands.Context, tedad: int = 1):
    # if ctx.author.id in (855710405993168896,1054610457106849862,192654116869242880,759944498746359818,951777100606636042,906896528017330176,927697233527320648):
        await ctx.send(f" {tedad} | پیام پاک شد" , ephemeral = True)
        await ctx.channel.purge(limit = tedad)

    @clear.error
    async def clear_error(self,ctx: commands.Context,error):
     if isinstance(error, commands.MissingPermissions):
        member = 0
        emb = discord.Embed(description=  "**you don't have permission**")
        await ctx.send(f"||{ctx.author.mention}||",embed=emb ,ephemeral = True)

    
############################   timeout    #################################
    @app_commands.command(name = "timeout", description = "timeout-member")
    @app_commands.describe(member = "Member", time = "Time", reason = "Reason")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.checks.has_permissions(administrator = True)
    async def timeout(self, interaction: discord.Interaction, member : discord.Member, time: str, reason: str = None):
        if interaction.user.top_role <= member.top_role:
            return await interaction.response.send_message(f"پرم اون بالا تره ", ephemeral = True)
        if interaction.guild.me.top_role <= member.top_role:
            return await interaction.response.send_message(f"من پرمیشن کافی ندارم", ephemeral = True)
        if time == None:
            time_string = "" 
        else:
            time_string = f"\nTime: {time}"
            get_time = {
            "s": 1, "m": 60, "h": 3600, "d": 86400,
            "w": 604800, "mo": 2592000, "y": 31104000 }
            a = time[-1]
            b = get_time.get(a)
            c = time[:-1]
            try: int(c)
            except: return await interaction.response.send_message(" یادت رفت از اینا استفاده کنی (s,m,h,d,w,mo,y)", ephemeral = True)
            try: sleep = int(b) * int(c)
            except: return await interaction.response.send_message("یادت رفت از اینا استفاده کنی(s,m,h,d,w,mo,y)", ephemeral = True)
        await member.timeout(timedelta(seconds = sleep), reason = reason)
        if reason == None: reason = ""
        else: reason = f"\n reason: **{reason}**"
        timeout_embed = discord.Embed(title = "Timeout", description = f"{member.mention} تایم اویت شد توسط{interaction.user.mention}{time_string}{reason}", colour = discord.Colour.dark_blue())
        await interaction.response.send_message(embed = timeout_embed)
        await asyncio.sleep(int(sleep))
        timeout_embed = discord.Embed(title = "تموم شد", description = f"{member.mention}'تموم شد", colour = discord.Colour.green())
        await interaction.response.send_message(embed = timeout_embed)


    @timeout.error
    async def time_error(self,ctx: commands.Context,error):
     if isinstance(error, commands.MissingPermissions):
        member = 0
        emb = discord.Embed(description=  "**you don't have permission**")
        await ctx.send(f"||{ctx.author.mention}||",embed=emb ,ephemeral = True)



############################   kick    #################################
    @commands.hybrid_command(name="kick", with_app_command=True, description="kick-user")
    @commands.cooldown(3, 60, commands.BucketType.member)
    @commands.has_permissions(administrator = True)
    async def kick(self, ctx: commands.Context,member : discord.Member, reason: str = None):
      #  if ctx.author.id in (855710405993168896,1054610457106849862,192654116869242880,759944498746359818,951777100606636042,906896528017330176,927697233527320648):
        #check author role
        if ctx.author.top_role <= member.top_role:
            return await ctx.send(f"```پرم اون بالا تره```", ephemeral = True)
        #check bot role
        if ctx.guild.me.top_role <= member.top_role:
            return await ctx.send(f"```من پرمیشن کافی ندارم```", ephemeral = True)
        if reason == None: reason = ""
        else: reason = f"\nReason: {reason}"
        await member.kick(reason = reason)
        kick_embed = discord.Embed(title = "kick", description = f"{reason}\n🐱‍🏍**Moderator:**{ctx.author.mention}\n**💠Successful kick:**``{member}``")
        await ctx.send(embed = kick_embed)
        await member.send(f"```شما سیکت از سرور خورد‍‍``` ``{reason}``")


    @kick.error
    async def kick_error(self,ctx: commands.Context,error):
     if isinstance(error, commands.MissingPermissions):
        member = 0
        emb = discord.Embed(description=  "**you don't have permission**")
        await ctx.send(f"||{ctx.author.mention}||",embed=emb ,ephemeral = True)


############################   ban    #################################
    @commands.hybrid_command(name="ban", with_app_command=True, description="ban-user")
    @commands.cooldown(3, 60, commands.BucketType.member)
    @commands.has_permissions(administrator = True)
    async def ban(self, ctx: commands.Context, member: discord.Member, reason: str = None):
        #if ctx.author.id in (855710405993168896,1054610457106849862,192654116869242880,759944498746359818,951777100606636042,906896528017330176,927697233527320648):
        #check role
        if ctx.author.top_role <= member.top_role:
            return await ctx.send(f"```پرم اون بالا تره```", ephemeral = True)
        #check bot role
        if ctx.guild.me.top_role <= member.top_role:
            return await ctx.send(f"```من پرمیشن کافی ندارم```", ephemeral = True)
        await member.ban(reason = reason)
        if reason == None: reason = ""
        else: reason = f"\n**🌟Reason:** {reason}"
        ban_embed = discord.Embed(title = "Ban result:", description = f"{reason}\n🐱‍🏍**Moderator:**{ctx.author.mention}\n**💠Successful bans:**``{member}``")
        ban_embed.set_footer(text= ctx.guild.name)
        await ctx.send(embed = ban_embed,ephemeral = True)
        await member.send(f"```شما سیکت از سرور خورد‍‍``` ``{reason}``")

    @ban.error
    async def launch_error(self,ctx: commands.Context,error):
     if isinstance(error, commands.MissingPermissions):
        member = 0
        emb = discord.Embed(description=  "**you don't have permission**")
        await ctx.send(f"||{ctx.author.mention}||",embed=emb ,ephemeral = True)





#{member.mention} بن شد توسط {ctx.author.mention}{reason}

############################   unban all    #################################
    @app_commands.command(name = "unbanall", description = "unabnall")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.checks.has_permissions(ban_members = True)
    @guild_only()  # Might not need ()
    async def unbanall(self, interaction: discord.Interaction):
        await interaction.response.defer()
        global author
        global bans
        author = interaction.user
        bans = [ban_entry async for ban_entry in interaction.guild.bans()]   
        for ban_entry in bans:
            await interaction.guild.unban(user = ban_entry.user)
        unbanall_embed = discord.Embed(title = "سیستم", description = "مطمعنی میخوای این کارو انجام بدی؟")
        view = unbanallConfirm()
        await interaction.followup.send(embed = unbanall_embed, view = view, ephemeral = True)


    @unbanall.error
    async def unabnall_error(self,ctx: commands.Context,error):
     if isinstance(error, commands.MissingPermissions):
        member = 0
        emb = discord.Embed(description=  "**you don't have permission**")
        await ctx.send(f"||{ctx.author.mention}||",embed=emb ,ephemeral = True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Moderation(bot))
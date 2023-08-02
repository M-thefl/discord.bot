import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import MissingPermissions


############################   hide all    #################################
class hideallConfirm(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "c", style = discord.ButtonStyle.green)
    async def hideall_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != author: return await interaction.response.send_message("> این واسه تو نیست", ephemeral = True)
        await interaction.response.defer()
        for channel in interaction.guild.channels:
            overwrite = channel.overwrites_for(interaction.guild.default_role)
            overwrite.read_messages = False
            await channel.set_permissions(interaction.guild.default_role, overwrite = overwrite)
        emb = discord.Embed(title = f"👁️انجام شد", description = f"> {interaction.user.mention} فیکس شد")
        await interaction.followup.send(embed = emb)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
    @discord.ui.button(label = "کنسل", style = discord.ButtonStyle.red)
    async def hideall_cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != author:
            return await interaction.response.send_message("> این واسه تو نیست", ephemeral = True)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.send_message("> کنسل شد")

############################   hide all    #################################
class showallConfirm(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "c", style = discord.ButtonStyle.green)
    async def showall_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != author: return await interaction.response.send_message("> این واسه تو نیست", ephemeral = True)
        await interaction.response.defer()
        for channel in interaction.guild.channels:
            overwrite = channel.overwrites_for(interaction.guild.default_role)
            overwrite.read_messages = True
            await channel.set_permissions(interaction.guild.default_role, overwrite = overwrite)
        emb = discord.Embed(title = f"👁️انجام شد", description = f"> {interaction.user.mention} فیکس شد")
        await interaction.followup.send(embed = emb)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
    @discord.ui.button(label = "کنسل", style = discord.ButtonStyle.red)
    async def showall_cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != author:
            return await interaction.response.send_message("> این واسه تو نیست", ephemeral = True)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.send_message("> کنسل شد")

############################   lock all    #################################
class lockallConfirm(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "سیستم", style = discord.ButtonStyle.green)
    async def lockall_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != author: return await interaction.response.send_message("> این واسه تو نیست", ephemeral = True)
        await interaction.response.defer()
        for channel in interaction.guild.channels:
            overwrite = channel.overwrites_for(interaction.guild.default_role)
            overwrite.send_messages = False
            await channel.set_permissions(interaction.guild.default_role, overwrite = overwrite)
        emb = discord.Embed(title = f"🔒Done", description = f"||{interaction.user.mention}|| کول چنل ها قفل شد")
        await interaction.followup.send(embed = emb)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
    @discord.ui.button(label = "کنسل", style = discord.ButtonStyle.red)
    async def lockall_cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != author:
            return await interaction.response.send_message("این واسه تو نیست", ephemeral = True)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.send_message("> کنسل شد")

############################   unlock all    #################################
class unlockallConfirm(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "سیستم", style = discord.ButtonStyle.green)
    async def unlockall_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != author: return await interaction.response.send_message("> این واسه تو نیست!", ephemeral = True)
        await interaction.response.defer()
        for channel in interaction.guild.channels:
            overwrite = channel.overwrites_for(interaction.guild.default_role)
            overwrite.send_messages = True
            await channel.set_permissions(interaction.guild.default_role, overwrite = overwrite)
        emb = discord.Embed(title = f"انجام شد", description = f"||{interaction.user.mention}|| کول چنل ها باز شد")
        await interaction.followup.send(embed = emb)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
    @discord.ui.button(label = "کنسل", style = discord.ButtonStyle.red)
    async def unlockall_cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != author:
            return await interaction.response.send_message("> این واسه تو نیست", ephemeral = True)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.send_message("> کنسل شد")

class Settings(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    
    @commands.Cog.listener()
    async def on_ready(self):
        print("server")


############################   hide     #################################
    @commands.hybrid_command(name="hide", with_app_command=True, description="hide-channel")
    @app_commands.describe(channel = "Channel to hide")
    @commands.has_permissions(administrator = True)  
    @commands.cooldown(3, 60, commands.BucketType.member)
    async def hide(self, ctx: commands.Context, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        if overwrite.read_messages == False:
            await ctx.send("> چنل از قبل هاید شده", ephemeral = True)
            return
        overwrite.read_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite = overwrite)
        emb = discord.Embed(title = f"انجام شد", description = f"> **{channel.mention}**فیکس شد🎈", color = 16705372)
        await ctx.send(embed = emb)

    @hide.error
    async def hide_error(self,ctx: commands.Context,error):
     if isinstance(error, commands.MissingPermissions):
        member = 0
        emb = discord.Embed(description=  "**you don't have permission**")
        await ctx.send(f"||{ctx.author.mention}||",embed=emb ,ephemeral = True)

   


############################   hide all    #################################
    @app_commands.command(name = "hideall", description = " hide-all-channel")
    @commands.has_permissions(administrator = True)
    @commands.cooldown(3, 60, commands.BucketType.member)
    async def hideall(self, interaction: discord.Interaction):
        global author
        author = interaction.user
        hideall_em = discord.Embed(title = "سیستم", description = "از این کارت مطمعنی؟")
        view = hideallConfirm()
        await interaction.response.send_message(embed = hideall_em, view = view)

    @hideall.error
    async def hideall_error(self,ctx: commands.Context,error):
     if isinstance(error, commands.MissingPermissions):
        member = 0
        emb = discord.Embed(description=  "**you don't have permission**")
        await ctx.send(f"||{ctx.author.mention}||",embed=emb ,ephemeral = True)


############################   show    #################################
    @commands.hybrid_command(name="show", with_app_command=True, description="show-channel")
    @app_commands.describe(channel = "Channel to unhide")
    @commands.has_permissions(administrator = True)
    @commands.cooldown(3, 60, commands.BucketType.member)
    async def showchat(self, ctx: commands.Context,channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        if overwrite.read_messages == True:
            return await ctx.send("> چنل از قبل بازه", ephemeral = True)
        overwrite.read_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite = overwrite)
        emb = discord.Embed(title = f"👁️انجام شد", description = f"> **{channel.mention}** چنل باز شد", color = 16705372)
        await ctx.send(embed = emb)


    @showchat.error
    async def show_error(self,ctx: commands.Context,error):
     if isinstance(error, commands.MissingPermissions):
        member = 0
        emb = discord.Embed(description=  "**you don't have permission**")
        await ctx.send(f"||{ctx.author.mention}||",embed=emb ,ephemeral = True)

############################   show all    #################################
    @app_commands.command(name = "showall", description = "show-all-channel")
    @commands.has_permissions(administrator = True)
    @commands.cooldown(3, 60, commands.BucketType.member)
    async def showall(self, interaction: discord.Interaction):
        global author
        author = interaction.user
        hideall_em = discord.Embed(title = "سیستم", description = "از این کارت مطمعنی؟")
        view = showallConfirm()
        await interaction.response.send_message(embed = hideall_em, view = view)

    @showall.error
    async def showall_error(self,ctx: commands.Context,error):
     if isinstance(error, commands.MissingPermissions):
        member = 0
        emb = discord.Embed(description=  "**you don't have permission**")
        await ctx.send(f"||{ctx.author.mention}||",embed=emb ,ephemeral = True)




############################   lock     #################################
    @commands.hybrid_command(name="lock", with_app_command=True, description="lock-channel")
    @commands.has_permissions(administrator = True)
    @commands.cooldown(3, 60, commands.BucketType.member)
    async def lock(self, ctx: commands.Context, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        if overwrite.send_messages == False:
            return await ctx.send("> چنل از قبل قفله", ephemeral = True)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite = overwrite)
        emb = discord.Embed(title = f"🔒انجام شد", description = f"> **{channel.mention}** چنل قفل شد", color = 15548997)
        await ctx.send(embed = emb)


    @lock.error
    async def lock_error(self,ctx: commands.Context,error):
     if isinstance(error, commands.MissingPermissions):
        member = 0
        emb = discord.Embed(description=  "**you don't have permission**")
        await ctx.send(f"||{ctx.author.mention}||",embed=emb ,ephemeral = True)



############################   lock all    #################################
    @commands.command(name = "lockall", description = "قفل کردن کول چنل ها")
    @commands.has_permissions(administrator = True)
    @commands.cooldown(3, 60, commands.BucketType.member)
    async def lockall(self, interaction: discord.Interaction):
        global author
        author = interaction.user
        lockall_em = discord.Embed(title = "سیستم", description = "از این کارت مطمعنی؟")
        view = lockallConfirm()
        await interaction.response.send_message(embed = lockall_em, view = view)

    @lockall.error
    async def lockall_error(self,ctx: commands.Context,error):
     if isinstance(error, commands.MissingPermissions):
        member = 0
        emb = discord.Embed(description=  "**you don't have permission**")
        await ctx.send(f"||{ctx.author.mention}||",embed=emb ,ephemeral = True)



############################   unlock     #################################
    @commands.hybrid_command(name="unlock", with_app_command=True, description="unlock-channel")
    @app_commands.describe(channel = "unlock")
    @commands.has_permissions(administrator = True)
    async def unlock(self, ctx: commands.Context, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        if overwrite.send_messages == True:
            return await ctx.send("> چنل از قبل بازه", ephemeral = True)
        overwrite.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite = overwrite)
        emb = discord.Embed(title = f"🔓انجام شد", description = f"> **{channel.mention}** چنل باز شد", color = 15844367)
        await ctx.send(embed = emb)

    @unlock.error
    async def unlock_error(self,ctx: commands.Context,error):
     if isinstance(error, commands.MissingPermissions):
        member = 0
        emb = discord.Embed(description=  "**you don't have permission**")
        await ctx.send(f"||{ctx.author.mention}||",embed=emb ,ephemeral = True)

############################   unlock all    #################################
    @commands.command(name = "unlockall", description = "باز شدن کول چنل ها")
    @commands.has_permissions(administrator = True)
    @commands.cooldown(3, 60, commands.BucketType.member)
    async def unlockall(self, interaction: discord.Interaction):
        global author
        author = interaction.user
        unlockall_em = discord.Embed(title = "سیستم", description = "از این کارت مطمعنی؟")
        view = unlockallConfirm()
        await interaction.response.send_message(embed = unlockall_em, view = view)


    @unlockall.error
    async def unlockall_error(self,ctx: commands.Context,error):
     if isinstance(error, commands.MissingPermissions):
        member = 0
        emb = discord.Embed(description=  "**you don't have permission**")
        await ctx.send(f"||{ctx.author.mention}||",embed=emb ,ephemeral = True)

    @commands.Cog.listener()
    async def on_mesage(self, message: discord.Message):
        if message.author.bot: return 

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Settings(bot))

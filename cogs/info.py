import discord
from discord import app_commands
from discord.ext import commands
class Disavatar(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    async def display_avatar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != author:
            return await interaction.response.send_message("This avatar is not for you!", ephemeral = True)
        displayAvatar = user.display_avatar.url
        userAvatar = user.avatar.url
        if displayAvatar == userAvatar:
            button.style=discord.ButtonStyle.gray
            await interaction.response.send_message("This user doesn't have a server's avatar.", ephemeral = True)
            return await interaction.message.edit(view = self)
        e = discord.Embed(title = "Server's Profile Avatar Link", url = displayAvatar, color = 0x000000)
        e.set_author(name = user.name, icon_url = userAvatar)
        e.set_image(url = displayAvatar)
        e.set_footer(text = f"requested by {interaction.user}", icon_url = interaction.user.avatar.url)
        view=CCCC()
        await interaction.message.edit(embed = e, view = view)
        await interaction.response.defer()

class CCCC(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Main Avatar", style = discord.ButtonStyle.blurple)
    async def main_avatar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != author:
            return await interaction.response.send_message("This avatar is not for you!", ephemeral = True)
        userAvatar = user.avatar.url
        e = discord.Embed(title = "Avatar Link", url = userAvatar, color = 0x000000)
        e.set_author(name = user.name, icon_url = userAvatar)
        e.set_image(url = userAvatar)
        e.set_footer(text = f"requested by {interaction.user}", icon_url = interaction.user.avatar.url)
        view=Disavatar()
        await interaction.message.edit(embed = e, view = view)
        await interaction.response.defer()

class Serverinfo(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #wakin~
    @commands.Cog.listener()
    async def on_ready(self):
        print("info")


############################   serverinfo    #################################

    @commands.hybrid_command(name="serverinfo", with_app_command=True, description="serverinfo")
    @commands.cooldown(3, 60, commands.BucketType.member)
    async def server(self, ctx: commands.Context):
        embed = discord.Embed(color = 0x2F3136)
        embed.add_field(name = " Server ID", value = ctx.guild.id) 
        embed.add_field(name = "Created On", value = ctx.guild.created_at.strftime('%b %d %Y'))
        embed.add_field(name = "Owner", value = ctx.guild.owner.mention)
        embed.add_field(name = "Members", value = f"{ctx.guild.member_count}")
        embed.add_field(name = f"Channels ({len(ctx.guild.text_channels) + len(ctx.guild.voice_channels)})", value = f"{len(ctx.guild.text_channels)}Text |{len(ctx.guild.voice_channels)}Voice")
        embed.add_field(name = f"Roles ({len(ctx.guild.roles)})", value = "", inline = False)
        embed.set_thumbnail(url = ctx.guild.icon.url)
        embed.set_author(name = ctx.guild.name, icon_url = ctx.guild.icon.url)
        await ctx.send(embed = embed)



    ############################   channel    #################################

    @commands.hybrid_command(name="channel", with_app_command=True, description="channel")
    @commands.cooldown(3, 60, commands.BucketType.member)
    async def launch(self, ctx: commands.Context):
        name = str(ctx.guild.name)
        embed = discord.Embed(title = name, color = 15548997)
        embed.add_field(name = "**channel**", value = f"> {len(ctx.guild.text_channels)} Text | {len(ctx.guild.voice_channels)} Voice", inline = True)
        await ctx.send(embed=embed)  




############################   userinfo    #################################
    @commands.hybrid_command(name="user", with_app_command=True, description="userinfo")
    @commands.cooldown(3, 60, commands.BucketType.member)
    async def user(self, ctx: commands.Context, member: discord.Member = None):
        if member is None: member = ctx.author
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = discord.Embed(description = member.mention, color= 11342935 )
        embed.set_author(name = str(member), icon_url = member.avatar.url)
        embed.set_thumbnail(url = member.avatar.url)
        embed.add_field(name = "**تایم جوین**", value = f"> {member.joined_at.strftime(date_format)}")
        members = sorted(ctx.guild.members, key = lambda m: m.joined_at)
        embed.add_field(name = "**تایم ساخت اکانت**", value = f"> {member.created_at.strftime(date_format)}")
        embed.add_field(name="Top role:", value=member.top_role.mention)
        if len(member.roles) > 1:
            role_string = ' '.join([r.mention for r in member.roles][1:])
            embed.add_field(name = "**Roles ||[{}]||**".format(len(member.roles)-1), value = f"", inline = False)
        embed.set_footer(text = 'ID:' + str(member.id))
        await ctx.send(embed = embed)


############################   avatar    #################################
    @commands.hybrid_command(name="avarat", with_app_command=True, description="get avatar")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    async def avatar(self, ctx: commands.Context, member: discord.Member = None):
        if not member: member = ctx.author
        userAvatar = member.avatar.url
        e = discord.Embed()
        e.set_author(name = member.name, icon_url = userAvatar)
        e.set_image(url = userAvatar)
        global user
        global author
        user = member
        author = ctx.author
        view = Disavatar()
        await ctx.send(embed = e, view = view)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Serverinfo(bot))

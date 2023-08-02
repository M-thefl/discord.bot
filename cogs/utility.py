import discord
from discord import app_commands
from discord.ext import commands


class pollButtons(discord.ui.View):
    def __init__(self, *, timeout = None):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Yes", style = discord.ButtonStyle.green, emoji = "🚩")
    async def poll_yes_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        global upvotes, downvotes, yes_pollers, no_pollers
        if interaction.user in yes_pollers:
            upvotes = upvotes - 1
            yes_pollers.remove(interaction.user)
            await interaction.response.send_message("Done", ephemeral = True)
        elif interaction.user in no_pollers:
            downvotes = downvotes - 1
            no_pollers.remove(interaction.user)
            upvotes = upvotes + 1
            yes_pollers.append(interaction.user)
            await interaction.response.send_message("Done", ephemeral = True)
        else:
            upvotes = upvotes + 1
            yes_pollers.append(interaction.user)
            await interaction.response.send_message("Done", ephemeral = True)
        emb = discord.Embed(title = poll_title, description = poll_description)
        emb.set_author(name = f"Poll by {poll_author}", icon_url = poll_avatar)
        emb.set_footer(text = f"{upvotes} Yes | {downvotes} No")
        view = pollButtons()
        await interaction.message.edit(embed = emb, view = view)
    @discord.ui.button(label = "No", style = discord.ButtonStyle.green, emoji = "🚩")
    async def sugg_downvote(self, interaction: discord.Interaction, button: discord.ui.Button):
        global upvotes, downvotes, no_pollers, yes_pollers
        if interaction.user in no_pollers:
            downvotes = downvotes - 1
            no_pollers.remove(interaction.user)
            await interaction.response.send_message("Done", ephemeral = True)
        elif interaction.user in yes_pollers:
            upvotes = upvotes - 1
            yes_pollers.remove(interaction.user)
            downvotes = downvotes + 1
            no_pollers.append(interaction.user)
            await interaction.response.send_message("Done", ephemeral = True)
        else:
            downvotes = downvotes + 1
            no_pollers.append(interaction.user)
            await interaction.response.send_message("Done", ephemeral = True)
        emb = discord.Embed(title = poll_title, description = poll_description)
        emb.set_author(name = f"Poll by {poll_author}", icon_url = poll_avatar)
        emb.set_footer(text = f"{upvotes} Yes | {downvotes} No")
        view = pollButtons()
        await interaction.message.edit(embed = emb, view = view)

class Invite(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)


class Vote(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)


class Utility(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Utility")

############################   ping bot    #################################
    @commands.hybrid_command(name="ping", with_app_command=True, description="ping")
    @commands.cooldown(3, 60, commands.BucketType.member)
    async def ping(self, ctx: commands.Context):
     await ctx.send(f"\n{round(self.bot.latency * 1000)}ms")


############################   developer info    #################################

    @commands.hybrid_command(name="root", with_app_command=True, description="developer info")
    @commands.cooldown(3, 60, commands.BucketType.member)
    async def vote(self, ctx: commands.Context):
        view = Vote()
        view.add_item(discord.ui.Button(label = "discord", style = discord.ButtonStyle.link, url = "https://discord.gg/021"))
        emb = discord.Embed(title = "**information**", description = "Developer: Mahbodfl\nGithub: https://github.com/M-thefl\n\ndiscord.gg/021")
        emb.set_thumbnail(url="https://i.pinimg.com/1200x/93/1b/a7/931ba7aeb922938c5f61d261433e1d74.jpg")
        await ctx.send(embed = emb, view = view)

############################   serverlink    #################################

    @commands.hybrid_command(name="server", with_app_command=True, description="server.link")
    @commands.cooldown(3, 60, commands.BucketType.member)
    async def launch(self, ctx: commands.Context):
        name = str(ctx.guild.name)
        icon = str(ctx.guild.icon.url)
        link = await ctx.channel.create_invite(max_age = 300)
        embed = discord.Embed(title = name, color = 15418782)
        embed.set_thumbnail(url = icon)
        embed.add_field(name = "این لینک خراب نمیشه", value = link, inline = True)
        member = 0
        await ctx.send(embed=embed)

############################   poll    #################################


    @app_commands.command(name = "poll", description = "poll")
    @app_commands.default_permissions(administrator = True)
    @app_commands.describe(title = "تایتل", description = "متن")
    @app_commands.checks.cooldown(1, 10, key = lambda i: (i.user.id))
    @app_commands.checks.has_permissions(manage_messages = True)
    async def poll(self, interaction: discord.Interaction, title: str, description: str):
        global poll_title, poll_description, poll_author, poll_avatar, upvotes, downvotes, yes_pollers, no_pollers
        yes_pollers = []
        no_pollers = []
        upvotes = 0
        downvotes = 0
        poll_title = title
        poll_description = description
        poll_author = interaction.user
        poll_avatar = interaction.user.avatar.url
        view = pollButtons()
        emb = discord.Embed(title = poll_title, description = poll_description)
        emb.set_footer(text = f"{upvotes} Yes | {downvotes} No")
        await interaction.response.send_message(embed = emb, view = view)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Utility(bot))

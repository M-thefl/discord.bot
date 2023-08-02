import sqlite3
from discord import  app_commands
from discord.ext import commands
import discord
import aiosqlite
import os
from discord.ext import commands
import discord.utils
import math
from asyncio import *
from discord.ext.commands.errors import DisabledCommand
from dotenv import load_dotenv
load_dotenv()
colors = [7419530,]
####################################################################################################################################################################################
class MyBot(commands.Bot):

    def __init__(self):

        super().__init__(command_prefix ='e!', #perfix
                         intents = discord.Intents.all(),
                         case_insensitive=True,
                         application_id = 1110278647555829780)  # id Bot
        self.initial_extensions = [
            "cogs.ticket",
            "cogs.info",
            "cogs.fun",
            "cogs.mod",
            "cogs.utility",
            "cogs.server",
            "cogs.help",
            ]
    async def setup_hook(self):
        for cogs in self.initial_extensions: 
            await self.load_extension(cogs)
        await self.tree.sync()
        print(f"Synced for {self.user}!")

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        if  self.added:
            await self.change_presence(activity = discord.Game(name = "e!help"))
            self.added = True

bot = MyBot()
bot.remove_command("help")
##########################  Welcome mesaage   ####################################
@bot.event
async def on_member_join(member):
    members = 0
    for guild in bot.guilds:
        members += guild.member_count - 1
    server = bot.get_guild(813695586653700096) # server id
    welcome1_channel = server.get_channel(1127001708728430684) # channel id
    embed1 = discord.Embed(title='Welcome\n', description=f'\n\n **👋〢 Hey {member} Welcome To Server**\n **📜〢 Please Follow The ~~Rules~~**\n **👥 〢 Member Count: {members}**', color = 00000) 
    embed1.set_author(name = str(member), icon_url = member.avatar.url)
    embed1.set_thumbnail(url="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e7e3020a-80fc-4574-9164-f7fa9c38df99/d269z23-ea8c90a9-37d6-4b9a-ad8a-01f9679a3b30.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcL2U3ZTMwMjBhLTgwZmMtNDU3NC05MTY0LWY3ZmE5YzM4ZGY5OVwvZDI2OXoyMy1lYThjOTBhOS0zN2Q2LTRiOWEtYWQ4YS0wMWY5Njc5YTNiMzAuanBnIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.Lo_KPepxhNQR4uWBGiKqG8RYdxm4_DuPZYEWJHWDNxM")
    embed1.set_footer(text='ᴇxᴇ ᴄᴏᴍᴘᴀɴʏ')
    await welcome1_channel.send(f"||{member.mention}||",embed=embed1)
    await member.send(f"**Developer server \n discord.gg/021**")
#############################   connect voice channel   #################################
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    voice_channel_id = 1126290562098663505  
    voice_channel = bot.get_channel(voice_channel_id)

    if voice_channel is not None:
        if bot.voice_clients:
            await bot.voice_clients[0].move_to(voice_channel)
        else:
            await voice_channel.connect()
    else:
        print(f"Voice channel with ID {voice_channel_id} not found.")
############################   permission    #################################
class errorButtons(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout = timeout)
    @discord.ui.button(label = "Yes", style = discord.ButtonStyle.green)
    async def edits_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        await error_channel.send(error_message)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.send_message("Error")
    @discord.ui.button(label = "No", style = discord.ButtonStyle.red)
    async def edits_cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != interaction.message.interaction.user: return await interaction.response.send_message("This is not for you!", ephemeral = True)
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.send_message("Cancelled.")

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        cool_error = discord.Embed(title = f"آروم باش دوست عزیز یواش یواش", description = f"صبر داشته باش{error.retry_after:.2f}s.", colour = discord.Colour.light_grey())
        await interaction.response.send_message(embed = cool_error, ephemeral = True)
    elif isinstance(error, app_commands.MissingPermissions):
        missing_perm = error.missing_permissions[0].replace("_", " ").title()
        per_error = discord.Embed(title = f"دوست عزیز شما پرم نداری",)
        await interaction.response.send_message(embed = per_error, ephemeral = True)
    elif isinstance(error, app_commands.BotMissingPermissions):
        missing_perm = error.missing_permissions[0].replace("_", " ").title()
        per_error = discord.Embed(title = f"من پرمیشن کافی ندارم", description = f"I don't have {missing_perm} permission.", colour = discord.Colour.light_grey())
        await interaction.response.send_message(embed = per_error, ephemeral = True)
    else:
        global error_message, error_channel
        error_message = error
        error_channel = bot.get_channel(int(os.getenv("ERROR_CHANNEL_ID")))
        embed = discord.Embed(title = "Error",
                            description = f"باگ",
                            color = discord.Color.red())
        await interaction.response.send_message(embed = embed, view = errorButtons())
        raise error
############################   sql | Log    #################################
@bot.event
async def on_guild_remove(guild: discord.Guild):
   
    async with aiosqlite.connect("tickets_role.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS roles (role INTEGER, guild ID)")
            await cursor.execute("SELECT role FROM roles WHERE guild = ?", (guild.id,))
            data = await cursor.fetchone()
            if data: await cursor.execute("DELETE FROM roles WHERE guild = ?", (guild.id,))
        await db.commit()
    async with aiosqlite.connect("suggestions.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS channels (sugg_channel INTEGER, rev_channel INTEGER, guild ID)")
            await cursor.execute("SELECT sugg_channel AND rev_channel FROM channels WHERE guild = ?", (guild.id,))
            data = await cursor.fetchone()
            if data: await cursor.execute("DELETE FROM channels WHERE guild = ?", (guild.id,))
        await db.commit()
    async with aiosqlite.connect("antispam.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS antispam (switch INTEGER, punishment STRING, whitelist STRING, guild ID)")
            await cursor.execute("SELECT switch FROM antispam WHERE guild = ?", (guild.id,))
            data = await cursor.fetchone()
            if data: await cursor.execute("DELETE FROM antispam WHERE guild = ?", (guild.id,))
        await db.commit()
    logs_files_list = ["joins", "leaves", "messages_edits", "messages_deletes", "role_create", "role_delete", "role_updates", "role_given", "role_remove",
                      "channel_create", "channel_delete", "channel_updates", "member_ban", "member_unban", "member_timeout" ,"nickname_change", "server_updates"]
    for log_file in logs_files_list:
        async with aiosqlite.connect(f"log_{log_file}.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS log (channel INTEGER, guild ID)")
                await cursor.execute("SELECT channel FROM log WHERE guild = ?", (guild.id,))
                data = await cursor.fetchone()
                if data: await cursor.execute("DELETE FROM log WHERE guild = ?", (guild.id,))
            await db.commit()
############################   Level    #################################
db = sqlite3.connect("levels.db")
cursor = db.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS levels (user_id INTEGER PRIMARY KEY, xp INTEGER, level INTEGER)"
)
db.commit()

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    xp_earned = 10
    user_id = message.author.id

    cursor.execute("SELECT xp, level FROM levels WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    if result is None:
        cursor.execute("INSERT INTO levels (user_id, xp, level) VALUES (?, ?, ?)", (user_id, xp_earned, 1))
    else:
        xp, level = result
        xp += xp_earned
        new_level = int(0.1 * math.sqrt(xp))
        if new_level > level:
            levelup_message = f"**Nice, {message.author.mention}!,you just advanced to leve {new_level}!**🚀"
            await message.channel.send(levelup_message)

        cursor.execute("UPDATE levels SET xp = ?, level = ? WHERE user_id = ?", (xp, new_level, user_id))

    db.commit()
    await bot.process_commands(message)

@bot.command()
async def level(ctx):
    user_id = ctx.author.id
    cursor.execute("SELECT xp, level FROM levels WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    if result is None:
        await ctx.send("You haven't earned any XP yet!")
    else:
        xp, level = result
        await ctx.send(f"** Level {level} | {xp} XP.**")

bot.run(os.getenv("TOKEN"))
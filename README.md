# Discord Bot| Tickets｜welcome｜voice channel｜Moderation | level

# Installation Guide
Create a new bot from https://discord.com/developers/applications and copy your bot token and application ID

``Install python 3.8 or higher ``

```git clone https://github.com/M-thefl/Sinco_Bot_persianbot.git```

```cd Sinco_Bot_persianbot```

Install modules</p>
```pip install -r requirements.txt```

# Run the bot

‍```Paste your token in the .env file```‍‍</p>
```Paste your bot id in the main.py file```</p>
```python main.py```</p>

# settings for bot 

```set CATEGORY for ticket [ticket.py] ```</p>
```python
import discord
from discord.ext import commands 
from datetime import datetime
import aiosqlite

CATEGORY_ID = 000000000  

class ticket_launcher(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 600, commands.BucketType.member)
```

```connect voice channel [main.py] ```</p>

```python
bot.event
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
```
```Welcome mesaage [main.py] ```
```python
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
```


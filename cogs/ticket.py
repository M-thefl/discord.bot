import discord
from discord.ext import commands 
from datetime import datetime
import aiosqlite

CATEGORY_ID = 000000000  

class ticket_launcher(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 600, commands.BucketType.member)

    @discord.ui.button(label="Create Ticket", style=discord.ButtonStyle.blurple, custom_id="ticket_button", emoji="🚀")
    async def ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        ticket = discord.utils.get(interaction.guild.text_channels, name=f"ticket-{interaction.user.name.lower().replace(' ', '-')}")
        if ticket is not None:
            await interaction.response.send_message(f"ticket baz shode darid {ticket.mention}!", ephemeral=True)
        else:
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                interaction.user: discord.PermissionOverwrite(view_channel=True, read_message_history=True, send_messages=True, attach_files=True, embed_links=True),
                interaction.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)
            }
            async with aiosqlite.connect("tickets_role.db") as db:
                async with db.cursor() as cursor:
                    await cursor.execute("CREATE TABLE IF NOT EXISTS roles (role INTEGER, guild ID)")
                    await cursor.execute("SELECT role FROM roles WHERE guild = ?", (interaction.guild.id,))
                    data = await cursor.fetchone()
                    if data:
                        ticket_role = data[0]
                    else:
                        ticket_role = None
            if not ticket_role == None:
                ticket_role = interaction.guild.get_role(ticket_role)
                overwrites[ticket_role] = discord.PermissionOverwrite(view_channel=True, read_message_history=True, send_messages=True, attach_files=True, embed_links=True)
                ticket_sentence = f"{ticket_role.mention}, ||{interaction.user.mention}||\nTicket opened"
            else:
                ticket_sentence = f"||{interaction.user.mention}||\n**تیکت شما با موفقیت باز شد**"

            category = discord.utils.get(interaction.guild.channels, id=CATEGORY_ID)
            if category:
                channel = await interaction.guild.create_text_channel(name=f"ticket-{interaction.user.name}", overwrites=overwrites, topic=f"{interaction.user.id}", category=category)
                await channel.send(ticket_sentence, view=main())
                await interaction.response.send_message(f"Ticket opened {channel.mention}", ephemeral=True)
            else:
                await interaction.response.send_message("Category not found. Please set the correct CATEGORY_ID in the code.", ephemeral=True)

class main(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.gray, custom_id="close")
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        ticket_creator_id = int(interaction.channel.topic)
        ticket_creator = interaction.guild.get_member(ticket_creator_id)

        await interaction.channel.set_permissions(ticket_creator, send_messages=False, read_messages=False, add_reactions=False,
                                                  embed_links=False, attach_files=False, read_message_history=False,
                                                  external_emojis=False)

        await interaction.response.send_message('تیکت بسته شد', ephemeral=True)

class Ticket(commands.Cog, name="ticket"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Ticket")

    @commands.hybrid_command(name="ticket", with_app_command=True, description="ticket")
    @commands.has_permissions(administrator = True)
    @commands.cooldown(3, 60, commands.BucketType.member)
    async def launch(self, ctx: commands.Context):
        embed = discord.Embed(title="Ticket", description="If you have any questions, you can click the button below.\nThank you! 🌟", color=000000)
        embed.set_thumbnail(url="https://gifdb.com/images/high/dark-trippy-tunnel-rqdgp7elrp3yu6pb.gif")
        await ctx.send(embed=embed, view=ticket_launcher())

    @launch.error
    async def launch_error(self,ctx: commands.Context,error):
     if isinstance(error, commands.MissingPermissions):
        member = 0
        emb = discord.Embed(description=  "**you don't have permission**")
        await ctx.send(f"||{ctx.author.mention}||",embed=emb ,ephemeral = True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ticket(bot))

import discord
from discord import app_commands
from discord.ext import commands


class Sever(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="sever_list",description = "列出機器人所在伺服器")
    async def sever_list(self, interaction: discord.Interaction,):
        if interaction.user.id == 710128890240041091 or 1022588836032806993 or 906188519083491359 or 1158951186452451440:
            await interaction.response.send_message('伺服器列表:')
            guilds = self.bot.guilds
            for guild in guilds: 
                invites = await guild.invites()
                if invites:
                    invite_url = invites[0].url
                    await interaction.followup.send(f"Invite for {guild.name}: {invite_url}")
                else:
                    await interaction.followup.send(f"No invite found for {guild.name}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Sever(bot),guild = discord.Object(id = 1213748875471364137))
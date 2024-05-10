import datetime
import discord
from discord import app_commands
from discord.ext import commands
import asyncio

class Mute(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = "mute", description = "禁言在語音頻道的使用者")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def mute(self,interaction: discord.Interaction, user: discord.Member, duration: int):
        await user.edit(mute=True)
        await interaction.response.send_message(f"{user.mention} 已被禁言 {duration} 秒")
        await asyncio.sleep(duration)
        await user.edit(mute=False)
        await interaction.followup.send(f"{user.mention} 禁言已解除")

    @app_commands.command(name = "timeout", description = "禁言使用者")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def timeout(self,interaction: discord.Interaction, user: discord.Member, duration: int):
        await user.edit(timed_out_until=discord.utils.utcnow() + datetime.timedelta(minutes=duration))
        await interaction.response.send_message(f"{user.mention} 已被禁言 {duration} 秒")
        await asyncio.sleep(duration)
        await interaction.followup.send(f"{user.mention} 禁言已解除")

    @app_commands.command(name = "outtimeout", description = "解禁使用者")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def outtimeout(self,interaction: discord.Interaction, user: discord.Member):
        await user.edit(timed_out_until=discord.utils.utcnow())
        await interaction.followup.send(f"{user.mention} 禁言已解除")

    

async def setup(bot: commands.Bot):
    await bot.add_cog(Mute(bot))

# timed_out_until=discord.utils.utcnow() + datetime.timedelta(minutes=minutes))
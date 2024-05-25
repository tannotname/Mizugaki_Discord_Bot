import datetime
import discord
from discord import app_commands
from discord.ext import commands
import asyncio


class Messagecommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.user_menu = app_commands.ContextMenu(
            name='User Info',
            callback=self.user_info
        )
        self.bot.tree.add_command(self.user_menu)

        # Message context menu
        self.message_menu = app_commands.ContextMenu(
            name="標雷諾",
            callback=self.message_info
        )
        self.bot.tree.add_command(self.message_menu)

        self.message_menu = app_commands.ContextMenu(
            name="測試",
            callback=self.test
        )
        self.bot.tree.add_command(self.message_menu)


    async def user_info(self, interaction: discord.Interaction, user: discord.User):
        """Handle the user context menu action."""
        await interaction.response.send_message(f'User: {user.name}\nID: {user.id}')

    async def message_info(self, interaction: discord.Interaction, message: discord.Message):
        if interaction.guild.id == 1213748875471364137:
            await message.reply("<@557540063525994496>",mention_author=False)
            await interaction.response.send_message("已執行命令",ephemeral=True)
        else:
            await interaction.response.send_message("此伺服器不支援此命令",ephemeral=True)

    async def test(self, interaction:discord.Interaction,message:discord.Message):
        await message.reply("測試",mention_author=False)
        await interaction.response.send_message("已執行命令",ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Messagecommand(bot))



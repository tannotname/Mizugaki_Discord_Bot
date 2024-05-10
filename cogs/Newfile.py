import discord
from discord.ext import commands
from discord import app_commands

class Newfile(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="upcogspy",description = "上傳指令檔案至cogs")
    async def upcogspy(self, interaction: discord.Interaction, cogsname: str,cogsfile:discord.Attachment):
        if interaction.user.id == 710128890240041091:
            await interaction.response.send_message("認證權限通過")
            attachment = cogsfile
            # 保存文件到指定位置
            await attachment.save('C:\\Users\\曉黑\\Desktop\\DISCORDBOTmain\\cogs\\{}'.format(attachment.filename))
            await interaction.response.send_message(F'文件{cogsname}已保存至指定位置！')
        elif interaction.user.id != 710128890240041091:
            await interaction.response.send_message("你沒有權限進行此命令")

async def setup(bot: commands.Bot):
    await bot.add_cog(Newfile(bot)) # ,guild = discord.Object(id = 1213748875471364137)
import discord
from discord import app_commands
from discord.ext import commands
from PIL import Image
import os



class Messagecommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.message_menu = app_commands.ContextMenu(
            name="翻轉圖片",
            callback=self.rotate
        )
        self.bot.tree.add_command(self.message_menu)

    async def rotate(self, interaction:discord.Interaction,message:discord.Message):
        try:
            if message.attachments:
                for attachment in message.attachments:
                    try:
                        await attachment.save(f'pho\\{attachment.filename}')
                    except Exception as e:
                        await interaction.response.send_message(f"發生儲存錯誤:{e}",ephemeral=True)
                        return
                    try:
                        os.chdir('pho\\')
                    except Exception as e:
                        await interaction.response.send_message(f"發生開啟錯誤:{e}",ephemeral=True)
                    img = Image.open(f'{attachment.filename}')
                    img_r1 = img.rotate(90,expand=1)
                    img_r1.save(f'pho\\{attachment.filename}')
                    await message.reply(file=discord.File(f'pho\\{attachment.filename}'),mention_author=False)
                    os.remove(f'{attachment.filename}') 
                    await interaction.response.send_message("已執行命令",ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"發生錯誤:{e}",ephemeral=True)



async def setup(bot: commands.Bot):
    await bot.add_cog(Messagecommand(bot))



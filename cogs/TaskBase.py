import time
import discord
from discord.ext import commands
from discord.ext import tasks
from discord import app_commands
from dotenv import load_dotenv
import os

error_channel = 1273144773435326545

class TaskBase(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # 開始執行函式
        self.count.start()
        self.start_time = time.time()

    def cog_unload(self):
        # 取消執行函式
        self.count.cancel()

    # 定義要執行的循環函式
    @tasks.loop(seconds = 6)
    async def count(self):
        try:
            execution_time = int(time.time() - self.start_time)
            # 偵測所在伺服器數
            guildssum = len(self.bot.guilds)
            # 偵測使用者人數
            guilds = self.bot.guilds
            count=0
            for guild in guilds:
                count += guild.member_count
            # 等待bot ready
            await self.bot.wait_until_ready()
            # 變更bot狀態
            slash = await self.bot.tree.sync()
            await self.bot.change_presence(activity=discord.Game(name=f"/help|服務 {guildssum} 個伺服器|{count} 位使用者|載入{len(slash)}個指令中"))
            
        except Exception as erro:
            # 錯誤輸出
            print(erro)
            channel = self.bot.get_channel(error_channel)
            await channel.send(f"# 機器人狀態報錯\n>錯誤:{erro}")

            
    @app_commands.command(name = "set_online", description = "重設機器人狀態")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_online(self, interaction: discord.Interaction):
        try:
            guildssum = len(self.bot.guilds)
            # 偵測使用者人數
            slash = await self.bot.tree.sync()
            guilds = self.bot.guilds
            count=0
            for guild in guilds:
                count += guild.member_count
            await self.bot.change_presence(activity=discord.Game(name=f"/help|服務{guildssum}個伺服器|{count}位使用者|載入{len(slash)}個指令中"))
            await interaction.response.send_message(f"已設定bot狀態為 /help|服務{guildssum}個伺服器|{count}位使用者|載入{len(slash)}個指令中")
        except Exception as e:
            await interaction.response.send_message(f"發生錯誤:{e}",ephemeral=True)
            channel = self.bot.get_channel(error_channel)
            await channel.send(f"# 機器人狀態報錯\n>錯誤:{e}")

# Cog 載入 Bot 中
async def setup(bot: commands.Bot):
    await bot.add_cog(TaskBase(bot))
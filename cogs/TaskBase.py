import time
import discord
from discord.ext import commands
from discord.ext import tasks
from discord import app_commands

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
        execution_time = int(time.time() - self.start_time)
        # 偵測所在伺服器數
        guilds = len(self.bot.guilds)
        # 偵測使用者人數
        count = sum(len(guild.members) for guild in self.bot.guilds)
        try:
            # 等待bot ready
            await self.bot.wait_until_ready()
            # 變更bot狀態
            slash = await self.bot.tree.sync()
            await self.bot.change_presence(activity=discord.Game(name=f"載入 {len(slash)} 個斜線指令"))
            
        except Exception as erro:
            # 錯誤輸出
            print(erro)



        


    @app_commands.command(name = "delete_online", description = "清除機器人狀態")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def delete_online(self, interaction: discord.Interaction):
        await self.bot.change_presence(activity=None)
        await interaction.response.send_message("已清除狀態")

# Cog 載入 Bot 中
async def setup(bot: commands.Bot):
    await bot.add_cog(TaskBase(bot),guild = discord.Object(id = 1213748875471364137))
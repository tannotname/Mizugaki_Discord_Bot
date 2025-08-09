import random
import discord
from discord.ext import commands
from discord import app_commands
from discord.ext import commands
import sqlite3


class Voicenew_2(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("已載入動態語音模組_2")

    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if (before.channel is not None and after.channel is None) or (before.channel != after.channel and before.channel is not None):
            try:
                # 連接
                conn = sqlite3.connect("voicenew.db")
                cursor = conn.cursor()
                # 查詢
                cursor.execute("SELECT * FROM newchannel") # 檢查所有頻道是否有被刪除
                rows = cursor.fetchall()
                for row in rows:
                    channel_id = int(row[1])
                    channel = self.bot.get_channel(channel_id)
                    channel_name = channel.name
                    if channel is None:
                        cursor.execute("DELETE FROM newchannel WHERE channelid=?", (channel_id,))
                    elif len(channel.members) == 0: # 檢查channel.members是否為空
                        await channel.delete() # 刪除channel
                        print(f"頻道 {channel.name} 已被刪除")
                        cursor.execute("DELETE FROM newchannel WHERE channelid=?", (channel_id,)) # 刪除資料庫中資料
                conn.commit()
                cursor.close()
                conn.close()

                # 刪除監測討論串資料刪除
                conn = sqlite3.connect("voice_surveillanc.db")
                cursor = conn.cursor()
                channel = self.bot.get_channel(channel_id)
                if channel is None:
                    cursor.execute("DELETE FROM voice_surveillanc WHERE surveillanc_channel_id=?", (channel_id,)) # 刪除資料庫中資料
                    print(f"監測討論串 {channel_name} 登記資料已被刪除")
                conn.commit()
                cursor.close()
                conn.close()
            except sqlite3.Error as e:
                print(f"資料庫連接時發生錯誤4: {e}")


        

async def setup(bot: commands.Bot):
    await bot.add_cog(Voicenew_2(bot))
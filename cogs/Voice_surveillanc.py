import random
import sqlite3
import discord
from discord.ext import commands
from discord import app_commands


def voice_surveillanc():
    #drop table 
    con = sqlite3.connect('voice_surveillanc.db') # 連線資料庫
    cur = con.cursor() # 建立游標
    # 查詢第一筆資料
    cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?", ("voice_surveillanc",))
    row = cur.fetchone()[0]
        # 查詢資料庫是否存在
    if row == 0:
        cur.execute("CREATE TABLE voice_surveillanc(surveillanc_guild_name TEXT,surveillanc_guild_id NUMERIC,surveillanc_channel_id NUMERIC,surveillanc_reply_channel_id NUMERIC)")
        con.commit()
        print("表格 'voice_surveillanc' 已建立.")
    else:
        print("表格“voice_surveillanc”已存在.")
        con.commit()

class Voice_surveillanc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self,message:discord.Message):
    #排除自己的訊息，避免陷入無限循環
        if message.author == self.bot.user:
            return


            # 獲取要發言的頻道
        if message.channel.type == discord.ChannelType.voice:

                try:
                    can = sqlite3.connect("voice_surveillanc.db")
                    car = can.cursor()
                    car.execute("SELECT * FROM voice_surveillanc WHERE surveillanc_channel_id=?",(message.channel.id,))
                    rows = car.fetchall()
                    can.commit()
                except sqlite3.Error as e:
                    channel = self.bot.get_channel(1273144773435326545)
                    await channel.send(f"{message.guild.name} {message.author.name} 監測錯誤:{e}")
                for row in rows:
                    channelid = row[3]
                    channel = self.bot.get_channel(channelid)
                    await channel.send(f"# 監測訊息\n```\n發言人:{message.author.name}({message.author.nick if message.author.nick else message.author.name})\n發言頻道:{message.channel}\n發言內容:\n{message.content}\n```")
    
    @commands.Cog.listener()
    async def on_message_edit(self,before: discord.Message, after: discord.Message):
        if before.author == self.bot.user:
            return
        if before.author.bot:
            return
        try:
           if before.channel.type == discord.ChannelType.voice:

                try:
                    can = sqlite3.connect("voice_surveillanc.db")
                    car = can.cursor()
                    car.execute("SELECT * FROM voice_surveillanc WHERE surveillanc_channel_id=?",(before.channel.id,))
                    rows = car.fetchall()
                    can.commit()
                except sqlite3.Error as e:
                    channel = self.bot.get_channel(1273144773435326545)
                    await channel.send(f"{before.guild.name} {before.author.name} 監測錯誤:{e}")
                for row in rows:
                    channelid = row[3]
                    channel = self.bot.get_channel(channelid)
                    await channel.send(f"# 監測更改訊息\n```\n更改人:{before.author.name}({before.author.nick if before.author.nick else before.author.name})\n訊息更改頻道:{before.channel}\n更改前訊息內容:\n{before.content}\n更改後訊息內容:\n{after.content}\n```")
                    if before.attachments:
                        for attachment in before.attachments:
                            await channel.send(file=discord.File(f'pho\\{attachment.filename}'))
        except Exception as e:
            channel = self.bot.get_channel(1273144773435326545)
            await channel.send(f"{before.guild.name} {before.author.name} 修改監測錯誤:{e}")
            
    @commands.Cog.listener()
    async def on_message_delete(self,message: discord.Message):
        if message.author == self.bot.user:
            return
        if message.author.bot:
            return
        try:
           if message.channel.type == discord.ChannelType.voice:

                try:
                    can = sqlite3.connect("voice_surveillanc.db")
                    car = can.cursor()
                    car.execute("SELECT * FROM voice_surveillanc WHERE surveillanc_channel_id=?",(message.channel.id,))
                    rows = car.fetchall()
                    can.commit()
                except sqlite3.Error as e:
                    channel = self.bot.get_channel(1273144773435326545)
                    await channel.send(f"{message.guild.name} {message.author.name} 監測錯誤:{e}")
                for row in rows:
                    channelid = row[3]
                    channel = self.bot.get_channel(channelid)
                    await channel.send(f"# 監測刪除訊息\n```\n刪除訊息之使用者:{message.author.name}({message.author.nick if message.author.nick else message.author.name})\n刪除訊息頻道:{message.channel}\n刪除內容:\n{message.content}\n```")
                    if message.attachments:
                        for attachment in message.attachments:
                            await channel.send(file=discord.File(f'pho\\{attachment.filename}'))
        except Exception as e:
            channel = self.bot.get_channel(1273144773435326545)
            await channel.send(f"{message.guild.name} {message.author.name} 刪除監測錯誤:{e}")


async def setup(bot: commands.Bot):
    voice_surveillanc()
    await bot.add_cog(Voice_surveillanc(bot))
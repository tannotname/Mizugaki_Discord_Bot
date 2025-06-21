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

    @app_commands.command(name="voice_surveillanc_set",description="將選擇的語音頻到納入監測範圍")
    @app_commands.checks.has_permissions(administrator=True)    
    async def voice_surveillanc_set(self,interaction:discord.Interaction,set_channel:discord.VoiceChannel):
        try:
            guild = interaction.guild
            user = interaction.user
            conn = sqlite3.connect('voice_monitor_channel.db') # 將創建的語音頻道寫入資料庫
            comn = conn.cursor()
            comn.execute("SELECT * FROM voice_monitor_channel WHERE server_id=?",(guild.id,)) # 搜尋伺服器設定的監測頻道
            rows = comn.fetchall()
            conn.commit()
            comn.close()
            conn.close()
        except sqlite3.Error as e:
            channel = self.bot.get_channel(1273144773435326545)
            await channel.send(f"{guild.name} {user.name} 資料連接錯誤:{e}")
        try:
            for row in rows:
                if row is None:
                    return
                elif row != None:
                    channel = self.bot.get_channel(row[3])
                    print(row[3])
                    new_channel = await channel.create_thread(name=f"{set_channel.name}", type=discord.ChannelType.public_thread)
                    try:
                        conn = sqlite3.connect("voice_surveillanc.db")
                        comn = conn.cursor()
                        comn.execute("INSERT INTO voice_surveillanc (surveillanc_guild_name,surveillanc_guild_id,surveillanc_channel_id,surveillanc_reply_channel_id) VALUES (?,?,?,?)", (new_channel.guild.name,new_channel.guild.id,set_channel.id,new_channel.id))
                        conn.commit() # 將創建的語音頻道寫入監測資料庫
                        comn.close()
                        conn.close()
                    except sqlite3.Error as e:
                        channel = self.bot.get_channel(1273144773435326545)
                        await channel.send(f"{guild.name} {user.name} 資料連接錯誤:{e}")
            await interaction.response.send_message("已執行命令",ephemeral=True)
        except Exception as e:
            channel = self.bot.get_channel(1273144773435326545)
            await channel.send(f"{guild.name} {user.name} 資料連接錯誤:{e}")
    
    
    
    
    
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
                    random7_int = random.randint(0, 255)
                    random8_int = random.randint(0, 255)
                    random9_int = random.randint(0, 255)
                    if message.author.color is not None:
                        emb_color = message.author.color
                    elif message.author.color is None:
                        emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
                    embed = discord.Embed(title="訊息", description=message.content, color= emb_color)
                    embed.set_author(name= f"{message.author.name}",  icon_url= message.author.avatar.url)#作者
                    await channel.send(embed=embed)
                    if message.attachments:
                        for attachment in message.attachments:
                            await channel.send(file=discord.File(f'pho\\{attachment.filename}'))
                    if message.stickers:
                        for sticker in message.stickers:
                            await channel.send(sticker.url)

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
                    random7_int = random.randint(0, 255)
                    random8_int = random.randint(0, 255)
                    random9_int = random.randint(0, 255)
                    if before.author.color is not None:
                        emb_color = before.author.color
                    elif before.author.color is None:
                        emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
                    embed = discord.Embed(title="修改訊息", description=before.content, color= emb_color)
                    embed.set_author(name= f"{before.author.name}",  icon_url= before.author.avatar.url)#作者
                    embed.add_field(name="修改後:",value=after.content,inline=False)
                    await channel.send(embed=embed)
                    if before.attachments:
                        for attachment in before.attachments:
                            await channel.send(file=discord.File(f'pho\\{attachment.filename}'))
                    if before.stickers:
                        for sticker in before.stickers:
                            await channel.send(sticker.url)
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
                    random7_int = random.randint(0, 255)
                    random8_int = random.randint(0, 255)
                    random9_int = random.randint(0, 255)
                    if message.author.color is not None:
                        emb_color = message.author.color
                    elif message.author.color is None:
                        emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
                    embed = discord.Embed(title="刪除訊息", description=message.content, color= emb_color)
                    embed.set_author(name= f"{message.author.name}",  icon_url= message.author.avatar.url)#作者
                    await channel.send(embed=embed)
                    if message.attachments:
                        for attachment in message.attachments:
                            await channel.send(file=discord.File(f'pho\\{attachment.filename}'))
                    if message.stickers:
                        for sticker in message.stickers:
                            await channel.send(sticker.url)
        except Exception as e:
            channel = self.bot.get_channel(1273144773435326545)
            await channel.send(f"{message.guild.name} {message.author.name} 刪除監測錯誤:{e}")

async def setup(bot: commands.Bot):
    voice_surveillanc()
    await bot.add_cog(Voice_surveillanc(bot))
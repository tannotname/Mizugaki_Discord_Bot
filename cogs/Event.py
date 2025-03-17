import time
import discord
import sqlite3
import random
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os

load_dotenv()

errorchannel = os.getenv("ERRORCHANNEL")
if errorchannel is None:
    print("錯誤：找不到 報錯頻道。請設置 報錯頻道。")
    exit()

error_channel = int(errorchannel)

ABC = "iso_4217"

#drop table 
con = sqlite3.connect('event.db') # 連線資料庫
cur = con.cursor() # 建立游標
 # 查詢第一筆資料
cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?", ("event",))
row = cur.fetchone()[0]
    # 查詢資料庫是否存在
if row == 0:
    cur.execute("CREATE TABLE event(eventguild NUMERIC,eventmessage TEXT,eventreply TEXT)")
    con.commit()
    print("表格 'event' 已建立.")
else:
    print("表格“event”已存在.")
    con.commit()

def check_if_guild(interaction: discord.Interaction) -> bool:
    return interaction.guild.id == 1238133524662325351

#drop table 
con = sqlite3.connect('myserver.db') # 連線資料庫
cur = con.cursor() # 建立游標
 # 查詢第一筆資料
cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?", ("myserver",))
row = cur.fetchone()[0]
    # 查詢資料庫是否存在
if row == 0:
    cur.execute("CREATE TABLE myserver(myserverguild NUMERIC,myservermessage TEXT,myserverreply TEXT,user TEXT)")
    con.commit()
    print("表格 'myserver' 已建立.")
else:
    print("表格“myserver”已存在.")
    con.commit()



#drop table 
cer = sqlite3.connect('userbool.db') # 連線資料庫
coo = cer.cursor() # 建立游標
 # 查詢第一筆資料
coo.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?", ("userbool",))
row = coo.fetchone()[0]
    # 查詢資料庫是否存在
if row == 0:
    coo.execute("CREATE TABLE userbool(username TEXT,user_id NUMERIC)")
    cer.commit()
    print("表格 'userbool' 已建立.")
else:
    print("表格“userbool”已存在.")
    cer.commit()


#drop table 
cer = sqlite3.connect('serverbool.db') # 連線資料庫
coo = cer.cursor() # 建立游標
 # 查詢第一筆資料
coo.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?", ("serverbool",))
row = coo.fetchone()[0]
    # 查詢資料庫是否存在
if row == 0:
    coo.execute("CREATE TABLE serverbool(servername TEXT,server_id NUMERIC)")
    cer.commit()
    print("表格 'serverbool' 已建立.")
else:
    print("表格“serverbool”已存在.")
    cer.commit()

class Event(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # 開始執行函式
        self.start_time = time.time()

    @commands.Cog.listener()
    #當有訊息時
    async def on_message(self, message: discord.Message):
        #排除自己的訊息，避免陷入無限循環
        if message.author == self.bot.user:
            return
    
        
              

        try:
            conn = sqlite3.connect("userbool.db")
            comn = conn.cursor()
            comn.execute("SELECT * FROM userbool WHERE user_id=?",(message.author.id,))
            rows = comn.fetchall()
            conn.commit()
            comn.close()
            conn.close()
        except sqlite3.Error as e:
            channel = self.bot.get_channel(error_channel)
            await channel.send(f"{message.guild.name} {message.channel.name} 發生錯誤:{e}")
        for row in rows:
            if message.author.id == row[1]:
                can = sqlite3.connect("event.db")
                car = can.cursor()
                car.execute("SELECT * FROM event WHERE eventguild=?",(message.guild.id,))
                rows = car.fetchall()
                can.commit()
                for row in rows:
                    if row[1] in message.content:
                        await message.channel.send(f"{row[2]}")


                    if message.author.name == 'tan_00_00':
                        if ('晚安' in message.content and len(message.content) <= 3) or message.content == '晚' or '晚晚'in message.content or '浣安' in message.content or message.content == '浣' or message.content == '睡' : 
                            replies = [
                                    ('睡你麻痺 起來嗨', 0.1),
                                    ('晚安', 0.6),
                                    ('浣安', 0.3)
                            ]
                            # 選擇回覆
                            reply = random.choices([reply[0] for reply in replies], weights=[reply[1] for reply in replies], k=1)[0]
                            await message.reply(reply,mention_author=False)
                    elif  ('晚安' in message.content and len(message.content) <= 3) or message.content == '晚' or '晚晚'in message.content or '浣安' in message.content or message.content == '浣' or message.content == '睡' : 
                            replies = [
                                    ('睡你麻痺 起來嗨', 0.2),
                                    ('晚安', 0.7),
                                    ('浣安', 0.1)
                            ]
                            # 選擇回覆
                            reply = random.choices([reply[0] for reply in replies], weights=[reply[1] for reply in replies], k=1)[0]
                            await message.reply(reply,mention_author=False)

        # 以下為支援伺服器專用
        if  message.guild.id == 1238133524662325351:
            try:
                try:
                    conn = sqlite3.connect("userbool.db")
                    comn = conn.cursor()
                    comn.execute("SELECT * FROM userbool WHERE user_id=?",(message.author.id,))
                    rows = comn.fetchall()
                    conn.commit()
                    comn.close()
                    conn.close()
                except sqlite3.Error as e:
                    channel = self.bot.get_channel(error_channel)
                    await channel.send(f"{message.guild.name} {message.channel.name} 發生錯誤:{e}")
                for row in rows:
                    if message.author.id == row[1]:
                        cao = sqlite3.connect("myserver.db")
                        cor = cao.cursor()
                        cor.execute("SELECT * FROM myserver WHERE myserverguild=?",(message.guild.id,))
                        raws = cor.fetchall()
                        cao.commit()
                        for raw in raws:
                            if message.content == raw[1]:
                                await message.channel.send(f"{raw[2]}")
            except sqlite3.Error as e:
                channel = self.bot.get_channel(error_channel)
                await channel.send(f"{message.guild.name} {message.channel.name} 發生錯誤:{e}")

            if '我上課不專心' in message.content or '受夠台北的天氣' in message.content or "呀嘞呀嘞" in message.content:
                await message.delete()
            
            if '好啊沒關係啊' in message.content :
                await message.reply('# 對!你不重要 <a:123456:1231591204228173914>')

    @app_commands.command(name="usermessage",description="註冊訊息反應服務")
    async def usermessage(self,interaction:discord.Interaction,yes_or_no:str):
        try:
            con = sqlite3.connect("userbool.db")
            cur = con.cursor()
            cur.execute("INSERT INTO userbool (username,user_id) VALUES (?,?)",(interaction.user.name,interaction.user.id))
            con.commit()
            await interaction.response.send_message(f"已將您的訊息反應設為啟用",ephemeral=True)
            channel = self.bot.get_channel(error_channel)
            await channel.send(f"{interaction.user.name} 已將訊息反應設為啟用")
            con.close()
            cur.close()
        except Exception as e:
            random7_int = random.randint(0, 255)
            random8_int = random.randint(0, 255)
            random9_int = random.randint(0, 255)
            emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
            await interaction.response.send_message(embed=embed)

        
    

# Cog 載入 Bot 中
async def setup(bot: commands.Bot):
    await bot.add_cog(Event(bot))

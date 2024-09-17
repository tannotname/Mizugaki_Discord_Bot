import time
import discord
import sqlite3
import random
import asyncio
from discord.ext import commands
import re
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
        
        if "https://www.instagram.com/" in message.content :
            try:
                try:
                    conn = sqlite3.connect("serverbool.db")
                    comn = conn.cursor()
                    comn.execute("SELECT * FROM serverbool WHERE server_id=?",(message.guild.id,))
                    rows = comn.fetchall()
                    conn.commit()
                    comn.close()
                    conn.close()
                except sqlite3.Error as e:
                    channel = self.bot.get_channel(error_channel)
                    await channel.send(f"{message.guild.name} {message.channel.name} 發生錯誤:{e}")
                for row in rows:
                    if message.guild.id != row[1]:
                        url = message.content
                        end = url.replace("https://www.instagram.com/","https://www.ddinstagram.com/")
                        await message.channel.send(f"[instagram]({end})")
                        await asyncio.sleep(1)
                        if message.embeds:  # 檢查訊息是否有 embeds
                            await message.edit(embeds=[])  # 刪除 embeds
            except Exception as e:
                channel = self.bot.get_channel(error_channel)
                await channel.send(f"{message.guild.name} {message.channel.name} 發生錯誤:{e}")
        if message.author.id != 1273144645580357675:
            if message.author.name == 'tan_07_24':
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

        if message.author.name == 'tan_07_24':
            if message.content == '早安' or  message.content == '早' or  '早上好' in message.content or '早灣' in message.content :
                await message.reply(random.choice(['早上好','早安']),mention_author=False)
        elif message.content == '早安' or  message.content == '早' or  '早上好' in message.content or '早灣' in message.content :
            #發送訊息，並將本次訊息資料存入tmpmsg，方便之後刪除
            await message.reply(random.choice(['早上好','不早了','都幾點了？還早？','早安']),mention_author=False)

        if message.content == "&marry <@998929254265929788>" :
                await asyncio.sleep(2)
                await message.reply(random.choice(['喔！親愛的，我覺得你太好了，我配不上你！','你很好！但抱歉，我現在還不想結婚、進入婚姻！','比起當夫妻，我覺得我們當朋友會更適合！','很抱歉讓你誤會，但我真的把你當好朋友！','我真的也很喜歡你，但我覺得真的在一起會是個錯誤！','我已經看見在一起後未來會發生的問題，所以當朋友比較長久！','我相信你一定會找到更適合的人，我真的不適合你！']))

        

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

            if message.content == '毯毯養我':
                await message.channel.send('<:worryCoffee:416636282324910100>')
                await asyncio.sleep(1)
                await message.reply(0)

            if '我上課不專心' in message.content or '受夠台北的天氣' in message.content or "呀嘞呀嘞" in message.content:
                await message.delete()
            
            if '好啊沒關係啊' in message.content :
                await message.reply('# 對!你不重要 <a:123456:1231591204228173914>')

    @app_commands.command(name="增加反應",description="增加機器人訊息反應")
    @app_commands.describe(message = "偵測訊息",reply = "回復訊息")
    async def eventmessage(self,interaction:discord.Interaction,message:str,reply:str):
        try:
            con = sqlite3.connect("event.db")
            cur = con.cursor()
            cur.execute("INSERT INTO event (eventguild,eventmessage,eventreply) VALUES (?,?,?)",(interaction.guild.id,message,reply))
            con.commit()
            await interaction.response.send_message(f"{message},{reply} 存入")
            channel = self.bot.get_channel(1273145125773639752)
            await channel.send(f"{message},{reply} 存入")
            con.close()
            cur.close()
        except Exception as e:
            random7_int = random.randint(0, 255)
            random8_int = random.randint(0, 255)
            random9_int = random.randint(0, 255)
            emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="若有問題請告知 <@710128890240041091> ",inline=False)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="myservermessage",description="增加本伺服器專屬訊息反應")
    @app_commands.check(check_if_guild)
    @app_commands.describe(message = "偵測訊息",reply = "回復訊息")
    async def myservermessage(self,interaction:discord.Interaction,message:str,reply:str):
        try:
            if interaction.user.id != 966291389522530365:
                con = sqlite3.connect("myserver.db")
                cur = con.cursor()
                cur.execute("INSERT INTO myserver (myserverguild,myservermessage,myserverreply,user) VALUES (?,?,?,?)",(interaction.guild.id,message,reply,interaction.user.name))
                con.commit()
                await interaction.response.send_message(f"{message},{reply} 存入")
                channel = self.bot.get_channel(error_channel)
                await channel.send(f"{interaction.user.name}新增{message},{reply} 存入")
                con.close()
                cur.close()
            else:
                await interaction.response.send_message(f"{message},{reply} 存入")
        except Exception as e:
            random7_int = random.randint(0, 255)
            random8_int = random.randint(0, 255)
            random9_int = random.randint(0, 255)
            emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="若有問題請告知 <@710128890240041091> ",inline=False)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="usermessage",description="註冊訊息反應服務(早安晚安不在此限)")
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
            embed.add_field(name=e,value="若有問題請告知 <@710128890240041091> ",inline=False)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="instagramurl反應",description="啟用instagram連接反應(預設true)")
    @app_commands.checks.has_permissions(administrator=True)
    async def instagramurl(self,interaction:discord.Interaction,y_or_n:bool):
        try:
            if y_or_n == False:
                con = sqlite3.connect("serverbool.db")
                cur = con.cursor()
                cur.execute("INSERT INTO serverbool (servername,server_id) VALUES (?,?)",(interaction.guild.name,interaction.guild.id))
                con.commit()
                await interaction.response.send_message(f"已將此伺服器的ig連接設為禁用",ephemeral=True)
                channel = self.bot.get_channel(1273145125773639752)
                await channel.send(f"{interaction.user.name} 已將{interaction.guild.name}伺服器的ig連接設為禁用")
                con.close()
                cur.close()
            if y_or_n == True:
                try:
                    conn = sqlite3.connect("serverbool.db")
                    comn = conn.cursor()
                    comn.execute("SELECT * FROM serverbool WHERE server_id=?",(interaction.guild.id,))
                    rows = comn.fetchall()
                    conn.commit()
                    comn.close()
                    conn.close()
                except sqlite3.Error as e:
                    channel = self.bot.get_channel(1273144773435326545)
                    await channel.send(f"{interaction.guild.name} {interaction.channel.name} 發生錯誤:{e}")
                for row in rows:
                    if interaction.guild.id == row[1]:
                        try:
                            con = sqlite3.connect("serverbool.db")
                            cur = con.cursor()
                            cur.execute("DELETE FROM serverbool WHERE server_id=?",(interaction.guild.id,))
                            conn.commit()
                            comn.close()
                            conn.close()
                            await interaction.response.send_message(f"已將此伺服器的ig連接設為啟用",ephemeral=True)
                        except sqlite3.Error as e:
                            channel = self.bot.get_channel(1273144773435326545)
                            await channel.send(f"{interaction.guild.name} {interaction.channel.name} 發生錯誤:{e}")
        except Exception as e:
            channel = self.bot.get_channel(1273144773435326545)
            await channel.send(f"{interaction.guild.name} {interaction.channel.name} 發生錯誤:{e}")

        
    

# Cog 載入 Bot 中
async def setup(bot: commands.Bot):
    await bot.add_cog(Event(bot))

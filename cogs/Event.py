import time
import discord
import sqlite3
import random
import asyncio
from discord.ext import commands
import re
from discord import app_commands

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

emoji_pattern = re.compile(
    '['
    '\U0001F600-\U0001F64F'  # 表情符號
    '\U0001F300-\U0001F5FF'  # 符號 & 圖標
    '\U0001F680-\U0001F6FF'  # 交通 & 地點
    '\U0001F700-\U0001F77F'  # 其他符號
    '\U0001F780-\U0001F7FF'  # 擴展區塊
    '\U0001F800-\U0001F8FF'  # 擴展區塊
    '\U0001F900-\U0001F9FF'  # 表情 & 手勢
    '\U0001FA00-\U0001FA6F'  # 表情符號附加區
    '\U0001FA70-\U0001FAFF'  # 表情符號附加區
    '\U00002702-\U000027B0'  # 符號 & 標誌
    '\U000024C2-\U0001F251'
    ']+', flags=re.UNICODE)

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
        
        if message.author.name == 'tan_07_24':
            if '晚安' in message.content or message.content == '晚' or '晚晚'in message.content or '浣安' in message.content or message.content == '浣' or message.content == '睡' : 
                replies = [
                        ('睡你麻痺 起來嗨', 0.1),
                        ('晚安', 0.6),
                        ('浣安', 0.3)
                ]
                # 選擇回覆
                reply = random.choices([reply[0] for reply in replies], weights=[reply[1] for reply in replies], k=1)[0]
                await message.reply(reply,mention_author=False)
        elif  '晚安' in message.content or message.content == '晚' or '晚晚'in message.content or '浣安' in message.content or message.content == '浣' or message.content == '睡' : 
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

        if "看開了" in message.content:
            await message.reply("https://cdn.discordapp.com/attachments/1226176299647893575/1241067493448089783/IMG_0488.jpg?ex=6648d9ac&is=6647882c&hm=1e02c6ab7f6b2d0429095c8e44d198e1a61a65d618afaaf9d75055aa789c49b8&")


        # 以下為支援伺服器專用
        can = sqlite3.connect("event.db")
        car = can.cursor()
        car.execute("SELECT * FROM event WHERE eventguild=?",(message.guild.id,))
        rows = car.fetchall()
        can.commit()
        for row in rows:
            if row[1] in message.content:
                await message.channel.send(f"{row[2]}")

        if  message.guild.id == 1213748875471364137 or message.guild.id == 1238133524662325351:
            if message.content == """富婆養我""":
                await message.channel.send('https://tenor.com/view/richfemale-gif-27270977')

            if message.content == '養我' or message.content == '月月養我' or message.content == '月月富婆養我' or "<@1055932398031884319> 我要跟你借錢" in message.content:
                await message.reply('# は～！！りしれごんさ小 <:820914027559125002:1224396364411310172>')

            if message.content == '毯毯養我':
                await message.channel.send('<:worryCoffee:416636282324910100>')
                await asyncio.sleep(1)
                await message.reply(0)

            if message.content == '破盤':
                await message.channel.send("https://tenor.com/view/%E5%B0%8F%E7%95%B6%E5%AE%B6-%E7%9B%A4%E5%AD%90-%E9%BE%8D%E8%9D%A6%E4%B8%89%E7%88%AD%E9%9C%B8-%E6%9D%8E%E5%9A%B4-gif-22898444")

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
            channel = self.bot.get_channel(1064943718014124142)
            await channel.send(f"{message},{reply} 存入")
            con.close()
            cur.close()
        except Exception as e:
            await interaction.response.send_message(f"錯誤:{e}")
# Cog 載入 Bot 中
async def setup(bot: commands.Bot):
    await bot.add_cog(Event(bot))

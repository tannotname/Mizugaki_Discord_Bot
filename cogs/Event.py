import time
import discord
import sqlite3
import random
import asyncio
from discord.ext import commands

ABC = "iso_4217"

con = sqlite3.connect('wansunfapanpandiscordbot.db')
cur = con.cursor()
row = cur.fetchone()
cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?", (ABC,))
existing_table_count = cur.fetchone()[0]
    # 如果查询结果不为空
if existing_table_count == 0:
    cur.execute("CREATE TABLE iso_4217(name TEXT, code TEXT)")
    con.commit()
    print("Table 'iso_4217' created successfully.")
else:
    print("Table 'iso_4217' already exists.")



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
        message_content = f'{message.content}'
        user = message.author
        iso4217 = 'iso4217'.lower()

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
                await message.reply(random.choice(['早上好','早安']))
        elif message.content == '早安' or  message.content == '早' or  '早上好' in message.content or '早灣' in message.content :
            #發送訊息，並將本次訊息資料存入tmpmsg，方便之後刪除
            await message.reply(random.choice(['早上好','不早了','都幾點了？還早？','早安']),mention_author=False)

        if  message.content == '下班':
            await message.reply(random.choice(['恭下','去加班','攻下']))

        if message.content == """富婆養我""":
            await message.channel.send('https://tenor.com/view/richfemale-gif-27270977')

        if message.content == "&marry <@998929254265929788>" :
            await asyncio.sleep(2)
            await message.reply(random.choice(['喔！親愛的，我覺得你太好了，我配不上你！','你很好！但抱歉，我現在還不想結婚、進入婚姻！','比起當夫妻，我覺得我們當朋友會更適合！','很抱歉讓你誤會，但我真的把你當好朋友！','我真的也很喜歡你，但我覺得真的在一起會是個錯誤！','我已經看見在一起後未來會發生的問題，所以當朋友比較長久！','我相信你一定會找到更適合的人，我真的不適合你！']))

        if message.content == 'mch':
            await message.channel.send('<a:modcheck:1227279045633511545>')

        if message.content == 'wow':
            await message.channel.send('<a:1007:1224395982746292487>')

        if message.content == '心碎' or message.content == '心碎了':
            await message.channel.send('<a:1006:1224397588418265088>')

        if message.content == 'never give' or message.content == '瑞克搖' or message.content == 'bjo4dk4ul6':
            await message.channel.send('<a:1010:1221281210588987464>')

        if message.content == '雷盤':
            await message.channel.send(random.choice(['<:_7867867678_66:1209737435026825226><:__76786786786786:1209737437585350656><:__28778278578:1209737445436956752><:__6786786786:1209737443339935774><:__678678678678:1209737439657197619><:__78678678678:1209737441477533776>','<:_7867867678_66:1209737435026825226><:__76786786786786:1209737437585350656><:__272782782578:1209737447601344565><:__6786786786:1209737443339935774><:__72782782:1209737449975054356>']))

        if message.content == '養我' or message.content == '月月養我' or message.content == '月月富婆養我' or "<@1055932398031884319> 我要跟你借錢" in message.content:
            await message.reply('# は～！！りしれごんさ小 <:820914027559125002:1224396364411310172>')

        if message.content == '毯毯養我':
            await message.channel.send('<:worryCoffee:416636282324910100>')
            await asyncio.sleep(1)
            await message.reply(0)

        if message.content == '破盤':
            await message.channel.send("https://tenor.com/view/%E5%B0%8F%E7%95%B6%E5%AE%B6-%E7%9B%A4%E5%AD%90-%E9%BE%8D%E8%9D%A6%E4%B8%89%E7%88%AD%E9%9C%B8-%E6%9D%8E%E5%9A%B4-gif-22898444")

        if '我上課不專心' in message.content or '受夠台北的天氣' in message.content:
            await message.delete()
        
        if '好啊沒關係啊' in message.content :
            await message.reply('# 對!你不重要 <a:123456:1231591204228173914>')

        if '半夜三點' in message.content or '美味蟹堡' in message.content :
            await message.channel.send('https://tenor.com/view/patrick-star-eating-3am-sleep-up-for-food-gif-10318105')

        if message.content == '歐洲人' :
            await message.channel.send('https://tenor.com/view/cartoons-lion-king-prank-lol-fail-gif-4881393')

        # 檢查消息是否以 !exchange 開頭
        if message.content.startswith('!匯率'):
            await message.channel.send('此功能已轉成斜線指令')

        if message.content.startswith(iso4217):
            content_without_ISO_4217 = message_content[len(iso4217):]
            message_ISO_4217 = content_without_ISO_4217.split()
            if len(message_ISO_4217) >= 2:
                # 第一个部分是提问内容
                name_ISO_4217 = message_ISO_4217[0]
                print(name_ISO_4217)
                # 第二个部分是用户的服务器昵称或 Discord 用户名
                code_ISO_4217 = message_ISO_4217[1].upper()       
                print(code_ISO_4217)
                # 剩下的部分是其它信息，将其合并成一个字符串
                additional_info = ' '.join(message_ISO_4217[2:])
                print(additional_info)
                # 其他代码...
                con = sqlite3.connect('wansunfapanpandiscordbot.db')
                cur = con.cursor()
                cur.execute("INSERT INTO iso_4217 (name,code) VALUES (?,?)",(name_ISO_4217, code_ISO_4217))
                con.commit()
                await message.reply('{} = {}'.format(name_ISO_4217,code_ISO_4217))
                name20 = name_ISO_4217
                code20 = code_ISO_4217
                cur.execute("SELECT * FROM iso_4217 WHERE name=? AND code=?", (name20, code20))
                existing_data = cur.fetchone()
                if existing_data:
                    cur.execute("DELETE FROM iso_4217 WHERE name=? AND code=?", (name20, code20))
                    cur.execute("INSERT INTO iso_4217 (name,code) VALUES (?,?)",(name_ISO_4217, code_ISO_4217))
                    con.commit()
                    con.close()


# Cog 載入 Bot 中
async def setup(bot: commands.Bot):
    await bot.add_cog(Event(bot))

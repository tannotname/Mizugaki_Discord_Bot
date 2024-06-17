import datetime
import random
import sqlite3
import discord
from discord.ext import commands
from discord import app_commands

#drop table 
con = sqlite3.connect('surveillanc.db') # 連線資料庫
cur = con.cursor() # 建立游標
 # 查詢第一筆資料
cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?", ("surveillanc",))
row = cur.fetchone()[0]
    # 查詢資料庫是否存在
if row == 0:
    cur.execute("CREATE TABLE surveillanc(surveillancguildname TEXT,surveillancguildid NUMERIC,surveillancchannelname TEXT,surveillancreplychannelid NUMERIC)")
    con.commit()
    print("表格 'surveillanc' 已建立.")
else:
    print("表格“surveillanc”已存在.")
    con.commit()

class Surveillanc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self,message:discord.Message):
    #排除自己的訊息，避免陷入無限循環
        if message.author == self.bot.user:
            return


        if message.channel != 'sever':
            # 獲取要發言的頻道
            channel = self.bot.get_channel(1232331488528171129)  # 替換 YOUR_CHANNEL_ID 為目標頻道的 ID
            random3_int = random.randint(0, 255)
            random4_int = random.randint(0, 255)
            random5_int = random.randint(0, 255)
            emb_color = discord.Color.from_rgb(random3_int, random4_int, random5_int)
            embed = discord.Embed(title='監測訊息',
                                description=f'{message.content}',
                                color=emb_color,
                                timestamp=datetime.datetime.now())
            embed.add_field(name='發送人', value=f"{message.author.name}({message.author.nick if message.author.nick else message.author.name})", inline=False)
            embed.add_field(name='發送頻道', value=message.channel, inline=False)
            embed.add_field(name='發送伺服器', value=message.guild.name, inline=False)
            await channel.send(embed=embed)
            if message.attachments:
                for attachment in message.attachments:
                    # 發送圖片連結
                    try:
                        await attachment.save(f'C:\\Users\\曉黑\\Desktop\\DISCORDBOTmain\\cogs\\pho\\{attachment.filename}')
                    except Exception as e:
                        print(f"發生儲存錯誤:{e}")
                        return
                    await channel.send(file=discord.File(f'C:\\Users\\曉黑\\Desktop\\DISCORDBOTmain\\cogs\\pho\\{attachment.filename}'))

        try:
            can = sqlite3.connect("surveillanc.db")
            car = can.cursor()
            car.execute("SELECT * FROM surveillanc WHERE surveillancguildid=?",(message.guild.id ,))
            rows = car.fetchall()
            can.commit()
            for row in rows:
                channelid = row[3]
                channel = self.bot.get_channel(channelid)
                await channel.send(f"# 監測訊息\n```\n發送人:{message.author.name}({message.author.nick if message.author.nick else message.author.name})\n發送頻道:{message.channel}\n訊息內容:\n{message.content}```")
                if message.attachments:
                    for attachment in message.attachments:
                        await channel.send(file=discord.File(f'C:\\Users\\曉黑\\Desktop\\DISCORDBOTmain\\cogs\\pho\\{attachment.filename}'))
        except Exception as e:
            channel = self.bot.get_channel(1064943718014124142)
            await channel.send(f"錯誤:{e}")

    @app_commands.command(name="set_transmission_channel",description="設定監測訊息傳送頻道")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_transmission_channel(self,interaction:discord.Interaction,channel:discord.TextChannel):
        try:
            Username = interaction.user.name
            guild_name = interaction.guild.name
            guild_id = interaction.guild.id
            channel_id = channel.id
            channel_name = channel.name
            con = sqlite3.connect("surveillanc.db")
            cur = con.cursor()
            cur.execute("INSERT INTO surveillanc (surveillancguildname,surveillancguildid,surveillancchannelname,surveillancreplychannelid) VALUES (?,?,?,?)",(guild_name,guild_id,channel_name,channel_id))
            con.commit()
            await interaction.response.send_message(f"{guild_name},{channel_name} 存入")
            channel = self.bot.get_channel(1064943718014124142)
            await channel.send(f"{Username}新增:{guild_name},{guild_id},{channel_name},{channel_id} 存入")
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

    @app_commands.command(name="look_transmission_channel",description="查看監測訊息傳送頻道")
    @app_commands.checks.has_permissions(administrator=True)
    async def look_transmission_channel(self,interaction:discord.Interaction):
        try:
            can = sqlite3.connect("surveillanc.db")
            car = can.cursor()
            car.execute("SELECT * FROM surveillanc WHERE surveillancguildid=?",(interaction.guild.id ,))
            rows = car.fetchall()
            can.commit()
            for row in rows:
                await interaction.response.send_message(row[1],row[2])
        except Exception as e:
            random7_int = random.randint(0, 255)
            random8_int = random.randint(0, 255)
            random9_int = random.randint(0, 255)
            emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="若有問題請告知 <@710128890240041091> ",inline=False)
            await interaction.response.send_message(embed=embed) 



async def setup(bot: commands.Bot):
    await bot.add_cog(Surveillanc(bot))
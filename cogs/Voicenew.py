import random
import discord
from discord.ext import commands
from discord import app_commands
from discord.ext import commands
import sqlite3

#drop table 
con = sqlite3.connect('voicenew.db') # 連線資料庫
cur = con.cursor() # 建立游標
 # 查詢第一筆資料
cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?", ("voicenew",))
row = cur.fetchone()[0]
    # 查詢資料庫是否存在

if row == 0:
    cur.execute("CREATE TABLE voicenew(sever TEXT,categoryname TEXT, categoryid NUMERIC,channelname TEXT,channelid NUMERIC)")
    cur.execute("CREATE TABLE newchannel(channelname TEXT,channelid NUMERIC)")
    con.commit()
    print("表格 'voicenew' 已建立.")
else:
    print("表格“voicenew”已存在.")
    con.commit()
    



class Voicenew(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("已載入voicenew")
    

    @app_commands.command(name="設定動態語音頻道", description="設定動態語音頻道入口")
    @app_commands.checks.has_permissions(administrator=True)
    async def newvoicechannel(self, interaction: discord.Interaction, category: discord.CategoryChannel, voice: discord.VoiceChannel): 
        await interaction.response.send_message(f"已設定動態語音入口為 {voice.name}")
        sever = interaction.guild
        print(sever,category,voice)
        con = sqlite3.connect('voicenew.db')
        print("已連線資料庫")
        cur = con.cursor()
        print("已建立游標")
        cur.execute("INSERT INTO voicenew (sever,categoryname,categoryid,channelname,channelid) VALUES (?,?,?,?,?)",(sever.name, category.name,category.id, voice.name,voice.id))
        con.commit()
        print(f"{sever},{category},{voice} 存入")
        con.close()
        cur.close()

    @app_commands.command(name="創建動態語音頻道",description="創建動態語音頻道(需在語音頻道內)")
    async def newvoicenew(self,interaction:discord.Interaction):
        try:
                guild = interaction.guild
                user = interaction.user
                category = interaction.channel.category
                newchannel = await guild.create_voice_channel(name=f"{user.display_name} 的房間", category=category,rtc_region="japan")
                print(f"已創建 {newchannel.name} 在 {category.name}")
                await user.move_to(newchannel)
                print(f"已移動 {user.display_name} 到 {newchannel.name}")
                try:
                    await newchannel.set_permissions(user, manage_channels=True)
                    print(f"已給予{user.name} {newchannel.name} 的管理權限")              
                except:
                    print("給予權限時發生未知錯誤")
                try:
                    conn = sqlite3.connect('voicenew.db')
                    print("資料庫連接成功")
                except sqlite3.Error as e:
                    print(f"資料庫連接時發生錯誤: {e}")
                try:
                    cur = conn.cursor()
                    cur.execute("INSERT INTO newchannel (channelname, channelid) VALUES (?, ?)", (newchannel.name, newchannel.id))
                    conn.commit()
                    conn.close()
                except sqlite3.Error as e:
                    random7_int = random.randint(0, 255)
                    random8_int = random.randint(0, 255)
                    random9_int = random.randint(0, 255)
                    emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
                    embed = discord.Embed(title="錯誤", color= emb_color)
                    embed.add_field(name=e,value="若有問題請告知 @tan_07_24 ",inline=False)
                    await interaction.response.send_message(embed=embed)
                await interaction.response.send_message("已創建動態語音頻道,開始將您傳送過去")
        except Exception as e:
            random7_int = random.randint(0, 255)
            random8_int = random.randint(0, 255)
            random9_int = random.randint(0, 255)
            emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="若有問題請告知 @tan_07_24 ",inline=False)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="登入語音動態房",description="將語音房間設為動態刪除")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def Retain_the_channel(self,interaction:discord.Interaction,channel:discord.VoiceChannel):
        try:
            con = sqlite3.connect("voicenew.db")
            cur = con.cursor()
            cur.execute("INSERT INTO newchannel (channelname, channelid) VALUES (?, ?)", (channel.name, channel.id))
            con.commit()
            cur.close()
            con.close()
            await interaction.response.send_message("已登入指定頻道")
        except sqlite3.Error as e:
            random7_int = random.randint(0, 255)
            random8_int = random.randint(0, 255)
            random9_int = random.randint(0, 255)
            emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="若有問題請告知 @tan_07_24 ",inline=False)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="保留語音動態房",description="將語音房間設為永久存留")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def delete_the_channel(self,interaction:discord.Interaction,channel:discord.VoiceChannel):
        try:
            channel_id = channel.id
            con = sqlite3.connect("voicenew.db")
            cur = con.cursor()
            cur.execute("DELETE FROM newchannel WHERE channelid=?", (channel_id,))
            con.commit()
            cur.close()
            con.close()
            await interaction.response.send_message("已保存指定頻道")
        except Exception as e:
            random7_int = random.randint(0, 255)
            random8_int = random.randint(0, 255)
            random9_int = random.randint(0, 255)
            emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="若有問題請告知 @tan_07_24 ",inline=False)
            await interaction.response.send_message(embed=embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if (after.channel is not None and before.channel is None) or (before.channel != after.channel and after.channel is not None):
            try:
                conn = sqlite3.connect("voicenew.db")
                comn = conn.cursor()
                comn.execute("SELECT * FROM voicenew WHERE sever=?",(member.guild.name,))
                rows = comn.fetchall()
                conn.commit()
                comn.close()
                conn.close()
            except sqlite3.Error as e:
                await after.channel.send(f"錯誤:{e}")
            try:
                for row in rows:
                    print(f"{member.display_name} 加入 {after.channel.name}")
                if after.channel.id == row[4]:
                    guild = member.guild
                    category = after.channel.category
                    newchannel = await guild.create_voice_channel(name=f"{member.display_name} 的房間", category=category,rtc_region="japan")
                    print(f"已創建 {newchannel.name} 在 {category.name}")
                    await member.move_to(newchannel)
                    print(f"已移動 {member.display_name} 到 {newchannel.name}")
                    try:
                        await newchannel.set_permissions(member, manage_channels=True)
                        print(f"已給予{member.name} {newchannel.name} 的管理權限")              
                    except:
                        print("給予權限時發生未知錯誤")
                    try:
                        conn = sqlite3.connect('voicenew.db')
                        print("資料庫連接成功")
                        cur = conn.cursor()
                        cur.execute("INSERT INTO newchannel (channelname, channelid) VALUES (?, ?)", (newchannel.name, newchannel.id))
                        conn.commit()
                        conn.close()
                    except sqlite3.Error as e:
                        print(f"資料庫連接時發生錯誤: {e}")
            except Exception as e:
                await after.channel.send(f"錯誤:{e}")

        if (before.channel is not None and after.channel is None) or (before.channel != after.channel and before.channel is not None):
            try:
                # 連接
                conn = sqlite3.connect("voicenew.db")
                cursor = conn.cursor()
                # 查詢
                cursor.execute("SELECT * FROM newchannel")
                rows = cursor.fetchall()
                for row in rows:
                    channel_id = int(row[1])
                    channel = self.bot.get_channel(channel_id)
                    if channel is None:
                        cursor.execute("DELETE FROM newchannel WHERE channelid=?", (channel_id,))
                    elif len(channel.members) == 0:
                        await channel.delete()
                        print(f"頻道 {channel.name} 已被刪除")
                        cursor.execute("DELETE FROM newchannel WHERE channelid=?", (channel_id,))
                # 提交事务并关闭数据库连接
                conn.commit()
                cursor.close()
                conn.close()

            except sqlite3.Error as e:
                print(f"資料庫連接時發生錯誤4: {e}")
    

async def setup(bot: commands.Bot):
    await bot.add_cog(Voicenew(bot))
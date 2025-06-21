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
    cur.execute("CREATE TABLE voicenew(server_id NUMERIC,server_name TEXT,categoryname TEXT, categoryid NUMERIC,channelname TEXT,channelid NUMERIC)")
    con.commit()
    print("表格'voicenew'已建立.")
else:
    print("表格“voicenew”已存在.")
    con.commit()
try:
    cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?", ("newchannel",))
    if row == 0:
        cur.execute("CREATE TABLE newchannel(channelname TEXT,channelid NUMERIC,channelmember NUMERIC)")
        con.commit()
        print("表格'newchannel'已建立.")
    else:
        print("表格“newchannel”已存在.")
        con.commit()
except sqlite3.Error as e:
    print(f"資料庫連接時發生錯誤: {e}")


con = sqlite3.connect('channel_to_user.db') # 連線資料庫
cur = con.cursor() # 建立游標
 # 查詢第一筆資料
cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?", ("channel_to_user",))
row = cur.fetchone()[0]
    # 查詢資料庫是否存在

if row == 0:
    cur.execute("CREATE TABLE channel_to_user(server_id NUMERIC,server_name TEXT,channelname TEXT,userid NUMERIC,username TEXT)")
    con.commit()
    print("表格 'channel_to_user' 已建立.")
else:
    print("表格“channel_to_user”已存在.")
    con.commit()

con = sqlite3.connect('newchannel_id.db') # 連線資料庫
cur = con.cursor() # 建立游標
 # 查詢第一筆資料
cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?", ("newchannel_id",))
row = cur.fetchone()[0]
    # 查詢資料庫是否存在

if row == 0:
    cur.execute("CREATE TABLE newchannel_id(server_id NUMERIC,server_name TEXT,channelname TEXT,userid NUMERIC,username TEXT)")
    con.commit()
    print("表格 'newchannel_id' 已建立.")
else:
    print("表格“newchannel_id”已存在.")
    con.commit()

con = sqlite3.connect('voice_monitor_channel.db') # 連線資料庫
cur = con.cursor() # 建立游標
 # 查詢第一筆資料
cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?", ("voice_monitor_channel",))
row = cur.fetchone()[0]
    # 查詢資料庫是否存在

if row == 0:
    cur.execute("CREATE TABLE voice_monitor_channel(server_name TEXT,server_id NUMERIC,channel_name TEXT,channel_id NUMERIC)")
    con.commit()
    print("表格 'voice_monitor_channel' 已建立.")
else:
    print("表格'voice_monitor_channel'已存在.")
    con.commit()


class Voicenew(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("已載入動態語音模組")

    @app_commands.command(name="設定動態語音頻道", description="設定動態語音頻道入口")
    @app_commands.checks.has_permissions(administrator=True)
    async def newvoicechannel(self, interaction: discord.Interaction, category: discord.CategoryChannel, voice: discord.VoiceChannel): 
        await interaction.response.send_message(f"已設定動態語音入口為 {voice.name}")
        server = interaction.guild
        print(server,category,voice)
        con = sqlite3.connect('voicenew.db')
        print("已連線資料庫")
        cur = con.cursor()
        print("已建立游標")
        cur.execute("INSERT INTO voicenew (server_id,server_name,categoryname,categoryid,channelname,channelid) VALUES (?,?,?,?,?,?)",(server.id,server.name, category.name,category.id, voice.name,voice.id))
        con.commit()
        print(f"{server},{category},{voice} 存入")
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
                    cur.execute("INSERT INTO newchannel (channelname, channelid,channelmember) VALUES (?,?,?)", (newchannel.name, newchannel.id,interaction.user.id))
                    conn.commit()
                    conn.close()
                except sqlite3.Error as e:
                    random7_int = random.randint(0, 255)
                    random8_int = random.randint(0, 255)
                    random9_int = random.randint(0, 255)
                    emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
                    embed = discord.Embed(title="錯誤", color= emb_color)
                    embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
                    await interaction.response.send_message(embed=embed) 
                await interaction.response.send_message("已創建動態語音頻道,開始將您傳送過去")
                try:
                    conn = sqlite3.connect('voice_monitor_channel.db') # 將創建的語音頻道寫入資料庫
                    comn = conn.cursor()
                    comn.execute("SELECT * FROM voice_monitor_channel WHERE server_id=?",(interaction.guild.id,)) # 搜尋伺服器設定的監測頻道
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
                            new_channel = await channel.create_thread(name=f"{newchannel.name}", type=discord.ChannelType.private_thread)
                            try:
                                conn = sqlite3.connect("voice_surveillanc.db")
                                comn = conn.cursor()
                                comn.execute("INSERT INTO voice_surveillanc (surveillanc_guild_name,surveillanc_guild_id,surveillanc_channel_id,surveillanc_reply_channel_id) VALUES (?,?,?,?)", (new_channel.guild.name,new_channel.guild.id,newchannel.id,new_channel.id))
                                conn.commit()
                                comn.close()
                                conn.close()
                            except sqlite3.Error as e:
                                channel = self.bot.get_channel(1273144773435326545)
                                await channel.send(f"{guild.name} {user.name} 資料連接錯誤:{e}")
                except Exception as e:
                    channel = self.bot.get_channel(1273144773435326545)
                    await channel.send(f"{guild.name} {user.name} 資料連接錯誤:{e}")
        except Exception as e:
            emb_color = discord.Color.from_rgb(255,0,0)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
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
            embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
            await interaction.response.send_message(embed=embed) 

    @app_commands.command(name="customized_voicename_to_user", description="讓使用者自定義自己的語音頻道名稱,只在使用指令的伺服器生效")
    @app_commands.describe(channel_name = "請使用*user*代替使用者名稱,例如:*user*的房間")
    async def customized_voicename_to_user(self, interaction: discord.Interaction,channel_name:str):
        try:
            user_id = interaction.user.id
            user_name = interaction.user.display_name
            guild_id = interaction.guild.id
            guild_name = interaction.guild.name
            channel_name2 = channel_name
            if "*user*" in channel_name: # 檢查頻道名稱是否包含 *user*
                channel_name = channel_name.replace("*user*",user_name,2) # 替換 *user* 為使用者名稱
            con = sqlite3.connect("channel_to_user.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM channel_to_user WHERE server_id=? AND userid=?",(guild_id,user_id,))
            rows = cur.fetchall()
            if rows ==[]:
                cur.execute("INSERT INTO channel_to_user (server_id,server_name,channelname,userid,username) VALUES (?,?,?,?,?)",(guild_id,guild_name,channel_name2,user_id,user_name))
            if rows != []:
                cur.execute("UPDATE channel_to_user SET channelname=? WHERE server_id=? AND userid=?",(channel_name2,guild_id,user_id))
            con.commit()
            await interaction.response.send_message(f"已設置您的語音頻道為:{channel_name}",ephemeral=True)
            con.close()
            cur.close()
            channel = self.bot.get_channel(1273145437259305001)
            await channel.send(f"{user_name} 已設置您的語音頻道為:{channel_name}")
        except Exception as e:
            random7_int = random.randint(0, 255)
            random8_int = random.randint(0, 255)
            random9_int = random.randint(0, 255)
            emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
            await interaction.response.send_message(embed=embed,ephemeral=True)

    @app_commands.command(name="解除動態語音入口",description="將動態語音入口刪除")
    @app_commands.checks.has_permissions(administrator=True)
    async def deletevoicenew(self,interaction:discord.Interaction):
        try:
            conn = sqlite3.connect("voicenew.db")
            comn = conn.cursor()
            comn.execute("DELETE FROM voicenew WHERE server_id=?", (interaction.guild.id,))
            conn.commit()
            comn.close()
            conn.close()
            await interaction.response.send_message("已解除動態語音入口")
        except sqlite3.Error as e:
            await interaction.response.send_message(f"錯誤:{e}",ephemeral=True)

    @app_commands.command(name="設定語音監測頻道",description="設定語音監測訊息傳送的頻道")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_voice_monitor_channel(self,interaction:discord.Interaction,channel:discord.TextChannel):
        try:
            server = interaction.guild
            conn = sqlite3.connect("voice_monitor_channel.db")
            comn = conn.cursor()
            comn.execute("INSERT INTO voice_monitor_channel (server_name,server_id,channel_name,channel_id) VALUES (?,?,?,?)", (server.name,server.id,channel.name,channel.id))
            conn.commit()
            comn.close()
            conn.close()
            await interaction.response.send_message("已設定語音監測頻道")
        except sqlite3.Error as e:
            await interaction.response.send_message(f"錯誤:{e}",ephemeral=True)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if (after.channel is not None and before.channel is None) or (before.channel != after.channel and after.channel is not None):
            try:
                conn = sqlite3.connect("voicenew.db")
                comn = conn.cursor()
                comn.execute("SELECT * FROM voicenew WHERE server_id=?",(after.channel.guild.id,)) # 搜尋伺服器設定的頻道
                rows = comn.fetchall()
                conn.commit()
                comn.close()
                conn.close()
            except sqlite3.Error as e:
                await after.channel.send(f"錯誤1:{e}")
            try:
                for row in rows:
                    if after.channel.id == row[5]:  # 檢查進入的channel是否為設定頻道
                        conn = sqlite3.connect("voicenew.db")
                        comn = conn.cursor()
                        comn.execute("SELECT * FROM newchannel WHERE channelmember=?",(member.id,)) # 搜尋伺服器設定的頻道
                        row = comn.fetchall()
                        print(row)
                        for row in row:
                            if row != None:
                                channel = self.bot.get_channel(row[1])
                                if channel == None:
                                    comn.execute("DELETE FROM newchannel WHERE channelid=?", (row[1],))
                                else:
                                    await member.move_to(channel)
                                    print(f"已移動 {member.display_name} 到舊有頻道 {row[0]}")
                                    return
                        conn.commit()
                        comn.close()
                        conn.close()
                        guild = member.guild
                        category = after.channel.category
                        can = sqlite3.connect("channel_to_user.db") # 搜尋user是否有自訂語音頻道名稱
                        car = can.cursor()
                        car.execute("SELECT * FROM channel_to_user WHERE server_id=? AND userid=?",(guild.id,member.id ,))
                        rows = car.fetchall()
                        can.commit()
                        car.close()
                        can.close()
                        if rows == []:
                            newchannel = await guild.create_voice_channel(name=f"{member.display_name} 的房間", category=category,rtc_region="japan") # 創建動態語音頻道
                            print(f"已創建 {newchannel.name} 在 {category.name}")
                        if rows != []:
                            for row in rows:
                                channel_name = row[2]
                                channel_name = str(channel_name)
                                if "*user*" in channel_name:
                                    channel_name = channel_name.replace("*user*",f"{member.display_name}")
                                newchannel = await guild.create_voice_channel(name=f"{channel_name}", category=category,rtc_region="japan")
                                print(f"已創建 {channel_name} 在 {category.name}")
                        await member.move_to(newchannel) # 移動成員至語音頻道
                        print(f"已移動 {member.display_name} 到 {newchannel.name}")
                        try:
                            await newchannel.set_permissions(member, manage_channels=True) # 給予成員channel管理權
                            print(f"已給予{member.name} {newchannel.name} 的管理權限")              
                        except:
                            channel = self.bot.get_channel(1273144773435326545)
                            await channel.send(f"{guild.name} {member.name} 創建動態動態語音頻道給予權限時發生錯誤")
                        try:
                            conn = sqlite3.connect('voicenew.db') # 將創建的語音頻道寫入資料庫
                            print("資料庫連接成功")
                            cur = conn.cursor()
                            cur.execute("INSERT INTO newchannel (channelname, channelid,channelmember) VALUES (?,?,?)", (newchannel.name, newchannel.id,member.id))
                            conn.commit()
                            conn.close()
                        except sqlite3.Error as e:
                            channel = self.bot.get_channel(1273144773435326545)
                            await channel.send(f"{guild.name} {member.name} 資料連接錯誤:{e}")
                        try:
                            conn = sqlite3.connect('voice_monitor_channel.db') # 將創建的語音頻道寫入資料庫
                            comn = conn.cursor()
                            comn.execute("SELECT * FROM voice_monitor_channel WHERE server_id=?",(after.channel.guild.id,)) # 搜尋伺服器設定的監測頻道
                            rows = comn.fetchall()
                            conn.commit()
                            comn.close()
                            conn.close()
                        except sqlite3.Error as e:
                            channel = self.bot.get_channel(1273144773435326545)
                            await channel.send(f"{guild.name} {member.name} 資料連接錯誤:{e}")
                        try:
                            for row in rows:
                                if row is None:
                                    return
                                elif row != None:
                                    channel = self.bot.get_channel(row[3])
                                    print(row[3])
                                    new_channel = await channel.create_thread(name=f"{newchannel.name}", type=discord.ChannelType.public_thread)
                                    try:
                                        conn = sqlite3.connect("voice_surveillanc.db")
                                        comn = conn.cursor()
                                        comn.execute("INSERT INTO voice_surveillanc (surveillanc_guild_name,surveillanc_guild_id,surveillanc_channel_id,surveillanc_reply_channel_id) VALUES (?,?,?,?)", (new_channel.guild.name,new_channel.guild.id,newchannel.id,new_channel.id))
                                        conn.commit() # 將創建的語音頻道寫入監測資料庫
                                        comn.close()
                                        conn.close()
                                    except sqlite3.Error as e:
                                        channel = self.bot.get_channel(1273144773435326545)
                                        await channel.send(f"{guild.name} {member.name} 資料連接錯誤:{e}")
                        except Exception as e:
                            channel = self.bot.get_channel(1273144773435326545)
                            await channel.send(f"{guild.name} {member.name} 資料連接錯誤:{e}")
            except Exception as e:
                channel = self.bot.get_channel(1273144773435326545)
                await channel.send(f"{guild.name} {member.name} 動態語音錯誤:{e}")


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

    @app_commands.command(name="delete_voice_surveillanc_data",description="刪除監測討論串登記資料")
    @app_commands.checks.has_permissions(administrator=True)
    async def delete_voice_surveillanc_data(self,interaction:discord.Interaction):
        if interaction.user.id == 710128890240041091:
            try:
                conn = sqlite3.connect("voice_surveillanc.db")
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM voice_surveillanc")
                rows = cursor.fetchall()
                for row in rows:
                    channel_id = int(row[2])
                    channel = self.bot.get_channel(channel_id)
                    if channel is None:
                        cursor.execute("DELETE FROM voice_surveillanc WHERE surveillanc_channel_id=?", (channel_id,)) # 刪除資料庫中資料
                        print(f"監測討論串登記資料已被刪除")
                        conn.commit()
                cursor.close()
                conn.close()
                await interaction.response.send_message("監測討論串登記資料已被刪除",ephemeral=True)
            except sqlite3.Error as e:
                await interaction.response.send_message(f"錯誤:{e}",ephemeral=True)
async def setup(bot: commands.Bot):
    await bot.add_cog(Voicenew(bot))
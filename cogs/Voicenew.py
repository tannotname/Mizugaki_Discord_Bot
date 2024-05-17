import discord
from discord.ext import commands
from discord import app_commands
from discord.ext import commands, tasks
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

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if (after.channel is not None and before.channel is None) or (before.channel != after.channel and after.channel is not None):
            conn = sqlite3.connect("voicenew.db")
            comn = conn.cursor()
            comn.execute("SELECT * FROM voicenew WHERE sever=?",(member.guild.name,))
            rows = comn.fetchall()
            conn.commit()
            comn.close()
            conn.close()
            for row in rows:
                print(f"{member.display_name} 加入 {after.channel.name}")
            if after.channel.id == row[4]:
                guild = member.guild
                category = after.channel.category
                newchannel = await guild.create_voice_channel(name=f"{member.display_name} 的麻將桌", category=category)
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
                except sqlite3.Error as e:
                    print(f"資料庫連接時發生錯誤: {e}")
                cur = conn.cursor()
                cur.execute("INSERT INTO newchannel (channelname, channelid) VALUES (?, ?)", (newchannel.name, newchannel.id))
                conn.commit()
                conn.close()
        
        if (before.channel is not None and after.channel is None) or (before.channel != after.channel and before.channel is not None):
            try:
                # 連接
                conn = sqlite3.connect("voicenew.db")
                cursor = conn.cursor()
                print("資料庫連接成功4")
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
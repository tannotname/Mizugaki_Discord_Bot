import random
import sqlite3
from typing import Optional
import discord
from discord import app_commands
from discord.ext import commands


#drop table 
con = sqlite3.connect('server_booster.db') # 連線資料庫
cur = con.cursor() # 建立游標
 # 查詢第一筆資料
cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?", ("server_booster",))
row = cur.fetchone()[0]
    # 查詢資料庫是否存在
if row == 0:
    cur.execute("CREATE TABLE server_booster(server_name TEXT,server_id MUMERIC,server_booster_role_id NUMERIC)")
    con.commit()
    print("表格 'server_booster' 已建立.")
else:
    print("表格“server_booster”已存在.")
    con.commit()


error_channel_id = 1273144773435326545

class Server_booster(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="enable_new_booster_role_feature",description="決定是否啟用new_booster_role功能,並登記或刪除server_booster_role_id(預設停用)")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(yes_or_no = "是否啟用new_booster_role功能,True為啟用,Fals則為禁用",server_booster_role_id = "server_booster_role 的id")
    async def e_t_n_b_r_f(self,interaction:discord.Interaction,yes_or_no:bool,server_booster_role_id:str):
        try:
            server_name = interaction.guild.name
            server_id = interaction.guild.id
            server_booster_role_id = int(server_booster_role_id)
            if yes_or_no == True:
                try:
                    coon = sqlite3.connect("server_booster.db")
                    cuur = coon.cursor()
                    cuur.execute(f"INSERT INTO server_booster (server_name,server_id,server_booster_role_id) VALUES (?,?,?)",(server_name,server_id,server_booster_role_id))
                    coon.commit()
                    cuur.close()
                    coon.close()
                    await interaction.response.send_message("已啟用new_booster_role功能")
                except sqlite3.Error as e:
                    random7_int = random.randint(0, 255)
                    random8_int = random.randint(0, 255)
                    random9_int = random.randint(0, 255)
                    emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
                    embed = discord.Embed(title="錯誤", color= emb_color)
                    embed.add_field(name=f"1:{e}",value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
                    await interaction.response.send_message(embed=embed)
            elif yes_or_no == False:
                coon = sqlite3.connect("server_booster.db")
                cuur = coon.cursor()
                cuur.execute("DELETE FROM server_booster WHERE server_id=?", (server_id,))
                coon.commit()
                await interaction.response.send_message("已禁用new_booster_role功能",ephemeral=True)
                cuur.close()
                coon.close()
        except Exception as e:
            random7_int = random.randint(0, 255)
            random8_int = random.randint(0, 255)
            random9_int = random.randint(0, 255)
            emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
            await interaction.response.send_message(embed=embed)
            channel = self.bot.get_channel(error_channel_id)
            await channel.send(f"server:{interaction.guild.name}使用者:{interaction.user.name}使用new_booster_role錯誤:{e}")

    @app_commands.command(name="set_role_color",description="自訂自己的身分組顏色")
    @app_commands.describe(colour = "16進位制的色碼")
    async def set_role_color(self,interaction:discord.Interaction,colour:str):
        try:
            guild = interaction.guild
            member = interaction.user
            roles = sorted(member.roles, key=lambda r: r.position, reverse=True)  # 依據優先順序排序
            # 轉換 Hex 顏色為 discord.Color
            try:
                color = discord.Colour(int(colour, 16))  # 例如 "#ff0000" 轉換成數值
            except ValueError:
                await interaction.response.send_message("請提供有效的 16 進位顏色，例如 `#ff0000`")
                return
            # 修改角色顏色
            await roles[0].edit(color=color)
            await interaction.response.send_message(f"已將 {roles[0].name} 的顏色更改為 `{color}`!")   
        except Exception as e:
            await interaction.response.send_message(f"錯誤:{e}",ephemeral=True)

    @app_commands.command(name="new_booster_role",description="自訂身分組顏色跟圖示並給予自己")
    @app_commands.describe(new_role_name = "新的身分組名字",colour = "16進位制的色碼",give_in_you ="是否給予自己此身分組",icoon_fill="身分組圖示,256kb以下的圖檔,與icoon_emoji二選一",icoon_emoji="身分組圖示,此伺服器的emoji,與icoon_fill二選一")
    async def new_booster_role(self,interaction:discord.Interaction,new_role_name:str,colour:str,give_in_you:bool,icoon_fill:Optional[discord.Attachment],icoon_emoji:Optional[str]):
        try:
            coonn = sqlite3.connect("server_booster.db")
            comn = coonn.cursor()
            comn.execute("SELECT * FROM server_booster WHERE server_id=?",(interaction.guild.id,))
            rows = comn.fetchall()
            coonn.commit()
            comn.close()
            coonn.close()
            for row in rows:
                if row[2]:
                    roles = interaction.guild.roles
                    for role in roles:
                        if role.id == row[2]:
                            users = role.members
                            for user in users:
                                if user.id == interaction.user.id:
                                    guild = interaction.guild
                                    member = interaction.user
                                    try:
                                        if icoon_fill is not None:
                                            if icoon_fill.size > 256000:  # 確保圖片小於 256KB
                                                await interaction.response.send_message("圖片大小超過 256KB,請選擇較小的圖示。")
                                                return
                                            icoon = await icoon_fill.read()  # 讀取二進制數據
                                        elif icoon_emoji is not None:
                                            icoon = icoon_emoji
                                    except Exception as e:
                                        await interaction.response.send_message(f"圖片或emoji錯誤:{e}",ephemeral=True)
                                        channel = self.bot.get_channel(error_channel_id)
                                        await channel.send(f"server:{interaction.guild.name}使用者:{interaction.user.name}使用new_booster_role圖片或emoji錯誤:{e}")
                                        return
                                    try:
                                        colour = discord.Colour(int(colour, 16))
                                        if icoon is not None:
                                            newrole = await guild.create_role(name=new_role_name,colour=colour,display_icoon=icoon)
                                        elif icoon is None:
                                            newrole = await guild.create_role(name=new_role_name,colour=colour)
                                        await interaction.response.send_message(f"已新增{newrole.name}")
                                        if give_in_you == True:
                                            await member.add_roles(newrole)
                                            await interaction.followup.send(f"已給予{member.nick} {newrole.name} 身分組")
                                    except Exception as e:
                                        await interaction.response.send_message(f"顏色格式錯誤{e},請使用十六進制顏色碼，例如 'FF5733'。")
                                        return
                if row is None:
                    await interaction.response.send_message("您並沒有啟用此功能")
        except Exception as e:
            await interaction.response.send_message(f"錯誤:{e}",ephemeral=True)
            channel = self.bot.get_channel(error_channel_id)
            await channel.send(f"server:{interaction.guild.name}使用者:{interaction.user.name}使用new_booster_role4錯誤:{e}")

    @app_commands.command(name="see_guild_booster",description="查看伺服器的加成者")
    @app_commands.describe(server_id = "伺服器id")
    @app_commands.checks.has_permissions(administrator=True)
    async def see_guild_booster(self,interaction:discord.Interaction,server_id:str):
        try:
            guild = self.bot.get_guild(int(server_id))
            if guild is None:
                await interaction.response.send_message("伺服器不存在")
                return
            coonn = sqlite3.connect("server_booster.db")
            comn = coonn.cursor()
            comn.execute("SELECT * FROM server_booster WHERE server_id=?",(int(server_id),))
            rows = comn.fetchall()
            comn.close()
            coonn.close()
            for row in rows:
                if row[2]:
                    role = guild.get_role(row[2])
                    users = role.members
                    member = f"伺服器加成者身分組名稱{role.name}:\n"
                    for user in users:
                        member += f"{user.name}\n"
                    if len(users) == 0:
                        member += "目前沒有擁有加成身分組的人"
            await interaction.response.send_message(member)
        except Exception as e:
            await interaction.response.send_message(f"錯誤:{e}",ephemeral=True)
            channel = self.bot.get_channel(error_channel_id)
            await channel.send(f"server:{interaction.guild.name}使用者:{interaction.user.name}使用see_guild_booster錯誤:{e}")
    

async def setup(bot: commands.Bot):
    await bot.add_cog(Server_booster(bot))
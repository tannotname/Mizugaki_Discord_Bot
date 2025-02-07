import random
import sqlite3
from typing import Optional
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

serverinoutchannel = 1273144645580357675

def check_if_user_is_me(interaction: discord.Interaction) -> bool:
    return interaction.user.id == 710128890240041091


#drop table 
con = sqlite3.connect('announcementchannel.db') # 連線資料庫
cur = con.cursor() # 建立游標
 # 查詢第一筆資料
cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?", ("announcementchannel",))
row = cur.fetchone()[0]
    # 查詢資料庫是否存在
if row == 0:
    cur.execute("CREATE TABLE announcementchannel(guildid NUMERIC,guildname TEXT,channelid NUMERIC,channelname TEXT)")
    con.commit()
    print("表格 'announcementchannel' 已建立.")
else:
    print("表格“announcementchannel”已存在.")
    con.commit()


class Server(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    

    @app_commands.command(name="server_user_info",description = "列出使用者資訊")
    async def user_info(self, interaction: discord.Interaction, userid:str):
        try:
            user_id = int(userid)
            if interaction.user.name == "tan_00_00":
                user = await self.bot.fetch_user(user_id)
                if user is None:
                    await interaction.response.send_message("找不到此使用者",ephemeral=True)
                await interaction.response.send_message(f'User: {user.name}\nID: {user.id}' ,ephemeral=True)
            else:
                await interaction.response.send_message("沒有權限",ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"錯誤:{e}",ephemeral=True)

    @app_commands.command(name="serverlist",description = "列出機器人所在伺服器")
    async def serverlist(self, interaction: discord.Interaction,):
        try:
            if interaction.user.name == "tan_00_00":
                guilds = self.bot.guilds
                lite = "機器人加入伺服器：\n\n"
                for guild in guilds: 
                    lite += f"```{guild.name} {guild.id} {guild.owner_id} 人數:{guild.member_count}\n```\n"
                await interaction.response.send_message(lite,ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"錯誤:{e}",ephemeral=True)

    @app_commands.command(name="server_channel",description="列出伺服器文字頻道")
    async def server_channel(self,interaction:discord.Interaction,guildid:str):
        try:
            if interaction.user.name == "tan_00_00":
                guild = self.bot.get_guild(int(guildid))
                if guild is not None:
                    channels = guild.text_channels
                    channel1 = f"以下為{guild.name}所有頻道\n\n"
                    for channel in channels:
                        channel1 += f"{channel.name} id:{channel.id}\n"
                    await interaction.response.send_message(channel1,ephemeral=True)
                else:
                    await interaction.response.send_message("錯誤guild為None",ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"錯誤:{e}",ephemeral=True)

    @app_commands.command(name="server_kensuku_bot_channel",description="搜尋頻道")
    @app_commands.check(check_if_user_is_me)
    async def kesoku_bot_channel(self,interaction:discord.Interaction,channel_id:str):
        try:
            if interaction.user.name == "tan_00_00" and interaction.user.id == 710128890240041091:
                channel = self.bot.get_channel(int(channel_id))
                if channel is not None:
                    await interaction.response.send_message(f"{channel.guild.name} {channel.guild.id} {channel.name} id:{channel.id} 擁有者:{channel.guild.owner.id}",ephemeral=True)
                else:
                    await interaction.response.send_message("找不到此頻道",ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"錯誤:{e}",ephemeral=True)

    @app_commands.command(name="contact_robotmaker",description="聯絡機器人製作者")
    @app_commands.checks.has_permissions(administrator=True)
    async def Contact_administrator(self,interaction:discord.Interaction,message:str):
        try:
            channel = 1273145222813057045
            guild = interaction.guild
            username = interaction.user.name
            userid = interaction.user.id
            channel2 =interaction.channel.id
            channel = self.bot.get_channel(channel)
            await channel.send(f"# 使用者回報\n{username};{userid}\n{guild.name};{guild.id};{channel2}\n{message}")
            await interaction.response.send_message("已回報",ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"錯誤:{e}",ephemeral=True)

    @app_commands.command(name="server_creator_announcement",description="製作者公告") #於指定的channel發送公告
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(title = "公告標題",description = "公告描述",message = "公告內容")
    async def creator_announcement(self,interaction:discord.Interaction,title:str,description:str,message_name:str,message:str,message2_name:Optional[str],message2:Optional[str],guildid:str,channelid:str):
        try:
            if interaction.user.id == 710128890240041091:
                guildid = int(guildid)
                channelid = int(channelid)
                guild = self.bot.get_guild(guildid)
                channel = self.bot.get_channel(channelid)
                random7_int = random.randint(0, 255)
                random8_int = random.randint(0, 255)
                random9_int = random.randint(0, 255)
                emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int) # 決定embed顏色
                embed = discord.Embed(title=title, description= description, color= emb_color)
                embed.set_author(name= f"{interaction.user.name}",  icon_url= interaction.user.avatar.url)#作者
                embed.add_field(name=message_name,value=f"{message}",inline=False) #第一行(一定要有)
                if message2 is not None:
                    embed.add_field(name=message2_name,value=message2,inline=False) #第二行(可空白)
                embed.set_footer(text= "機器人支援伺服器:https://discord.gg/Eq52KNPca9") #頁尾

                await channel.send(embed=embed)
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message("沒有權限",ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"錯誤:{e}",ephemeral=True)

    @app_commands.command(name="server_announcement",description="機器人全域公告")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(title = "公告標題",description = "公告描述",message = "公告內容")
    @app_commands.check(check_if_user_is_me)
    async def server_announcement(self,interaction:discord.Interaction,title:str,description:Optional[str],message_name:str,message:str,message2_name:Optional[str],message2:Optional[str]):
        try:
            if interaction.user.id == 710128890240041091:
                guilds = self.bot.guilds
                random7_int = random.randint(0, 255)
                random8_int = random.randint(0, 255)
                random9_int = random.randint(0, 255)
                emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int) # 決定embed顏色
                if description is not None:
                    embed = discord.Embed(title=title, description= description, color= emb_color)
                if description is None:
                    embed = discord.Embed(title=title, color= emb_color)
                embed.set_author(name= f"{interaction.user.name}",  icon_url= interaction.user.avatar.url)#作者
                embed.add_field(name=message_name,value=f"{message}",inline=False) #第一行(一定要有)
                if message2 is not None:
                    embed.add_field(name=message2_name,value=message2,inline=False) #第二行(可空白)
                embed.set_footer(text= "機器人支援伺服器:https://discord.gg/Eq52KNPca9") #頁尾
                for guild in guilds:
                    guild_id = guild.id
                    conn = sqlite3.connect("announcementchannel.db")
                    comn = conn.cursor()
                    comn.execute("SELECT * FROM announcementchannel WHERE guildid=?",(guild_id,)) # 搜尋伺服器設定的頻道
                    rows = comn.fetchall()
                    conn.commit()
                    comn.close()
                    conn.close()
                    error = ""
                    try:
                        if rows == []:
                            guild = self.bot.get_guild(int(guild_id))
                            channels = guild.text_channels
                            if len(channels) > 1:
                                channel = channels[2]
                            else:
                                channel = channels[0]
                            print(f"{guild.name} {channel.name}")
                            await channel.send(embed=embed)
                            error += f"{guild.name} {message}"
                        if rows != []:
                            for row in rows:
                                channel = self.bot.get_channel(row[2])
                                print(f"{guild.name} {channel.name}")
                                await channel.send(embed=embed)
                                error += f"{guild.name} {message}"
                    except Exception as e:
                        error += f"{guild.name} {e}\n" 
                await interaction.response.send_message(error,ephemeral=True)
            else:
                await interaction.response.send_message("沒有權限",ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"{guild.name}錯誤:{e}",ephemeral=True)


    @app_commands.command(name="set_announcement_channel",description="設定機器人公告頻道")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_announcement_channel(self,interaction:discord.Interaction,channel:discord.TextChannel):
        try:
            channel_name = channel.name
            channel_id = channel.id
            guild_name = interaction.guild.name
            guild_id = interaction.guild.id
            con = sqlite3.connect("announcementchannel.db")
            cur = con.cursor()
            cur.execute("INSERT INTO announcementchannel (guildid,guildname,channelid,channelname) VALUES (?,?,?,?)",(guild_id,guild_name,channel_id,channel_name))
            con.commit()
            await interaction.response.send_message(f"已設置機器人公告頻道為:{guild_name},{channel_name}")
            con.close()
            cur.close()
            channel = self.bot.get_channel(1273145222813057045)
            await channel.send(f"伺服器:{guild_name}設置 {channel_name} 為公告頻道")
        except Exception as e:
            random7_int = random.randint(0, 255)
            random8_int = random.randint(0, 255)
            random9_int = random.randint(0, 255)
            emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
            await interaction.response.send_message(embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(self,guild: discord.Guild):
        channel = self.bot.get_channel(serverinoutchannel)
        try:
            guildurl = await guild.invites()
        except Exception as e:
            guildurl = f"No invite found:{e}"
        await channel.send(f"```\n機器人進入伺服器:{guild.name} {guild.id} {guild.member_count}\n```")

    @commands.Cog.listener()
    async def on_guild_remove(self,guild: discord.Guild):
        channel = self.bot.get_channel(serverinoutchannel)
        try:
            guildurl = await guild.invites()
        except Exception as e:
            guildurl = f"No invite found:{e}"
        await channel.send(f"```\n機器人離開伺服器:{guild.name} {guild.id} {guild.member_count}\n``` ")

        

async def setup(bot: commands.Bot):
    await bot.add_cog(Server(bot))
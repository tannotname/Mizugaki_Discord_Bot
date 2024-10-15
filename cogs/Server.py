import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

serverinoutchannel = 1273144645580357675

def check_if_user_is_me(interaction: discord.Interaction) -> bool:
    return interaction.user.id == 710128890240041091

class Server(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="serverlist",description = "列出機器人所在伺服器")
    async def serverlist(self, interaction: discord.Interaction,):
        try:
            if interaction.user.name == "tan_07_24":
                guilds = self.bot.guilds
                lite = "機器人加入伺服器：\n\n"
                for guild in guilds: 
                    lite += f"```{guild.name} {guild.id} {guild.owner_id}```\n"
                await interaction.response.send_message(lite,ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"錯誤:{e}")

    @app_commands.command(name="server_channel",description="列出伺服器頻道")
    async def server_channel(self,interaction:discord.Interaction,guildid:str):
        try:
            if interaction.user.name == "tan_07_24":
                guild = self.bot.get_guild(int(guildid))
                if guild is not None:
                    channels = guild.channels
                    channel1 = f"以下為{guild.name}所有頻道\n\n"
                    for channel in channels:
                        channel1 += f"{channel.name} id:{channel.id}\n"
                    await interaction.response.send_message(channel1,ephemeral=True)
                else:
                    await interaction.response.send_message("錯誤guild為None",ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"錯誤:{e}",ephemeral=True)

    @app_commands.command(name="kensuku_bot_channel",description="搜尋頻道")
    @app_commands.check(check_if_user_is_me)
    async def kesoku_bot_channel(self,interaction:discord.Interaction,channel_id:str):
        try:
            if interaction.user.name == "tan_07_24" and interaction.user.id == 710128890240041091:
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
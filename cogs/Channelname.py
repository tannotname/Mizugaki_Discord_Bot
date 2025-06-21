import random
import discord
from discord import app_commands
from discord.ext import commands

class Channelname(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = "text_channel_name_set", description = "更改文字頻道名稱")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def text_channel_name_set(self,interaction: discord.Interaction, channel: discord.TextChannel, new_name: str):
        try:    
            channelname = channel.name
            await channel.edit(name=new_name)
            await interaction.response.send_message(f"{interaction.user.nick or interaction.user.name}已將文字頻道{channelname}名稱更改為 {new_name}")
        except Exception as e:
            emb_color = discord.Color.from_rgb(255,0,0)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name = "voice_channel_name_set", description = "更改語音頻道名稱")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def voice_channel_name_set(self,interaction: discord.Interaction, channel: discord.VoiceChannel, new_name: str):
        try:
            channelname = channel.name
            await channel.edit(name=new_name)
            await interaction.response.send_message(f"{interaction.user.nick or interaction.user.name}已將語音頻道{channelname}名稱更改為 {new_name}")
        except Exception as e:
            emb_color = discord.Color.from_rgb(255,0,0)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name = "text_channel_delete", description = "刪除文字頻道")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def text_channel_delete(self,interaction: discord.Interaction, channel: discord.TextChannel):
        try:
            channelname = channel.name
            await interaction.response.send_message(f"已刪除{channelname}頻道")
            await channel.delete()
        except Exception as e:
            emb_color = discord.Color.from_rgb(255,0,0)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
            await interaction.response.send_message(embed=embed)


    @app_commands.command(name = "category_channel_delete", description = "刪除類別以及類別內的所有頻道")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def category_channel_delete(self,interaction: discord.Interaction, category: discord.CategoryChannel):
        try:
            categoryname = category.name
            channels = category.channels
            for channel in channels:
                print(f"已刪除{channel.name}頻道")
                await channel.delete()
            await interaction.response.send_message(f"已刪除{categoryname}類別以及類別內的所有頻道")
            await category.delete()
        except Exception as e:
            emb_color = discord.Color.from_rgb(255,0,0)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
            await interaction.response.send_message(embed=embed)

            
    @app_commands.command(name = "voice_channel_delete", description = "刪除語音頻道")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def voice_channel_delete(self,interaction: discord.Interaction, channel: discord.VoiceChannel):
        try:
            channelname = channel.name
            await interaction.response.send_message(f"已刪除{channelname}頻道")
            await channel.delete()
        except Exception as e:
            emb_color = discord.Color.from_rgb(255,0,0)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="voice_channel_bitrate_set", description="更改語音頻道位元率")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def voice_channel_bitrate_set(self,interaction:discord.Interaction,channel:discord.VoiceChannel,bitrate1:int):
        try:
            await channel.edit(bitrate=bitrate1)
            await interaction.response.send_message(f"已將頻道:{channel.name}位元率改成{bitrate1}")
        except Exception as e:
            emb_color = discord.Color.from_rgb(255,0,0)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
            await interaction.response.send_message(embed=embed) 

    @app_commands.command(name="更改語音頻道限制人數", description="更改語音頻道限制人數")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def user_limitVoiceChannel(self,interaction:discord.Interaction,channel:discord.VoiceChannel,user_limit:int):
        try:
            await channel.edit(user_limit=user_limit)
            await interaction.response.send_message(f"已限制頻道{channel.name}的人數為:{user_limit}位使用者")
        except Exception as e:
            emb_color = discord.Color.from_rgb(255,0,0)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
            await interaction.response.send_message(embed=embed) 

    @app_commands.command(name="更改文字頻道說明", description="更改文字頻道說明")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def topicTextChannel(self,interaction:discord.Interaction,channel:discord.TextChannel,topic:str):
        try:    
            await channel.edit(topic=topic)
            await interaction.response.send_message(f"已將文字頻道 {channel.name }說明設為: {topic}")
        except Exception as e:
            emb_color = discord.Color.from_rgb(255,0,0)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
            await interaction.response.send_message(embed=embed)
          
    @app_commands.command(name="move_to_none",description="移出語音頻道中的成員")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def movetonone(self,interaction:discord.Interaction,user:discord.Member):
        try:
            await user.move_to(None)
            await interaction.response.send_message(f"已將{user.name}踢出語音頻道",ephemeral=True)
        except Exception as e:
            emb_color = discord.Color.from_rgb(255,0,0)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
            await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Channelname(bot))
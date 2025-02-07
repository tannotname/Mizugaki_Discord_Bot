import random
import discord
from discord import app_commands
from discord.ext import commands
from typing import List, Union

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
            random7_int = random.randint(0, 255)
            random8_int = random.randint(0, 255)
            random9_int = random.randint(0, 255)
            emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name = "voice_channel_name_set", description = "更改語音頻道名稱")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def voice_channel_name_set(self,interaction: discord.Interaction, channel: discord.VoiceChannel, new_name: str):
            await channel.edit(name=new_name)
            await interaction.response.send_message(f"{interaction.user.nick or interaction.user.name}已將此頻道名稱更改為 {new_name}")

    @app_commands.command(name = "text_channel_delete", description = "刪除文字頻道")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def text_channel_delete(self,interaction: discord.Interaction, channel: discord.TextChannel):
            await interaction.response.send_message(f"已刪除{channel.name}頻道")
            await channel.delete()

    @app_commands.command(name = "category_channel_delete", description = "刪除類別以及類別內的所有頻道")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def category_channel_delete(self,interaction: discord.Interaction, category: discord.CategoryChannel):
            channels = category.channels
            for channel in channels:
                print(f"已刪除{channel.name}頻道")
                await channel.delete()
            await interaction.response.send_message(f"已刪除{category.name}")
            await category.delete()
            

    @app_commands.command(name = "voice_channel_delete", description = "刪除語音頻道")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def voice_channel_delete(self,interaction: discord.Interaction, channel: discord.VoiceChannel):
            await interaction.response.send_message(f"已刪除{channel.name}頻道")
            await channel.delete()

    @app_commands.command(name="voice_channel_bitrate_set", description="更改語音頻道位元率")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def voice_channel_bitrate_set(self,interaction:discord.Interaction,channel:discord.VoiceChannel,bitrate1:int):
        try:
            await channel.edit(bitrate=bitrate1)
            await interaction.response.send_message(f"已將位元率改成{bitrate1}")
        except Exception as e:
            random7_int = random.randint(0, 255)
            random8_int = random.randint(0, 255)
            random9_int = random.randint(0, 255)
            emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
            await interaction.response.send_message(embed=embed) 

    @app_commands.command(name="更改語音頻道限制人數", description="更改語音頻道限制人數")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def user_limitVoiceChannel(self,interaction:discord.Interaction,channel:discord.VoiceChannel,user_limit:int):
        try:
            await channel.edit(user_limit=user_limit)
            await interaction.response.send_message(f"已限制頻道人數為: {user_limit}")
        except Exception as e:
            random7_int = random.randint(0, 255)
            random8_int = random.randint(0, 255)
            random9_int = random.randint(0, 255)
            emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
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
            random7_int = random.randint(0, 255)
            random8_int = random.randint(0, 255)
            random9_int = random.randint(0, 255)
            emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
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
            random7_int = random.randint(0, 255)
            random8_int = random.randint(0, 255)
            random9_int = random.randint(0, 255)
            emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
            await interaction.response.send_message(embed=embed,ephemeral=True) 

async def setup(bot: commands.Bot):
    await bot.add_cog(Channelname(bot))
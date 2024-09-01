import random
import discord
from discord.ext import commands
from discord import app_commands
from discord.ext import commands
from pytube import YouTube
import os
import ssl
ssl._create_default_https_context = ssl._create_stdlib_context
os.chdir('C:\\Users\\曉黑\\Desktop\\DISCORDBOTmain\\')



class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    
    @app_commands.command(name="join_in_voicechanne",description="讓機器人進入語音播放音樂")
    async def record(self, interaction: discord.Interaction, channel: discord.VoiceChannel, musicename: str, musicurl: str):
        try:
            await channel.connect()
            await self.download_music(interaction, musicename, musicurl)
        except Exception as e:
            await self.handle_error(interaction, e, "錯誤")

    async def download_music(self, interaction: discord.Interaction, musicename: str, musicurl: str):
        try:
            yt = YouTube(musicurl)
            print('download...')
            os.chdir('C:\\Users\\曉黑\\Desktop\\DISCORDBOTmain\\')
            yt.streams.filter().get_audio_only().download(filename=f'{musicename}.mp3')
            await self.play_music(interaction, musicename)
        except Exception as e:
            await self.handle_error(interaction, e, "下載錯誤")

    async def play_music(self, interaction: discord.Interaction, musicename: str):
        try:
            voice_client = interaction.guild.voice_client
            if voice_client and voice_client.is_connected():
                voice_client.play(discord.FFmpegPCMAudio(f"C:\\Users\\曉黑\\Desktop\\DISCORDBOTmain\\{musicename}.mp3"))
                await interaction.response.send_message(f"播放{musicename}")
            else:
                await interaction.response.send_message("機器人未連接語音頻道")
        except Exception as e:
            await self.handle_error(interaction, e, "播放錯誤")

    async def handle_error(self, interaction: discord.Interaction, exception: Exception, title: str):
        random7_int = random.randint(0, 255)
        random8_int = random.randint(0, 255)
        random9_int = random.randint(0, 255)
        emb_color = discord.Color.from_rgb(random7_int, random8_int, random9_int)
        embed = discord.Embed(title=title, color=emb_color)
        embed.add_field(name=str(exception), value="若有問題請告知 <@710128890240041091> ", inline=False)
        await interaction.response.send_message(embed=embed)
    
    
    @app_commands.command(name="stop_record",description="讓機器人離開語音")
    async def stoprecord(self,interaction:discord.Interaction):
        try:
            guild = interaction.guild
            channel = await guild.voice_client.disconnect()
            await interaction.response.send_message(f"機器人已離開 channel:{channel}")
        except Exception as e:
            random7_int = random.randint(0, 255)
            random8_int = random.randint(0, 255)
            random9_int = random.randint(0, 255)
            emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="若有問題請告知 <@710128890240041091> ",inline=False)
            await interaction.response.send_message(embed=embed)

    
    @app_commands.command(name="播放音樂", description="讓機器人播放指定音樂")
    async def musicbot(self, interaction: discord.Interaction, musicename: str, musicurl: str):
        try:
            # Download and play music
            try:
                yt = YouTube(musicurl)
                print('download...')
                os.chdir('C:\\Users\\曉黑\\Desktop\\DISCORDBOTmain\\')
                yt.streams.filter().get_audio_only().download(filename=f'{musicename}.mp3')
            except Exception as e:
                # Handle download error
                await self.handle_error(interaction, e, "下載錯誤")

            try:
                # Play music
                voice_client = interaction.guild.voice_client
                if voice_client and voice_client.is_connected():
                    voice_client.play(discord.FFmpegPCMAudio(f"C:\\Users\\曉黑\\Desktop\\DISCORDBOTmain\\{musicename}.mp3"))
                    await interaction.response.send_message(f"播放{musicename}")
                else:
                    await interaction.response.send_message("機器人未連接語音頻道")
            except Exception as e:
                # Handle play error
                await self.handle_error(interaction, e, "播放錯誤")
        except Exception as e:
            # Handle general error
            await self.handle_error(interaction, e, "錯誤")

    async def handle_error(self, interaction: discord.Interaction, exception: Exception, title: str):
        random7_int = random.randint(0, 255)
        random8_int = random.randint(0, 255)
        random9_int = random.randint(0, 255)
        emb_color = discord.Color.from_rgb(random7_int, random8_int, random9_int)
        embed = discord.Embed(title=title, color=emb_color)
        embed.add_field(name=str(exception), value="若有問題請告知 <@710128890240041091> ", inline=False)
        await interaction.response.send_message(embed=embed)
            






async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))
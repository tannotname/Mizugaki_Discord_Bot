import random
import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
import yt_dlp
from yt_dlp import YoutubeDL

class Musicedownload(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="yt_musice_download",description = "下載YT上的影片成MP3")
    async def yt_musice_download(self, interaction: discord.Interaction,url:str):
        try:
                def download_mp3(url, output_path="musice\\%(title)s"):
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': output_path,
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                    }

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info_dict = ydl.extract_info(url, download=True)  # 下載影片
                        filename = ydl.prepare_filename(info_dict)  # 取得下載的檔案名稱
                        return filename
                await interaction.response.send_message("下載中...",ephemeral=True)
                # 測試下載
                video_url = url  # 替換為你的影片網址
                downloaded_file = download_mp3(video_url)
                try:
                    print(downloaded_file)
                    await interaction.followup.send(file=discord.File(f"{downloaded_file}.mp3"),ephemeral=True) # 有問題
                    print("傳送成功")
                except Exception as e:
                    random7_int = random.randint(0, 255)
                    random8_int = random.randint(0, 255)
                    random9_int = random.randint(0, 255)
                    emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
                    embed = discord.Embed(title="錯誤", color= emb_color)
                    embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
                    await interaction.response.send_message(embed=embed)
                    channel = self.bot.get_channel(1273144773435326545)
                    await channel.send(f"{interaction.guild.name} {interaction.user.name} 音樂下載錯誤錯誤:{e}")      
        except Exception as e:
            random7_int = random.randint(0, 255)
            random8_int = random.randint(0, 255)
            random9_int = random.randint(0, 255)
            emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
            await interaction.response.send_message(embed=embed)
            channel = self.bot.get_channel(1273144773435326545)
            await channel.send(f"{interaction.guild.name} {interaction.user.name} 音樂下載錯誤錯誤:{e}")
        

        




async def setup(bot: commands.Bot):
    await bot.add_cog(Musicedownload(bot)) # ,guild = discord.Object(id = 1213748875471364137)
import datetime
import random
import discord
from discord.ext import commands
from discord import app_commands
from discord.ext import commands, tasks

channel_creators = {}

class Voiceinout(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("已載入voice")

    @commands.Cog.listener()
    async def on_voice_state_update(self,member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if before.channel is None and after.channel is not None:
            nickname = member.nick if member.nick else member.name
            channel = after.channel
            random7_int = random.randint(0, 255)
            random8_int = random.randint(0, 255)
            random9_int = random.randint(0, 255)
            emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
            embed = discord.Embed(title="成員加入", description=f"{nickname} 加入 {after.channel.name}", color= emb_color)
            await channel.send(embed=embed)
        elif after.channel is None and before.channel is not None:
            nickname = member.nick if member.nick else member.name
            channel = before.channel
            random7_int = random.randint(0, 255)
            random8_int = random.randint(0, 255)
            random9_int = random.randint(0, 255)
            emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
            embed = discord.Embed(title="成員離開", description=f"{nickname} 離開 {before.channel.name}", color= emb_color)
            await channel.send(embed=embed)
        elif before.channel != after.channel:
            if after.channel is not None:
                nickname = member.nick if member.nick else member.name
                channel = after.channel
                random7_int = random.randint(0, 255)
                random8_int = random.randint(0, 255)
                random9_int = random.randint(0, 255)
                emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
                embed = discord.Embed(title="成員加入", description=f"{nickname} 從 {before.channel.name}移動過來", color= emb_color)
                await channel.send(embed=embed)
                channel = before.channel
                random7_int = random.randint(0, 255)
                random8_int = random.randint(0, 255)
                random9_int = random.randint(0, 255)
                emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
                embed = discord.Embed(title="成員移動", description=f"{nickname} 移動到 {after.channel.name}", color= emb_color)
                await channel.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Voiceinout(bot))
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
            replies1 = (f"耶!他成功了 {nickname}")
            replies2 = (f"讓我們歡迎 {nickname} 我們希望他帶個披薩")
            replies3 = (f"{nickname} 墜入了 {after.channel.name}")
            replies4 = (f"{nickname} 成功降落到 {after.channel.name}")
            replies5 = (f"{nickname} 不小心滑進了 {after.channel.name}")
            replies6 = (f"{nickname} 跳進了 {after.channel.name}")
            replies7 = (f"{nickname} 他來了")
            replies8 = (f"{nickname} 駕到")
            replies9 = (f"{nickname} 已加入隊伍")
            replies10 = (f"野生的 {nickname} 出現了")
            replies = [
                        (replies1, 0.1),
                        (replies2, 0.1),
                        (replies3, 0.1),
                        (replies4, 0.1),
                        (replies5, 0.1),
                        (replies6, 0.1),
                        (replies7, 0.1),
                        (replies8, 0.1),
                        (replies9, 0.1),
                        (replies10, 0.1)
                ]
                # 選擇回覆
            reply = random.choices([reply[0] for reply in replies], weights=[reply[1] for reply in replies], k=1)[0]
            embed = discord.Embed(title="成員加入", description=reply, color= emb_color)
            await channel.send(embed=embed)
        elif after.channel is None and before.channel is not None:
            nickname = member.nick if member.nick else member.name
            channel = before.channel
            random7_int = random.randint(0, 255)
            random8_int = random.randint(0, 255)
            random9_int = random.randint(0, 255)
            emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
            replies1 = (f"讓我們哀弔 {nickname}")
            replies2 = (f" {nickname} 他不愛我們所以離開了")
            replies3 = (f"{nickname} 跳出了 {before.channel.name}")
            replies4 = (f"{nickname} 成功離開了 {before.channel.name}")
            replies5 = (f"{nickname} 不小心掉出了 {before.channel.name}")
            replies6 = (f"{nickname} 跑走了")
            replies7 = (f"{nickname} 他離開了")
            replies8 = (f"{nickname} 墜落")
            replies9 = (f"{nickname} 起飛")
            replies10 = (f"不野生的 {nickname} 離開了")
            replies = [
                        (replies1, 0.1),
                        (replies2, 0.1),
                        (replies3, 0.1),
                        (replies4, 0.1),
                        (replies5, 0.1),
                        (replies6, 0.1),
                        (replies7, 0.1),
                        (replies8, 0.1),
                        (replies9, 0.1),
                        (replies10, 0.1)
                ]
                # 選擇回覆
            reply = random.choices([reply[0] for reply in replies], weights=[reply[1] for reply in replies], k=1)[0]
            embed = discord.Embed(title="成員out", description=reply, color= emb_color)
            await channel.send(embed=embed)
        elif before.channel != after.channel:
            if after.channel is not None:
                nickname = member.nick if member.nick else member.name
                channel = after.channel
                random7_int = random.randint(0, 255)
                random8_int = random.randint(0, 255)
                random9_int = random.randint(0, 255)
                emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
                embed = discord.Embed(title="成員加入", description=f"{nickname} 降落!", color= emb_color)
                await channel.send(embed=embed)
                channel = before.channel
                random7_int = random.randint(0, 255)
                random8_int = random.randint(0, 255)
                random9_int = random.randint(0, 255)
                emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
                embed = discord.Embed(title="成員out", description=f"{nickname} out", color= emb_color)
                await channel.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Voiceinout(bot))
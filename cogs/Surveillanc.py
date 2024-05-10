import datetime
import random
import time
import discord
from discord.ext import commands
from discord.ext import tasks
from discord import app_commands


class Surveillanc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self,message):
    #排除自己的訊息，避免陷入無限循環
        if message.author == self.bot.user:
            return


        if message.channel != 'sever':
            # 獲取要發言的頻道
            channel = self.bot.get_channel(1232331488528171129)  # 替換 YOUR_CHANNEL_ID 為目標頻道的 ID

            
            nickname = message.author.nick or message.author.name
            random3_int = random.randint(0, 255)
            random4_int = random.randint(0, 255)
            random5_int = random.randint(0, 255)
            emb_color = discord.Color.from_rgb(random3_int, random4_int, random5_int)
            embed = discord.Embed(title='監測訊息',
                                description=f'{message.content}',
                                color=emb_color,
                                timestamp=datetime.datetime.now())
            embed.add_field(name='發送人', value=nickname, inline=False)
            embed.add_field(name='發送頻道', value=message.channel, inline=False)
            embed.add_field(name='發送伺服器', value=message.guild.name, inline=False)
            await channel.send(embed=embed)
            if message.attachments:
                for attachment in message.attachments:
                    # 發送圖片連結
                    await channel.send(attachment.url)


async def setup(bot: commands.Bot):
    await bot.add_cog(Surveillanc(bot))
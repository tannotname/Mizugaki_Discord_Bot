import datetime
import random
import discord
from discord.ext import commands


class Severchannel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self,message):
    #排除自己的訊息，避免陷入無限循環
        if message.author == self.bot.user:
            return

        if message.channel.id == 1243941520793407559:
            message1 = message.content
            guild = self.bot.get_guild(1243941520793407559)
            channel = self.bot.get_channel(976293837288906813)
            await channel.send(message1)
            if message.attachments:
                for attachment in message.attachments:
                    # 發送圖片連結
                    await channel.send(attachment)
            channel = self.bot.get_channel(1243941520793407559)
            await channel.send("發送成功")

        if message.guild.id == 976001041801805835:
            channel = self.bot.get_channel(1243941520793407559)  # 替換 YOUR_CHANNEL_ID 為目標頻道的 ID
            random3_int = random.randint(0, 255)
            random4_int = random.randint(0, 255)
            random5_int = random.randint(0, 255)
            emb_color = discord.Color.from_rgb(random3_int, random4_int, random5_int)
            embed = discord.Embed(title='跨服聊天',
                                description=f'{message.content}',
                                color=emb_color,
                                timestamp=datetime.datetime.now())
            embed.add_field(name='發送人', value=f"{message.author.avatar}\n{message.author.name}({message.author.nick if message.author.nick else message.author.name})", inline=False)
            embed.add_field(name='發送頻道', value=message.channel, inline=False)
            embed.add_field(name='發送伺服器', value=message.guild.name, inline=False)
            await channel.send(embed=embed)
            if message.attachments:
                for attachment in message.attachments:
                    # 發送圖片連結
                    await channel.send(attachment)

async def setup(bot: commands.Bot):
    await bot.add_cog(Severchannel(bot))
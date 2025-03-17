import time
import discord
import sqlite3
import random
from discord.ext import commands



class Mante(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    error_channel_id = 1273144773435326545
    iris_id = 869508194383298612
    my_guild_id = 1238133524662325351




async def setup(bot: commands.Bot):
    await bot.add_cog(Mante(bot))
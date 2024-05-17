from typing import Optional
import discord
import random
import datetime
import requests
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
if API_KEY is None:
    print("錯誤：找不到 API 令牌。請設置 API 環境變數。")
    exit()



class Slash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = "提問", description = "讓機器人回答你的問題")
    async def 提問(self, interaction: discord.Interaction, 問題: str):
        # 生成一個 1 到 10 之間的隨機整數（包含 1 和 10）
        random2_int = random.randint(1, 99) 
        my_list = ['不是', '是']
        random_element = random.choice(my_list)
        sentence = "{} % {}".format(random2_int, random_element)
        replies2 = [
                    ('就是了拉', 0.2),
                    (sentence, 0.6),
                    ('或許大概應該不是', 0.2)
                ]
        random3_int = random.randint(0, 255)
        random4_int = random.randint(0, 255)
        random5_int = random.randint(0, 255)
        reply = random.choices([reply[0] for reply in replies2], weights=[reply[1] for reply in replies2], k=1)[0]
        sentence1 ="我覺得 {} <:986296828322525224:1026433054958440508>".format(reply)
        emb_color = discord.Color.from_rgb(random3_int, random4_int , random5_int)
        embed = discord.Embed(title='<:74277272:1209520682728427551> | '+ 問題 , description = sentence1 , color = emb_color)
        await interaction.response.send_message(embed = embed)

    @app_commands.command(name = "匯率", description = "查看匯率")
    @app_commands.choices(
        iso = [
            Choice(name = "澳幣", value = "AUD"),
            Choice(name = "加幣", value = "CAD" ),
            Choice(name = "人民幣", value = "CNY"),
            Choice(name = "歐元", value = "EUR"),
            Choice(name = "港幣", value = "HKD"),
            Choice(name = "日圓", value = "JPY"),
            Choice(name = "澳門幣", value = "MOP"),
            Choice(name = "新臺幣", value = "TWD"),
            Choice(name = "英鎊", value = "GBP"),
            Choice(name = "韓圜", value = "KRW"),
            Choice(name = "美元", value = "USD"),
            Choice(name = "越南盾", value = "VND"),
        ]
)
    async def 匯率(self,interaction: discord.Interaction, iso:Choice[str]):
            # 發送請求到 Open Exchange Rates API 以獲取匯率
            iso = iso.value # type: ignore
            response = requests.get(f'https://open.er-api.com/v6/latest/TWD', params={'app_id': API_KEY})
            data = response.json()
            # 檢查是否成功取得匯率數據
            if response.status_code == 200:
                # 檢查貨幣是否有效
                if iso in data['rates']:
                    exchange_rate = data['rates'][iso]
                    await interaction.response.send_message(f'1 TWD = {exchange_rate} {iso} ')
                else:
                    await interaction.response.send_message('無效的貨幣代碼')
            else:
                await interaction.response.send_message('無法獲取匯率數據')

    @app_commands.command(name = "help", description = "機器人幫助指令")
    async def help(self,interaction: discord.Interaction):
        random7_int = random.randint(0, 255)
        random8_int = random.randint(0, 255)
        random9_int = random.randint(0, 255)
        emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
        embed = discord.Embed(title='指令列表', description='以下是可用指令列表：', color= emb_color,timestamp = datetime.datetime.now())
        embed.add_field(name='/help', value='幫助指令', inline=False)
        embed.add_field(name='/提問', value='讓機器人回答你的問題', inline=False)
        embed.add_field(name='/匯率', value='查看匯率', inline=False)
        embed.add_field(name='/查代碼', value='查詢貨幣代碼', inline=False)
        embed.add_field(name='新增貨幣代碼', value='使用方式 【iso4217 貨幣中文 貨幣代碼】', inline=False)
        embed.add_field(name='/更改文字頻道名稱', value='<文字頻道> <新的名稱>', inline=False)
        embed.add_field(name='/更改語音頻道名稱', value='<語音頻道> <新的名稱>', inline=False)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name = "upfile", description = "讓機器人幫你傳送訊息並提及全部人")
    async def upfile(self,interaction: discord.Interaction,file: Optional[discord.Attachment],file2:Optional[discord.Attachment] ,say:str):
        await interaction.response.send_message(f"@everyone {say} {file} {file2}")

    @app_commands.command(name="標雷盤",description="發送食物 標 雷盤")
    @app_commands.choices(
        say = [
            Choice(name = "早餐", value = "1"),
            Choice(name = "午餐", value = "2"),
            Choice(name = "晚餐", value = "3"),
            Choice(name = "宵夜", value = "4"),
        ]
)
    async def qnor(self,interaction: discord.Interaction,file:discord.Attachment,say:Choice[str]):
        say = say.name
        if interaction.guild.id == 1213748875471364137 :
            await interaction.response.send_message(f"<@557540063525994496> {say} {file}")
        else:
            await interaction.response.send_message("此伺服器禁用此功能")

    @app_commands.command(name="新增動態文字頻道",description="新增屬於你的文字頻道")
    async def newchannelyou(self,interaction:discord.Interaction,channelneme:str):
        guild = interaction.guild
        newchannel = await guild.create_text_channel(name=channelneme,topic=f"屬於 {interaction.user.name} 與他的朋友們的專屬文字頻道,使用完畢記得刪除!請注意!扳手還是看的到此頻道")
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False)
        }
        await newchannel.edit(overwrites=overwrites)
        await newchannel.set_permissions(interaction.user, manage_channels=True,read_messages=True)
        await interaction.user.send(f"""已創建專屬於你的文字頻道在: {interaction.guild.name} 
現在快使用/給予你的朋友觀看頻道的權利吧! 
頻道使用完畢請記得刪除 /刪除文字頻道""")
        await newchannel.send(f"""{interaction.user.mention}已創建專屬於你的文字頻道在: {interaction.guild.name} 
現在快使用/給予你的朋友觀看頻道的權利吧! 
頻道使用完畢請記得刪除 /刪除文字頻道""")

    @app_commands.command(name="給予專屬頻道加入權限",description="給予專屬頻道加入權限")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def giveglass(self,interaction:discord.Interaction,username:discord.Member,channel:discord.TextChannel,give_or_out:bool):
        if give_or_out == True:
            await channel.set_permissions(username, read_messages=True)
            await interaction.response.send_message(f"已給予{username} 頻道 {channel.name} 觀看權限")
        if give_or_out == False:
            await channel.set_permissions(username, read_messages=False)
            await interaction.response.send_message(f"已剝奪{username} 頻道 {channel.name} 觀看權限")



async def setup(bot: commands.Bot):
    await bot.add_cog(Slash(bot))
 
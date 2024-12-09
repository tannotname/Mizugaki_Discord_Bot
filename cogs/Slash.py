import subprocess
from typing import Optional
import discord
import random
import requests
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice
import os
import string
import random
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
if API_KEY is None:
    print("錯誤：找不到 API 令牌。請設置 API 環境變數。")
    exit()

ffmpeg_process = None  # 將ffmpeg_process定義為全局變量

def check_if_guild_is_me(interaction: discord.Interaction) -> bool:
    return interaction.guild.id == 1238133524662325351

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

    @app_commands.command(name="新增動態文字_and_語音頻道",description="新增屬於你的頻道組合")
    async def newchannelyou(self,interaction:discord.Interaction,channelname:str):
        guild = interaction.guild
        newcategory = await guild.create_category(name=channelname,position=0)
        newchannel = await guild.create_text_channel(name=channelname,category=newcategory,topic=f"屬於 {interaction.user.name} 與他的朋友們的專屬文字頻道,使用完畢記得刪除!請注意!扳手還是看的到此頻道")
        newvoicechannel = await guild.create_voice_channel(name=channelname,category=newcategory,rtc_region="japan")
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False)
        }
        await newcategory.edit(overwrites=overwrites)
        await newcategory.set_permissions(interaction.user, manage_channels=True,read_messages=True)
        try:
            # 同步頻道權限
            await newchannel.edit(sync_permissions=True)
            await newvoicechannel.edit(sync_permissions=True)
            print(f'頻道 {newchannel.name} 的權限已同步至分類 {newchannel.category.name}。')
        except Exception as e:
            print(f'同步頻道權限時發生錯誤：{e}')

        await interaction.user.send(f"""已創建專屬於你的文字頻道在: {interaction.guild.name} \n現在快使用/給予你的朋友觀看頻道的權利吧! \n頻道使用完畢請記得刪除 /刪除文字頻道""")
        await newchannel.send(f"""{interaction.user.mention}已創建專屬於你的文字頻道在: {interaction.guild.name} 
現在快使用/給予你的朋友觀看頻道的權利吧!
頻道使用完畢請記得刪除 /刪除文字頻道""")

    @app_commands.command(name="給予專屬頻道加入權限",description="給予專屬頻道加入權限")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def giveglass(self,interaction:discord.Interaction,username:discord.Member,username1:Optional[discord.Member],category:discord.CategoryChannel,give_or_out:bool):
        if give_or_out == True:
            await category.set_permissions(username, read_messages=True)
            channels = category.channels
        if give_or_out == True:
            if username1 is not None:
                await category.set_permissions(username1, read_messages=True)
        if not channels:
            print(f'分類 {category.name} 中沒有頻道。')
            return
        try:
            # 同步每個頻道的權限
            for channel in channels:
                await channel.edit(sync_permissions=True)
            print(f'分類 {category.name} 中的所有頻道權限已同步。')
            await interaction.response.send_message(f"已給予{username} 頻道 {category.name} 觀看權限")
        except Exception as e:
            print(f'同步分類內頻道權限時發生錯誤：{e}')
        if give_or_out == False:
            await category.set_permissions(username, read_messages=False)
        if not channels:
            print(f'分類 {category.name} 中沒有頻道。')
            return
        try:
            # 同步每個頻道的權限
            for channel in channels:
                await channel.edit(sync_permissions=True)
            print(f'分類 {category.name} 中的所有頻道權限已同步。')
            await interaction.response.send_message(f"已剝奪{username} 頻道 {category.name} 觀看權限")
        except Exception as e:
            print(f'同步分類內頻道權限時發生錯誤：{e}')

    @app_commands.command(name="help", description="列出所有斜杠指令")
    async def help_command(self, interaction: discord.Interaction):
        try:
            commands = self.bot.tree.walk_commands()
            help_message = ""
            for command in commands:
                if isinstance(command, app_commands.Command):
                    if command.description:
                        help_message += f"/{command.name} - {command.description}\n"
                    else:
                        help_message += f"/{command.name}\n"
            await interaction.response.send_message(f"```{help_message}```")
        except Exception as e:
            await interaction.response.send_message(f'發送訊息時發生錯誤：{e}',ephemeral=True)

    @app_commands.command(name="new_role",description="創建新的身分組並給予自己")
    @app_commands.describe(new_role_name = "新的身分組名字",color = "16進位制的色碼",give_in_you ="是否給予自己此身分組",reason="原因")
    async def newrole(self,interaction:discord.Interaction,new_role_name:str,color:str,give_in_you:bool,reason:str):
        try:
            guild = interaction.guild
            member = interaction.user
            try:
                color = discord.Colour(int(color, 16))
                newrloe = await guild.create_role(name=new_role_name,colour=color,reason=reason)
                await interaction.response.send_message(f"已新增{newrloe.name}")
                if give_in_you == True:
                    await member.add_roles(newrloe)
                    await interaction.followup.send(f"已給予{member.nick} {newrloe.name} 身分組")
            except ValueError:
                await interaction.response.send_message("顏色格式錯誤，請使用十六進制顏色碼，例如 'FF5733'。")
                return
        except Exception as e:
            await interaction.response.send_message(f"錯誤:{e}",ephemeral=True)
    
    @app_commands.command(name="give_or_out_user_new_role",description="給予或移除伺服器成員新的身分組")
    @app_commands.checks.has_permissions(administrator=True)
    async def usernewrole(self,interaction:discord.Interaction,role:discord.Role,member:discord.Member,out_give:bool):
        try:
            if out_give == True:
                await member.add_roles(role)
                await interaction.response.send_message(f"已給予{member.nick} {role.name} 身分組")
            else:
                await member.remove_roles(role)
                await interaction.response.send_message(f"已刪除{member.nick} 的 {role} 身分組")
        except Exception as e:
            await interaction.response.send_message(f"報錯:{e}",ephemeral=True)

    @app_commands.command(name="giverole",description="給予或移除伺服器成員新的身分組")
    async def user12365478(self,interaction:discord.Interaction,role:discord.Role,member:discord.Member,out_give:bool):
        try:
            if interaction.user.name == "tan_07_24":
                if out_give == True:
                    await member.add_roles(role)
                    await interaction.response.send_message(f"已給予{member.nick} {role.name} 身分組",ephemeral=True)
                else:
                    await member.remove_roles(role)
                    await interaction.response.send_message(f"已刪除{member.nick} 的 {role} 身分組")
        except Exception as e:
            await interaction.response.send_message(f"報錯:{e}",ephemeral=True)


    @app_commands.command(name="say",description="讓機器人幫你說話")
    async def say(self,interaction:discord.Interaction,話:str):
        try:
            if "@" in 話:
                await interaction.response.send_message(f"{interaction.user.name} {"別想用我@人"}")
            else:
                channel = interaction.channel
                await channel.send(f"{話}")
                channel = self.bot.get_channel(1273144773435326545)
                await channel.send(f"{interaction.user.name} 使用:{話}")
                await interaction.response.send_message("已執行指令",ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"發生錯誤:{e}")

    @app_commands.command(name="ban",description="停權使用者")
    @app_commands.checks.has_permissions(administrator=True)
    async def ban(self,interaction:discord.Interaction,member:discord.Member):
        try:
            await member.ban()
            await interaction.response.send_message(f"已封鎖{member.name}")
        except Exception as e:
            random7_int = random.randint(0, 255)
            random8_int = random.randint(0, 255)
            random9_int = random.randint(0, 255)
            emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
            await interaction.response.send_message(embed=embed) 

    @app_commands.command(name="ὀστρακισμός",description="放逐指定成員")
    @app_commands.checks.has_permissions(administrator=True)
    async def ὀστρακισμός(self,interaction:discord.Interaction,member:discord.Member):
        try:
            await member.kick()
            await interaction.response.send_message(f"已放逐指定成員{member.name}")
        except Exception as e:
            random7_int = random.randint(0, 255)
            random8_int = random.randint(0, 255)
            random9_int = random.randint(0, 255)
            emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
            await interaction.response.send_message(embed=embed) 

    @app_commands.command(name="複製伺服器頻道",description="複製所選的伺服器所有頻道")
    @app_commands.checks.has_permissions(administrator=True)
    async def copychannel(self,interaction:discord.Interaction,guildid1:str,guildid2:str):
        try:
            guild = self.bot.get_guild(int(guildid1))
            guild2 = self.bot.get_guild(int(guildid2))
            try:
                for category in guild.categories:
                    await guild2.create_category(name=category.name)
            except Exception as e:
                random7_int = random.randint(0, 255)
                random8_int = random.randint(0, 255)
                random9_int = random.randint(0, 255)
                emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
                embed = discord.Embed(title="錯誤", color= emb_color)
                embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
                await interaction.response.send_message(embed=embed) 
            try:
                for channel in guild.text_channels:
                    await guild2.create_text_channel(name=channel.name, category=channel.category)
            except Exception as e:
                random7_int = random.randint(0, 255)
                random8_int = random.randint(0, 255)
                random9_int = random.randint(0, 255)
                emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
                embed = discord.Embed(title="錯誤", color= emb_color)
                embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
                await interaction.response.send_message(embed=embed) 
            try:
                for channel in guild.voice_channels:
                    await guild2.create_voice_channel(name=channel.name, category=channel.category)
            except Exception as e:
                random7_int = random.randint(0, 255)
                random8_int = random.randint(0, 255)
                random9_int = random.randint(0, 255)
                emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
                embed = discord.Embed(title="錯誤", color= emb_color)
                embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
                await interaction.response.send_message(embed=embed) 
            await interaction.response.send_message("執行",ephemeral=True)
        except Exception as e:
            random7_int = random.randint(0, 255)
            random8_int = random.randint(0, 255)
            random9_int = random.randint(0, 255)
            emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
            await interaction.response.send_message(embed=embed) 

    @app_commands.command(name="新增文字_and_語音頻道",description="新增頻道組合")
    @app_commands.checks.has_permissions(administrator=True)
    async def newcategory(self,interaction:discord.Interaction,channelname:str,categoryname:str,):
        guild = interaction.guild
        newcategory = await guild.create_category(name=categoryname,position=2)
        await guild.create_text_channel(name=channelname,category=newcategory)
        await guild.create_voice_channel(name=channelname,category=newcategory,rtc_region="japan")
        await interaction.response.send_message("執行",ephemeral=True)

    @app_commands.command(name="新增文字頻道",description="新增文字頻道")
    @app_commands.checks.has_permissions(administrator=True)
    async def newchannel(self,interaction:discord.Interaction,channelname:str,category:discord.CategoryChannel):
        try:
            guild = interaction.guild
            await guild.create_text_channel(name=channelname,category=category)
            await interaction.response.send_message("執行",ephemeral=True)
        except Exception as e:
            random7_int = random.randint(0, 255)
            random8_int = random.randint(0, 255)
            random9_int = random.randint(0, 255)
            emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
            await interaction.response.send_message(embed=embed) 

    @app_commands.command(name="新的表情符號",description="新增表情符號")
    @app_commands.checks.has_permissions(administrator=True)
    async def newemoji(self,interaction:discord.Interaction,newemoji:discord.Attachment,emojiname:str):
        if interaction.guild.id == 1238133524662325351:
            try:
                image_data = await newemoji.read()
                if len(emojiname) < 23:
                    emoji = await interaction.guild.create_custom_emoji(name=emojiname, image=image_data)
                    await interaction.response.send_message(f"成功新增表情符號: <:{emoji.name}:{emoji.id}>")
                else:
                    number_of_strings = 1
                    length_of_string = 8
                    for x in range(number_of_strings):
                        emojiname2 = "".join(
                                random.choice(string.ascii_letters + string.digits)
                                for _ in range(length_of_string)
                            )                      
                    emoji = await interaction.guild.create_custom_emoji(name=emojiname2, image=image_data)
                    await interaction.response.send_message(f"成功新增表情符號: <:{emoji.name}:{emoji.id}>")
            except Exception as e:
                random7_int = random.randint(0, 255)
                random8_int = random.randint(0, 255)
                random9_int = random.randint(0, 255)
                emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
                embed = discord.Embed(title="錯誤", color= emb_color)
                embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
                await interaction.response.send_message(embed=embed)
                
    @app_commands.command(name="new_sticker",description="為伺服器新增貼圖")
    @app_commands.describe(newtickerfile = "貼圖的檔案",stickername = "貼圖的名字(可用中文)",emoji = "代表貼圖的表情符號(只能使用原始emoji或本伺服器的emoji)",description = "貼圖的說明",reason ="新增貼圖原因")
    @app_commands.checks.has_permissions(administrator=True)
    async def newsticker(self,interaction:discord.Interaction,newtickerfile :discord.Attachment,stickername:str,emoji:str,description:str,reason:str):
        try:
            if interaction.guild.id == 1238133524662325351:
                if len(stickername) < 23:
                    try:
                        await newtickerfile.save(f'C:\\Users\\曉黑\\Desktop\\DISCORDBOTmain\\cogs\\pho\\{newtickerfile.filename}')
                    except Exception as e:
                        random7_int = random.randint(0, 255)
                        random8_int = random.randint(0, 255)
                        random9_int = random.randint(0, 255)
                        emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
                        embed = discord.Embed(title="錯誤", color= emb_color)
                        embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
                        await interaction.response.send_message(embed=embed)
                    file = discord.File(f'C:\\Users\\曉黑\\Desktop\\DISCORDBOTmain\\cogs\\pho\\{newtickerfile.filename}')
                    sticker = await interaction.guild.create_sticker(name=stickername,file=file,emoji=emoji,description=description,reason=reason)
                    await interaction.response.send_message(f"以新增貼圖 {sticker.name}")
        except Exception as e:
            random7_int = random.randint(0, 255)
            random8_int = random.randint(0, 255)
            random9_int = random.randint(0, 255)
            emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="隱藏語音頻道",description="隱藏語音頻道並只讓當前在於頻道內的人可見該頻道")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def hide_voice_channel(self,interaction:discord.Interaction,channel:discord.VoiceChannel):
        try:
            guildmembers = interaction.guild.members
            for guildmember in guildmembers:
                await channel.set_permissions(guildmember, read_messages=False)
            channelmembers = channel.members
            membername = "已給予:"
            for member in channelmembers:
                await channel.set_permissions(member, read_messages=True)
                membername += f"{member.name},"
            await interaction.response.send_message(f"{membername}觀看權限",ephemeral=True)
        except Exception as e:
            random7_int = random.randint(0, 255)
            random8_int = random.randint(0, 255)
            random9_int = random.randint(0, 255)
            emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
            await interaction.response.send_message(embed=embed) 

    @app_commands.command(name="voting",description="幫機器人投票")
    async def botVoting(self,interaction:discord.Interaction):
        try:
            random7_int = random.randint(0, 255)
            random8_int = random.randint(0, 255)
            random9_int = random.randint(0, 255)
            emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
            embed = discord.Embed(title="幫機器人投票", color= emb_color)
            embed.add_field(name="https://top.gg/bot/998929254265929788/vote",value="",inline=False)
            await interaction.response.send_message(embed=embed) 
        except Exception as e:
            random7_int = random.randint(0, 255)
            random8_int = random.randint(0, 255)
            random9_int = random.randint(0, 255)
            emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
            await interaction.response.send_message(embed=embed) 

async def setup(bot: commands.Bot):
    await bot.add_cog(Slash(bot))
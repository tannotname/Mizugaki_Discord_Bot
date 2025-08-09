import sqlite3
from typing import Optional
import discord
import random
from discord import app_commands
from discord.ext import commands
import string
import random
from dotenv import load_dotenv

load_dotenv()


ffmpeg_process = None  # 將ffmpeg_process定義為全局變量

#drop table 
con = sqlite3.connect('interaction_surveillanc.db') # 連線資料庫
cur = con.cursor() # 建立游標
 # 查詢第一筆資料
cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?", ("interaction_surveillanc",))
row = cur.fetchone()[0]
    # 查詢資料庫是否存在
if row == 0:
    cur.execute("CREATE TABLE interaction_surveillanc(name Text,use_times NUMERIC)")
    con.commit()
    print("表格 'interaction_surveillanc' 已建立.")
else:
    print("表格“interaction_surveillanc”已存在.")
    con.commit()


class Slash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    

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
                    if "server" not in command.name:
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

    @app_commands.command(name="server_give_role",description="給予或移除伺服器成員新的身分組")
    async def give_role(self,interaction:discord.Interaction,role:discord.Role,member:discord.Member,out_give:bool):
        try:
            if interaction.user.name == "tan_00_00":
                if out_give == True:
                    await member.add_roles(role)
                    await interaction.response.send_message(f"已給予{member.nick} {role.name} 身分組",ephemeral=True)
                else:
                    await member.remove_roles(role)
                    await interaction.response.send_message(f"已刪除{member.nick} 的 {role} 身分組")
        except Exception as e:
            await interaction.response.send_message(f"報錯:{e}",ephemeral=True)


    @app_commands.command(name="say",description="讓機器人幫你說話")
    @app_commands.user_install()
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
            emb_color = discord.Color.from_rgb(255,0,0)
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
            emb_color = discord.Color.from_rgb(255,0,0)
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

    @app_commands.command(name="add_text_channel",description="新增文字頻道")
    @app_commands.checks.has_permissions(administrator=True)
    async def add_text_channel(self,interaction:discord.Interaction,channelname:str,category:discord.CategoryChannel):
        try:
            guild = interaction.guild
            await guild.create_text_channel(name=channelname,category=category)
            await interaction.response.send_message("執行",ephemeral=True)
        except Exception as e:
            emb_color = discord.Color.from_rgb(255,0,0)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
            await interaction.response.send_message(embed=embed) 

    @app_commands.command(name="新增表情符號",description="新增表情符號")
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
                emb_color = discord.Color.from_rgb(255,0,0)
                embed = discord.Embed(title="錯誤", color= emb_color)
                embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
                await interaction.response.send_message(embed=embed) 

    @app_commands.command(name="user_info",description="列出使用者資訊")
    async def user_info(self,interaction:discord.Interaction,user:discord.User):
        try:
            await interaction.response.send_message(f"使用者ID:{user.id}\n使用者名稱:{user.name}\n使用者頭像:{user.avatar.url}",ephemeral=True)
        except Exception as e:
            emb_color = discord.Color.from_rgb(255,0,0)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
            await interaction.response.send_message(embed=embed)


    @app_commands.command(name = "question", description = "讓機器人回答你的問題")
    async def question(self, interaction:discord.Interaction, 問題:str):
        try:
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
            sentence1 ="我覺得 {}".format(reply)
            emb_color = discord.Color.from_rgb(random3_int, random4_int , random5_int)
            embed = discord.Embed(title='<:5765653:1380741187261956206> | '+ 問題 , description = sentence1 , color = emb_color)
            await interaction.response.send_message(embed = embed)
        except Exception as e:
            emb_color = discord.Color.from_rgb(255,0,0)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
            await interaction.response.send_message(embed=embed)

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        try:
            name = interaction.command.name
            user = interaction.user
            interaction_channel = interaction.channel
            channel = self.bot.get_channel(1273145125773639752)
            await channel.send(f"{user.name} 在 {interaction_channel.name} 使用指令:{name}")
        except Exception as e:
            emb_color = discord.Color.from_rgb(255,0,0)
            embed = discord.Embed(title="錯誤", color= emb_color)
            channel= self.bot.get_channel(1273144773435326545)
            await channel.send(f"發生錯誤:{e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Slash(bot))
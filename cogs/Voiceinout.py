import random
import sqlite3
import discord
from discord.ext import commands
from discord import app_commands
from discord.ext import commands


channel_creators = {}
error_channel = 1273144773435326545

#drop table 
con = sqlite3.connect('voicechannelinout.db') # 連線資料庫
cur = con.cursor() # 建立游標
 # 查詢第一筆資料
cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?", ("voicechannelinout",))
row = cur.fetchone()[0]
    # 查詢資料庫是否存在
if row == 0:
    cur.execute("CREATE TABLE voicechannelinout(user_id NUMERIC,user_name TEXT,in_reply TEXT,out_reply TEXT)")
    con.commit()
    print("表格 'voicechannelinout' 已建立.")
else:
    print("表格“voicechannelinout”已存在.")
    con.commit()


#drop table 
con = sqlite3.connect('customizedtruelist.db') # 連線資料庫
cur = con.cursor() # 建立游標
 # 查詢第一筆資料
cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?", ("customizedtruelist",))
row = cur.fetchone()[0]
    # 查詢資料庫是否存在
if row == 0:
    cur.execute("CREATE TABLE customizedtruelist(guild_id NUMERIC,gulid_name TEXT)")
    con.commit()
    print("表格 'customizedtruelist' 已建立.")
else:
    print("表格“customizedtruelist”已存在.")
    con.commit()



class Voiceinout(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("已載入語音頻道通知模組")

    @app_commands.command(name = "customized_true_list", description = "設定伺服器是否啟用語音進出通知")
    @app_commands.describe(true_or_false = "true為啟用,false為禁用")
    @app_commands.checks.has_permissions(administrator=True)
    async def customized_true_list(self, interaction: discord.Interaction,true_or_false: bool):
        try:
            guild_id = interaction.guild.id
            guild_name = interaction.guild.name
            if true_or_false == True:
                con = sqlite3.connect("customizedtruelist.db")
                cur = con.cursor()
                cur.execute("INSERT INTO customizedtruelist (guild_id,gulid_name) VALUES (?,?)",(guild_id,guild_name))
                con.commit()
                await interaction.response.send_message("已啟用語音頻道進出通知",ephemeral=True)
                con.close()
                cur.close()
            if true_or_false == False:
                con = sqlite3.connect("customizedtruelist.db")
                cur = con.cursor()
                cur.execute("DELETE FROM customizedtruelist WHERE guild_id=?", (guild_id,))
                con.commit()
                await interaction.response.send_message("已禁用語音頻道進出通知",ephemeral=True)
                con.close()
                cur.close()
        except sqlite3.Error as e:
            channel = self.bot.get_channel(1273144773435326545)
            await channel.send(f"{interaction.guild.name} {interaction.channel.name} \n發生語音進出設定錯誤:\n{e}")

    @app_commands.command(name="customized_voice_in_out_notify", description="自訂語音頻道進出通知")
    @app_commands.describe(in_reply = "進入頻道回覆(請以 *user* 代替使用者名稱,若要包含頻道名稱請以 *channel* 代替)",out_reply = "離開頻道回覆(請以 *user* 代替使用者名稱,若要包含頻道名稱請以 *channel* 代替)")
    async def customized_voice_in_out_notify(self, interaction: discord.Interaction,in_reply: str, out_reply: str):
        try:
            user_id = interaction.user.id
            user_name = interaction.user.name
            if "*user*" in in_reply: # 檢查進入回覆是否包含 *user*
                in_reply_bool = True
            else:
                in_reply_bool = False
            if "*user*" in out_reply: # 檢查離開回覆是否包含 *user*
                out_reply_bool = True
            else:
                out_reply_bool = False
            if (in_reply_bool == True) and (out_reply_bool == True): # 如果都包含及存入資料庫
                con = sqlite3.connect("voicechannelinout.db")
                cur = con.cursor()
                cur.execute("INSERT INTO voicechannelinout (user_id,user_name,in_reply,out_reply) VALUES (?,?,?,?)",(user_id,user_name,in_reply,out_reply))
                con.commit()
                user_in_reply = in_reply.replace("*user*",user_name,2) # 替換 *user* 為使用者名稱
                user_out_reply = out_reply.replace("*user*",user_name,2)
                await interaction.response.send_message(f"已設置進入語音頻道通知為:{user_in_reply}\n已設置離開語音頻道通知為:{user_out_reply}",ephemeral=True)
                con.close()
                cur.close()
                channel = self.bot.get_channel(1273145437259305001)
                await channel.send(f"{user_name} 已設置進入語音頻道通知為:{user_in_reply}\n已設置離開語音頻道通知為:{user_out_reply}")
            elif (in_reply_bool == False) or (out_reply_bool == False):
                await interaction.response.send_message(f"請輸入包含 *user* 的回覆",ephemeral=True)
        except Exception as e:
            random7_int = random.randint(0, 255)
            random8_int = random.randint(0, 255)
            random9_int = random.randint(0, 255)
            emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
            await interaction.response.send_message(embed=embed,ephemeral=True)

    @app_commands.command(name="delete_voice_in_out_notify", description="刪除自訂語音頻道進出通知")
    async def delete_customized_voice_in_out_notify(self, interaction: discord.Interaction):
        try:
            user_id = interaction.user.id
            user_name = interaction.user.name
            con = sqlite3.connect("voicechannelinout.db")
            cur = con.cursor()
            cur.execute("DELETE FROM voicechannelinout WHERE user_id=?", (user_id,))
            con.commit()
            await interaction.response.send_message("已刪除自訂語音頻道進出通知",ephemeral=True)
            con.close()
            cur.close()
            channel = self.bot.get_channel(1273145437259305001)
            await channel.send(f"{user_name} 已刪除自訂語音頻道進出通知")
        except Exception as e:
            random7_int = random.randint(0, 255)
            random8_int = random.randint(0, 255)
            random9_int = random.randint(0, 255)
            emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
            embed = discord.Embed(title="錯誤", color= emb_color)
            embed.add_field(name=e,value="機器人支援伺服器:https://discord.gg/Eq52KNPca9",inline=False)
            await interaction.response.send_message(embed=embed,ephemeral=True)

    @commands.Cog.listener()
    async def on_voice_state_update(self,member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        try:
            con = sqlite3.connect("customizedtruelist.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM customizedtruelist WHERE guild_id=?", (member.guild.id,))
            rows = cur.fetchall()
            con.commit()
            cur.close()
            con.close()
            if rows != []:
                if before.channel is None and after.channel is not None:
                    try:
                        conn = sqlite3.connect("voicenew.db")
                        comn = conn.cursor()
                        comn.execute("SELECT * FROM voicenew WHERE server_id=?",(after.channel.guild.id,)) # 搜尋伺服器設定的頻道
                        rows = comn.fetchall()
                        conn.commit()
                        comn.close()
                        conn.close()
                    except sqlite3.Error as e:
                        await after.channel.send(f"錯誤1:{e}")
                    try:
                            for row in rows:
                                if after.channel.id == row[5]:
                                    return
                            nickname = member.nick if member.nick else member.name
                            can = sqlite3.connect("voicechannelinout.db")
                            car = can.cursor()
                            car.execute("SELECT * FROM voicechannelinout WHERE user_id=?",(member.id ,))
                            rows = car.fetchall()
                            can.commit()
                            car.close()
                            can.close()
                            if rows == []:
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
                            if rows != []:
                                for row in rows:
                                    in_reply = row[2]
                                    in_reply = str(in_reply)
                                    user_in_reply = in_reply.replace("*user*",nickname,2) # 替換 *user* 為使用者名稱
                                    if "*channel*" in user_in_reply:
                                        user_in_reply = user_in_reply.replace("*channel*",after.channel.name,2)
                                reply = user_in_reply
                            channel = after.channel
                            random7_int = random.randint(0, 255)
                            random8_int = random.randint(0, 255)
                            random9_int = random.randint(0, 255)
                            if member.color is not None:
                                emb_color = member.color
                            elif member.color is None:
                                emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
                            embed = discord.Embed(title="成員加入", description=reply, color= emb_color)
                            if member.guild_avatar is not None:
                                member_avatar = member.guild_avatar.url
                            elif member.guild_avatar is None:
                                member_avatar = member.avatar.url
                            embed.set_author(name= f"{member.name}",  icon_url= member_avatar)#作者
                            await channel.send(embed=embed)
                    except Exception as e:
                        await after.channel.send(f"錯誤2:{e}")
                elif after.channel is None and before.channel is not None:
                    try:
                        conn = sqlite3.connect("voicenew.db")
                        comn = conn.cursor()
                        comn.execute("SELECT * FROM voicenew WHERE server_id=?",(before.channel.guild.id,)) # 搜尋伺服器設定的頻道
                        rows = comn.fetchall()
                        conn.commit()
                        comn.close()
                        conn.close()
                    except sqlite3.Error as e:
                        await before.channel.send(f"錯誤1:{e}")
                    try:
                            for row in rows:
                                if before.channel.id == row[5]:
                                    return
                            nickname = member.nick if member.nick else member.name
                            can = sqlite3.connect("voicechannelinout.db")
                            car = can.cursor()
                            car.execute("SELECT * FROM voicechannelinout WHERE user_id=?",(member.id ,))
                            rows = car.fetchall()
                            can.commit()
                            car.close()
                            can.close()
                            if rows == []:
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
                            if rows != []:
                                for row in rows:
                                    out_reply = row[3]
                                    out_reply = str(out_reply)
                                    user_out_reply = out_reply.replace("*user*",nickname,2)
                                    if "*channel*" in user_out_reply:
                                        user_out_reply = user_out_reply.replace("*channel*",before.channel.name,2)
                                reply = user_out_reply
                            
                            
                            channel = before.channel
                            random7_int = random.randint(0, 255)
                            random8_int = random.randint(0, 255)
                            random9_int = random.randint(0, 255)
                            if member.color is not None:
                                emb_color = member.color
                            elif member.color is None:
                                emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
                            embed = discord.Embed(title="成員out", description=reply, color= emb_color)
                            if member.guild_avatar is not None:
                                member_avatar = member.guild_avatar.url
                            elif member.guild_avatar is None:
                                member_avatar = member.avatar.url
                            embed.set_author(name= f"{member.name}",  icon_url= member_avatar)#作者
                            
                            await channel.send(embed=embed)
                    except Exception as e:
                        await before.channel.send(f"錯誤2:{e}")
                elif before.channel != after.channel:
                    if after.channel is not None:
                        nickname = member.nick if member.nick else member.name
                        # 發送加入訊息
                        can = sqlite3.connect("voicechannelinout.db")
                        car = can.cursor()
                        car.execute("SELECT * FROM voicechannelinout WHERE user_id=?",(member.id ,))
                        rows = car.fetchall()
                        can.commit()
                        car.close()
                        can.close()
                        if rows == []:
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
                        if rows != []:
                            for row in rows:
                                in_reply = row[2]
                                in_reply = str(in_reply)
                                user_in_reply = in_reply.replace("*user*",nickname,2) # 替換 *user* 為使用者名稱
                                if "*channel*" in user_in_reply:
                                    user_in_reply = user_in_reply.replace("*channel*",after.channel.name,2)
                            reply = user_in_reply
                        

                        channel = after.channel
                        random7_int = random.randint(0, 255)
                        random8_int = random.randint(0, 255)
                        random9_int = random.randint(0, 255)
                        if member.color is not None:
                            emb_color = member.color
                        elif member.color is None:
                            emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
                        embed = discord.Embed(title="成員加入", description=reply, color= emb_color)
                        if member.guild_avatar is not None:
                                member_avatar = member.guild_avatar.url
                        elif member.guild_avatar is None:
                                member_avatar = member.avatar.url
                        embed.set_author(name= f"{member.name}",  icon_url= member_avatar)#作者
                        await channel.send(embed=embed)
                        # 發送離開訊息
                        can = sqlite3.connect("voicechannelinout.db")
                        car = can.cursor()
                        car.execute("SELECT * FROM voicechannelinout WHERE user_id=?",(member.id ,))
                        rows = car.fetchall()
                        can.commit()
                        car.close()
                        can.close()
                        if rows == []:
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
                        if rows != []:
                            for row in rows:
                                out_reply = row[3]
                                out_reply = str(out_reply)
                                user_out_reply = out_reply.replace("*user*",nickname,2)
                                if "*channel*" in user_out_reply:
                                    user_out_reply = user_out_reply.replace("*channel*",before.channel.name,2)
                            reply = user_out_reply
                        
                        channel = before.channel
                        random7_int = random.randint(0, 255)
                        random8_int = random.randint(0, 255)
                        random9_int = random.randint(0, 255)
                        if member.color is not None:
                            emb_color = member.color
                        elif member.color is None:
                            emb_color = discord.Color.from_rgb(random7_int, random8_int , random9_int)
                        embed = discord.Embed(title="成員out", description=reply, color= emb_color)
                        if member.guild_avatar is not None:
                                member_avatar = member.guild_avatar.url
                        elif member.guild_avatar is None:
                                member_avatar = member.avatar.url
                        embed.set_author(name= f"{member.name}",  icon_url= member_avatar)#作者
                        await channel.send(embed=embed)

        except Exception as e:
            if before.channel is None and after.channel is not None: # 進入語音頻道
                await after.channel.send(f"語音進出通知錯誤:{e}")

            elif after.channel is None and before.channel is not None: # 離開語音頻道
                await before.channel.send(f"語音進出通知錯誤:{e}")

            elif before.channel != after.channel: # 跳轉語音頻道
                if after.channel is not None:
                    await after.channel.send(f"語音進出通知錯誤:{e}")

            channel = self.bot.get_channel(error_channel)
            await channel.send(f"{before.channel.guild.name or after.channel.guild.name} {member.name} 語音進出通知錯誤:{e}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Voiceinout(bot))
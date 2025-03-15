from typing import Optional
import discord
from discord import app_commands
from discord.ext import commands


class Server_booster(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="new_booster_role",description="自訂身分組顏色跟圖示並給予自己")
    @app_commands.describe(new_role_name = "新的身分組名字",color = "16進位制的色碼",give_in_you ="是否給予自己此身分組",icon_fill="身分組圖示,256kb以下的圖檔,與icon_emoji二選一",icon_emoji="身分組圖示,此伺服器的emoji,與icon_fill二選一")
    async def new_booster_role(self,interaction:discord.Interaction,new_role_name:str,color:str,give_in_you:bool,icon_fill:Optional[discord.Attachment],icon_emoji:Optional[str]):
        try:
            guild = interaction.guild
            member = interaction.user
            if icon_fill is not None:
                icon = icon_fill.url
            elif icon_emoji is not None:
                icon = icon_emoji.url
            try:
                color = discord.Colour(int(color, 16))
                newrloe = await guild.create_role(name=new_role_name,colour=color,display_icon=icon)
                await interaction.response.send_message(f"已新增{newrloe.name}")
                if give_in_you == True:
                    await member.add_roles(newrloe)
                    await interaction.followup.send(f"已給予{member.nick} {newrloe.name} 身分組")
            except ValueError:
                await interaction.response.send_message("顏色格式錯誤，請使用十六進制顏色碼，例如 'FF5733'。")
                return
        except Exception as e:
            await interaction.response.send_message(f"錯誤:{e}",ephemeral=True)
            channel = self.bot.get_channel(1273144773435326545)
            await channel.send(f"server:{interaction.guild.name}使用者:{interaction.user.name}使用new_booster_role錯誤:{e}")

    
    

async def setup(bot: commands.Bot):
    await bot.add_cog(Server_booster(bot))
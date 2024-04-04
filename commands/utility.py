from ctypes import util
import datetime
from os import startfile
import sys
import time
import discord 
from discord.ext import commands 
from discord.ext.commands import Context
from main import CustomBot
import config

class utility(commands.Cog, name="utility"):
    def __init__(self, bot: CustomBot) -> None:
        self.bot = bot


#botinfo------------>

@commands.hybrid_command(name="botinfo",
                             aliases=['bi'],
                             help="Get info about me!",with_app_command = True)
async def botinfo(self, ctx: commands.Context):
        users = sum(g.member_count for g in self.bot.guilds
                    if g.member_count != None)
        channel = len(set(self.bot.get_all_channels()))
        embed = discord.Embed(color=0x0d0d13,
                              title="heavens's Information",
                              description=f"""
**Bot's Mention:** {self.bot.user.mention}
**Bot's Username:** {self.bot.user}
**Total Guilds:** {len(self.bot.guilds)}
**Total Users:** {users}
**Total Channels:** {channel}
**Total Commands: **{len(set(self.bot.walk_commands()))}
**Total Shards:** {len(self.bot.shards)}
**Uptime:** {str(datetime.timedelta(seconds=int(round(time.time()-startfile))))}
**CPU usage:** {round(util.cpu_percent())}%
**Memory usage:** {int((util.virtual_memory().total - util.virtual_memory().available)
 / 1024 / 1024)} MB
**My Websocket Latency:** {int(self.bot.latency * 1000)} ms
**Python Version:** {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}
**Discord.py Version:** {discord.__version__}
""")
        embed.set_footer(text=f"Requested By {ctx.author}",
                         icon_url=ctx.author.avatar.url if ctx.author.avatar
                         else ctx.author.default_avatar.url)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        await ctx.send(embed=embed)







#Ping------------>


@commands.hybrid_command(name="ping",
                             aliases=["latency"],
                             usage="Checks the bot latency .",with_app_command = True)
   
async def ping(self, ctx):
        embed = discord.Embed(
            title="""
            <:2984goodping:1225411097419579395> Ping! """,
            description=f"<:5909_SayoriSleep:1225411999463247912> **__websocket Latency__** :  {int(self.bot.latency * 1000)} **__ms__**",
            color=0x0f8be2)
        embed.set_footer(
                         icon_url=ctx.author.avatar.url if ctx.author.avatar
                         else ctx.author.default_avatar.url)
        await ctx.reply(embed=embed)





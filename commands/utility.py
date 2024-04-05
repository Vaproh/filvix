# importing discord modules
import discord
from discord.ext import commands

# importing utility modules
from ctypes import util
import datetime
from os import startfile
import sys
import time
import psutil

# importing custom bot
from main import CustomBot


class Utility(commands.Cog):
    def __init__(self, bot: CustomBot):
        self.bot = bot

    @commands.hybrid_command(name="botinfo",
                                aliases=['bi'],
                                help="Get info about me!",with_app_command = True)
    async def botinfo(self, ctx: commands.Context):
                users = sum(g.member_count for g in self.bot.guilds
                        if g.member_count != None)
                channel = len(set(self.bot.get_all_channels()))
                # Get the CPU usage as a percentage
                cpu_usage = psutil.cpu_percent()

                # Round the CPU usage to the nearest integer
                cpu_usage = round(cpu_usage)
                embed = discord.Embed(color=0x0d0d13,
                                title="heavens's Information",
                                description=f"""
        **Bot's Mention:** {self.bot.user.mention}
        **Bot's Username:** {self.bot.user}
        **Total Guilds:** {len(self.bot.guilds)}
        **Total Users:** {users}
        **Total Channels:** {channel}
        **Total Commands: **{len(set(self.bot.walk_commands()))}
        **CPU usage:** {cpu_usage}%
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
    

async def setup(bot: CustomBot) -> None:
    await bot.add_cog(Utility(bot))

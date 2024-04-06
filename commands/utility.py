# importing discord modules
import discord
from discord.ext import commands

# importing utility modules
import sys
import psutil
import random

# importing custom bot
from main import CustomBot

# get virtual mem usage
def get_virtual_memory_usage():
  """Get the virtual memory usage."""

  vm = psutil.virtual_memory()
  return vm.used

# cog starts here
class Utility(commands.Cog):
    def __init__(self, bot: CustomBot):
        self.bot = bot

    # botinfo command
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
                
                # embed
                embed = discord.Embed(color=random.randint(0, 0xFFFFFF),
                                title= str(self.bot.user.name).capitalize() + " " + "Information",
                                description=f"""
        **Bot's Mention:** {self.bot.user.mention}
        **Bot's Username:** {self.bot.user}
        **Total Guilds:** {len(self.bot.guilds)}
        **Total Users:** {users}
        **Total Channels:** {channel}
        **Total Commands: **{len(set(self.bot.walk_commands()))}
        **CPU usage:** {cpu_usage}%
        **Memory usage:** {int(get_virtual_memory_usage() / 1024 / 1024)} MB
        **My Websocket Latency:** {int(self.bot.latency * 1000)} ms
        **Python Version:** {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}
        **Discord.py Version:** {discord.__version__}
        """)
                embed.set_footer(text=f"Requested By {ctx.author}",
                                icon_url=ctx.author.avatar.url if ctx.author.avatar
                                else ctx.author.default_avatar.url)
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                await ctx.send(embed=embed)
    
    # ping command
    @commands.hybrid_command(name="ping",
                             aliases=["latency"],
                             usage="Checks the bot latency.",with_app_command = True,
                             help="Checks the bot latency.")
   
    async def ping(self, ctx):
        embed = discord.Embed(
                title="""
                <:2984goodping:1225411097419579395> Ping! """,
                description=f"<:5909_SayoriSleep:1225411999463247912> **__websocket Latency__** :  {int(self.bot.latency * 1000)} **__ms__**",
                color=random.randint(0, 0xFFFFFF))
        embed.set_footer(
                            icon_url=ctx.author.avatar.url if ctx.author.avatar
                            else ctx.author.default_avatar.url)
        await ctx.reply(embed=embed)



    #Invite
    @commands.hybrid_command(name="invite", aliases=['inv'])
    async def invite(self, ctx: commands.Context):
            embed = discord.Embed(
                description=
                "> • [Click Here To Invite Zoynix To Your Server](https://discord.com/oauth2/authorize?client_id=1213860294301061122&permissions=8&scope=bot)\n> • [Click Here To Join My Support Server](https://discord.gg/sxhGCtjX9R)",
                color=0x0565ff)
            embed.set_author(name=f"{ctx.author.name}",
                            icon_url=f"{ctx.author.avatar}")
            await ctx.send(embed=embed)

    #Membercount  
    @commands.hybrid_command(name="membercount",
                             help="Get total member count of the server",
                             usage="membercount",
                             aliases=["mc"])
    async def membercount(self, ctx: commands.Context):
        embed = discord.Embed(
               title=ctx.guild.name,
               description="**MemberCount**\n- %s members" % (len(ctx.guild.members)),
    )




# add cogs
async def setup(bot: CustomBot) -> None:
    await bot.add_cog(Utility(bot))

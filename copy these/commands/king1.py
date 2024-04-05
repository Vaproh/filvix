import discord
from discord.ext import commands


class logging1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Logging Commands"""
  
    def help_custom(self):
		      emoji = '<:logging:1214606283953410088>'
		      label = "Logging"
		      description = "Show You Commands Of Logging"
		      return emoji, label, description

    @commands.group()
    async def __here__(self, ctx: commands.Context):
        """`logging`, `channellog`, `logall disable`, `logall enable`, `logall`, `memberlog`, `modlog`, `msglog`, `rolelog`, `serverlog`"""
import discord
from discord.ext import commands


class anti1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """AntiNuke Commands"""
  
    def help_custom(self):
		      emoji = '<:antinuke:1212414104468455485>'
		      label = "AntiNuke"
		      description = "Show You Commands Of Antinuke"
		      return emoji, label, description

    @commands.group()
    async def __AntiNuke__(self, ctx: commands.Context):
        """`antinuke` , `antinuke enable` , `antinuke disable` , `antinuke show` , `antinuke punishment set` , `antinuke whitelist add` , `antinuke whitelist remove` , `antinuke whitelist show` , `antinuke whitelist reset` , `antinuke channelclean` , `antinuke roleclean` , `antinuke wl role`"""
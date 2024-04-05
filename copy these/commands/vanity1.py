import discord
from discord.ext import commands


class vanity1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Vanityroles Commands"""
  
    def help_custom(self):
		      emoji = '<:VanityRoles:1214802988145582080>'
		      label = "Vanityroles"
		      description = "Show You Commands Of Vanityroles"
		      return emoji, label, description

    @commands.group()
    async def __Vanityroles__(self, ctx: commands.Context):
        """`vanityroles setup` , `vanityroles show` , `vanityroles reset`"""
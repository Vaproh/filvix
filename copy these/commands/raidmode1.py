import discord
from discord.ext import commands


class raidmode1(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  """Raidmode Commands"""

  def help_custom(self):
    emoji = '<:raidmode:1213539411141201991>'
    label = "Raidmode"
    description = "Show You Commands Of Raidmode"
    return emoji, label, description

  @commands.group()
  async def __Raidmode__(self, ctx: commands.Context):
    """`automod` , `antispam on` , `antispam off` , `antilink off` ,  `antilink on`"""

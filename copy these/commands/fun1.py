import discord
from discord.ext import commands


class fun1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Fun Commands"""
  
    def help_custom(self):
		      emoji = '<:rinx3:1214657416659079219>'
		      label = "Fun"
		      description = "Show You Commands Of Fun"
		      return emoji, label, description

    @commands.group()
    async def __Fun__(self, ctx: commands.Context):
        """` tickle` , `kiss` , `hug` , `slap` , `pat` , `feed` , `pet` , `howgay` , `slots` , ` penis` , `meme` , `cat` , `iplookup` , `nitro`"""
import discord
from discord.ext import commands


class hacker1111111111111111111(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Ticket commands"""
  
    def help_custom(self):
		      emoji = '<:icon_ticket:1214607134373707867>'
		      label = "Ticket"
		      description = "Show You Ticket Commands"
		      return emoji, label, description

    @commands.group()
    async def __Ticket__(self, ctx: commands.Context):
        """`sendpanel`"""
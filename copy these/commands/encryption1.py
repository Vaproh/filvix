import discord
from discord.ext import commands
import json

class encryption1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Encryption Commands"""  

    def help_custom(self):
		      emoji = '<:encryptionv1:1214802696612085770>'
		      label = "Encryption"
		      description = "Show You Commands Of Encryption"
		      return emoji, label, description

    @commands.group()
    async def __Encryption__(self, ctx: commands.Context):
        """`h encode` , `encode base85` , `encode ascii85` ,`encode base64` , `encode rot13` , `encode base32` , `encode hex` , `h decode` , `decode base85` , `decode base64` , `decode hex` , `decode ascii85` , `decode base32` , `decode rot13`"""
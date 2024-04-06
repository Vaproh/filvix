from typing import Optional, Union
import discord 
from discord.ext import commands 
from main import CustomBot

class General(commands.Cog):
    def __init__(self, bot: CustomBot):
        self.bot = bot

    # avatar command
    @commands.hybrid_command(name='avatar', help='Displays the user\'s avatar.',aliases=['av'])
    async def avatar(self, ctx, member: Optional[Union[discord.User, discord.Member]] = None):
        user = user or ctx.author
        embed = discord.Embed(title=f"{self.user.name}'s Avatar", color=0x0565ff)
        embed.set_image(url=self.author.avatar_url)
        await ctx.send(embed=embed)


# add cogs
async def setup(bot: CustomBot) -> None:
    await bot.add_cog(General(bot))
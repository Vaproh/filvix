from typing import Optional, Union
import discord 
from discord.ext import commands 
import random
from main import CustomBot

color = random.randint(0, 0xFFFFFF)

class General(commands.Cog):
    def __init__(self, bot: CustomBot):
        self.bot = bot

    @commands.hybrid_command(
            usage="Avatar [member]",
            name='avatar',
            aliases=['av', 'ac', 'pfp', 'ico'],
            help="""Wanna steal someone's avatar here you go
    Aliases""")
    async def user(self,
                        ctx,
                        member: Optional[Union[discord.Member,
                                            discord.User]] = None):
            if member == None or member == "":
                member = ctx.author
            user = await self.bot.fetch_user(member.id)     
            webp = user.avatar.replace(format='webp')
            jpg = user.avatar.replace(format='jpg')
            png = user.avatar.replace(format='png')
            embed = discord.Embed(
                    color=random.randint(0, 0xFFFFFF),
                    description=f"[`PNG`]({png}) | [`JPG`]({jpg}) | [`WEBP`]({webp})"
                    if not user.avatar.is_animated() else
                    f"[`PNG`]({png}) | [`JPG`]({jpg}) | [`WEBP`]({webp}) | [`GIF`]({user.avatar.replace(format='gif')})"
                )
            embed.set_author(name=f"{member}",
                                icon_url=member.avatar.url
                                if member.avatar else member.default_avatar.url)
            embed.set_image(url=user.avatar.url)
            embed.set_footer(
                    text=f"Requested By {ctx.author}",
                    icon_url=ctx.author.avatar.url
                    if ctx.author.avatar else ctx.author.default_avatar.url)
                
            await ctx.send(embed=embed)
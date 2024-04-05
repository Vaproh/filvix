# importing discord modules
import wavelink
import discord
from discord.ext import commands

# importing bot subclass
from main import CustomBot

# importing music module
import wavelink

# command starts here
class Music(commands.Cog):
    vc : wavelink.Player = None
    def __init__(self, bot: CustomBot):
        self.bot = bot
    
    # join command
    @commands.hybrid_command(
        name="join",
        description="join the user vc.",
        )
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel
        if channel:
            self.vc = channel.connect(cls=wavelink.Player)
            await self.vc
            await ctx.send(f"Joined `{channel.name}`")
    
    @commands.hybrid_command(
        name="add",
        description="add the named song",
        )
    async def add(self, ctx, *, title: str):
        ...


    @commands.hybrid_command
    async def play(self, ctx):
        ...


async def setup(bot: CustomBot) -> None:
    await bot.add_cog(Music(bot))

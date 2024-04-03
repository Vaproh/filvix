# importing discord modules
import discord
from discord.ext import commands
import random

# improting main bot class
from main import CustomBot

# mentioning embeds
missing_arg = discord.Embed(title="Error occurred!", description="You did not enter on of the arguements!", color=random.randint(0, 0xFFFFFF))


# cog starts here
class ErrorHandler(commands.Cog):
    def __init__(self, bot: CustomBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CommandNotFound):
            return await ctx.send("This command does not exist.")
        elif isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(embed=missing_arg)
        elif isinstance(error, commands.BadArgument):
            return await ctx.send("You provided an invalid argument.")
        elif isinstance(error, commands.CommandOnCooldown):
            return await ctx.send("This command is on cooldown.")
        elif isinstance(error, commands.NotOwner):
            return await ctx.send("You are not the owner of this bot.")



async def setup(bot: CustomBot):
    await bot.add_cog(ErrorHandler(bot))

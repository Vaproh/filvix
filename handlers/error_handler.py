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
    
    # event listener
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You are missing a required argument!")
        elif isinstance(error, commands.MissingRequiredAttachment):
            await ctx.send("You are missing a required attachment!")
        elif isinstance(error, commands.ArgumentParsingError):
            await ctx.send("Bot failed to parse your argument")
        elif isinstance(error, commands.UnexpectedQuoteError):
            await ctx.send("Bot parser encountered an unexpected quote error")
        elif isinstance(error, commands.InvalidEndOfQuotedStringError):
            await ctx.send("Bot parser encountered an invalid end of quoted string error")
        elif isinstance(error, commands.ExpectedClosingQuoteError):
            await ctx.send("Bot parser encountered an expected closing quote error")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Bot parser encountered a bad argument error")
        elif isinstance(error, commands.BadUnionArgument):
            await ctx.send("Bot parser encountered a bad union argument error")
        elif isinstance(error, commands.BadLiteralArgument):
            await ctx.send("Bot has encountered a bad literal argument error")
        elif isinstance(error, commands.BadBoolArgument):
            await ctx.send("Bot has encountered a bad bool argument error")

        # add more from https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#discord.ext.commands.PrivateMessageOnly
# setup
async def setup(bot: CustomBot):
    await bot.add_cog(ErrorHandler(bot))

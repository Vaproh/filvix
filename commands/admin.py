# discord modules
import discord
from discord.ext import commands
from main import CustomBot

# importing utility modules
import os
from os import sys

# restart_bot function
def restart_bot(): 
  os.execv(sys.executable, ['python'] + sys.argv)

# class starts here
class Admin(commands.Cog):
    def __init__(self, bot: CustomBot):
        self.bot = bot

    # restart command
    @commands.command(name="restart", help="Restarts the client.")
    @commands.is_owner()
    async def _restart(self, ctx):
        await ctx.reply("Restarting! <:tick_icons:1124596979813580801> Pls Wait It Takes 5-6 Second")
        restart_bot()

    @commands.command(name="shutdown", help="Shutdown the client.")
    @commands.is_owner()
    async def _shutdown(self, ctx):
        await ctx.bot.logout()

    @commands.command(name="nickname")
    @commands.is_owner()
    async def change_nickname(self, ctx, *, name: str = None):
        """ Change nickname. """
        try:
            await ctx.guild.me.edit(nick=name)
            if name:
                await ctx.send(f"<:IconTick:1213170250267492383> | Successfully changed nickname to **{name}**")
            else:
                await ctx.send("<:IconTick:1213170250267492383> | Successfully cleared nickname")
        except Exception as err:
            await ctx.send(err)


    @commands.command()
    @commands.is_owner()
    async def globalban(self, ctx, *, user: discord.User = None):
        if user is None:
            return await ctx.send(
                "You need to define the user"
            )
        for guild in self.client.guilds:
            for member in guild.members:
                if member == user:
                    await user.ban(reason="...")

async def setup(bot):
    await bot.add_cog(Admin(bot))
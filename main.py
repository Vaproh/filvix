# importing discord modules
import discord
from discord.ext import commands

#importing cogs
from commands.moderation import Moderation
from commands.general import General

# importing utility modules
# import os
# import json
import time
import config

# bot variable
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# on connect event
@bot.event
async def on_connect():
  await bot.change_presence(status=discord.Status.dnd,activity=discord.Activity(type=discord.ActivityType.listening,name="Cloudy "))


# on  ready event
@bot.event
async def on_ready():
    #
    print(f"Logged In As {bot.user}\nID - {bot.user.id}")
    print("Zoyx Here!")
    print(f"logged In as {bot.user.name}")
    print(f"Total servers ~ {len(bot.guilds)}")
    print(f"Total Users ~ {len(bot.users)}")

    await bot.add_cog(Moderation(bot)) # moderation module load
    print("Loaded Moderation module")
    time.sleep(0.5)
    await bot.add_cog(General(bot)) #general module load
    print("Loaded General module")
    time.sleep(0.5)
    print("Registering Slash Commands")
    await bot.tree.sync() # register slash commands
    print("Registerd all Slash Commands")

# loging in with token
bot.run(config.token)

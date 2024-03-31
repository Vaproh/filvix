import discord
from discord.ext import commands
import config


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_connect():
  await bot.change_presence(status=discord.Status.dnd,activity=discord.Activity(type=discord.ActivityType.listening,name="Cloudy "))


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def hello(ctx):
    await ctx.send("Hello, I am a robot")

bot.run(config.token)

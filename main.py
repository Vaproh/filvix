import discord
from discord.ext import commands
#import os
import json
#import jiskhau
import config



bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_connect():
  await bot.change_presence(status=discord.Status.dnd,activity=discord.Activity(type=discord.ActivityType.listening,name="Cloudy "))



@bot.event
async def on_ready():
  
    print(f"Logged In As {bot.user}\nID - {bot.user.id}")
    print("Zoyx Here!")
    print(f"logged In as {bot.user.name}")
    print(f"Total servers ~ {len(bot.guilds)}")
    print(f"Total Users ~ {len(bot.users)}")



@bot.hybrid_command()
@commands.has_permissions(manage_messages = True)
@commands.bot_has_permissions(manage_messages = True)
async def purge(ctx, amount:int):
   await ctx.response.defer(thinking=True, ephemeral=True) 
   await ctx.channel.purge(limit=amount)
   embed = discord.Embed(title="purged messages", description=f"Purged {amount} of messages")
   await ctx.send(embed=embed, ephemeral=True)

@purge.error
async def on_error(ctx, error: commands.CommandError):
   if isinstance(error, commands.MissingPermissions):
      await ctx.send("You dont have enough perms!")

bot.run(config.token)




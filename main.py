import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingPermissions
import os
import json
#import jiskhau
import config
#import cogs
import time




bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_connect():
  await bot.change_presence(status=discord.Status.dnd,activity=discord.Activity(type=discord.ActivityType.listening,name="Cloudy "))

def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            cogs = filename[:-2]
            bot.load_extension(f'cogs.{"general"}')
            bot.load_extension(f'cogs.{"moderation"}')


@bot.event
async def on_ready():
  
    print(f"Logged In As {bot.user}\nID - {bot.user.id}")
    print("Zoyx Here!")
    print(f"logged In as {bot.user.name}")
    print(f"Total servers ~ {len(bot.guilds)}")
    print(f"Total Users ~ {len(bot.users)}")
    await bot.load_extension("cogs.moderation") # loading moderation module
    print("Loaded module: Moderation")
    time.sleep(0.5)
    # await bot.load_extension("cogs.music") # loading music commands
    # print("Loaded module: Music")
    # time.sleep(0.5)
    print("Registering Slash Commands")
    await bot.tree.sync() # register slash commands
    print("Registerd all Slash Commands")



#@bot.hybrid_command()
#@commands.has_permissions(manage_messages = True)
#@commands.bot_has_permissions(manage_messages = True)
#async def purge(ctx, amount:int):
 #  await ctx.response.defer(thinking=True, ephemeral=True) 
  # await ctx.channel.purge(limit=amount)
   #embed = discord.Embed(title="purged messages", description=f"Purged {amount} of messages")
   #await ctx.send(embed=embed, ephemeral=True)


#@purge.error
#async def on_error(ctx, error: commands.CommandError):
 #  if isinstance(error, commands.MissingPermissions):
  #    await ctx.send("You dont have enough perms!")






# @commands.has_permissions(manage_messages=True)
# @bot.hybrid_command(name='purge', brief='Deletes a specified number of messages from the current channel')
# async def purge(ctx, amount: int):
#   # Delete the specified number of messages
#   deleted = await ctx.channel.purge(limit=amount)
#   if len(deleted) == 0:
#     # If no messages were deleted, create an embed message with a custom color and text
#     embed = discord.Embed(title='Purge complete', color=0xFFFF00)
#     embed.description = 'No messages were deleted'
#     # Set the user's profile picture as the thumbnail of the embed
#     embed.set_thumbnail(url=ctx.author.avatar.url)
#     # Send the embed message
#     await ctx.send(embed=embed)
#   else:
#     # Create an embed message with a custom color and text
#     embed = discord.Embed(title='Purge complete', color=0xFFFF00)
#     if len(deleted) == 1:
#       # If only one message was deleted, use singular text
#       embed.description = '1 message was deleted'
#     else:
#       # If more than one message was deleted, use plural text
#       embed.description = f'{len(deleted)} messages were deleted'
#     # Set the user's profile picture as the thumbnail of the embed
#     embed.set_thumbnail(url=ctx.author.avatar.url)
#     # Send the embed message
#     await ctx.send(embed=embed)





# @bot.event
# async def on_command_error(ctx, error):
#   if isinstance(error, commands.MissingPermissions):
#     await ctx.send(
#       f"{ctx.author.mention} You do not have enough permissions to use the `{ctx.command}` command."
#     )
#   elif isinstance(error, commands.CommandNotFound):
#     pass  # do nothing if the command doesn't exist
#   else:
#     print(f"Error occurred: {str(error)}")     

bot.run(config.token)

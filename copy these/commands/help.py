import discord
from traceback import format_exception
from discord.ext import commands
from difflib import get_close_matches
import io
import textwrap
from datetime import datetime, timedelta
import sys
from contextlib import suppress
from core import Context
from core.Astroz import Astroz
from core.Cog import Cog
from utils.Tools import getConfig
from itertools import chain
import psutil
import time
import platform
import os
import logging
import motor.motor_asyncio
from pymongo import MongoClient
import requests
import motor.motor_asyncio as mongodb
from typing import *
from utils import *
import json
from utils import help as vhelp
from utils import Paginator, DescriptionEmbedPaginator, FieldPagePaginator, TextPaginator

from core import Cog, Astroz, Context
from typing import Optional
from discord import app_commands

start_time = time.time()


def datetime_to_seconds(thing: datetime):
  current_time = datetime.fromtimestamp(time.time())
  return round(
    round(time.time()) +
    (current_time - thing.replace(tzinfo=None)).total_seconds())


client = Astroz()


class HelpCommand(commands.HelpCommand):

  async def on_help_command_error(self, ctx, error):
    serverCount = len(self.bot.guilds)
    users = sum(g.member_count for g in self.bot.guilds
                if g.member_count != None)

    total_members = sum(g.member_count for g in self.bot.guilds
                        if g.member_count != None)
    damn = [
      commands.CommandOnCooldown, commands.CommandNotFound,
      discord.HTTPException, commands.CommandInvokeError
    ]
    if not type(error) in damn:
      await self.context.reply(f"Unknown Error Occurred\n{error.original}",
                               mention_author=False)
    else:
      if type(error) == commands.CommandOnCooldown:
        return

        return await super().on_help_command_error(ctx, error)

  async def command_not_found(self, string: str) -> None:
    with open('blacklist.json', 'r') as f:
      data = json.load(f)
    if str(self.context.author.id) in data["ids"]:
      embed = discord.Embed(
        title="<:blacklist:1217854048993280020> Blacklisted",
        description=
        "You Are Blacklisted From Using My Commands.\nIf You Think That It Is A Mistake, You Can Appeal In Our Support Server By Clicking [here](https://discord.gg/h1ontop)",
        color=0x00FFCA)
      await self.context.reply(embed=embed, mention_author=False)
    else:

      if string in ("security", "anti", "antinuke"):
        cog = self.context.bot.get_cog("Antinuke")
        with suppress(discord.HTTPException):
          await self.send_cog_help(cog)
      else:
        msg = f"Command `{string}` is not found...\n"
        piyush = await self.context.bot.fetch_user(1078333867175465162)
        cmds = (str(cmd) for cmd in self.context.bot.walk_commands())
        mtchs = get_close_matches(string, cmds)
        if mtchs:
          for okaay, okay in enumerate(mtchs, start=1):
            msg += f"Did You Mean: \n`[{okaay}]`. `{okay}`\n"
        embed1 = discord.Embed(
          color=0x11100d,
          title=f"Command `{string}` is not found...\n",
          description=f"Did You Mean: \n`[{okaay}]`. `{okay}`\n")

        return None

  async def send_bot_help(self, mapping):
    await self.context.typing()
    with open('ignore.json', 'r') as heck:
      randi = json.load(heck)
    with open('blacklist.json', 'r') as f:
      bled = json.load(f)
    if str(self.context.author.id) in bled["ids"]:
      embed = discord.Embed(
        title="<:blacklist:1217854048993280020> Blacklisted",
        description=
        "You Are Blacklisted From Using My Commands.\nIf You Think That It Is A Mistake, You Can Appeal In Our Support Server By Clicking [here](https://discord.gg/h1ontop)",
        color=0x11100d)
      return await self.context.reply(embed=embed, mention_author=False)
    elif str(self.context.channel.id) in randi["ids"]:
      return None
    data = getConfig(self.context.guild.id)
    prefix = data["prefix"]
    perms = discord.Permissions.none()
    perms.read_messages = True
    perms.external_emojis = True
    perms.send_messages = True
    perms.manage_roles = True
    perms.manage_channels = True
    perms.ban_members = True
    perms.kick_members = True
    perms.manage_messages = True
    perms.embed_links = True
    perms.read_message_history = True
    perms.attach_files = True
    perms.add_reactions = True
    perms.administrator = True
    inv = discord.utils.oauth_url(self.context.bot.user.id, permissions=perms)
    filtered = await self.filter_commands(self.context.bot.walk_commands(),
                                          sort=True)
    nexus = await self.context.bot.fetch_user(1096394407823028276)
    embed = discord.Embed(
      title="Help Command Overview :",
      description=
      f"•  My defult Prefix is `{prefix}`\n •  Total Commands: {len(set(self.context.bot.walk_commands()))} | Usable by you (here): {len(set(filtered))}\n •  Links ~ [Invite](https://youtu.be/dQw4w9WgXcQhttps://youtu.be/dQw4w9WgXcQ) | [Support](https://discord.gg/h1ontop)\n• Type `{prefix}help <command | module>` for more info.\n```    <> - Required | [] - Optional``` ",
      color=0x11100d)
    embed.set_thumbnail(url=self.context.bot.user.display_avatar.url)

    embed.set_footer(text=f"Thanks for using me.",
                     icon_url=self.context.author.display_avatar.url)

    embed.add_field(name="__Main Modules __",
                    value="""
 ** <:invisible:1214604355190390835><:automod:1212414534963433482> Antinuke\n <:invisible:1214604355190390835><:icon_GiveawayIcon:1214584516849696788> Giveaway\n <:invisible:1214604355190390835><:logging:1214606283953410088> Logging\n <:invisible:1214604355190390835><:moderation:1212415056772595714> Moderation\n <:invisible:1214604355190390835><:icon_ticket:1214607134373707867> Ticket\n <:invisible:1214604355190390835><:extra:1213546253649186926>  Extra** """,
                    inline=True)

    embed.add_field(
      name="__Basics Modules __",
      value=
      """** <:invisible:1214604355190390835><:welcome:1212419295024386068> Welcome\n <:invisible:1214604355190390835><:raidmode:1214618360587878500> Raidmode\n <:invisible:1214604355190390835><:dm_Loop:1214618794631106571> Join Dm\n <:invisible:1214604355190390835><:server:1214619189457719396> Server\n <:invisible:1214604355190390835><:icons_human:1214619431217659935> Verification\n <:invisible:1214604355190390835><:icon_generalinfo:1214619941546762240> General\n <:invisible:1214604355190390835><:RX_pfp:1214620166760173648> pfp **""",
      inline=True)
    #embed.add_field(
    #name="__Stats__",
    #value=f"""・**Ping** - {int(self.bot.latency * 1000)} ms """,
    #inline=False
    #)
    embed.set_author(name=self.context.author.name,
                     icon_url=self.context.author.display_avatar.url)
    embed.timestamp = discord.utils.utcnow()

    # Create the invite button

    support_button = discord.ui.Button(style=discord.ButtonStyle.link,
                                       label="Support Server",
                                       url="https://discord.gg/h1ontop")

    view = vhelp.View(mapping=mapping, ctx=self.context, homeembed=embed, ui=2)

    view.add_item(support_button)

    await self.context.reply(embed=embed, mention_author=False, view=view)

  async def send_command_help(self, command):
    with open('ignore.json', 'r') as heck:
      randi = json.load(heck)
    with open('blacklist.json', 'r') as f:
      data = json.load(f)
    if str(self.context.author.id) in data["ids"]:
      embed = discord.Embed(
        title="<:blacklist:1217854048993280020> Blacklisted",
        description=
        "You Are Blacklisted From Using My Commands.\nIf You Think That It Is A Mistake, You Can Appeal In Our Support Server By Clicking [here](https://discord.gg/h1ontop)",
        color=0x00FFCA)
      await self.context.reply(embed=embed, mention_author=False)
    elif str(self.context.channel.id) in randi["ids"]:
      return None
    else:
      hacker = f">>> {command.help}" if command.help else '>>> No Help Provided...'
      embed = discord.Embed(
        description=
        f"""```yaml\n- [] = optional argument\n- <> = required argument\n- Do NOT Type These When Using Commands !```\n{hacker}""",
        color=0x00FFCA)
      alias = ' | '.join(command.aliases)

      embed.add_field(name="**Aliases**",
                      value=f"{alias}" if command.aliases else "No Aliases",
                      inline=False)
      embed.add_field(name="**Usage**",
                      value=f"`{self.context.prefix}{command.signature}`\n")
      embed.set_author(name=f"{command.cog.qualified_name.title()}",
                       icon_url=self.context.bot.user.display_avatar.url)
      await self.context.reply(embed=embed, mention_author=False)

  def get_command_signature(self, command: commands.Command) -> str:
    parent = command.full_parent_name
    if len(command.aliases) > 0:
      aliases = ' | '.join(command.aliases)
      fmt = f'[{command.name} | {aliases}]'
      if parent:
        fmt = f'{parent}'
      alias = f'[{command.name} | {aliases}]'
    else:
      alias = command.name if not parent else f'{parent} {command.name}'
    return f'{alias} {command.signature}'

  def common_command_formatting(self, embed_like, command):
    embed_like.title = self.get_command_signature(command)
    if command.description:
      embed_like.description = f'{command.description}\n\n{command.help}'
    else:
      embed_like.description = command.help or 'No help found...'

  async def send_group_help(self, group):
    with open('blacklist.json', 'r') as f:
      idk = json.load(f)
    with open('ignore.json', 'r') as heck:
      randi = json.load(heck)
    if str(self.context.author.id) in idk["ids"]:
      embed = discord.Embed(
        title="<:blacklist:1217854048993280020> Blacklisted",
        description=
        "You Are Blacklisted From Using My Commands.\nIf You Think That It Is A Mistake, You Can Appeal In Our Support Server By Clicking [here](https://discord.gg/h1ontop)",
        color=0x00FFCA)
      await self.context.reply(embed=embed, mention_author=False)
    elif str(self.context.channel.id) in randi["ids"]:
      return None
    else:
      entries = [(
        f"`{self.context.prefix}{cmd.qualified_name}`",
        f"{cmd.short_doc if cmd.short_doc else 'No Description Provided...'}\n\n"
      ) for cmd in group.commands]
    paginator = Paginator(source=FieldPagePaginator(
      entries=entries,
      title=f"{group.qualified_name} Commands",
      description=
      "```yaml\n- [] = optional argument\n- <> = required argument\n- Do NOT Type These When Using Commands !```",
      color=0x00FFCA,
      per_page=10),
                          ctx=self.context)
    await paginator.paginate()

  async def send_cog_help(self, cog):
    with open('blacklist.json', 'r') as f:
      data = json.load(f)
    with open('ignore.json', 'r') as heck:
      randi = json.load(heck)
    if str(self.context.author.id) in data["ids"]:
      embed = discord.Embed(
        title="<:blacklist:1217854048993280020> Blacklisted",
        description=
        "You Are Blacklisted From Using My Commands.\nIf You Think That It Is A Mistake, You Can Appeal In Our Support Server By Clicking [here](https://discord.gg/h1ontop)",
        color=0x00FFCA)
      return await self.context.reply(embed=embed, mention_author=False)
    elif str(self.context.channel.id) in randi["ids"]:
      return None
    #await self.context.typing()
    entries = [(
      f"`{self.context.prefix}{cmd.qualified_name}`",
      f"{cmd.short_doc if cmd.short_doc else 'No Description Provided...'}\n\n"
    ) for cmd in cog.get_commands()]
    paginator = Paginator(source=FieldPagePaginator(
      entries=entries,
      title=f"{cog.qualified_name.title()} ({len(cog.get_commands())})",
      description=
      "```yaml\n- [] = optional argument\n- <> = required argument\n- Do NOT Type These When Using Commands !```\n\n",
      color=0x00FFCA,
      per_page=10),
                          ctx=self.context)
    await paginator.paginate()


class Help(Cog, name="help"):

  def __init__(self, client: Astroz):
    self._original_help_command = client.help_command
    attributes = {
      'name':
      "help",
      'aliases': ['h'],
      'cooldown':
      commands.CooldownMapping.from_cooldown(1, 5, commands.BucketType.user),
      'help':
      'Shows help about bot, a command or a category'
    }
    client.help_command = HelpCommand(command_attrs=attributes)
    client.help_command.cog = self

  async def cog_unload(self):
    self.help_command = self._original_help_command

import discord
from discord.ext import commands
import reactionmenu
from reactionmenu import ViewMenu, ViewButton
from utils.Tools import *
import asyncio
import math
import json
print(os.getcwd())


class Slist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = "Shows the top 5 songs in the server"
        self.usage = "slist"
        self.aliases = ["slist", "serverlist"]
        self.bot.remove_command("help")
        self.bot.remove_command("help_command")
        self.bot.remove_command("help_cog")
        self.bot.remove_command("help_command_cog")

    @commands.command(name="slist", aliases=["serverlist"])
    @commands.guild_only()
    async def server_list(self, ctx):
        servers = sorted(ctx.bot.guilds, key=lambda s: s.member_count, reverse=True)
        page = 1
        per_page = 10
        total_pages = math.ceil(len(servers) / per_page)

        def generate_embed(page):
            start_index = (page - 1) * per_page
            end_index = start_index + per_page
            current_servers = servers[start_index:end_index]

            description = ""
            for i, server in enumerate(current_servers, start=start_index+1):
                description += f"`[{i}]` | [{server.name}](https://discord.com/channels/{server.id}) - {server.member_count}\n"

            embed = discord.Embed(title=f"Server List ({len(servers)})", description=description, color=0x00FFCA)
            return embed

        message = await ctx.send(embed=generate_embed(page))

        await message.add_reaction("◀️")
        await message.add_reaction("⏪")
        await message.add_reaction("🗑️")
        await message.add_reaction("▶️")
        await message.add_reaction("⏩")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀️", "⏪", "🗑️", "▶️", "⏩"]

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await message.clear_reactions()
                break

            if str(reaction.emoji) == "🗑️":
                await message.delete()
                break
            elif str(reaction.emoji) == "◀️":
                page -= 1
                if page < 1:
                    page = total_pages
            elif str(reaction.emoji) == "⏪":
                page = 1
            elif str(reaction.emoji) == "▶️":
                page += 1
                if page > total_pages:
                    page = 1
            elif str(reaction.emoji) == "⏩":
                page = total_pages

            await message.edit(embed=generate_embed(page))
            await message.remove_reaction(reaction, user)

        # Record the server list data in a JSON file
        data = {
            "guild_id": ctx.guild.id,
            "page": page,
            "total_pages": total_pages
        }
        with open("server_list_data.json", "w") as file:
            json.dump(data, file)
          
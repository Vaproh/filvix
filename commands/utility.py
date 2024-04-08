# importing discord modules
from typing import Optional, Union
import discord
from discord.ext import commands

# importing utility modules
import sys
import psutil
import random
import datetime
from datetime import timezone
import json

# importing custom bot
from main import CustomBot

# get virtual mem usage
def get_virtual_memory_usage():
  """Get the virtual memory usage."""

  vm = psutil.virtual_memory()
  return vm.used

# cog starts here
class Utility(commands.Cog):
    def __init__(self, bot: CustomBot):
        self.bot = bot
        self.custom_responses = self.load_custom_responses()

    # botinfo command
    @commands.hybrid_command(name="botinfo",
                                aliases=['bi'],
                                help="Get info about me!",with_app_command = True)
    async def botinfo(self, ctx: commands.Context):
                users = sum(g.member_count for g in self.bot.guilds
                        if g.member_count != None)
                channel = len(set(self.bot.get_all_channels()))
                # Get the CPU usage as a percentage
                cpu_usage = psutil.cpu_percent()

                # Round the CPU usage to the nearest integer
                cpu_usage = round(cpu_usage)
                
                # embed
                embed = discord.Embed(color=random.randint(0, 0xFFFFFF),
                                title= str(self.bot.user.name).capitalize() + " " + "Information",
                                description=f"""
        **Bot's Mention:** {self.bot.user.mention}
        **Bot's Username:** {self.bot.user}
        **Total Guilds:** {len(self.bot.guilds)}
        **Total Users:** {users}
        **Total Channels:** {channel}
        **Total Commands: **{len(set(self.bot.walk_commands()))}
        **CPU usage:** {cpu_usage}%
        **Memory usage:** {int(get_virtual_memory_usage() / 1024 / 1024)} MB
        **My Websocket Latency:** {int(self.bot.latency * 1000)} ms
        **Python Version:** {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}
        **Discord.py Version:** {discord.__version__}
        """)
                embed.set_footer(text=f"Requested By {ctx.author}",
                                icon_url=ctx.author.avatar.url if ctx.author.avatar
                                else ctx.author.default_avatar.url)
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                await ctx.send(embed=embed)
    
    # ping command
    @commands.hybrid_command(name="ping",
                             aliases=["latency"],
                             usage="Checks the bot latency.",with_app_command = True,
                             help="Checks the bot latency.")
   
    async def ping(self, ctx):
        embed = discord.Embed(
                title="""
                <:2984goodping:1225411097419579395> Ping! """,
                description=f"<:5909_SayoriSleep:1225411999463247912> **__websocket Latency__** :  {int(self.bot.latency * 1000)} **__ms__**",
                color=random.randint(0, 0xFFFFFF))
        embed.set_footer(
                            icon_url=ctx.author.avatar.url if ctx.author.avatar
                            else ctx.author.default_avatar.url)
        await ctx.reply(embed=embed)



    #Invite
    @commands.hybrid_command(name="invite", aliases=['inv'])
    async def invite(self, ctx: commands.Context):
            embed = discord.Embed(
                description=
                "> • [Click Here To Invite Zoynix To Your Server](https://discord.com/oauth2/authorize?client_id=1213860294301061122&permissions=8&scope=bot)\n> • [Click Here To Join My Support Server](https://discord.gg/sxhGCtjX9R)",
                color=0x0565ff)
            embed.set_author(name=f"{ctx.author.name}",
                            icon_url=f"{ctx.author.avatar}")
            await ctx.send(embed=embed)

    #Membercount  
    @commands.hybrid_command(name="membercount",
                             help="Get total member count of the server",
                             usage="membercount",
                             aliases=["mc"])
    async def membercount(self, ctx: commands.Context):
        embed = discord.Embed(
               title=ctx.guild.name,
               description="**MemberCount**\n- %s members" % (len(ctx.guild.members)),
    )

    @commands.command(name='userinfo', help='Displays information about a user.',aliases=['ui'])
    async def userinfo(self, ctx, user: discord.Member = None):
       user = user or ctx.author
  
       embed = discord.Embed(title=f"**{user.name}'s Information**", color=0x0565ff)
       embed.add_field(name="User ID", value=user.id, inline=False)
       embed.add_field(name="**<a:dot:1218087533141819413> | `Joined Server`**", value=user.joined_at.strftime('%Y-%m-%d, at %H:%M:%S'), inline=False)
       embed.add_field(name="**<a:dot:1218087533141819413> | `Created Account`**", value=user.created_at.strftime('%Y-%m-%d, at %H:%M:%S'), inline=False)
       embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
       await ctx.send(embed=embed)

    @commands.command(aliases=["up", "u"])
    async def uptime(self, ctx):    
        now = datetime.utcnow().replace(tzinfo=timezone.utc)
        uptime = now - self.start_time

        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        uptime_str = "```{:d}d {:02d}h {:02d}m {:02d}s```".format(days, hours, minutes, seconds)

        embed = discord.Embed(title="Arch Uptime", description=uptime_str, color=0x0565ff)
        member = ctx.guild.get_member(ctx.author.id)
        if member:
            embed.set_author(name=f"Arch Uptime",icon_url=self.bot.user.display_avatar.url)
            embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        else:
            embed.set_footer(text=f"Requested by {ctx.author.name}")
            embed.set_thumbnail(url=self.bot.user.avatar.url)          
        await ctx.send(embed=embed)   

    @commands.command()
    async def whois(self, ctx, member: Optional[Union[discord.User, discord.Member]] = None):
        if member is None or member == "":
            member = ctx.author
        elif member not in ctx.guild.members:
            member = await self.bot.fetch_user(member.id)

        badges = ""
        if member.public_flags.hypesquad_balance:
            badges += "<:hypesquadbalance:1215686770570825768>"
        if member.public_flags.hypesquad_bravery:
            badges += "<:hypesquadbravery:1215686743626350603>"
        if member.public_flags.hypesquad_brilliance:
            badges += "<:DGH_hypesquadbrillance:1215686832902377584>"
        if member.public_flags.early_supporter:
            badges += "<:EarlySupporter:1216385290969813093>"
        if member.public_flags.active_developer:
            badges += "<:active_developer:1216385084811116634>"
        if member.public_flags.verified_bot_developer:
            badges += "<:VerifiedBotDeveloper:1216385467994472479>"
        if member.public_flags.discord_certified_moderator:
            badges += "<:DiscordCertifiedModerator:1216385670101074000>"
        if member.public_flags.staff:
            badges += "<:DiscordStaff:1216385969578836208>"
        if member.public_flags.partner:
            badges += "<:partners:1216386169311461537>"
        if badges == "" or badges is None:
            badges += "None"

        if member in ctx.guild.members:
            nickk = f"{member.nick if member.nick else 'None'}"
            joinedat = f"<t:{round(member.joined_at.timestamp())}:R>"
        else:
            nickk = "None"
            joinedat = "None"

        kp = ""
        if member in ctx.guild.members:
            if member.guild_permissions.kick_members:
                kp += " , Kick Members"
            if member.guild_permissions.ban_members:
                kp += " , Ban Members"
            if member.guild_permissions.administrator:
                kp += " , Administrator"
            if member.guild_permissions.manage_channels:
                kp += " , Manage Channels"
            if member.guild_permissions.manage_messages:
                kp += " , Manage Messages"
            if member.guild_permissions.mention_everyone:
                kp += " , Mention Everyone"
            if member.guild_permissions.manage_nicknames:
                kp += " , Manage Nicknames"
            if member.guild_permissions.manage_roles:
                kp += " , Manage Roles"
            if member.guild_permissions.manage_webhooks:
                kp += " , Manage Webhooks"
            if member.guild_permissions.manage_emojis:
                kp += " , Manage Emojis"

            if kp is None or kp == "":
                kp = "None"

        if member in ctx.guild.members:
            if member == ctx.guild.owner:
                aklm = "Server Owner"
            elif member.guild_permissions.administrator:
                aklm = "Server Admin"
            elif member.guild_permissions.ban_members or member.guild_permissions.kick_members:
                aklm = "Server Moderator"
            else:
                aklm = "Server Member"

        bannerUser = await self.bot.fetch_user(member.id)
        embed = discord.Embed(color=0x0565ff)
        embed.timestamp = discord.utils.utcnow()
        if not bannerUser.banner:
            pass
        else:
            embed.set_image(url=bannerUser.banner)
        embed.set_author(name=f"{member.name}'s Information",
                         icon_url=member.avatar.url
                         if member.avatar else member.default_avatar.url)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.add_field(name="__General Information__",
                        value=f"""
                        **Name:** {member}
                        **ID:** {member.id}
                        **Nickname:** {nickk}
                        **Bot?:** {'<:IconTick:1213170250267492383> Yes' if member.bot else '<:crosss:1212440602659262505> No'}
                        **Badges:** {badges}
                        **Account Created:** <t:{round(member.created_at.timestamp())}:R>
                        **Server Joined:** {joinedat}
                                    """,
                        inline=False)
        if member in ctx.guild.members:
            r = (', '.join(role.mention for role in member.roles[1:][::-1])
                 if len(member.roles) > 1 else 'None.')
            embed.add_field(name="__Role Info__",
                            value=f"""
**Highest Role:** {member.top_role.mention if len(member.roles) > 1 else 'None'}
**Roles [{f'{len(member.roles) - 1}' if member.roles else '0'}]:** {r if len(r) <= 1024 else r[0:1006] + ' and more...'}
**Color:** {member.color if member.color else '000000'}
                """,
                            inline=False)
        if member in ctx.guild.members:
            embed.add_field(
                name="__Extra__",
                value=f"**Boosting:** {f'<t:{round(member.premium_since.timestamp())}:R>' if member in ctx.guild.premium_subscribers else 'None'}\n**Voice <:icons_mic:1124695914397827224>:** {'None' if not member.voice else member.voice.channel.mention}",
                inline=False)
        if member in ctx.guild.members:
            embed.add_field(name="__Key Permissions__",
                            value=", ".join([kp]),
                            inline=False)
        if member in ctx.guild.members:
            embed.add_field(name="__Acknowledgement__",
                            value=f"{aklm}",
                            inline=False)
        if member in ctx.guild.members:
            embed.set_footer(
                text=f"Requested by {ctx.author}",
                icon_url=ctx.author.avatar.url
                if ctx.author.avatar else ctx.author.default_avatar.url)
        else:
            if member not in ctx.guild.members:
                embed.set_footer(
                    text=f"{member.name} not in this this server.",
                    icon_url=ctx.author.avatar.url
                    if ctx.author.avatar else ctx.author.default_avatar.url)
        await ctx.send(embed=embed)


     # Auto Responder  
    def load_custom_responses(self):
        try:
            with open("custom_responses.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_custom_responses(self):
        with open("custom_responses.json", "w") as f:
            json.dump(self.custom_responses, f)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return  # Don't respond to the bot's own messages
        content = message.content.lower()

        # Check if the message content is a trigger for a custom response
        if content in self.custom_responses:
            response = self.custom_responses[content]
            await message.channel.send(response)
        # Add more conditional statements for other responses as needed

    @commands.command(name="addresponse", help="Add a custom response for a trigger.")
    @commands.has_permissions(administrator=True)
    async def add_custom_response(self, ctx, trigger, *, response):
        # Allow only administrators to add custom responses
        self.custom_responses[trigger.lower()] = response
        self.save_custom_responses()
        await ctx.send(f"Custom response added for trigger: {trigger}")

    @commands.command(
        name="removeresponse", help="Remove a custom response for a trigger."
    )
    @commands.has_permissions(administrator=True)
    async def remove_custom_response(self, ctx, trigger):
        # Allow only administrators to remove custom responses
        if trigger.lower() in self.custom_responses:
            del self.custom_responses[trigger.lower()]
            self.save_custom_responses()
            await ctx.send(f"Custom response removed for trigger: {trigger}")
        else:
            await ctx.send(f"No custom response found for trigger: {trigger}")


# add cogs
async def setup(bot: CustomBot) -> None:
    await bot.add_cog(Utility(bot))

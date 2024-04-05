from __future__ import annotations
from discord.ext import commands
from utils.Tools import *
from discord import *
from utils.config import OWNER_IDS, No_Prefix
import json, discord
import typing
from utils import Paginator, DescriptionEmbedPaginator, FieldPagePaginator, TextPaginator

from typing import Optional

#Cyg90MAh7a0
class Owner(commands.Cog):

    def __init__(self, client):
        self.client = client


  




    @commands.command(name="restart", help="Restarts the client.")
    @commands.is_owner()
    async def _restart(self, ctx: Context):
        await ctx.reply("Restarting! <:tick_icons:1124596979813580801> Pls Wait It Takes 5-6 Second")
        restart_program()

    @commands.command(name="shutdown", help="Shutdown the client.")
    @commands.is_owner()
    async def _shutdown(self, ctx: Context):
        await ctx.bot.logout()

    @commands.command(name="sync", help="Syncs all database.")
    @commands.is_owner()
    async def _sync(self, ctx):
        await ctx.reply("Syncing...", mention_author=False)
        with open('anti.json', 'r') as f:
            data = json.load(f)
        for guild in self.client.guilds:
            if str(guild.id) not in data['guild']:
                data['guilds'][str(guild.id)] = 'on'
                with open('anti.json', 'w') as f:
                    json.dump(data, f, indent=4)
            else:
                pass
        with open('config.json', 'r') as f:
            data = json.load(f)
        for op in data["guilds"]:
            g = self.client.get_guild(int(op))
            if not g:
                data["guilds"].pop(str(op))
                with open('config.json', 'w') as f:
                    json.dump(data, f, indent=4)

    @commands.group(name="blacklist",
                    help="let's you add someone in blacklist",
                    aliases=["bl"])
    @commands.is_owner()
    async def blacklist(self, ctx):
        if ctx.invoked_subcommand is None:
            with open("blacklist.json") as file:
                blacklist = json.load(file)
                entries = [
                    f"`[{no}]` | <@!{mem}> (ID: {mem})"
                    for no, mem in enumerate(blacklist['ids'], start=1)
                ]
                paginator = Paginator(source=DescriptionEmbedPaginator(
                    entries=entries,
                    title=
                    f"List of Blacklisted users of Heavens - {len(blacklist['ids'])}",
                    description="",
                    per_page=10,
                    color=0x00FFCA),
                                      ctx=ctx)
                await paginator.paginate()

    @blacklist.command(name="add")
    @commands.is_owner()
    async def blacklist_add(self, ctx: Context, member: discord.Member):
        try:
            with open('blacklist.json', 'r') as bl:
                blacklist = json.load(bl)
                if str(member.id) in blacklist["ids"]:
                    embed = discord.Embed(
                        title="Error!",
                        description=f"{member.name} is already blacklisted",
                        color=discord.Colour(0x00FFCA))
                    await ctx.reply(embed=embed, mention_author=False)
                else:
                    add_user_to_blacklist(member.id)
                    embed = discord.Embed(
                        title="Blacklisted",
                        description=f"Successfully Blacklisted {member.name}",
                        color=discord.Colour(0x00FFCA))
                    with open("blacklist.json") as file:
                        blacklist = json.load(file)
                        embed.set_footer(
                            text=
                            f"There are now {len(blacklist['ids'])} users in the blacklist"
                        )
                        await ctx.reply(embed=embed, mention_author=False)
        except:
            embed = discord.Embed(title="Error!",
                                  description=f"An Error Occurred",
                                  color=discord.Colour(0x00FFCA))
            await ctx.reply(embed=embed, mention_author=False)

    @blacklist.command(name="remove")
    @commands.is_owner()
    async def blacklist_remove(self, ctx, member: discord.Member = None):
        try:
            remove_user_from_blacklist(member.id)
            embed = discord.Embed(
                title="User removed from blacklist",
                description=
                f" **{member.name}** has been successfully removed from the blacklist",
                color=0x00FFCA)
            with open("blacklist.json") as file:
                blacklist = json.load(file)
                embed.set_footer(
                    text=
                    f"There are now {len(blacklist['ids'])} users in the blacklist"
                )
                await ctx.reply(embed=embed, mention_author=False)
        except:
            embed = discord.Embed(
                title="Error!",
                description=f"**{member.name}** is not in the blacklist.",
                color=0x00FFCA)
            embed.set_thumbnail(url=f"{self.client.user.display_avatar.url}")
            await ctx.reply(embed=embed, mention_author=False)


    @commands.group(name="bdg", help="Allows owner to add badges for a user")
    @commands.is_owner()
    async def _badge(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @_badge.command(name="add",
                    aliases=["give"],
                    help="Add some badges to a user.")
  
    @commands.is_owner()
    async def badge_add(self, ctx, member: discord.Member, *, badge: str):
        ok = getbadges(member.id)
        if badge.lower() in ["dev", "developer", "devp"]:
            idk = "**<a:developer:1101763075012567131>・DEVELOPER**"
            ok.append(idk)
            makebadges(member.id, ok)
            embed2 = discord.Embed(
        
          
    
                description=
                f"<:IconTick:1213170250267492383> | **Successfully Added `Developer` Badge To {member}**",
                color=0x50101)
            await ctx.reply(embed=embed2)
        elif badge.lower() in ["king", "owner"]:
            idk = "**<:owner:1212437923404972113>・OWNER**"
            ok.append(idk)
            makebadges(member.id, ok)
            embed8 = discord.Embed(
                
                description=
                f"<:IconTick:1213170250267492383> | **Successfully Added `OWNER` Badge To {member}**",
                color=0x50101)
            await ctx.reply(embed=embed8)
        elif badge.lower() in ["co", "coowner"]:
            idk = "**<:CoOwner:1101790386080456745>・CO OWNER**"
            ok.append(idk)
            makebadges(member.id, ok)
            embed12 = discord.Embed(
                
                description=
                f"<:IconTick:1213170250267492383> | **Successfully Added `CO OWNER` Badge To {member}**",
                color=0x50101)
            await ctx.reply(embed=embed12)
        elif badge.lower() in ["admin", "ad"]:
            idk = "**<:admin_icon:1215274170875645992>・ADMIN**"
            ok.append(idk)
            makebadges(member.id, ok)
            embed20 = discord.Embed(
                
                description=
                f"<:IconTick:1213170250267492383> | **Successfully Added `ADMIN` Badge To {member}**",
                color=0x50101)
            await ctx.reply(embed=embed20)
        elif badge.lower() in ["mods", "moderator"]:
            idk = "**・MODERATOR**"
            ok.append(idk)
            makebadges(member.id, ok)
            embed15 = discord.Embed(
                
                description=
                f"<:IconTick:1213170250267492383> | **Successfully Added `MODERATOR` Badge To {member}**",
                color=0x50101)
            await ctx.reply(embed=embed15)
                          
          
       
            
        
        elif badge.lower() in ["staff", "support staff"]:
            idk = "**<:moderation:1212415056772595714>・STAFF**"
            ok.append(idk)
            makebadges(member.id, ok)
            embed3 = discord.Embed(
                
                description=
                f"<:IconTick:1213170250267492383> | **Successfully Added `STAFF` Badge To {member}**",
                color=0x50101)
            await ctx.reply(embed=embed3)
        elif badge.lower() in ["partner"]:
            idk = "**:icon_partner:1215275014903832597>・PARTNER**"
            ok.append(idk)
            makebadges(member.id, ok)
            embed4 = discord.Embed(
                
                description=
                f"<:IconTick:1213170250267492383> | **Successfully Added `PARTNER` Badge To {member}**",
                color=0x50101)
            
            await ctx.reply(embed=embed4)
        elif badge.lower() in ["sponser", "sp"]:
            idk = "**<a:sponsor:1101773574747992157>・SPONSER**"
            ok.append(idk)
            makebadges(member.id, ok)
            embed5 = discord.Embed(
                
                description=
                f"<:IconTick:1213170250267492383> | **Successfully Added `SPONSER` Badge To {member}**",
                color=0x50101)
            
            await ctx.reply(embed=embed5)
        elif badge.lower() in [
                "friend", "friends", "homies", "owner's friend"
        ]:
            idk = "**<a:friends:1101772553623703565>・FRIENDS**"
            ok.append(idk)
            makebadges(member.id, ok)
            embed1 = discord.Embed(
                
                description=
                f"<:IconTick:1213170250267492383> | **Successfully Added `FRIENDS` Badge To {member}**",
                color=0x50101)
            
            await ctx.reply(embed=embed1)
        elif badge.lower() in ["early", "supporter", "support"]:
            idk = "**<:supporter:1101765853843836948>・EARLY SUPPORTER**"
            ok.append(idk)
            makebadges(member.id, ok)
            embed6 = discord.Embed(
                
                description=
                f"<:IconTick:1213170250267492383> | **Successfully Added `SUPPORTER` Badge To {member}**",
                color=0x50101)
            
            await ctx.reply(embed=embed6)

        elif badge.lower() in ["vip"]:
            idk = "**<:VIP:1101772542227779625>・VIP**"
            ok.append(idk)
            makebadges(member.id, ok)
            embed7 = discord.Embed(
                
                description=
                f"<:IconTick:1213170250267492383> | **Successfully Added `VIP` Badge To {member}**",
                color=0x50101)
            
            await ctx.reply(embed=embed7)

        elif badge.lower() in ["bug", "hunter", "bh"]:
            idk = "**<:bot_hunter:1101792120429355018>・BUG HUNTER**"
            ok.append(idk)
            makebadges(member.id, ok)
            embed8 = discord.Embed(
                
                description=
                f"<:IconTick:1213170250267492383> | **Successfully Added `BUG HUNTER` Badge To {member}**",
                color=0x50101)
            
            await ctx.reply(embed=embed8)
        
        elif badge.lower() in ["hindu"]:
            idk = "**<:jai_shree_ram:1123650351552282624>・KATTAR HINDU**"
            ok.append(idk)
            makebadges(member.id, ok)
            embed9 = discord.Embed(
                
                description=
                f"<:IconTick:1213170250267492383> | **Successfully Added `KATTAR HINDU` Badge To {member}**",
                color=0x50101)
            
            await ctx.reply(embed=embed9)

        elif badge.lower() in ["all"]:
            idk = "**<:devloper:1215273270744588311>・DEVELOPER\n<:owner:1212437923404972113>・OWNER\n<:CoOwnerIcon:1215273848665284629>・CO OWNER\n<:admin_icon:1215274170875645992>・ADMIN\n<:moderation:1212415056772595714>・MODERATOR\n<:staff_icon:1215274732169994301>・STAFF\n<:icon_partner:1215275014903832597>・PARTNER\n<:sponser:1215275332878205048>・SPONSER\n<:icons_partner:1215275031224000572>・FRIENDS\n<:early_bot_supporter:1215275688953647184>・EARLY SUPPORTER\n<:VIP_Icon:1215275899025363005>・VIP\n<:LM_Icons_BugHunter:1215276177149796352>・BUG HUNTER\n<:hindu_hinduism:1215276433463713802>・KATTAR HINDU**"
            ok.append(idk)
            makebadges(member.id, ok)
            embedall = discord.Embed(
                
                description=
                f"<:IconTick:1213170250267492383> | **Successfully Added `All` Badges To {member}**",
                color=0x50101)
            
            await ctx.reply(embed=embedall)
        else:
            hacker = discord.Embed(
                                   description="**Invalid Badge**",
                                   color=0x50101)
            
            await ctx.reply(embed=hacker)

    @_badge.command(name="remove",
                    help="Remove badges from a user.",
                    aliases=["re"])
    @commands.is_owner()
    async def badge_remove(self, ctx, member: discord.Member, *, badge: str):
        ok = getbadges(member.id)
        if badge.lower() in ["dev", "developer", "devp"]:
            idk = "**<a:developer:1101763075012567131>・DEVELOPER**"
            ok.remove(idk)
            makebadges(member.id, ok)
            embed2 = discord.Embed(
        
          
    
                description=
                f"<:IconTick:1213170250267492383> | **Successfully Removed `Developer` Badge To {member}**",
                color=0x50101)
            await ctx.reply(embed=embed2)
        elif badge.lower() in ["king", "owner"]:
            idk = "**<a:AnimatedCrown:1100765218553999492>・OWNER**"
            ok.remove(idk)
            makebadges(member.id, ok)
            embed8 = discord.Embed(
                
                description=
                f"<:IconTick:1213170250267492383> | **Successfully Removed `OWNER` Badge To {member}**",
                color=0x50101)
            await ctx.reply(embed=embed8)
        elif badge.lower() in ["co", "coowner"]:
            idk = "**<:CoOwner:1101790386080456745>・CO OWNER**"
            ok.remove(idk)
            makebadges(member.id, ok)
            embed12 = discord.Embed(
                
                description=
                f"<:IconTick:1213170250267492383> | **Successfully Removed `CO OWNER` Badge To {member}**",
                color=0x50101)
            await ctx.reply(embed=embed12)
        elif badge.lower() in ["admin", "ad"]:
            idk = "**<a:phuck_u:1102102966992908329>・ADMIN**"
            ok.remove(idk)
            makebadges(member.id, ok)
            embed20 = discord.Embed(
                
                description=
                f"<:IconTick:1213170250267492383> | **Successfully Removed `ADMIN` Badge To {member}**",
                color=0x50101)
            await ctx.reply(embed=embed20)
        elif badge.lower() in ["mods", "moderator"]:
            idk = "**<:automod:1101354580199084032>・MODERATOR**"
            ok.remove(idk)
            makebadges(member.id, ok)
            embed15 = discord.Embed(
                
                description=
                f"<:IconTick:1213170250267492383> | **Successfully Removed `MODERATOR` Badge To {member}**",
                color=0x50101)
            await ctx.reply(embed=embed15)
                          
          
       
            
        
        elif badge.lower() in ["staff", "support staff"]:
            idk = "**<:bff_Staff:1101761690401513522>・STAFF**"
            ok.remove(idk)
            makebadges(member.id, ok)
            embed3 = discord.Embed(
                
                description=
                f"<:IconTick:1213170250267492383> | **Successfully Removed `STAFF` Badge To {member}**",
                color=0x50101)
            await ctx.reply(embed=embed3)
        elif badge.lower() in ["partner"]:
            idk = "**<:partner:1101762417681248336>・PARTNER**"
            ok.remove(idk)
            makebadges(member.id, ok)
            embed4 = discord.Embed(
                
                description=
                f"<:IconTick:1213170250267492383> | **Successfully Removed `PARTNER` Badge To {member}**",
                color=0x50101)
            
            await ctx.reply(embed=embed4)
        elif badge.lower in ["sponser"]:
            idk = "<a:sponsor:1101773574747992157>・SPONSER**"
            ok.remove(idk)
            makebadges(member.id, ok)
            embed5 = discord.Embed(
                
                description=
                f"<:IconTick:1213170250267492383> | **Successfully Removed `SPONSER` Badge To {member}**",
                color=0x50101)
            
            await ctx.reply(embed=embed5)
        elif badge.lower() in [
                "friend", "friends", "homies", "owner's friend"
        ]:
            idk = "**<a:friends:1101772553623703565>・FRIENDS**"
            ok.remove(idk)
            makebadges(member.id, ok)
            embed1 = discord.Embed(
                
                description=
                f"<:IconTick:1213170250267492383> | **Successfully Removed `FRIENDS` Badge To {member}**",
                color=0x50101)
            
            await ctx.reply(embed=embed1)
        elif badge.lower() in ["early", "supporter", "support"]:
            idk = "**<:supporter:1101765853843836948>・EARLY SUPPORTER**"
            ok.remove(idk)
            makebadges(member.id, ok)
            embed6 = discord.Embed(
                
                description=
                f"<:IconTick:1213170250267492383> | **Successfully Removed `SUPPORTER` Badge To {member}**",
                color=0x50101)
            
            await ctx.reply(embed=embed6)

        elif badge.lower() in ["vip"]:
            idk = "**<:VIP:1101772542227779625>・VIP**"
            ok.remove(idk)
            makebadges(member.id, ok)
            embed7 = discord.Embed(
                
                description=
                f"<:IconTick:1213170250267492383> | **Successfully Removed `VIP` Badge To {member}**",
                color=0x50101)
            
            await ctx.reply(embed=embed7)

        elif badge.lower() in ["hindu"]:
            idk = "**<:jai_shree_ram:1123650351552282624>・KATTAR HINDU**"
            ok.remove(idk)
            makebadges(member.id, ok)
            embed8 = discord.Embed(
                
                description=
                f"<:IconTick:1213170250267492383> | **Successfully Removed `KATTAR HINDU` Badge To {member}**",
                color=0x50101)
            
            await ctx.reply(embed=embed8) 
          
        elif badge.lower() in ["bug", "hunter"]:
            idk = "**<:bot_hunter:1101792120429355018>・BUG HUNTER**"
            ok.remove(idk)
            makebadges(member.id, ok)
            embed9 = discord.Embed(
                
                description=
                f"<:IconTick:1213170250267492383> | **Successfully Removed `BUG HUNTER` Badge To {member}**",
                color=0x50101)
            
            await ctx.reply(embed=embed9)
        elif badge.lower() in ["all"]:
            idk = "**<a:developer:1101763075012567131>・DEVELOPER\n<a:AnimatedCrown:1100765218553999492>・OWNER\n<:CoOwner:1101790386080456745>・CO OWNER\n<a:phuck_u:1102102966992908329>・ADMIN\n<:automod:1101354580199084032>・MODERATOR\n<:bff_Staff:1101761690401513522>・STAFF\n<:partner:1101762417681248336>・PARTNER\n<a:sponsor:1101773574747992157>・SPONSER\n<a:friends:1101772553623703565>・FRIENDS\n<:supporter:1101765853843836948>・EARLY SUPPORTER\n<:VIP:1101772542227779625>・VIP\n<:bot_hunter:1101792120429355018>・BUG HUNTER\n<:jai_shree_ram:1123650351552282624>・KATTAR HINDU**"
            ok.remove(idk)
            makebadges(member.id, ok)
            embedall = discord.Embed(
                
                description=
                f"<:IconTick:1213170250267492383> | **Successfully Removed `All` Badges To {member}**",
                color=0x50101)
            
            await ctx.reply(embed=embedall)
        else:
            hacker = discord.Embed(
                                   description="**Invalid Badge**",
                                   color=0x50101)
            
            await ctx.reply(embed=hacker)


    @commands.command()
    async def dm(self, ctx, user: discord.User, *, message: str):
        """ DM the user of your choice """
        try:
            await user.send(message)
            await ctx.send(f"<:IconTick:1213170250267492383> | Successfully Sent a DM to **{user}**")
        except discord.Forbidden:
            await ctx.send("This user might be having DMs blocked or it's a bot account...")           



    @commands.group()
    @commands.is_owner()
    async def change(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))
            
            
    @change.command(name="nickname")
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
                      










@commands.command(help="Make the bot say something in a given channel.")
@commands.is_owner()
async def say(self, ctx: commands.Context, channel_id: int, *, message):
    channel = self.bot.get_channel(channel_id)
    guild = channel.guild
    target_channel = await ctx.message.author.create_dm()
    await ctx.send(f"Sending message to **{guild}** <#{channel.id}>\n> {message}")
    await target_channel.send(message)

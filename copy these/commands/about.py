import discord
from discord.ext import commands
from discord.ui import Button, View

class About(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user in message.mentions and ('about' in message.content.lower() or '$about' in message.content.lower()):
            ctx = await self.bot.get_context(message)
            await self.bot.invoke(ctx)

    @commands.command(name='about')
    async def about(self, ctx):
        embed = discord.Embed(title='About Me', color=0x11100d)

        embed.add_field(name='', value='Heavens is the Best bot with over 450+ commands. It protects your server and provides various features.', inline=False)
        embed.add_field(name='Commands', value='You can use `$help` to see a list of available commands.', inline=False)      
        embed.add_field(name='**・OWNER**', value='[!      Shadow](https://discord.com/users/765865384011628574, 1212431696381612132)', inline=False)#
        embed.add_field(name='**・DEVELOPER**', value='[!      Shadow](https://discord.com/users/765865384011628574, 1212431696381612132) ', inline=False)

        embed.set_author(name=f"About Me",icon_url=self.bot.user.display_avatar.url)
        embed.set_footer(text=f"Requested by {ctx.author.name}",icon_url=ctx.author.avatar.url)
        embed.set_thumbnail(url=self.bot.user.avatar.url)

  #check server


        invite_link = 'https://youtu.be/dQw4w9WgXcQ'
        support_server_link = 'https://discord.gg/h1ontop'
      

        buttons = [
            Button(style=discord.ButtonStyle.link, label='Invite Me', url=invite_link),
            Button(style=discord.ButtonStyle.link, label='Join Support Server', url=support_server_link)
        ]

        view = View()
        view.add_item(buttons[0])
        view.add_item(buttons[1])

        await ctx.send(embed=embed, view=view)
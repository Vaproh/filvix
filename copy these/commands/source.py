import discord
from discord.ext import commands
from discord.ui import Button, View

class Source(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user in message.mentions and ('Source' , 'source code' , 'src' in message.content.lower() or '$Source' , '$source code' , '$src' in message.content.lower()):
            ctx = await self.bot.get_context(message)
            await self.bot.invoke(ctx)

    @commands.command(name='Source')
    async def Source(self, ctx):
        embed = discord.Embed(title='Heavens Source Code', color=0x03f0c4)

        embed.add_field(name='', value='If You Need Heavens Source Code Then click In Source Code Button', inline=False)
        embed.set_author(name=f"Source Heavens",icon_url=self.bot.user.display_avatar.url)
        embed.set_footer(text=f"Requested by {ctx.author.name}",icon_url=ctx.author.avatar.url)
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/1101031984299511919/1113186842821533866/image0.gif")

  #check server


        invite_link = 'https://discord.com/oauth2/authorize?client_id=1096394407823028276&permissions=1239031351480&scope=bot'
        support_server_link = 'https://discord.gg/h1ontop'
      

        buttons = [
            Button(style=discord.ButtonStyle.link, label='Source Code', url=invite_link),
            Button(style=discord.ButtonStyle.link, label='Tutorial', url=support_server_link)
        ]

        view = View()
        view.add_item(buttons[0])
        view.add_item(buttons[1])

        await ctx.send(embed=embed, view=view)
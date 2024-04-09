import discord
import asyncio
from discord.ext import commands
from discord import app_commands, SelectOption, Button
from discord import ButtonStyle
import config
link1 = "https://discord.com/oauth2/authorize?client_id=1223267226719748197&permissions=8&scope=bot"
link = "https://discord.gg/8PNTDecC"

giveaway = "<:icon_GiveawayIcon:1214584516849696788>"
Extra = "<:extra:1213546253649186926>"
autoresp = "<:icon_12:1214562796755484744>"
moderation = "<:moderation:1212415056772595714>"
utility = "<:utility:1214563086585954344>"
leaderboards = "<:icons_loading:1214569603292725330>"
Custom_roles = "<:ruby_antinuke:1212414349738647582>"
info = "<:error:1212814863240400946>"
antinuke = "<:automod:1212414534963433482>"
autorole ="<:autoroles:1217137198738968677>"
music = "<:icons_Music:1213177796336164944>"
class MenuView(discord.ui.View):
    def __init__(self, author, timeout=60):
        super().__init__(timeout=timeout)
        self.author = author

    @discord.ui.select(placeholder="Hey !! I'm filvix  ", options=[
        SelectOption(label="Music", value="music"),
        SelectOption(label="Utility", value="utility")
    ])
    async def select_category(self, interaction: discord.Interaction, select: discord.ui.Select):
        try:
            if interaction.user.id != self.author.id:
                await interaction.response.send_message("This is not your interaction.", ephemeral=True)
                return
            selected_values = select.values
            
            if selected_values and "music" in selected_values:
                embed = discord.Embed(color = config.color_main,
                                  description="**Music\n\n`Play`, `Stop`,`skip`, `Queue`,`clearqueue`,`Volume`,`Join`,`Disconnect/Dc`,`Nowplaying`,`Seek`,`Skipto`, `remove`, `loop`, `grab`, `previous`, `shuffle`...**")
                embed.set_author(name="Music Commands")
                await interaction.response.edit_message(embed=embed, view=self)
            
            elif selected_values and "utility" in selected_values:
                embed = discord.Embed(color = config.color_main, description="**`botinfo`,`Whois`,`ping`,`info`, `userinfo`, `uptime`, ...**")
                embed.set_author(name="Utility Commands")
                await interaction.response.edit_message(embed=embed, view=self)
            select.placeholder = None
        except Exception as e:
            print(f"An error occurred: {e}")
            raise


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

    @commands.Cog.listener()
    async def on_ready(self):
        print("Help Is Ready")

    @commands.command(aliases=['h'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def help(self, ctx):
        view = MenuView(ctx.author)
        embed = discord.Embed(color = config.color_main,
                              description=f'**My prefix is `!! and @Filvix`\nTotal Commands - {len(set(self.bot.walk_commands()))}\n[The Filvix]({link1}) | [Support]({link})\nThanks for using Filvix\n```- [] = optional argument\n- <> = required argument\n- Do NOT Type These When Using Commands !```**')
        embed.add_field(
            name="<:curvedline_B:1224397348667527274>__**Commands**__",
            value=f"**<:curvedline_B:1224397348667527274>{music} `:` Music\n<:curvedline_B:1224397348667527274>{utility} `:` Utility**")
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_footer(text="Powered By The Filvix") 
        button1 = discord.ui.Button(style=discord.ButtonStyle.link, label="The Filvix", url=link1)
        button2 = discord.ui.Button(style=discord.ButtonStyle.link, label="Support", url=link)

        view.add_item(button1)
        view.add_item(button2)

        message = await ctx.reply(embed=embed, view=view)
        try:
            await asyncio.sleep(view.timeout)
        except asyncio.CancelledError:
            pass
        else:
            for child in view.children:
                child.disabled = True
            await message.edit(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(Help(bot))

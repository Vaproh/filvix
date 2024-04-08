# importing discord modules
import typing
import wavelink
import discord
from discord.ext import commands

# importing bot subclass
from main import CustomBot

# importing music module
import wavelink
from wavelink import Player
from typing import cast

# importing utility modules
import config
import datetime

# just read the func name ;-;
def convert_to_minutes(milliseconds: int) -> str:
    """Converts milliseconds to minutes and seconds in a proper way.

    Args:
        milliseconds (int): The number of milliseconds to convert.

    Returns:
        str: The converted time in minutes and seconds.
    """

    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02.0f}:{seconds:02.0f}"

# checking bot is in vc, user is in vc,etc
async def check_perms(self, ctx: commands.Context):
    if not ctx.voice_client:
        embed = discord.Embed(title="Error detected", description="<:crosss:1212440602659262505> I am not in any vc.", color=config.color_err)
        return await ctx.reply(embed=embed) # bot is not in vc
    if ctx.voice_client is None:
        embed2 = discord.Embed(title="Error detected", description="<:crosss:1212440602659262505> You are not in a voice channel.", color=config.color_err)
        return await ctx.reply(embed=embed2) # user is not in vc
    vc: Player = ctx.voice_client
    if not vc.playing:
        embed3 = discord.Embed(title="Error detected", description="<:crosss:1212440602659262505> I am not playing any song.", color=config.color_err)
        return await ctx.reply(embed=embed3) # bot is not playing songs       
    if ctx.author.voice.channel.id != vc.channel.id:
        embed4 = discord.Embed(title="Error detected", description="<:crosss:1212440602659262505> You are in not the same voice channel.", color=config.color_err)
        return await ctx.reply(embed=embed4) # user is not in the same channel as bot

time = datetime.datetime.now()
# class starts here
class Music(commands.Cog):
    def __init__(self, bot: CustomBot):
        self.bot = bot
    
    # play command
    @commands.command(aliases=["p", "P", "PLAY"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def play(self, ctx: commands.Context, *, query: str) -> None:
        """Play a song with the given query."""
        
        # try to join vc
        try:
          vc: Player = await ctx.author.voice.channel.connect(cls=Player, reconnect=True, self_deaf=True)
        except:
          vc: Player = ctx.voice_client
        if not ctx.guild:
            return
        
        # joining vc...
        player: Player
        player = cast(Player, ctx.voice_client)  # type: ignore

        # checking some conditions
        if not player:
            try:
                player = await ctx.author.voice.channel.connect(cls=Player)  # type: ignore
            except AttributeError:
                embed = discord.Embed(title="Error detected", description="<:crosss:1212440602659262505> Please join a voice channel first before using this command.", color=config.color_err)
                await ctx.send(embed=embed)
                return
            except discord.ClientException:
                embed1 = discord.Embed(title="Error detected", description="<:crosss:1212440602659262505> I was unable to join this voice channel. Please try again.", color=config.color_err)
                await ctx.send(embed=embed1)
                return
        
        # checking if paused    
        if vc.paused:
            await ctx.send("Player is paued do `!resume` to play it again")

        # Turn on AutoPlay to enabled mode.
        # enabled = AutoPlay will play songs for us and fetch recommendations...
        # partial = AutoPlay will play songs for us, but WILL NOT fetch recommendations...
        # disabled = AutoPlay will do nothing...
        player.autoplay = wavelink.AutoPlayMode.enabled
        autoplay = player.autoplay

        # Lock the player to this channel...
        if not hasattr(player, "home"):
            player.home = ctx.channel
        elif player.home != ctx.channel:
            await ctx.send(f"You can only play songs in {player.home.mention}, as the player has already started there.")
            return

        # This will handle fetching Tracks and Playlists...
        # Seed the doc strings for more information on this method...
        # If spotify is enabled via LavaSrc, this will automatically fetch Spotify tracks if you pass a URL...
        # Defaults to YouTube for non URL based queries...
        tracks: wavelink.Search = await wavelink.Playable.search(query)
        if not tracks:
            await ctx.send(f"{ctx.author.mention} - Could not find any tracks with that query. Please try again.")
            return

        if isinstance(tracks, wavelink.Playlist):
            # tracks is a playlist...
            added: int = await player.queue.put_wait(tracks)
            await ctx.send(f"Added the playlist **`{tracks.name}`** ({added} songs) to the queue.")
        else:
            track: wavelink.Playable = tracks[0]
            await player.queue.put_wait(track)
            
            if wavelink.Queue.is_empty == True and Player.playing == False:
                return await player.play(player.queue.get(), volume=30)
            elif Player.playing == True:
                pass # fix this bug later in v2 to remove that added in queue message
            else:
                embed_queue = discord.Embed(color=config.color_sec)
                embed_queue.set_author(name=f"- Track added in the queue!", url=track.uri, icon_url="https://cdn.discordapp.com/emojis/1226985238891204762.gif?size=96&quality=lossless")
                embed_queue.set_thumbnail(url=track.artwork)
                embed_queue.add_field(name="Track", value=f"[{track.title}]({track.uri})", inline=False)
                embed_queue.add_field(name="Track Author", value=f"`{track.author}`")
                embed_queue.add_field(name="Track Length", value=f"{convert_to_minutes(track.length)}")
                #embed_queue2.add_field(name="Track position in queue", value=wavelink.Queue.index(item=track.title))
                embed_queue.set_footer(icon_url=ctx.author.avatar.url, text=f"Requested by {ctx.author.display_name}")
                #embed_queue2.timestamp(time)
                await ctx.send(embed=embed_queue)

        if not player.playing:
            # Play now since we aren't playing anything...
            await player.play(player.queue.get(), volume=30)

    
    # skip command
    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def skip(self, ctx) -> None:
        """Skip the current song."""
        
        # checking perms...
        await check_perms(self, ctx)
        
        # define player
        player: Player = cast(Player, ctx.voice_client)
        if not player:
            return
        
        # skip current song...
        await player.skip(force=True)
        await ctx.message.add_reaction("\u2705")


    # nightcore command
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def nightcore(self, ctx) -> None:
        """Set the filter to a nightcore style."""
        
        # checking perms...
        await check_perms(self, ctx)
        
        # define player
        player: Player = cast(Player, ctx.voice_client)
        if not player:
            return

        # apply filter
        filters: wavelink.Filters = player.filters
        filters.timescale.set(pitch=1.2, speed=1.2, rate=1)
        await player.set_filters(filters)

        await ctx.message.add_reaction("\u2705")


    # pause_resume command
    @commands.command(name="toggle", aliases=["pause", "resume"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pause_resume(self, ctx) -> None:
        """Pause or Resume the Player depending on its current state."""
        
        # checking perms...
        await check_perms(self, ctx)
        
        # define player
        player: Player = cast(Player, ctx.voice_client)
        if not player:
            return

        # pause or resume current track
        await player.pause(not player.paused)
        await ctx.send("Player is now " + ("paused" if player.paused else "resumed") + ".")

    # volume command
    @commands.command(aliases=['vol'])
    async def volume(self, ctx: commands.Context , _volume: typing.Optional[int]):
        """
        Set the volume of the bot.
        {command_prefix}{command_name} volume
        volume(optional): The volume for the music playing. If not provide, return current volume
        {command_prefix}{command_name} 200
        NOTE: max is 100, and makes it inaudible.
        """
        
        # checking perms...
        await check_perms(self, ctx)
        
        # define player
        player:Player = typing.cast(Player,ctx.voice_client)
        
        # check volume
        if not _volume:
            return await ctx.send(f'Volume: **{player.volume}%**') #
        elif _volume >100: # volume limit
            await ctx.send("Cannot exceed 100 volume hard limit.")
        else: # set volume
            await player.set_volume(_volume)
            return await ctx.send(f"Set volume to {_volume}")

    # Disconnect command
    @commands.command(aliases=["dc", "disconnect"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def stop(self, ctx) -> None:
        """Disconnect the Player."""
        
        # checking bot is in vc, user is in vc,etc
        if not ctx.voice_client:
            embed = discord.Embed(title="Error detected", description="<:crosss:1212440602659262505> I am not in any vc.", color=config.color_err)
            return await ctx.reply(embed=embed) # bot is not in vc
        if ctx.voice_client is None:
            embed2 = discord.Embed(title="Error detected", description="<:crosss:1212440602659262505> You are not in a voice channel.", color=config.color_err)
            return await ctx.reply(embed=embed2) # user is not in vc
        vc: Player = ctx.voice_client    
        if ctx.author.voice.channel.id != vc.channel.id:
            embed4 = discord.Embed(title="Error detected", description="<:crosss:1212440602659262505> You are in not the same voice channel.", color=config.color_err)
            return await ctx.reply(embed=embed4) # user is not in the same channel as bot
        
        # define player
        player: Player = cast(Player, ctx.voice_client)
        if not player:
            return

        # disconnect the bot from current vc
        await player.disconnect()
        await ctx.send(f"Successfully disconnected from `{player.channel.name}`.")

    # shuffle command
    @commands.command(aliases=['shuf'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def shuffle(self, ctx) -> None:
        """Shuffle the queue."""
        
        # checking perms...
        await check_perms(self, ctx)
        
        # define player 
        player: Player = ctx.voice_client
        
        # shuffle current queue
        player.queue.shuffle()
        await ctx.send("Queue shuffled.")
        
    # now playing command
    @commands.command(aliases=["nowp", "np"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def nowplaying(self, ctx) -> None:
        """Show the current playing song."""
        
        # checking perms...
        await check_perms(self, ctx)
        
        # define player
        vc: Player = ctx.voice_client
        
        # send message
        await ctx.send(f"playing `{vc.current.title}` by `{vc.current.author}` in `{vc.channel.name}`.")
    
    # queue
    @commands.command(aliases=['q', 'que'], help="Look Into The Queue", usage = "queue")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def queue(self, ctx):
        
        # checking perms...
        await check_perms(self, ctx)
        
        # define player
        vc: Player = ctx.voice_client
        
        # enumerate current queue
        queue = enumerate(list(vc.queue), start=1) # queue list
        
        # retrieve track list
        track_list = '\n'.join(f'[{num}] {track.title}' for num, track in queue) # track list
        
        # convert length
        length_seconds = round(vc.current.length) / 1000 # length of song
        hours, remainder = divmod(length_seconds, 3600) # secs converter.
        minutes, seconds = divmod(remainder, 60) # another converter..
        duration_str = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}" # another converter...
        
        # embed
        embed5 = discord.Embed(description=f'**__Now Playing__**\n  {vc.current.title}・{duration_str}\n\n```\n{track_list}```') # embed
        await ctx.reply(embed=embed5, mention_author=False)
    
    # clear queue command    
    @commands.command(aliases=['cq', "cls"], help="Clear The Queue", usage = "clearqueue")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def clearqueue(self, ctx):
        
        # checking perms...
        await check_perms(self, ctx)
        
        #define player
        vc: Player = ctx.voice_client
        
        # clear queue
        vc.queue.clear()
        embed5 = discord.Embed(description="Successfully Cleared The Queue.")
        await ctx.reply(embed=embed5, mention_author=False)
    
    # join command    
    @commands.command(aliases=["connect", "connect_vc", "join_vc"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def join(self, ctx) -> None:
        """Join the voice channel of the message author."""
        
        # check perms
        if ctx.author.voice.channel is None:
            embed2 = discord.Embed(description="You are not in a voice channel.")
            return await ctx.reply(embed=embed2) # user is not in vc
        vc: Player = ctx.voice_client
        if vc is not None and vc.playing:
            embed3 = discord.Embed(description=f"I am playing songs in another channel named `{vc.channel.name}`")
            return await ctx.reply(embed=embed3) # bot is not playing songs
        
        # join author voice channel
        await ctx.author.voice.channel.connect(cls=Player, reconnect=True, self_deaf=True)
        await ctx.send("Successfully joined the voice channel.")
    
    # previous command
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def previous(self, ctx) -> None:
        """Play the previous song in the queue."""

        # checking perms...
        await check_perms(self, ctx)
        
        #define player
        player: Player = cast(Player, ctx.voice_client)
        if not player:
            return

        # geeting previous track and play it else send no previous track to play
        if player.queue.history:
            previous_track = player.queue.history[0]
            await player.queue.put_wait(previous_track)
            await player.stop()
            await ctx.send(f"Now playing the previous track: {previous_track.title}")
        else:
            await ctx.send("There is no previous track to play.")
    
    # grab command        
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def grab(self, ctx, *, query: str) -> None:
        """Grab the song info and send it to your DM."""
        
        # define track
        tracks: wavelink.Search = await wavelink.Playable.search(query)
        
        # cannot get track
        if not tracks:
            await ctx.send(f"{ctx.author.mention} - Could not find any tracks with that query. Please try again.")
            return
        
        if isinstance(tracks, wavelink.Playlist):
            # tracks is a playlist...
            embed = discord.Embed(title=f"Playlist: {tracks.name}", description=f"**Tracks:**\n{', '.join([track.title for track in tracks.tracks])}")
            embed.set_thumbnail(url=tracks.thumbnail)
            await ctx.author.send(embed=embed)
        else:
            track: wavelink.Playable = tracks[0]
            embed = discord.Embed(title=track.title, description=f"**Artist:** {track.author}\n**Album:** {track.album.name}\n**Duration:** {convert_to_minutes(track.length)}")
            embed.set_thumbnail(url=track.artwork)
            await ctx.author.send(embed=embed)

    # loop
    @commands.command(aliases=["repeat"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def loop(self, ctx, mode: str = None) -> None:
        """Loop the current song."""

        # checking perms...
        await check_perms(self, ctx)
        
        #define player
        player: Player = ctx.voice_client
        
        # loop and other modes
        if mode == None:
            wavelink.QueueMode.loop
            await ctx.send(f"Looping is now enabled for track `{player.current.title}`.")
        elif mode == "all":
            wavelink.QueueMode.loop_all
            await ctx.send(f"Looping is now enable for the entire queue.")
        elif mode == "off":
            wavelink.QueueMode.normal
            await ctx.send("Looping is now disabled.")

    # remove command
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def remove(self, ctx, index: int) -> None:
        """Remove a song from the queue."""

        # checking perms...
        await check_perms(self, ctx)
        
        # define player
        player: Player = cast(Player, ctx.voice_client)
        if not player:
            return

        # checking if it a valid index
        if index < 1 or index > len(player.queue):
            await ctx.send("Invalid Song number.")
            return

        # remove track
        removed_track = player.queue.remove(index - 1)
        await ctx.send(f"Removed **`{removed_track.title}`** from the queue.")

    # skip to command
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def skipto(self, ctx: commands.Context, position: int) -> None:
        """Skip to a specific song in the queue."""

        # checking perms...
        await check_perms(self, ctx)
            
        # player
        player: Player = typing.cast(Player,ctx.voice_client)
            
        # checks index
        if isinstance(position,str):
            position = int(position)
        if len(player.queue) == 0: # check index
            return await ctx.send("No songs in queue to skip to.")
        if position:
            if position > len(player.queue):
                return await ctx.send(f"Position exceeds queue count of {len(player.queue)}")
            else: # plays new track
                new_track = player.queue[position-1]
                await player.queue.delete(position-1)
                await player.play(new_track)
                
        await ctx.send(f"Skipped to **`{player.current.title}`**.")
    
    # seek command
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def seek(self,ctx: commands.Context,position:int):
        """
        Jump to a specific in the current audio playing. Value must be in seconds.
        {command_prefix}{command_name} track_time
        track(required): The time to skip to in seconds
        {command_prefix}{command_name} 120
        """
        
        # checking perms...
        await check_perms(self, ctx)
        
        # seeking the position    
        if isinstance(position,str):
            position = int(position)
        position*1000
        player:Player = typing.cast(Player,ctx.voice_client)
        if position >= player.current.length:
            return await ctx.send("Position exceeds or equals to song duration")
        
        # seek func
        return await player.seek(position)

# setup command
async def setup(bot: CustomBot) -> None:
    await bot.add_cog(Music(bot))

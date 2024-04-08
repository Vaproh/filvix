# importing discord modules
import typing
import wavelink
import discord
from discord.ext import commands

# importing bot subclass
from main import CustomBot

# importing music module
import wavelink
from typing import cast

# importing utility modules
import jishaku
import os
import time

# env variables
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_FORCE_PAGINATOR"] = "True"

# class starts here
class Music(commands.Cog):
    def __init__(self, bot: CustomBot):
        self.bot = bot
    
    # play command
    @commands.hybrid_command(aliases=["p", "play_song"])
    async def play(self, ctx, *, query: str) -> None:
        """Play a song with the given query."""
        try:
          vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player, reconnect=True, self_deaf=True)
        except:
          vc: wavelink.Player = ctx.voice_client
        if not ctx.guild:
            return

        player: wavelink.Player
        player = cast(wavelink.Player, ctx.voice_client)  # type: ignore

        if not player:
            try:
                player = await ctx.author.voice.channel.connect(cls=wavelink.Player)  # type: ignore
            except AttributeError:
                await ctx.send("Please join a voice channel first before using this command.")
                return
            except discord.ClientException:
                await ctx.send("I was unable to join this voice channel. Please try again.")
                return
            
        if vc.paused:
            await ctx.send("Player is paued do `!resume` to play it again")

        # Turn on AutoPlay to enabled mode.
        # enabled = AutoPlay will play songs for us and fetch recommendations...
        # partial = AutoPlay will play songs for us, but WILL NOT fetch recommendations...
        # disabled = AutoPlay will do nothing...
        player.autoplay = wavelink.AutoPlayMode.enabled

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
            await ctx.send(f"Added **`{track}`** to the queue.")

        if not player.playing:
            # Play now since we aren't playing anything...
            await player.play(player.queue.get(), volume=30)

    
    # skip command
    @commands.hybrid_command()
    async def skip(self, ctx) -> None:
        """Skip the current song."""
        
        # checking bot is in vc, user is in vc,etc
        if not ctx.voice_client:
            embed = discord.Embed(description="I am not in any vc.")
            return await ctx.reply(embed=embed) # bot is not in vc
        if ctx.voice_client is None:
            embed2 = discord.Embed(description="You are not in a voice channel.")
            return await ctx.reply(embed=embed2) # user is not in vc
        vc: wavelink.Player = ctx.voice_client
        if not vc.playing:
            embed3 = discord.Embed(description="I am not playing any song.")
            return await ctx.reply(embed=embed3) # bot is not playing songs       
        if ctx.author.voice.channel.id != vc.channel.id:
            embed4 = discord.Embed(description="You are in not the same voice channel.")
            return await ctx.reply(embed=embed4) # user is not in the same channel as bot
        
        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        if not player:
            return

        await player.skip(force=True)
        await ctx.message.add_reaction("\u2705")


    # nightcore command
    @commands.hybrid_command()
    async def nightcore(self, ctx) -> None:
        """Set the filter to a nightcore style."""
        
        # checking bot is in vc, user is in vc,etc
        if not ctx.voice_client:
            embed = discord.Embed(description="I am not in any vc.")
            return await ctx.reply(embed=embed) # bot is not in vc
        if ctx.voice_client is None:
            embed2 = discord.Embed(description="You are not in a voice channel.")
            return await ctx.reply(embed=embed2) # user is not in vc
        vc: wavelink.Player = ctx.voice_client
        if not vc.playing:
            embed3 = discord.Embed(description="I am not playing any song.")
            return await ctx.reply(embed=embed3) # bot is not playing songs       
        if ctx.author.voice.channel.id != vc.channel.id:
            embed4 = discord.Embed(description="You are in not the same voice channel.")
            return await ctx.reply(embed=embed4) # user is not in the same channel as bot
        
        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        if not player:
            return

        filters: wavelink.Filters = player.filters
        filters.timescale.set(pitch=1.2, speed=1.2, rate=1)
        await player.set_filters(filters)

        await ctx.message.add_reaction("\u2705")


    # pause_resume command
    @commands.hybrid_command(name="toggle", aliases=["pause", "resume"])
    async def pause_resume(self, ctx) -> None:
        """Pause or Resume the Player depending on its current state."""
        
        # checking bot is in vc, user is in vc,etc
        if not ctx.voice_client:
            embed = discord.Embed(description="I am not in any vc.")
            return await ctx.reply(embed=embed) # bot is not in vc
        if ctx.voice_client is None:
            embed2 = discord.Embed(description="You are not in a voice channel.")
            return await ctx.reply(embed=embed2) # user is not in vc
        vc: wavelink.Player = ctx.voice_client
        if not vc.playing:
            embed3 = discord.Embed(description="I am not playing any song.")
            return await ctx.reply(embed=embed3) # bot is not playing songs       
        if ctx.author.voice.channel.id != vc.channel.id:
            embed4 = discord.Embed(description="You are in not the same voice channel.")
            return await ctx.reply(embed=embed4) # user is not in the same channel as bot
        
        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        if not player:
            return

        await player.pause(not player.paused)
        await ctx.send("Player is now " + ("paused" if player.paused else "resumed") + ".")

    # volume command
    @commands.hybrid_command(aliases=["vol"])
    async def volume(self, ctx, value: int) -> None:
        """Change the volume of the player."""
        
        # checking bot is in vc, user is in vc,etc
        if not ctx.voice_client:
            embed = discord.Embed(description="I am not in any vc.")
            return await ctx.reply(embed=embed) # bot is not in vc
        if ctx.voice_client is None:
            embed2 = discord.Embed(description="You are not in a voice channel.")
            return await ctx.reply(embed=embed2) # user is not in vc
        vc: wavelink.Player = ctx.voice_client 
        if ctx.author.voice.channel.id != vc.channel.id:
            embed4 = discord.Embed(description="You are in not the same voice channel.")
            return await ctx.reply(embed=embed4) # user is not in the same channel as bot
        
        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        if not player:
            return

        await player.set_volume(value)
        await ctx.send(f"Volume set to {value}.")

    # Disconnect command
    @commands.hybrid_command(aliases=["dc", "disconnect"])
    async def stop(self, ctx) -> None:
        """Disconnect the Player."""
        
        # checking bot is in vc, user is in vc,etc
        if not ctx.voice_client:
            embed = discord.Embed(description="I am not in any vc.")
            return await ctx.reply(embed=embed) # bot is not in vc
        if ctx.voice_client is None:
            embed2 = discord.Embed(description="You are not in a voice channel.")
            return await ctx.reply(embed=embed2) # user is not in vc
        vc: wavelink.Player = ctx.voice_client    
        if ctx.author.voice.channel.id != vc.channel.id:
            embed4 = discord.Embed(description="You are in not the same voice channel.")
            return await ctx.reply(embed=embed4) # user is not in the same channel as bot
        
        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        if not player:
            return

        await player.disconnect()
        await ctx.send(f"Successfully disconnected from `{player.channel.name}`.")

    @commands.command(aliases=['shuf'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def shuffle(self, ctx) -> None:
        """Shuffle the queue."""
        vc: wavelink.player
        player: wavelink.Player = ctx.voice_client

        # checking bot is in vc, user is in vc,etc
        if not ctx.voice_client:
            embed = discord.Embed(description="I am not in any vc.")
            return await ctx.reply(embed=embed) # bot is not in vc
        if ctx.voice_client is None:
            embed2 = discord.Embed(description="You are not in a voice channel.")
            return await ctx.reply(embed=embed2) # user is not in vc
        vc: wavelink.Player = ctx.voice_client
        if not vc.playing:
            embed3 = discord.Embed(description="I am not playing any song.")
            return await ctx.reply(embed=embed3) # bot is not playing songs       
        if ctx.author.voice.channel.id != vc.channel.id:
            embed4 = discord.Embed(description="You are in not the same voice channel.")
            return await ctx.reply(embed=embed4) # user is not in the same channel as bot
        
        player.queue.shuffle()
        await ctx.send("Queue shuffled.")
        
    # now playing command
    @commands.hybrid_command(aliases=["nowp", "np"])
    async def nowplaying(self, ctx) -> None:
        """Show the current playing song."""
        
        # checking bot is in vc, user is in vc,etc
        if not ctx.voice_client:
            embed = discord.Embed(description="I am not in any vc.")
            return await ctx.reply(embed=embed) # bot is not in vc
        if ctx.voice_client is None:
            embed2 = discord.Embed(description="You are not in a voice channel.")
            return await ctx.reply(embed=embed2) # user is not in vc
        vc: wavelink.Player = ctx.voice_client
        if not vc.playing:
            embed3 = discord.Embed(description="I am not playing any song.")
            return await ctx.reply(embed=embed3) # bot is not playing songs       
        if ctx.author.voice.channel.id != vc.channel.id:
            embed4 = discord.Embed(description="You are in not the same voice channel.")
            return await ctx.reply(embed=embed4) # user is not in the same channel as bot
        
        
        vc: wavelink.Player = ctx.voice_client

        await ctx.send(f"playing `{vc.current.title}` by `{vc.current.author}` in `{vc.channel.name}`.")
    
    @commands.command(aliases=['q'], help="Look Into The Queue", usage = "queue")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def queue(self, ctx):
        
        # checking bot is in vc, user is in vc,etc
        if not ctx.voice_client:
            embed = discord.Embed(description="I am not in any vc.")
            return await ctx.reply(embed=embed) # bot is not in vc
        if ctx.voice_client is None:
            embed2 = discord.Embed(description="You are not in a voice channel.")
            return await ctx.reply(embed=embed2) # user is not in vc
        vc: wavelink.Player = ctx.voice_client
        if not vc.playing:
            embed3 = discord.Embed(description="I am not playing any song.")
            return await ctx.reply(embed=embed3) # bot is not playing songs       
        if ctx.author.voice.channel.id != vc.channel.id:
            embed4 = discord.Embed(description="You are in not the same voice channel.")
            return await ctx.reply(embed=embed4) # user is not in the same channel as bot
        
        queue = enumerate(list(vc.queue), start=1) # queue list
        
        track_list = '\n'.join(f'[{num}] {track.title}' for num, track in queue) # track list
        
        length_seconds = round(vc.current.length) / 1000 # length of song
        
        hours, remainder = divmod(length_seconds, 3600) # secs converter.
        
        minutes, seconds = divmod(remainder, 60) # another converter..
        
        duration_str = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}" # another converter...
        
        embed5 = discord.Embed(description=f'**__Now Playing__**\n  {vc.current.title}・{duration_str}\n\n```\n{track_list}```') # embed
        
        await ctx.reply(embed=embed5, mention_author=False)
        
    @commands.command(aliases=['cq', "cls"], help="Clear The Queue", usage = "clearqueue")
    async def clearqueue(self, ctx):
        
                # checking bot is in vc, user is in vc,etc
        if not ctx.voice_client:
            embed = discord.Embed(description="I am not in any vc.")
            return await ctx.reply(embed=embed) # bot is not in vc
        if ctx.voice_client is None:
            embed2 = discord.Embed(description="You are not in a voice channel.")
            return await ctx.reply(embed=embed2) # user is not in vc
        vc: wavelink.Player = ctx.voice_client
        if not vc.playing:
            embed3 = discord.Embed(description="I am not playing any song.")
            return await ctx.reply(embed=embed3) # bot is not playing songs       
        if ctx.author.voice.channel.id != vc.channel.id:
            embed4 = discord.Embed(description="You are in not the same voice channel.")
            return await ctx.reply(embed=embed4) # user is not in the same channel as bot

        vc.queue.clear()
        embed5 = discord.Embed(description="Successfully Cleared The Queue.")
        await ctx.reply(embed=embed5, mention_author=False)
        
    @commands.command()
    async def join(self, ctx) -> None:
        """Join the voice channel of the message author."""
        
        if ctx.author.voice.channel is None:
            embed2 = discord.Embed(description="You are not in a voice channel.")
            return await ctx.reply(embed=embed2) # user is not in vc
        vc: wavelink.Player = ctx.voice_client
        if vc is not None and vc.playing:
            embed3 = discord.Embed(description=f"I am playing songs in another channel named `{vc.channel.name}`")
            return await ctx.reply(embed=embed3) # bot is not playing songs
        
        await ctx.author.voice.channel.connect(cls=wavelink.Player, reconnect=True, self_deaf=True)
        await ctx.send("Successfully joined the voice channel.")
    
    @commands.command()
    async def previous(self, ctx) -> None:
        """Play the previous song in the queue."""

        # checking bot is in vc, user is in vc,etc
        if not ctx.voice_client:
            embed = discord.Embed(description="I am not in any vc.")
            return await ctx.reply(embed=embed) # bot is not in vc
        if ctx.voice_client is None:
            embed2 = discord.Embed(description="You are not in a voice channel.")
            return await ctx.reply(embed=embed2) # user is not in vc
        vc: wavelink.Player = ctx.voice_client
        if not vc.playing:
            embed3 = discord.Embed(description="I am not playing any song.")
            return await ctx.reply(embed=embed3) # bot is not playing songs       
        if ctx.author.voice.channel.id != vc.channel.id:
            embed4 = discord.Embed(description="You are in not the same voice channel.")
            return await ctx.reply(embed=embed4) # user is not in the same channel as bot
        
        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        if not player:
            return

        if player.queue.history:
            previous_track = player.queue.history[0]
            await player.queue.put_wait(previous_track)
            await player.stop()
            await ctx.send(f"Now playing the previous track: {previous_track.title}")
        else:
            await ctx.send("There is no previous track to play.")
            
    @commands.command()
    async def grab(self, ctx, *, query: str) -> None:
        """Grab the song info and send it to your DM."""

        tracks: wavelink.Search = await wavelink.Playable.search(query)
        
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
            
    @commands.hybrid_command()
    async def loop(self, ctx, mode: str = None) -> None:
        """Loop the current song."""

        # checking bot is in vc, user is in vc,etc
        if not ctx.voice_client:
            embed = discord.Embed(description="I am not in any vc.")
            return await ctx.reply(embed=embed) # bot is not in vc
        if ctx.voice_client is None:
            embed2 = discord.Embed(description="You are not in a voice channel.")
            return await ctx.reply(embed=embed2) # user is not in vc
        vc: wavelink.Player = ctx.voice_client
        if not vc.playing:
            embed3 = discord.Embed(description="I am not playing any song.")
            return await ctx.reply(embed=embed3) # bot is not playing songs       
        if ctx.author.voice.channel.id != vc.channel.id:
            embed4 = discord.Embed(description="You are in not the same voice channel.")
            return await ctx.reply(embed=embed4) # user is not in the same channel as bot
        
        player: wavelink.Player = ctx.voice_client
        
        if mode == None:
            wavelink.QueueMode.loop
            await ctx.send(f"Looping is now enabled for track `{player.current.title}`.")
        elif mode == "all":
            wavelink.QueueMode.loop_all
            await ctx.send(f"Looping is now enable for the entire queue.")
        elif mode == "off":
            wavelink.QueueMode.normal
            await ctx.send("Looping is now disabled.")

    @commands.hybrid_command()
    async def remove(self, ctx, index: int) -> None:
        """Remove a song from the queue."""

        # checking bot is in vc, user is in vc,etc
        if not ctx.voice_client:
            embed = discord.Embed(description="I am not in any vc.")
            return await ctx.reply(embed=embed) # bot is not in vc
        if ctx.voice_client is None:
            embed2 = discord.Embed(description="You are not in a voice channel.")
            return await ctx.reply(embed=embed2) # user is not in vc
        vc: wavelink.Player = ctx.voice_client
        if not vc.playing:
            embed3 = discord.Embed(description="I am not playing any song.")
            return await ctx.reply(embed=embed3) # bot is not playing songs       
        if ctx.author.voice.channel.id != vc.channel.id:
            embed4 = discord.Embed(description="You are in not the same voice channel.")
            return await ctx.reply(embed=embed4) # user is not in the same channel as bot
        
        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        if not player:
            return

        if index < 1 or index > len(player.queue):
            await ctx.send("Invalid Song number.")
            return

        removed_track = player.queue.remove(index - 1)
        await ctx.send(f"Removed **`{removed_track.title}`** from the queue.")

    @commands.command()
    async def skipto(self, ctx, position: int) -> None:
        """Skip to a specific song in the queue."""

        # checking bot is in vc, user is in vc,etc
        if not ctx.voice_client:
            embed = discord.Embed(description="I am not in any vc.")
            return await ctx.reply(embed=embed) # bot is not in vc
        if ctx.voice_client is None:
            embed2 = discord.Embed(description="You are not in a voice channel.")
            return await ctx.reply(embed=embed2) # user is not in vc
        vc: wavelink.Player = ctx.voice_client
        if not vc.playing:
            embed3 = discord.Embed(description="I am not playing any song.")
            return await ctx.reply(embed=embed3) # bot is not playing songs       
        if ctx.author.voice.channel.id != vc.channel.id:
            embed4 = discord.Embed(description="You are in not the same voice channel.")
            return await ctx.reply(embed=embed4) # user is not in the same channel as bot
            
        # player
        player: wavelink.Player = typing.cast(wavelink.Player,ctx.voice_client)
            
        # checks index
        if isinstance(position,str):
            position = int(position)
        if len(player.queue) ==0:
            return await ctx.send("No songs in queue to skip to.")
        if position:
            if position > len(player.queue):
                return await ctx.send(f"Position exceeds queue count of {len(player.queue)}")
            else:
                new_track = player.queue[position-1]
                player.queue.delete(position-1)
                await player.play(new_track)
        
        await ctx.send(f"Skipped to **`{player.current.title}`**.")

    


async def setup(bot: CustomBot) -> None:
    await bot.add_cog(Music(bot))
    await bot.load_extension("jishaku") 

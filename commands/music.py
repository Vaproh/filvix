# importing discord modules
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
        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        if not player:
            return

        await player.skip(force=True)
        await ctx.message.add_reaction("\u2705")


    # nightcore command
    @commands.hybrid_command()
    async def nightcore(self, ctx) -> None:
        """Set the filter to a nightcore style."""
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
        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        if not player:
            return

        await player.pause(not player.paused)
        await ctx.send("Player is now " + ("paused" if player.paused else "resumed") + ".")

    # volume command
    @commands.hybrid_command(aliases=["vol"])
    async def volume(self, ctx, value: int) -> None:
        """Change the volume of the player."""
        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        if not player:
            return

        await player.set_volume(value)
        await ctx.send(f"Volume set to {value}.")

    # Disconnect command
    @commands.hybrid_command(aliases=["dc", "stop"])
    async def disconnect(self, ctx) -> None:
        """Disconnect the Player."""
        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        if not player:
            return

        await player.disconnect()
        await ctx.send(f"Successfully disconnected from `{player.channel.name}`.")

    @commands.command(aliases=['shuf'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def shuffle(self, ctx) -> None:
        """Now playing."""
        vc: wavelink.player
        player: wavelink.Player = ctx.voice_client

        if not ctx.voice_client:
            embed = discord.Embed(description="I am not in any vc.")
            return await ctx.reply(embed=embed, mention_author=False)     
        if ctx.voice_client is None:
            embed2 = discord.Embed(description="You are not in a voice channel.")
            return await ctx.reply(embed=embed2, mention_author=False)
        vc: wavelink.Player = ctx.voice_client
        if not vc.playing:
            embed3 = discord.Embed(description="I am not playing any song.")
            return await ctx.reply(embed=embed3, mention_author=False)       
        if ctx.author.voice.channel.id != vc.channel.id:
            embed4 = discord.Embed(description="You are in not the same voice channel.")
            return await ctx.reply(embed=embed4, mention_author=False)
        
        player.queue.shuffle()
        await ctx.send("Queue shuffled.")
        
    # now playing command
    @commands.hybrid_command(aliases=["nowp", "np"])
    async def nowplaying(self, ctx) -> None:
        """Disconnect the Player."""
        vc: wavelink.Player = ctx.voice_client

        await ctx.send(f"playing `{vc.current.title}` by `{vc.current.author}` in `{vc.channel.name}`.")
    
    @commands.command(aliases=['q'], help="Look Into The Queue", usage = "queue")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def queue(self, ctx):
        if not ctx.voice_client:
            embed = discord.Embed(description="I am not in any vc.")
            return await ctx.reply(embed=embed, mention_author=False)     
        if ctx.voice_client is None:
            embed2 = discord.Embed(description="You are not in a voice channel.")
            return await ctx.reply(embed=embed2, mention_author=False)
        vc: wavelink.Player = ctx.voice_client
        if not vc.playing:
            embed3 = discord.Embed(description="I am not playing any song.")
            return await ctx.reply(embed=embed3, mention_author=False)       
        if ctx.author.voice.channel.id != vc.channel.id:
            embed4 = discord.Embed(description="You are in not the same voice channel.")
            return await ctx.reply(embed=embed4, mention_author=False)
        queue = enumerate(list(vc.queue), start=1)
        track_list = '\n'.join(f'[{num}] {track.title}' for num, track in queue)
        length_seconds = round(vc.current.length) / 1000
        hours, remainder = divmod(length_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        duration_str = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
        embed5 = discord.Embed(description=f'**__Now Playing__**\n  {vc.current.title}・{duration_str}\n\n```\n{track_list}```')
        await ctx.reply(embed=embed5, mention_author=False)

async def setup(bot: CustomBot) -> None:
    await bot.add_cog(Music(bot))
    await bot.load_extension("jishaku") 

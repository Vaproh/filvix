# importing discord modules
from venv import logger
import discord
from discord.ext import commands # importing commands module from discord.ext

# importing utility modules
import time
import config
import signal
import os
import wavelink

# cogs
exts = ["commands.moderation", "commands.music", "commands.utility", "commands.admin"]#, "handlers.error_handler"]

# logger
logger = config.logging.getLogger("bot")

# bot subclass
class CustomBot(commands.Bot):
    def __init__(self, command_prefix: str, intents: discord.Intents, *args, **kwargs) -> None:
        # Forward all arguments, and keyword-only arguments to commands.Bot
        super().__init__(command_prefix, intents=intents, *args, **kwargs)

    # Here you are overriding the default start method and write your own code.
    async def setup_hook(self) -> None:
        
        print("loading cogs...")
        # loading cogs
        for ext in exts:
            await self.load_extension(ext)
        print("All cogs are loaded successfully!")
        print("Syncing slash commands...")
        
        # connecting wavelink
        print("connecting wavelink...")
        time.sleep(0.1)
        print("connecting wavelink..")
        nodes = [wavelink.Node(uri="http://15.207.84.229:2333", password="Doom129")] # decalring nodes variable
        time.sleep(0.1)
        print("connecting wavelink.")
        await wavelink.Pool.connect(nodes=nodes, client=self, cache_capacity=100) # connecting...
        time.sleep(0.1)
        print("Wavelink connected successfully!")

    # on connect event
    async def on_connect(self):
        # intro
        print(f"""Logged In As {bot.user}\nID - {bot.user.id}
        Zoyx Here!
        logged In as {bot.user.name}
        Total servers ~ {len(bot.guilds)}
        Total Users ~ {len(bot.users)}
        Bot is online!
        \nPress Ctrl+C to exit""")
        
        # syncing slash commands
        self.tree.sync
        print(f"Slash commands are synced successfully for user {self.user.name} in {len(self.guilds)} servers!")
    
    # on ready event
    async def on_ready(self):
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
    
    # wavelink node ready
    async def on_wavelink_node_ready(self, payload: wavelink.NodeReadyEventPayload) -> None:
        logger.info(f"Wavelink Node connected: {payload.node!r} | Resumed: {payload.resumed}")

    async def on_wavelink_track_start(self, payload: wavelink.TrackStartEventPayload) -> None:
        player: wavelink.Player | None = payload.player
        if not player:
            # Handle edge cases...
            return

        original: wavelink.Playable | None = payload.original
        track: wavelink.Playable = payload.track

        embed: discord.Embed = discord.Embed(title="Now Playing")
        embed.description = f"**{track.title}** by `{track.author}`"

        if track.artwork:
            embed.set_image(url=track.artwork)

        if original and original.recommended:
            embed.description += f"\n\n`This track was recommended via {track.source}`"

        if track.album.name:
            embed.add_field(name="Album", value=track.album.name)

        await player.home.send(embed=embed)
        
        print(f"A track has started on {player.channel.name} in guild {player.guild.name} and track name is {track}")

# bot variable
if __name__ == "__main__":
    bot = CustomBot(
        command_prefix="!", intents=discord.Intents.all()
    )

    # logging in with token
    bot.run(config.DISCORD_TOKEN, root_logger=True)

    # clearing the screen and proceeding
    os.system('cls' if os.name == 'nt' else 'clear')
    # printing sigint receiving
    print("Received SIGINT (Ctrl+C), exiting...")
    time.sleep(2.5)
    # signal input
    signal.signal(signal.SIGINT, lambda sig, frame: print("Received SIGINT (Ctrl+C), exiting...") or bot.close())

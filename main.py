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
exts = ["commands.moderation", "commands.music"]#, "handlers.error_handler"]

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
 
        # syncing slash commands
        self.tree.sync
        print("Slash commands are synced successfully!")
        
        # connecting wavelink
        print("connecting wavelink...")
        time.sleep(0.1)
        print("connecting wavelink..")
        nodes = [wavelink.Node(uri="http://13.201.64.18:2333", password="Doom129")] # decalring nodes variable
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
    
    # on ready event
    async def on_ready(self):
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")

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

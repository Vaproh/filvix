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
import json
import jishaku

# cogs
exts = ["commands.moderation", "commands.music", "commands.utility", "commands.admin", "jishaku", "handlers.error_handler", "handlers.music_handler"]

# logger
logger = config.logging.getLogger("bot")

# jishaku envirment variables
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_FORCE_PAGINATOR"] = "True"

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
        nodes = [wavelink.Node(uri="http://lavalink.vaproh.cloud:2333", password="Doom129", inactive_player_timeout= 300)] # decalring nodes variable
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

async def prefix(self, message: discord.Message):
    return commands.when_mentioned_or('!')(self,message)

# bot variable
if __name__ == "__main__":
    bot = CustomBot(
        command_prefix=prefix, intents=discord.Intents.all()
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

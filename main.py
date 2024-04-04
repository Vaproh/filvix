# importing discord modules
from venv import logger
import discord
from discord.ext import commands # importing commands module from discord.ext

# importing utility modules
import time
import config
import signal
import os
import logging

# cogs
exts = ["commands.moderation", "handlers.error_handler"]

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

    # on ready event

    async def on_connect(self):
        # intro
        print(f"""Logged In As {bot.user}\nID - {bot.user.id}
        Zoyx Here!
        logged In as {bot.user.name}
        Total servers ~ {len(bot.guilds)}
        Total Users ~ {len(bot.users)}
        Bot is online!
        \n\nPress Ctrl+C to exit
        \n\nLogs:""")

# bot variable
if __name__ == "__main__":
    bot = CustomBot(
        command_prefix="!", intents=discord.Intents.all()
    )

    # logging in with token
    bot.run(config.token)
    # adding a signal handler to handle SIGINT (Ctrl+C)
    print("""\n\n\n\n\n
    Answer in yes or no""")
    keep_logs = str(input("Do you want to clear the screen?: "))
    if keep_logs == "yes" or "y" or "Y" or "Yes" or "YES":
        # clearing the screen and proceeding
        os.system('cls' if os.name == 'nt' else 'clear')
    elif keep_logs == "no" or "n" or "N" or "No" or "NO":
        # pass
        pass
    print("Received SIGINT (Ctrl+C), exiting...")
    time.sleep(2.5)
    signal.signal(signal.SIGINT, lambda sig, frame: print("Received SIGINT (Ctrl+C), exiting...") or bot.close())

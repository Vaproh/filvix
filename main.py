# importing discord modules
import discord
from discord.ext import commands # importing commands module from discord.ext

# importing utility modules
import time
import config

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

    async def on_ready(self):
        # intro
        print(f"Logged In As {bot.user}\nID - {bot.user.id}")
        print("Zoyx Here!")
        print(f"logged In as {bot.user.name}")
        print(f"Total servers ~ {len(bot.guilds)}")
        print(f"Total Users ~ {len(bot.users)}")


# bot variable
if __name__ == "__main__":
    bot = CustomBot(
        command_prefix="!", intents=discord.Intents.all()
    )

    # logging in with token
    bot.run(config.token)
    print("Bot is online!")
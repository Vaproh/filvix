# importing discord modules
import discord
from discord.ext import commands # importing commands module from discord.ext

# importing utility modules
import time
import config


# bot subclass
class CustomBot(commands.Bot):
    def __init__(self, command_prefix: str, intents: discord.Intents, *args, **kwargs) -> None:
        # Forward all arguments, and keyword-only arguments to commands.Bot
        super().__init__(command_prefix, intents=intents, *args, **kwargs)

    # Here you are overriding the default start method and write your own code.
    async def setup_hook(self) -> None:
        await bot.load_extension("commands.moderation") # moderation module load
        print("Loaded Moderation module")
        time.sleep(0.5)
        # await bot.load_extension("commands.general") #general module load
        # print("Loaded General module")
        # time.sleep(0.5)
        print("Registering Slash Commands")
        await bot.tree.sync() # register slash commands
        print("Registered all Slash Commands")

    async def on_ready(self):
        # into
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

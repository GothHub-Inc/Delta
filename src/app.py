from discord.ext import commands
from dotenv import load_dotenv
import discord
import os

load_dotenv()


class Client(commands.Bot):
    def __init__(self):
        super().__init__(
            intents=discord.Intents.all(),
            debug_guilds=[1033025456242434089],
            owner_id=266286800950132736,
            help_command=commands.DefaultHelpCommand()
        )
        self.__load_extensions()

    def __load_extensions(self):
        for file in os.listdir('./src/extensions'):
            if file.endswith('.py'):
                self.load_extension(f"extensions.{file[:-3]}")

    async def close(self):
        await super().close()

    async def on_ready(self):
        await self.wait_until_ready()
        print(f"Logged in as {self.user.name}")

    async def on_connect(self):
        await self.sync_commands()


client = Client()
client.run(os.getenv("DELTA_DISCORD_TOKEN"))

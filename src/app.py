from discord.ext import commands
from dotenv import load_dotenv
import discord
import os

load_dotenv()


class Client(commands.Bot):
    def __init__(self):
        super().__init__(
            intents=discord.Intents.default(),
            debug_guilds=[1033025456242434089],
            owner_id=266286800950132736
        )

    async def close(self):
        await super().close()

    async def on_ready(self):
        await self.wait_until_ready()
        print(f"Logged in as {self.user.name}")


def load_extensions(client):
    for file in os.listdir('./src/extensions'):
        if file.endswith('.py'):
            client.load_extension(f"extensions.{file[:-3]}")


client = Client()
load_extensions(client)
client.run(os.getenv("DELTA_DISCORD_TOKEN"))

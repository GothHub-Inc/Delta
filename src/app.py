from discord.ext import commands
import discord
import asyncio
import os

client = commands.Bot(command_prefix="$", intents=discord.Intents.default())


async def load_extensions():
    for file in os.listdir('./src/extensions'):
        if file.endswith('.py'):
            await client.load_extension(f"extensions.{file[:-3]}")


async def main():
    async with client:
        await load_extensions()
        await client.start("")


asyncio.run(main())

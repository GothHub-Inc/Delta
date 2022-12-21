from discord.ext import commands
import discord

client = commands.Bot(command_prefix="$", intents=discord.Intents.all())

client.run(token="")
from discord.ext import commands
import requests
import discord


class Cat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.base_url = 'https://cataas.com/'

    def __get_cat(self):
        res = requests.get(f"{self.base_url}cat?json=true")
        return f"{self.base_url}{res.json()['url']}"

    def __create_embed(self):
        embed = discord.Embed(
            colour=discord.Colour.fuchsia()
        )

        embed.set_image(url=self.__get_cat())

        return embed

    @commands.slash_command(
        guild_ids=[1033025456242434089],
        description="Get a random cat picture :D"
    )
    async def cat(
        self,
        ctx: discord.ApplicationContext
    ):
        await ctx.respond(embed=self.__create_embed())


def setup(bot):
    bot.add_cog(Cat(bot))

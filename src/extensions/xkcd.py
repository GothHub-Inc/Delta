from discord.ext import commands
import requests
import random
import discord

latest = None


class Xkcd(commands.Cog):
    def __init__(self, bot: commands.Bot):
        res = requests.get('https://xkcd.com/info.0.json')
        self.latest = res.json()["num"]
        self.bot = bot

        global latest
        latest = self.latest

    def __get_comic(self, id: int = None):
        if id is None:
            id = self.latest

        res = requests.get(f'https://xkcd.com/{id}/info.0.json')

        return {
            "id": res.json()["num"],
            "title": res.json()["title"],
            "desc": res.json()["alt"],
            "image": res.json()["img"]
            }

    def __get_random_id(self):
        return random.randint(1, self.latest)

    def __create_embed(self, xkcd: tuple):
        embed = discord.Embed(
            colour=discord.Colour.og_blurple(),
            title=xkcd["title"],
            url=f"http://xkcd.com/{xkcd['id']}/",
            description=xkcd["desc"]
        )

        embed.set_image(url=xkcd["image"])

        return embed

    @commands.slash_command(guild_ids=[1033025456242434089])
    @discord.option(
        "id",
        description="The ID of the xkcd comic",
        min_value=1,
        max_value=latest,
        default=None
    )
    @discord.option(
        "random",
        description="Get a random xkcd",
        default=False
    )
    async def xkcd(
        self,
        ctx: discord.ApplicationContext,
        id: int,
        random: bool
    ):
        if random:
            id = self.__get_random_id()

        await ctx.respond(
            embed=self.__create_embed(
                self.__get_comic(id)
                )
            )


def setup(bot):
    bot.add_cog(Xkcd(bot))

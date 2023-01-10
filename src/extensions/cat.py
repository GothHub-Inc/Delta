from discord.ext import commands
import requests
import discord


class CatView(discord.ui.View):
    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url

    def __create_options():
        options = []

        res = requests.get("http://cataas.com/api/tags")
        for tag in res.json():
            print(tag)
            while len(options) < 25:
                options.append(
                    discord.SelectOption(
                        label=tag,
                        value=tag
                    )
                )

        return options

    def __get_cat(self, tag):
        res = requests.get(f"{self.base_url}cat/{tag}?json=true")
        return f"{self.base_url}{res.json()['url']}"

    def __create_embed(self, tag):
        embed = discord.Embed(
            colour=discord.Colour.brand_green()
        )

        embed.set_image(url=self.__get_cat(tag))

        return embed

    @discord.ui.select(
        placeholder="Choose a tag!",
        min_values=1,
        max_values=1,
        options=__create_options()
    )
    async def select_callback(self, select, interaction):
        await interaction.response.send_message(
            embed=self.__create_embed(select.values[0])
        )


class Cat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.base_url = 'https://cataas.com/'

    @commands.slash_command(
        guild_ids=[1033025456242434089],
        description="Get a random cat picture based on a tag :D"
    )
    async def cat(
        self,
        ctx: discord.ApplicationContext
    ):
        await ctx.respond("Pick a tag!", view=CatView(self.base_url))


def setup(bot):
    bot.add_cog(Cat(bot))

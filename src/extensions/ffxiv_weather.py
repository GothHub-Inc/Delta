from discord.ext import commands
import discord

import datetime
import ffxivweather

list = ["Limsa Lominsa", "Middle La Noscea", "Lower La Noscea", 
    "Eastern La Noscea", "Western La Noscea", "Upper La Noscea", 
    "Outer La Noscea", "Mist"]


class FFXIVWeather(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    def __create_embed(self, zone, amount: int = 15):
        try:
            forecast = ffxivweather.forecaster.get_forecast(
                place_name=zone,
                count=amount
            )
        except Exception:
            failEmbed = discord.Embed(
                title="FFXIV weather forecast",
                description=f"Location {zone} could not be found.",
            )
            return failEmbed

        embed = discord.Embed(
            title="FFXIV weather forecast",
            description=f"Forecast of the upcomming weather in {zone}",
            color=discord.Colour.blue(),
        )
        weathers = ""
        times = ""
        for weather, start_time in forecast:
            weathers += weather["name_en"]+"\n"
            times += str(
                datetime.datetime.time(start_time).strftime("%H:%M"))+"\n"
        embed.add_field(
            name="Weather",
            value=weathers,
            inline=True
        )
        embed.add_field(
            name="Time",
            value=times,
            inline=True
        )
        return embed

    @commands.slash_command(
        guild_ids=[1033025456242434089],
        description="Get the weather forecast of any place in FFXIV"
    )
    async def ffxivweather(
        self,
        ctx: discord.ApplicationContext,
        zone: discord.Option(
                str, autocomplete=discord.utils.basic_autocomplete(list)
            )
    ):
        await ctx.respond(embed=self.__create_embed(zone, 5))


def setup(bot):
    bot.add_cog(FFXIVWeather(bot))

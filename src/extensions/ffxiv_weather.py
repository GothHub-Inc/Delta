from discord.ext import commands
import discord
import datetime

import ffxivweather


class FFXIVWeather(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    def __create_embed(self, zone, amout=15):
        try:
            forecast = ffxivweather.forecaster.get_forcast(
                place_name=zone,
                count=amout
            )
        except Exception:
            failEmbed = discord.Embed(
                title="FFXIV weather forcaster",
                description=f"Location {zone} could not be found.",
            )
            return failEmbed

        embed = discord.Embed(
            title="FFXIV weather forecast",
            description=f"Forecast of the upcomming weather in {zone}",
            color=discord.Colour.blue,
        )
        weathers = ""
        times = ""
        for weather, start_time in forecast:
            weathers += weather+"\n"
            times += datetime.datetime.time(start_time)+"\n"
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
        guild_ids=[1066721914632032266],
        description="Get the weather forecast of any place in FFXIV"   
    )
    async def ffxivweather(
        self,
        ctx: discord.ApplicationContext,
    ):
        await ctx.respond(embed=self.__create_embed("Eureka Pyros"))


def setup(bot):
    bot.add_cog(FFXIVWeather(bot))

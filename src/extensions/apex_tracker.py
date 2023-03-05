from apex_legends import ApexLegends
from discord.ext import commands
import discord
import os

stats = ["kills", "wins", "damage"]
legends = ["Bangalore", "Revenant", "Fuse", "Ash", "Mad Maggie", "Pathfinder",
           "Wraith", "Mirage", "Octane", "Horizon", "Valkyrie", "BloodHound",
           "Crypto", "Seer", "Vantage", "Gibraltar", "Lifeline", "Loba",
           "Newcastle", "Caustic", "Wattson", "Rampart", "Catalyst"]


class ApexTracker(commands.Cog):
    def __init__(self, bot):
        self.client = bot
        self.apex = ApexLegends(os.getenv("APEX_API_KEY"))

    @commands.slash_command(
        guild_ids=[1033025456242434089],
        description="Get legend information from a specific player"
    )
    async def apextracker(
        self,
        ctx: discord.ApplicationContext,
        player_name: str,
        legend_name: discord.Option(
            str, autocomplete=discord.utils.basic_autocomplete(legends)
        )
    ):
        try:
            player = self.apex.player(player_name)
        except Exception:
            await ctx.respond(embed=self.__create_failed_embed(player_name))
        await ctx.respond(embed=self.__create_embed(player, legend_name))

    def __create_failed_embed(self, case: str):
        embed = discord.Embed(
            title="Apex tracker",
            description=f"{case} could not be found",
            color=discord.Colour.from_rgb(218, 38, 42)
        )
        return embed

    def __create_embed(
            self,
            player,
            legend_name
    ):
        for legend in player.legends:
            if legend.legend_name == legend_name:
                embed = discord.Embed(
                    title="Apex tracker",
                    description=f"Tracked stats from {player.username} as {legend.legend_name}",
                    color=discord.Colour.from_rgb(218, 38, 42)
                )
                embed.set_image(url=legend.icon)
                for stat in stats:
                    embed.add_field(
                        name=stat,
                        value=str(getattr(legend, stat, "could not be found")),
                        inline=False
                        )
                return embed
        return self.__create_failed_embed(f"{player.username}'s {legend_name}")


def setup(bot):
    bot.add_cog(ApexTracker(bot))

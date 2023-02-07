from discord.ext import commands
import discord


class Notifs(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    def __get_log_channel(self, guild: discord.Guild):
        return guild.get_channel(1033025457181954070)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.__get_log_channel(member.guild)
        if channel is not None:
            await channel.send(
                embed=discord.Embed(
                    title=f'{member.display_name} joined the server!',
                    colour=discord.Colour.blue()
                )
            )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.__get_log_channel(member.guild)
        if channel is not None:
            await channel.send(
                embed=discord.Embed(
                    title=f'{member.display_name} left the server!',
                    colour=discord.Colour.red()
                )
            )


def setup(bot):
    bot.add_cog(Notifs(bot))

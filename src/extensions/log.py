from discord.ext import commands
import discord


class Log(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot

    def __get_log_channel(self, guild: discord.Guild):
        return guild.get_channel(1066721914632032266)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        channel = self.__get_log_channel(message.guild)
        author = message.author

        await channel.send(embed=discord.Embed(
            title=f"Message deleted by {author.display_name}",
            description=message.content,
            colour=discord.Colour.red()
        ))

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message,
                              after: discord.Message):
        channel = self.__get_log_channel(before.guild)
        author = before.author

        embed = discord.Embed(
            title=f"Message edited by {author.display_name}",
            colour=discord.Colour.green()
        )

        embed.add_field(name="Before", value=before.content)
        embed.add_field(name="After", value=after.content)

        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Log(bot))

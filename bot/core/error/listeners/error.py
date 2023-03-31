from nextcord.ext import commands


class ErrorHandling(commands.Cog):
    def __init__(self, bot: commands):
        self.bot = bot

    @commands.Cog.listener()
    async def on_error(self, event: str, *args, **kwargs):
        print(event)


def setup(bot):
    bot.add_cog(ErrorHandling(bot))

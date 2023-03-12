import nextcord
from nextcord.ext import commands
from src.templates import embeds


class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(
        name="b-ping",
        description="Zeigt den Ping des Bots an.",
        force_global=True
    )
    async def ping(
            self,
            ctx: nextcord.Interaction
    ) -> None:

        """
        Attributes
        ----------
        :param ctx: Gives the interaction to discord
        :return: None
        ----------
        """

        embed_ping = embeds.EmbedNormal(
            bot=self.bot,
            ctx=ctx,
            description="Zeigt den Ping des Bots.",
            color=nextcord.Color.green()
        )
        embed_ping.add_field(
            name="Ping",
            value=f"**{round(self.bot.latency * 100)}ms**"
        )
        await ctx.send(embed=embed_ping, ephemeral=True)


def setup(bot):
    bot.add_cog(Ping(bot))

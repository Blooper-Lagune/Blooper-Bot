import nextcord
from nextcord.ext import commands
from src.templates import embeds, buttons


class TicketSetup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(
        name="ticket-setup",
        description="Richte das Ticket System ein.",
        force_global=True,
        default_member_permissions=8
    )
    async def ticket_setup(
            self,
            ctx: nextcord.Interaction,
    ) -> None:

        """
        Attributes
        ----------
        :param ctx: Gives the interaction to discord
        :return: None
        ----------
        """

        embed_ticket_setup = embeds.EmbedNormal(
            bot=self.bot,
            ctx=ctx,
            description="Du möchtest ein Ticket Erstellen? Bitte klicke auf den Button.",
            color=nextcord.Color.orange()
        )

        button_setup = buttons.ButtonTicket()

        await ctx.send(embed=embed_ticket_setup, view=button_setup)


def setup(bot):
    bot.add_cog(TicketSetup(bot))

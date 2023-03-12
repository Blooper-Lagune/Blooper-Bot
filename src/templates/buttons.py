import nextcord
from nextcord import Message


class ButtonTicket(nextcord.ui.View):
    def __init__(self):
        super().__init__()

    @nextcord.ui.button(label="Ticket Erstellen", style=nextcord.ButtonStyle.green)
    async def button(
            self,
            button: nextcord.Button,
            ctx: nextcord.Interaction
    ) -> Message:

        """
        Attributes
        ----------
        :param button:
        :param ctx:
        :return: None
        ----------
        """

        # get the ticket category
        ticket_category = nextcord.utils.get(ctx.guild.categories, name="Blooper Support")

        if ticket_category is None:
            ticket_category = await ctx.guild.create_category(name="Blooper Support")

        if len(ticket_category.channels) >= 50:
            return await ctx.user.send("Momentan sind zu viele Tickets. Bitte versuche es später erneut.")

        ticket_check = nextcord.utils.get(ticket_category.channels, name=f"ticket-{str(ctx.user.name).lower()}")
        if ticket_check is not None:
            return await ctx.user.send("Du hast bereits ein aktives Ticket.")

        ticket_channel = await ctx.guild.create_text_channel(name=f"ticket-{ctx.user.name}", category=ticket_category)
        await ticket_channel.set_permissions(target=ctx.guild.default_role, view_channel=False)
        await ticket_channel.set_permissions(target=ctx.user, view_channel=True)

        await ticket_channel.send(f"{ctx.user.mention}, wie können wir dir helfen?")

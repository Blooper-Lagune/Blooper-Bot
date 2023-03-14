import nextcord
from nextcord import Message
from nextcord.ext import commands
from src.templates import embeds, buttons
from src.loader.jsonLoader import Ticket


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

        text = Ticket().get_ticket()
        embed_image = embeds.EmbedNormal(
            bot=self.bot,
            ctx=ctx,
            description="",
            color=nextcord.Color.from_rgb(r=255, g=50, b=53)
        )
        embed_image.title = ""
        embed_image.remove_footer()
        embed_image.remove_author()
        embed_image.set_image(url="https://cdn-longterm.mee6.xyz/plugins/embeds/images/728633438441046016/8c8351db671e7144e035158890a4acb800974b1e8378a144efc87292db275668.png")
        embed_image.set_thumbnail(url="")

        embed_rules = embeds.EmbedNormal(
            bot=self.bot,
            ctx=ctx,
            description=text["main"],
            color=nextcord.Color.from_rgb(r=255, g=50, b=53)
        )
        embed_rules.add_field(
            name=":faq: 〣Stelle eine Frage...",
            value=text["block_one"],
            inline=False
        )
        embed_rules.add_field(
            name=":warning~1: 〣Bugs, Probleme o.Ä. melden...",
            value=text["block_two"],
            inline=False
        )
        embed_rules.add_field(
            name=":banhammer: 〣Melde einen Nutzer...",
            value=text["block_three"],
            inline=False
        )
        embed_rules.add_field(
            name=":support: 〣Verbesserungsvorschläge...",
            value=text["block_four"],
            inline=False
        )
        embed_rules.title = ":support: Support-Bereich der Blooper Lagune"
        embed_rules.remove_footer()
        embed_rules.remove_author()
        embed_rules.set_thumbnail(url="")

        button_setup = ButtonTicket(
            bot=self.bot
        )

        await ctx.send(embeds=[embed_image, embed_rules], view=button_setup)


class ButtonTicket(nextcord.ui.View):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    @nextcord.ui.button(label="Ticket erstellen", style=nextcord.ButtonStyle.green)
    async def button(
            self,
            button: nextcord.Button,
            ctx: nextcord.Interaction
    ) -> Message:

        """
        Attributes
        ----------
        :param button:
        :param ctx: Gives the interaction to discord
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

        ticket_channel = await ctx.guild.create_text_channel(name=f"ticket-{ctx.user.name}",
                                                             category=ticket_category)
        await ticket_channel.set_permissions(target=ctx.guild.default_role, view_channel=False)
        await ticket_channel.set_permissions(target=ctx.user, view_channel=True)

        await ticket_channel.send(f"{ctx.user.mention} Willkommen im Support Bereich der Blooper Lagune! :envelope_with_arrow:")
        embed_close = embeds.EmbedNormal(
            bot=self.bot,
            ctx=ctx,
            description="Du hast erfolgreich ein Ticket eröffnet :white_check_mark:",
            color=nextcord.Color.green()
        )
        embed_close.add_field(
            name="",
            value="Jemand aus dem Supporter-Team wird sich in kürze bei dir melden und sich um dein Anliegen kümmern. :alarm_clock:",
            inline=False
        )
        embed_close.remove_author()
        embed_close.remove_footer()
        embed_close.set_thumbnail(url="")
        embed_close.title = ""

        delete_button = TicketDelete(
            bot=self.bot,
            ticket=ticket_channel
        )

        await ticket_channel.send(embed=embed_close, view=delete_button)


class TicketDelete(nextcord.ui.View):
    def __init__(self, bot: commands.Bot, ticket: nextcord.TextChannel):
        self.bot = bot
        self.ticket_channel = ticket
        super().__init__()

    @nextcord.ui.button(label=f"Ticket schließen", style=nextcord.ButtonStyle.red)
    async def button_log(
            self,
            button: nextcord.Button,
            ctx: nextcord.Interaction
    ) -> None:

        """
        Attributes
        ----------
        :param button:
        :param ctx: Gives the interaction to discord
        :return: None
        ----------
        """

        await self.ticket_channel.set_permissions(target=ctx.user, view_channel=False)

        embed_close = embeds.EmbedNormal(
            bot=self.bot,
            ctx=ctx,
            description=f"{ctx.user.mention} hat das Ticket geschlossen. Wie soll es nun weiter gehen?",
            color=nextcord.Color.yellow()
        )
        embed_close.remove_footer()
        embed_close.remove_author()
        embed_close.title = ""
        embed_close.set_thumbnail(url="")

        button_menu = buttons.TicketCloseMenu(
            bot=self.bot,
            ctx=ctx,
            ticket=self.ticket_channel
        )
        await ctx.send(embed=embed_close, view=button_menu)


def setup(bot):
    bot.add_cog(TicketSetup(bot))

import nextcord
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
            color=nextcord.Color.red()
        )
        embed_image.title = ""
        embed_image.set_footer(text="")
        embed_image.set_author(name="")
        embed_image.set_image(url="https://cdn-longterm.mee6.xyz/plugins/embeds/images/728633438441046016/8c8351db671e7144e035158890a4acb800974b1e8378a144efc87292db275668.png")

        embed_rules = embeds.EmbedNormal(
            bot=self.bot,
            ctx=ctx,
            description=text["main"],
            color=nextcord.Color.dark_red()
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
        embed_rules.set_author(name="")
        embed_rules.title = ":support: Support-Bereich der Blooper Lagune"
        embed_rules.set_footer(text="")

        embed_ticket_setup = embeds.EmbedNormal(
            bot=self.bot,
            ctx=ctx,
            description="Du möchtest ein Ticket Erstellen? Bitte klicke auf den Button.",
            color=nextcord.Color.dark_red()
        )
        embed_ticket_setup.set_author(name="")
        embed_ticket_setup.title = ""
        embed_ticket_setup.set_footer(text="")

        button_setup = buttons.ButtonTicket()
        await ctx.send(embeds=[embed_image, embed_rules, embed_ticket_setup], view=button_setup)
        # ff3235


def setup(bot):
    bot.add_cog(TicketSetup(bot))

import nextcord
from nextcord.ext import commands
import os
from nextcord import Message
from src.templates import embeds


class TicketLogs(nextcord.ui.View):
    def __init__(self):
        super().__init__()

    @nextcord.ui.button(label="Dokument speichern", style=nextcord.ButtonStyle.gray)
    async def button_log(
            self,
            button: nextcord.Button,
            ctx: nextcord.Interaction
    ) -> None:
        pass


class TicketCloseMenu(nextcord.ui.View):
    def __init__(self, bot: commands.Bot, ctx: nextcord.Interaction, ticket: nextcord.TextChannel):
        super().__init__()
        self.bot = bot
        self.ctx = ctx
        self.ticket = ticket

        async def log_callback(ctx: nextcord.Interaction):
            ticket_category = nextcord.utils.get(ctx.guild.categories, name="Blooper Support")
            log_channel = nextcord.utils.get(ticket_category.channels, name="logs")

            if log_channel is None:
                await ctx.guild.create_text_channel(name="logs", category=ticket_category)
                await ticket_category.set_permissions(target=ctx.guild.default_role, view_channel=False)

            messages = await ctx.channel.history(limit=10000).flatten()
            files = [file for file in os.listdir("resources/logs")]

            with open(f"resources/logs/log-{len(files) + 1}.txt", "a") as f:
                for msg in messages:
                    f.write(f"{msg.author}: {msg.content}\n")
                f.close()

            await log_channel.send(
                f"Logs von ticket: {ctx.channel.name}",
                file=nextcord.File(fp=f"resources/logs/log-{len(files) + 1}.txt")
            )

            os.remove(f"resources/logs/log-{len(files) + 1}.txt")

        self.button_log = nextcord.ui.Button(
            label="Dokument speichern",
            style=nextcord.ButtonStyle.gray
        )
        self.button_log.callback = log_callback

        async def callback_reopen(ctx: nextcord.Interaction):
            print("Reopen")

        self.button_reopen = nextcord.ui.Button(
            label="Ticket wieder eröffnen",
            style=nextcord.ButtonStyle.green
        )
        self.button_reopen.callback = callback_reopen

        async def callback_delete(ctx: nextcord.Interaction):
            await ctx.channel.delete()

        self.button_delete = nextcord.ui.Button(
            label="Ticket löschen",
            style=nextcord.ButtonStyle.red
        )
        self.button_delete.callback = callback_delete

        self.add_item(self.button_log)
        self.add_item(self.button_reopen)
        self.add_item(self.button_delete)

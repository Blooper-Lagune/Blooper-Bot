import nextcord
from nextcord.ext import commands
from database.query import Query
from src.templates.embeds import EmbedMessage


class Logs(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = Query(
            pool_name="logs",
            pool_size=9
        )

    async def get_channel(
            self,
            message: nextcord.Message
    ) -> None | nextcord.TextChannel:

        channel = self.database.execute(
            query="SELECT channel FROM log_channel",
            data=[]
        )

        if not channel or message.author.bot:
            return

        return nextcord.utils.get(
            message.guild.channels,
            id=channel[0][0]
        )

    @commands.Cog.listener()
    async def on_message(
            self,
            message: nextcord.Message
    ) -> None:

        channel: nextcord.TextChannel = await self.get_channel(message=message)

        if not channel:
            return

        embed_logs = EmbedMessage(
            message=message,
            bot=self.bot,
            color=nextcord.Color.orange(),
            description=""
        )

        embed_logs.title = "Neuer Log"
        embed_logs.add_field(
            name=f"Neue Nachricht in {message.channel.mention}",
            value=message.content
        )

        await channel.send(embed=embed_logs)

    @commands.Cog.listener()
    async def on_message_edit(
            self,
            before: nextcord.Message,
            after: nextcord.Message
    ) -> None:

        channel: nextcord.TextChannel = await self.get_channel(message=after)

        if not channel:
            return

        embed_logs = EmbedMessage(
            message=after,
            bot=self.bot,
            color=nextcord.Color.orange(),
            description=""
        )

        embed_logs.title = "Neuer Log"
        embed_logs.add_field(
            name=f"Nachricht bearbeitet in {before.channel.mention} von:",
            value=before.content, inline=False)
        embed_logs.add_field(
            name="Zu:",
            value=after.content
        )

        await channel.send(embed=embed_logs)

    @commands.Cog.listener()
    async def on_message_delete(
            self,
            message: nextcord.Message
    ) -> None:

        channel: nextcord.TextChannel = await self.get_channel(message=message)

        if not channel:
            return

        embed_logs = EmbedMessage(
            message=message,
            bot=self.bot,
            color=nextcord.Color.orange(),
            description=""
        )

        embed_logs.title = "Neuer Log"
        embed_logs.add_field(
            name=f"Nachricht gelöscht in {message.channel.mention}:",
            value=message.content,
            inline=False
        )

        await channel.send(embed=embed_logs)


def setup(bot):
    bot.add_cog(Logs(bot))

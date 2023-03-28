import nextcord
from nextcord.ext import commands
from database.query import Query


class SetSupportChannel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = Query(
            pool_name="set-support-channel",
            pool_size=1
        )

    @nextcord.slash_command(
        name="set-support-channel",
        description="Lege einen Support channel fest.",
        force_global=True,
        default_member_permissions=8
    )
    async def set_ticket_channel(self, ctx: nextcord.Interaction):
        channel = self.database.execute(
            query="SELECT * From ticket_channel",
            data=[]
        )
        if not channel:
            self.database.execute(
                query="INSERT INTO ticket_channel (channel) VALUE (%s)",
                data=[int(ctx.guild.id)]
            )
            return await ctx.send(f"Neuer Support channel: **{ctx.channel.name}**", ephemeral=True)

        self.database.execute(
            query=f"UPDATE ticket_channel SET channel={int(ctx.channel_id)}",
            data=[]
        )
        await ctx.send(f"Neuer Support channel: **{ctx.channel.name}**", ephemeral=True)


def setup(bot):
    bot.add_cog(SetSupportChannel(bot))

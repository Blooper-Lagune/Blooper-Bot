import nextcord
from nextcord.ext import commands
from database.query import Query


class SetWelcomeChannel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = Query(
            pool_name="set-welcome-channel",
            pool_size=1
        )

    @nextcord.slash_command(
        name="set-welcome-channel",
        description="Lege einen Welcome channel fest.",
        force_global=True,
        default_member_permissions=8
    )
    async def set_welcome_messages(self, ctx: nextcord.Interaction):
        channel = self.database.execute(
            query="SELECT * From welcome_messages",
            data=[]
        )
        if not channel:
            self.database.execute(
                query="INSERT INTO welcome_messages (channel) VALUE (%s)",
                data=[int(ctx.guild.id)]
            )
            return await ctx.send(f"Neuer Welcome channel: **{ctx.channel.name}**", ephemeral=True)

        self.database.execute(
            query=f"UPDATE welcome_messages SET channel={int(ctx.channel_id)}",
            data=[]
        )
        await ctx.send(f"Neuer Welcome channel: **{ctx.channel.name}**", ephemeral=True)


def setup(bot):
    bot.add_cog(SetWelcomeChannel(bot))

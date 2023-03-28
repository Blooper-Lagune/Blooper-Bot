import nextcord
from nextcord.ext import commands
from database.query import Query


class SetReactionRoleChannel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = Query(
            pool_name="set-reaction-roles-channel",
            pool_size=1
        )

    @nextcord.slash_command(
        name="set-reaction-roles-channel",
        description="Lege einen Reaction Roles channel fest.",
        force_global=True,
        default_member_permissions=8
    )
    async def set_reaction_roles(self, ctx: nextcord.Interaction):
        channel = self.database.execute(
            query="SELECT * From reaction_roles",
            data=[]
        )
        if not channel:
            self.database.execute(
                query="INSERT INTO reaction_roles (channel) VALUE (%s)",
                data=[int(ctx.guild.id)]
            )
            return await ctx.send(f"Neuer Reaction Role channel: **{ctx.channel.name}**", ephemeral=True)

        self.database.execute(
            query=f"UPDATE reaction_roles SET channel={int(ctx.channel_id)}",
            data=[]
        )
        await ctx.send(f"Neuer Reaction Role channel: **{ctx.channel.name}**", ephemeral=True)


def setup(bot):
    bot.add_cog(SetReactionRoleChannel(bot))

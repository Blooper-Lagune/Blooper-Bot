import nextcord
from nextcord.ext import commands
from database.query import Query


class SetSocialMediaChannel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = Query(
            pool_name="set-social-media-channel",
            pool_size=1
        )

    @nextcord.slash_command(
        name="set-social-media-channel",
        description="Lege einen social media channel fest.",
        force_global=True,
        default_member_permissions=8
    )
    async def set_social_media_alerts(self, ctx: nextcord.Interaction):
        channel = self.database.execute(
            query="SELECT * From social_media_alerts",
            data=[]
        )
        if not channel:
            self.database.execute(
                query="INSERT INTO social_media_alerts (channel) VALUE (%s)",
                data=[int(ctx.guild.id)]
            )
            return await ctx.send(f"Neuer Social Media channel: **{ctx.channel.name}**", ephemeral=True)

        self.database.execute(
            query=f"UPDATE social_media_alerts SET channel={int(ctx.channel_id)}",
            data=[]
        )
        await ctx.send(f"Neuer Social Media channel: **{ctx.channel.name}**", ephemeral=True)


def setup(bot):
    bot.add_cog(SetSocialMediaChannel(bot))

import nextcord
from nextcord.ext import commands
from database.query import Query


class VoiceManager(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = Query(
            pool_name="voice_manager",
            pool_size=4
        )

    @commands.Cog.listener()
    async def on_voice_state_update(
            self,
            member:
            nextcord.Member,
            before: nextcord.VoiceState,
            after: nextcord.VoiceState
    ) -> None:

        """
        Attributes
        ----------
        :param member: 
        :param before: 
        :param after: 
        :return: None
        ----------
        """

        category = nextcord.utils.get(member.guild.categories, name="🔊 Sprachkanäle 🔊")

        if category is None:
            return

        if str(after.channel) == "Create Voice" and len(category.channels) <= 48:
            channel = await member.guild.create_voice_channel(name=f"{member.name}-VC", category=category)

            self.database.execute(
                query="INSERT INTO active_voice_channel (channel_id, member_id) VALUE (%s,%s)",
                data=[int(channel.id), int(member.id)]
            )

            await member.move_to(channel=channel)

        if before.channel in category.channels and str(before.channel) != "Create Voice" and len(before.channel.members) == 0:

            self.database.execute(
                query="DELETE FROM active_voice_channel WHERE channel_id=%s",
                data=[int(before.channel.id)]
            )

            channel = self.bot.get_channel(before.channel.id)
            await channel.delete()


def setup(bot):
    bot.add_cog(VoiceManager(bot))

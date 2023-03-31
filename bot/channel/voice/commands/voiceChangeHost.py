import nextcord
from nextcord.ext import commands
from src.handler.voiceHandler import VoiceHandler
from database.query import Query


class VoiceChangeHost(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = Query(
            pool_name="voice_change_host",
            pool_size=3
        )

    @nextcord.slash_command(
        name="voice-change-host",
        description="Ändere den Owner des Channels",
        force_global=True
    )
    async def voice_change_host(self, ctx: nextcord.Interaction, user: nextcord.Member):
        if ctx.user.voice is None or user.voice is None:
            return await ctx.send("Ihr müsst beide im selben Talk sein, um den Host zu wechseln.", ephemeral=True)

        if not await VoiceHandler().check_permissions(ctx=ctx, voice=ctx.user.voice.channel):
            return await ctx.send("Du hast keine Rechte um das zu tun.", ephemeral=True)

        channel = ctx.user.voice.channel
        self.database.execute(
            query=f"UPDATE active_voice_channel SET member_id={user.id} WHERE channel_id={channel.id}",
            data=[]
        )
        await ctx.send(f"Der Host wurde gewechselt zu **{user.name}**", ephemeral=True)


def setup(bot):
    bot.add_cog(VoiceChangeHost(bot))

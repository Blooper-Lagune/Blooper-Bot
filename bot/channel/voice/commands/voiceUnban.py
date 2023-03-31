import nextcord
from nextcord.ext import commands
from src.handler.voiceHandler import VoiceHandler


class VoiceUnban(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(
        name="voice-unban",
        description="Entbanne einen User von deinen Voice channel.",
        force_global=True
    )
    async def voice_unban(self, ctx: nextcord.Interaction, user: nextcord.Member):
        if ctx.user.voice is None:
            return await ctx.send("Du bist in keinem Voice channel.")

        if not await VoiceHandler().check_permissions(ctx=ctx, voice=ctx.user.voice.channel):
            return await ctx.send("Du hast keine Rechte um das zu tun.")

        channel = ctx.user.voice.channel

        await channel.set_permissions(target=user, view_channel=True)
        await ctx.send(f"Der User **{user.name}** wurde vom channel gebannt.")


def setup(bot):
    bot.add_cog(VoiceUnban(bot))

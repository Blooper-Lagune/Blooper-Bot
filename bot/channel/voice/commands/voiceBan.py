import nextcord
from nextcord.ext import commands
from src.handler.voiceHandler import VoiceHandler


class VoiceBan(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(
        name="voice-ban",
        description="Banne einen User von deinen Voice channel.",
        force_global=True
    )
    async def voice_ban(self, ctx: nextcord.Interaction, user: nextcord.Member):
        if ctx.user.voice is None:
            return await ctx.send("Du bist in keinem Voice channel.")

        if not await VoiceHandler().check_permissions(ctx=ctx, voice=ctx.user.voice.channel):
            return await ctx.send("Du hast keine Rechte um das zu tun.", ephemeral=True)

        channel = ctx.user.voice.channel

        if user.voice is not None:
            if channel == user.voice.channel:
                await user.disconnect()

        await channel.set_permissions(target=user, view_channel=False)
        await ctx.send(f"Der User **{user.name}** wurde vom channel gebannt.", ephemeral=True)


def setup(bot):
    bot.add_cog(VoiceBan(bot))

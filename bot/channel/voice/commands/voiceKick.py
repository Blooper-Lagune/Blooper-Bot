import nextcord
from nextcord.ext import commands
from src.handler.voiceHandler import VoiceHandler


class VoiceKick(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(
        name="voice-kick",
        description="Kicke einen user aus deinem Voice",
        force_global=True
    )
    async def voice_kick(self, ctx: nextcord.Interaction, user: nextcord.Member):
        if ctx.user.voice is None:
            return await ctx.send("Du bist in keinem Voice channel.", ephemeral=True)

        if not await VoiceHandler().check_permissions(ctx=ctx, voice=ctx.user.voice.channel):
            return await ctx.send("Du hast keine Rechte um das zu tun.", ephemeral=True)

        channel = ctx.user.voice.channel

        if user.voice is not None:
            if channel == user.voice.channel:
                await user.disconnect()

        await ctx.send(f"Der User **{user.name}** wurde gekickt.", ephemeral=True)


def setup(bot):
    bot.add_cog(VoiceKick(bot))

import nextcord
from nextcord.ext import commands
from src.handler.voiceHandler import VoiceHandler


class VoiceChangeName(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(
        name="voice-change-name",
        description="Ändere den Namen von deinem voice Channel.",
        force_global=True
    )
    async def voice_change_name(self, ctx: nextcord.Interaction, name: str):
        if ctx.user.voice is None:
            return await ctx.send("Du bist in keinem Voice channel.", ephemeral=True)

        if not await VoiceHandler().check_permissions(ctx=ctx, voice=ctx.user.voice.channel):
            return await ctx.send("Du hast keine Rechte um das zu tun.", ephemeral=True)

        channel = ctx.user.voice.channel
        await channel.edit(name=f"{name}-VC")
        await ctx.send(f"Der Name wurde auf **{name}** gesetzt.", ephemeral=True)


def setup(bot):
    bot.add_cog(VoiceChangeName(bot))

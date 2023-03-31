import nextcord
from nextcord.ext import commands
from src.handler.voiceHandler import VoiceHandler


class VoiceLimit(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(
        name="voice-user-limit",
        description="Setze ein limit für deinen Voice channel.",
        force_global=True
    )
    async def voice_limit(self, ctx: nextcord.Interaction, limit: int):
        if ctx.user.voice is None:
            return await ctx.send("Du bist in keinem Voice channel.", ephemeral=True)

        if not await VoiceHandler().check_permissions(ctx=ctx, voice=ctx.user.voice.channel):
            return await ctx.send("Du hast keine Rechte um das zu tun.", ephemeral=True)

        if limit > 99 or limit < 0:
            return await ctx.send("Du kannst maximal ein Limit von 0 bis 99 setzten", ephemeral=True)

        channel = ctx.user.voice.channel
        await channel.edit(user_limit=limit)
        await ctx.send(f"Das User Limit wurde auf {limit} gesetzt.", ephemeral=True)


def setup(bot):
    bot.add_cog(VoiceLimit(bot))

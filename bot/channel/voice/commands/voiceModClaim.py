import nextcord
from nextcord.ext import commands
from database.query import Query


class VoiceModClaim(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = Query(
            pool_name="voice_mod_claim",
            pool_size=1
        )

    @nextcord.slash_command(
        name="voice-mod-claim",
        description="Claim einen Talk.",
        force_global=True,
        default_member_permissions=8
    )
    async def voice_change_name(self, ctx: nextcord.Interaction, voice: nextcord.VoiceChannel):
        category = nextcord.utils.get(ctx.guild.categories, name="🔊 Sprachkanäle 🔊")

        if category is None:
            return await ctx.send("Das Voice System ist momentan nicht aktiv.", ephemeral=True)

        if voice not in category.channels or voice.name.lower() == "create voice":
            return await ctx.send("Der ausgewählte channel befindet sich nicht in der Category **🔊 Sprachkanäle 🔊**", ephemeral=True)

        self.database.execute(
            query=f"UPDATE active_voice_channel SET member_id={ctx.user.id} WHERE channel_id={voice.id}",
            data=[]
        )
        await ctx.send("Voice claimed", ephemeral=True)


def setup(bot):
    bot.add_cog(VoiceModClaim(bot))

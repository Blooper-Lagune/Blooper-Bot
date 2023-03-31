import nextcord
from nextcord.ext import commands
from src.templates.embeds import EmbedNormal
from database.query import Query


class VoiceCurrentSettings(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = Query(
            pool_name="voice_current_settings",
            pool_size=2
        )

    @nextcord.slash_command(
        name="voice-current-settings",
        description="Zeigt die settings des Voices an.",
        force_global=True
    )
    async def voice_change_name(self, ctx: nextcord.Interaction, voice: nextcord.VoiceChannel):
        category = nextcord.utils.get(ctx.guild.categories, name="🔊 Sprachkanäle 🔊")

        if category is None:
            return await ctx.send("Das Voice System ist momentan nicht aktiv.", ephemeral=True)

        if voice not in category.channels:
            return await ctx.send("Der ausgewählte channel befindet sich nicht in der Category **🔊 Sprachkanäle 🔊**", ephemeral=True)

        current_host_id = self.database.execute(
            query="SELECT member_id FROM active_voice_channel WHERE channel_id=%s",
            data=[int(voice.id)]
        )
        current_host = self.bot.get_user(current_host_id[0][0])

        embed_voice_settings = EmbedNormal(
            bot=self.bot,
            ctx=ctx,
            color=nextcord.Color.green(),
            description="Zeigt die aktuellen Einstellungen des Voices."
        )

        embed_voice_settings.add_field(
            name="Aktueller Host",
            value=current_host,
            inline=False
        )
        embed_voice_settings.add_field(
            name="Verbundene User",
            value=('\n'.join(map(str, voice.members)))
        )
        embed_voice_settings.add_field(
            name="User limit",
            value=voice.user_limit,
            inline=True
        )
        embed_voice_settings.add_field(
            name="Voice erstellt",
            value=voice.created_at.strftime("%H:%M:%S")
        )

        await ctx.send(embed=embed_voice_settings, ephemeral=True)


def setup(bot):
    bot.add_cog(VoiceCurrentSettings(bot))

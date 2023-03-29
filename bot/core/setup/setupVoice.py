import nextcord
from nextcord.ext import commands


class SetupVoice(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(
        name="setup-voice",
        description="Reset oder erstelle das Voice system.",
        force_global=True,
        default_member_permissions=8
    )
    async def setup_voice(self, ctx: nextcord.Interaction) -> None:

        """
        Attributes
        ----------
        :param ctx: Give the interaction content for discord
        :return: None
        ----------
        """

        category = nextcord.utils.get(ctx.guild.categories, name="🔊 Sprachkanäle 🔊")

        if category is None:
            category = await ctx.guild.create_category(
                name="🔊 Sprachkanäle 🔊"
            )
            await ctx.guild.create_text_channel(
                name="voice-manager",
                category=category
            )
            await ctx.guild.create_voice_channel(
                name="Create Voice",
                category=category
            )
            return

        manager = nextcord.utils.get(category.channels, name="voice-manager")
        if manager is None:
            await ctx.guild.create_text_channel(
                name="voice-manager",
                category=category
            )

        voice = nextcord.utils.get(category.channels, name="Create Voice")
        if voice is None:
            await ctx.guild.create_voice_channel(
                name="Create Voice",
                category=category
            )
        await ctx.send("Voice is ready to use.", ephemeral=True)


def setup(bot):
    bot.add_cog(SetupVoice(bot))

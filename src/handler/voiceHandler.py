import nextcord
from src.loader.jsonLoader import Token
import mysql.connector
from nextcord import PartialInteractionMessage, WebhookMessage


class VoiceHandler:
    def __init__(self):
        self.host, self.user, self.password, self.database = Token().maria_db()
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor(prepared=True)

    async def check_permissions(
            self,
            ctx: nextcord.Interaction,
            voice: nextcord.VoiceChannel
    ) -> PartialInteractionMessage | WebhookMessage | bool:

        """
        Attributes
        ----------
        :param ctx:
        :param voice:
        :return: PartialInteractionMessage | WebhookMessage | bool
        ----------
        """

        query = "SELECT member_id FROM active_voice_channel WHERE channel_id=%s"
        data = [int(ctx.user.voice.channel.id)]
        self.cursor.execute(query, data)

        channel_owner = self.cursor.fetchall()

        if channel_owner[0][0] == ctx.user.id and channel_owner is not None:
            self.cursor.close()
            self.connection.close()
            return True

        self.cursor.close()
        self.connection.close()
        return False

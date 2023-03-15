from nextcord.ext import commands
from database.query import Query


# saves the channel im RAM for better performance
__ticket_settings = {}

# connect to database pooling
query = Query(
    pool_name="ticket_channel",
    pool_size=2
)


# saves the channel in the dictionary
async def set_channel(
        bot: commands.Bot,
        server_id: int,
        channel_id: int
) -> None:

    """
    Attributes
    ----------
    :param bot: get bot instance
    :param server_id: Server id from the guild
    :param channel_id: Selected ticket channel
    :return: None
    ----------
    """

    channel = query.execute(
        query="SELECT channelId FROM ticket WHERE serverId=%s",
        data=[int(server_id)]
    )
    if not channel:
        query.execute(
            query="INSERT INTO ticket (serverId, channelId) VALUE (%s,%s)",
            data=[int(server_id), int(channel_id)]
        )
        __ticket_settings[server_id] = channel_id
        return

    old_channel = await bot.fetch_channel(__ticket_settings[server_id])
    await old_channel.delete()

    query.execute(
        query=f"UPDATE ticket SET channelId={channel_id} WHERE serverId=%s",
        data=[int(server_id)]
    )
    __ticket_settings[server_id] = channel_id


# can get the ticket channel from the dictionary
def get_channel(
        server_id: int
) -> int:
    return __ticket_settings[server_id]

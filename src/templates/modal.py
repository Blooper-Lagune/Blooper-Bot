import nextcord.ui


class ModalTicketClose(nextcord.ui.Modal):
    def __init__(self, title: str):
        self.title = title

        super().__init__(
            title=self.title
        )

        self.channel = nextcord.ui.TextInput(
            label=self.title
        )

        self.channel1 = nextcord.ui.TextInput(
            label=self.title
        )
        self.add_item(self.channel)
        self.add_item(self.channel1)

    async def callback(self, ctx: nextcord.Interaction) -> None:
        print("Hat geklappt")

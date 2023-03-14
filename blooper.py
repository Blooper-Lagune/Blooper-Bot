import nextcord
import os
from nextcord.ext import commands
from src.loader.jsonLoader import Token
from database.check import Check


class Blooper(commands.Bot):
    def __init__(self):
        super().__init__(
            intents=nextcord.Intents.all()
        )

        # get the token
        self.__token = Token().get_token()

        # load requirements
        self.remove_command("help")
        print("Requirements loaded")

        for root, dirs, files in os.walk("bot"):
            for name in files:
                if str(root).endswith("__pycache__"):
                    continue

                self.load_extension(os.path.join(root, name).replace("/", ".")[:-3])

        self.run(self.__token)


if __name__ == "__main__":
    # check if database faultless
    Check().inspect()
    # start the bot
    Blooper()

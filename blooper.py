import nextcord
import os
from nextcord.ext import commands
from src.loader.jsonLoader import Token
from database.check import Check
from src.logger.logger import Logger


class Blooper(commands.Bot):
    def __init__(self):
        super().__init__(
            intents=nextcord.Intents.all()
        )

        # get the token
        self.__token = Token().get_token()
        Logger().info("Token loaded")

        # load requirements
        self.remove_command("help")
        Logger().info("All requirements loaded")

        # load all cogs
        for root, dirs, files in os.walk("bot"):
            for name in files:
                if str(root).endswith("__pycache__"):
                    continue

                self.load_extension(os.path.join(root, name).replace("/", ".")[:-3])

        Logger().info("All cogs loaded")

        # run the bot
        self.run(self.__token)


if __name__ == "__main__":
    # check if database faultless
    Check().inspect()
    # start the bot
    Blooper()

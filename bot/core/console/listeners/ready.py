from nextcord.ext import commands
from src.logger.logger import Logger


class ConsoleReady(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        Logger().info(f"Logged in as {self.bot.user}")
        print("""
              ____  _                             
             |  _ \| |                            
             | |_) | | ___   ___  _ __   ___ _ __ 
             |  _ <| |/ _ \ / _ \| '_ \ / _ \ '__|
             | |_) | | (_) | (_) | |_) |  __/ |   
             |____/|_|\___/ \___/| .__/ \___|_|   
                                 | |              
                                 |_|              
        """)


def setup(bot):
    bot.add_cog(ConsoleReady(bot))

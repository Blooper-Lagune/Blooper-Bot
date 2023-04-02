from colorama import Fore, Style
import datetime


class Logger:
    def __init__(self):
        self.now = datetime.datetime.now()

    def info(self, msg: str):
        print(f"[{datetime.date.today()}] [{self.now.strftime('%H:%M:%S')}]" + Fore.GREEN + f" [info]> {msg}" + Style.RESET_ALL)

    def warn(self, msg: str):
        print(f"[{datetime.date.today()}] [{self.now.strftime('%H:%M:%S')}]" + Fore.YELLOW + f" [warn]> {msg}" + Style.RESET_ALL)

    def error(self, msg: str, error):
        print(Fore.RED + f"[{datetime.date.today()}] [{self.now.strftime('%H:%M:%S')}]" + Fore.RED + f" [error]> {msg}" + Style.RESET_ALL)

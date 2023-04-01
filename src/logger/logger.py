from termcolor import cprint, colored
import datetime


class Logger:
    def __init__(self):
        self.now = datetime.datetime.now()

    def info(self, msg: str):
        cprint(f"[{datetime.date.today()}] [{self.now.strftime('%H:%M:%S')}] [info]> {msg}", "green")

    def warn(self, msg: str):
        cprint(f"[{datetime.date.today()}] [{self.now.strftime('%H:%M:%S')}] [warn]> {msg}", "yellow")

    def error(self, msg: str, error):
        cprint(f"[{datetime.date.today()}] [{self.now.strftime('%H:%M:%S')}] [error]> {msg}", "red")

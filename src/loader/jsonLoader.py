import json


class Token:
    def __init__(self):
        with open("config.json", "r") as c:
            self.__config = json.load(c)

    def get_token(self):
        return self.__config["token"]


class Ticket:
    def __init__(self):
        with open("resources/text/ticket.json", "r") as c:
            self.__config = json.load(c)

    def get_ticket(self):
        return self.__config

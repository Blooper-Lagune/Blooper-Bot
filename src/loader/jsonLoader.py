import json


class Token:
    def __init__(self):
        with open("config.json", "r") as c:
            self.__config = json.load(c)

    def get_token(self):
        return self.__config["token"]

    def maria_db(self):
        return self.__config["mariadb"]["host"], self.__config["mariadb"]["user"], self.__config["mariadb"]["password"], self.__config["mariadb"]["database"]


class TicketText:
    def __init__(self):
        with open("resources/text/ticket.json", "r") as c:
            self.__config = json.load(c)

    def get_ticket(self):
        return self.__config

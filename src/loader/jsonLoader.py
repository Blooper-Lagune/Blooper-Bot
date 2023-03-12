import json


class Token:
    def __init__(self):
        with open("config.json", "r") as c:
            self.__config = json.load(c)

    def get_token(self):
        return self.__config["token"]

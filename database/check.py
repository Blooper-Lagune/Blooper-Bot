import mysql.connector
from src.loader.jsonLoader import Token
from mysql.connector.errors import Error


class Check:
    def __init__(self):
        self.host, self.user, self.password, self.database = Token().maria_db()
        self.state_database: bool = False

    def inspect(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
        except Error:
            raise Exception("Can't connect to database. Is your config right?")

        cursor = connection.cursor(prepared=True)
        cursor.execute("Show databases")
        databases = cursor.fetchall()

        for data in databases:
            if str(data[0]).lower() == "nyria":
                self.state_database = True
                print("Database faultless")
                connection.close()

        if not self.state_database:
            self.__create(connection=connection)

    @staticmethod
    def __create(connection: mysql.connector.MySQLConnection):
        cursor = connection.cursor()

        # create database Nyria
        cursor.execute("CREATE DATABASE Blooper")
        cursor.execute("USE Blooper")

        cursor.execute("CREATE TABLE ticket_setting (serverId BIGINT NOT NULL, channelId BIGINT NOT NULL)")

        connection.commit()
        connection.close()

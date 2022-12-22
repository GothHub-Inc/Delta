from dotenv import load_dotenv
import psycopg2
import os


class Postgres:
    def __init__(self):
        load_dotenv()

        if os.getenv("DELTA_CONNECTION_STRING"):
            # print(os.getenv("DELTA_CONNECTION_STRING"))
            self.connection = psycopg2.connect(
                os.getenv("DELTA_CONNECTION_STRING")
            )

            self.cursor = self.connection.cursor()
        else:
            raise ValueError("No connection string has been set")

    def __del__(self):
        if hasattr(self, "cursor"):
            self.cursor.close()

        if hasattr(self, "connection"):
            self.connection.close()


db = Postgres()

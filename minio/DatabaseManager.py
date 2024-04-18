#!/bin/python
# author : ipmstyle <ipmstyle@gmail.com>

import os
import pandas as pd

from dotenv import load_dotenv
from mysql.connector.locales.eng import client_error
import mysql.connector


class DatabaseManager:
    def __init__(self):
        load_dotenv()
        
        self.host = os.getenv("DATABASE_HOST", default=False)
        self.port = os.getenv("DATABASE_PORT", default=False)
        self.user = os.getenv("DATABASE_USER", default=False)
        self.password = os.getenv("DATABASE_PWD", default=False)
        self.database = os.getenv("DATABASE_NAME", default=False)
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                port=self.port,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(buffered=True)
                print("Connected to %s" % self.host)
            else:
                raise ConnectionError("Failed to connect to the database.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            raise

    def disconnect(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Disconnected from %s" % self.host)

    def execute_query(self, query):
        try:
            self.connect()
            self.cursor.execute(query)
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def fetch_all_rows(self):
        results = self.cursor.fetchall()
        if len(results) > 0:
            return results
        else:
            return None
    
    def execute_return_result(self, query):
        self.connect()
        self.execute_query(query)
        result = self.fetch_all_rows()
        self.disconnect()
        return result
    
    def execute_return_df(self, query):
        self.connect()
        try:
            result_df = pd.read_sql(query, con=self.connection)
            return result_df
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            self.disconnect()
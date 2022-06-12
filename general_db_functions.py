import sqlite3 as sq
import traceback


class SQLite3:
    def __init__(self, db_name):
        self.db_name = db_name

    def connect(self):
        self.connection = sq.connect(self.db_name)
        try:
            self.cursor = self.connection.cursor()
            return True
        except Exception as ex:
            print("connection didn't happened properly")
            return False


    def insert_data(self,table_name,name,description,lang,lati):
        try:
            self.connect()
            listOfTables = self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'; ").fetchall()

            if listOfTables == []:
                self.cursor.execute(f"CREATE TABLE {table_name} (Name VARCHAR(50) NOT NULL, Description VARCHAR(500) NOT NULL,Longitude REAL NOT NULL, Latitude REAL NOT NULL); ")
                self.cursor.execute(f"INSERT INTO {table_name} VALUES ('{name}', '{description}', {lang}, {lati});")
            else:
                self.cursor.execute(f"INSERT INTO {table_name} VALUES ('{name}', '{description}', {lang}, {lati});")

            self.connection.commit()
            return True
        except Exception as e:
            traceback.print_exc()
            return False
        finally:
            self.connection.close()



    def update_data(self,table_name, name, lang, lati):
        try:
            self.connect()
            self.cursor.execute(f"UPDATE {table_name} SET Longitude = {lang}, Latitude = {lati} WHERE Name = '{name}';")
            self.connection.commit()
            return True
        except Exception as e:
            traceback.print_exc()
            return False
        finally:
            self.connection.close()


    def delete_data(self,table_name, name=None, lang=None, lati=None):
        try:
            self.connect()
            if name:
                self.cursor.execute(f"DELETE FROM {table_name} WHERE Name = '{name}';")
            else:
                self.cursor.execute(f"DELETE FROM {table_name} WHERE Longitude = {lang} AND Latitude = {lati};")
            self.connection.commit()
            return True
        except Exception as e:
            traceback.print_exc()
            return False
        finally:
            self.connection.close()


    def find_data(self, table_name):
        try:
            self.connect()
            data = self.cursor.execute(f"SELECT * FROM {table_name}")
            self.connection.commit()
            return data.fetchall()
        except Exception as e:
            traceback.print_exc()
            return []
        finally:
            self.connection.close()




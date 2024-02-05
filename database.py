import mysql.connector

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.conn.cursor()
            return True
        except mysql.connector.Error as err:
            print("连接MySQL错误", err)
            return False

    def insert_user(self, type, appid, introduce, requirement_name):
        sql = "INSERT INTO test_information.test_demand (type, appid, introduce, requirement_name) VALUES (%s, %s, %s, %s)"
        val = (type, appid, introduce, requirement_name)
        self.cursor.execute(sql, val)
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

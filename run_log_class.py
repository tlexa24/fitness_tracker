
from main import *

class Run:
    def __init__(self, date, m, t):
        self.date = date
        self.miles = m
        self.time = t

    def insert(self):
        conn = connection
        with conn.cursor() as cursor:
            sql = "INSERT INTO run_log VALUES ('" + self.date + "', '" + self.miles + "', '" + self.time + "')"
            cursor.execute(sql)
            conn.commit()
            print('Run data successfully inserted')
            conn.close()

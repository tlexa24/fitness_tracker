import mysql_connections
import functions
import datetime

def get_weight():
    while True:
        try:
            weight = input('Enter weight(xxx.x): ')
            if functions.float41_checker(weight):
                return str(weight)
            else:
                raise ValueError
        except ValueError:
            print('Input again, using only numbers in xxx.x format:\n')
            continue

def get_bf():
    while True:
        try:
            bf = input('Enter the body fat % in xx.x format: ')
            if functions.float41_checker(bf):
                return str(bf)
            else:
                raise ValueError
        except ValueError:
            print('Input again, using only numbers in xxx.x format:\n')
            continue

def create_weight_instance():
    date_object = str(datetime.date.today())
    wt = get_weight()
    bodyfat = get_bf()
    waight = Weight(date_object, wt, bodyfat)
    return waight

class Weight:
    def __init__(self, d, wt, b):
        self.date = d
        self.weight = wt
        self.bodyfat = b

    def insert_to_sql(self):
        conn = mysql_connections.connection
        with conn.cursor() as cursor:
            sql = "INSERT INTO weight_log VALUES ('" + self.date + "', '" + self.weight + "', '" \
                  + self.bodyfat + "')"
            print('\n\n\nnWeight: ' + self.weight + '\nBody Fat: ' + self.bodyfat + '\nIs this info correct?')
            confirm = functions.get_yn()
            if confirm == 'y':
                cursor.execute(sql)
                conn.commit()
                print('Weight data successfully inserted')
                conn.close()
            else:
                print('Please retry with correct info')
                return ''

def create_insert_weight():
    weight = create_weight_instance()
    weight.insert_to_sql()

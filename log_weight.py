import mysql_connections
import functions
from datetime import timedelta


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


def get_run_yesterday(yesterday):
    conn = mysql_connections.connection
    with conn.cursor() as cursor:
        sql = 'SELECT * FROM run_log WHERE date_recorded = "{}";'.format(yesterday)
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
    if len(result) == 0:
        return 'n'
    else:
        return 'y'


def get_lift_yesterday(yesterday):
    conn = mysql_connections.connection
    with conn.cursor() as cursor:
        sql = 'SELECT * FROM lift_log WHERE date_recorded = "{}";'.format(yesterday)
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
    if len(result) == 0:
        return 'n'
    else:
        return 'y'


def create_weight_instance():
    date_object = functions.get_date()
    wt = get_weight()
    bodyfat = get_bf()
    lift = get_lift_yesterday(str(date_object - timedelta(days=1)))
    run = get_run_yesterday(str(date_object - timedelta(days=1)))
    waight = Weight(str(date_object), wt, bodyfat, lift, run)
    return waight


class Weight:
    def __init__(self, d, wt, b, lift, r):
        self.date = d
        self.weight = wt
        self.bodyfat = b
        self.lift = lift
        self.run = r

    def insert_to_sql(self):
        conn = mysql_connections.connection
        with conn.cursor() as cursor:
            sql = "INSERT INTO weight_log VALUES ('{}', '{}', '{}', '{}', '{}')".format(self.date, self.weight,
                                                                                        self.bodyfat, self.lift,
                                                                                        self.run)
            print('\n\nDate: {}\nWeight: {}\nBody Fat: {}\nLift Yesterday? {}\nRun Yesterday? {}'
                  '\nIs this info correct?'.format(self.date, self.weight, self.bodyfat, self.lift, self.run))
            confirm = functions.get_yn()
            if confirm == 'y':
                cursor.execute(sql)
                conn.commit()
                print('\n\nWeight data successfully inserted to SQL')
                conn.close()
            else:
                print('Please retry with correct info')
                return 'n'


def create_insert_weight():
    weight = create_weight_instance()
    weight.insert_to_sql()

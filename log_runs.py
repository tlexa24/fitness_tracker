import mysql_connections
import functions


def get_miles():
    while True:
        try:
            miles = input('How many miles (xxx.x): ')
            if functions.float41_checker(miles):
                return str(miles)
            else:
                raise ValueError
        except ValueError:
            print('Input again, using only numbers in xxx.x format:\n')
            continue


def run_time():
    times = functions.get_time('r')
    time = ':'.join(times)
    return time


def create_run_instance():
    date = str(functions.get_date())
    runtime = run_time()
    miles = get_miles()
    run_obj = Run(date, miles, runtime)
    return run_obj


class Run:
    def __init__(self, date, m, t):
        self.date = date
        self.miles = m
        self.time = t

    def insert_to_sql(self):
        conn = mysql_connections.connection
        with conn.cursor() as cursor:
            sql = "INSERT INTO run_log VALUES ('{}', '{}', '{}')".format(self.date, self.miles, self.time)
            print('\n\n\nDate: {}\nMiles: {}\nTime: {}\nIs this info correct?'.format(self.date, self.miles, self.time))
            confirm = functions.get_yn()
            if confirm == 'y':
                cursor.execute(sql)
                conn.commit()
                print('\n\nRun data successfully inserted')
                conn.close()
            else:
                print('\nPlease retry with correct info')
                return 'n'


def create_insert_run():
    run = create_run_instance()
    run.insert_to_sql()

import main
import functions
import datetime

def create_run_instance():
    date = str(datetime.date.today())
    runtime = functions.run_time()
    miles = functions.get_miles()
    run_obj = Run(date, miles, runtime)
    return run_obj

class Run:
    def __init__(self, date, m, t):
        self.date = date
        self.miles = m
        self.time = t

    def insert(self):
        conn = main.connection
        with conn.cursor() as cursor:
            sql = "INSERT INTO run_log VALUES ('" + self.date + "', '" + self.miles + "', '" + self.time + "')"
            print('\n\n\nMiles: ' + self.miles + '\nTime: ' + self.time + '\nIs this info correct?')
            confirm = functions.get_yn()
            if confirm == 'y':
                cursor.execute(sql)
                conn.commit()
                print('Run data successfully inserted')
                conn.close()
            else:
                print('Please retry with correct info')
                return ''

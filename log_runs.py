import mysql_connections
import functions
import datetime
import pandas as pd
from openpyxl import load_workbook

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
    date = str(datetime.date.today())
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
            sql = "INSERT INTO run_log VALUES ('" + self.date + "', '" + self.miles + "', '" + self.time + "')"
            print('\n\n\nMiles: ' + self.miles + '\nTime: ' + self.time + '\nIs this info correct?')
            confirm = functions.get_yn()
            if confirm == 'y':
                cursor.execute(sql)
                conn.commit()
                print('\n\nRun data successfully inserted')
                conn.close()
            else:
                print('\nPlease retry with correct info')
                return 'n'

    def insert_to_excel(self):
        data = {'Date': [self.date], 'Miles': [float(self.miles)], 'Time': [self.time]}
        df = pd.DataFrame.from_dict(data)
        writer = pd.ExcelWriter('fitness_data.xlsx', engine='openpyxl')
        writer.book = load_workbook('fitness_data.xlsx')
        writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)
        reader = pd.read_excel(r'fitness_data.xlsx', sheet_name='run')
        df.to_excel(writer, index=False, header=False, sheet_name='run', startrow=len(reader) + 1)
        writer.close()
        print('Run data successfully inserted to fitness_data.xlsx\n')

def create_insert_run():
    run = create_run_instance()
    confirm = run.insert_to_sql()
    if confirm != 'n':
        run.insert_to_excel()

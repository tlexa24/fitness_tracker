import mysql_connections
import pandas as pd
from openpyxl import load_workbook
writer = pd.ExcelWriter('fitness_data.xlsx', engine='openpyxl')
writer.book = load_workbook('fitness_data.xlsx')
writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)

def get_table():
    while True:
        print('\n\n1. Get lift data  \n'
              '2. Get run data  \n'
              '3. Get weight data \n'
              '4. Get diet data\n')
        choice = input('Enter one of the numbers above: ')
        try:
            if int(choice) in range(1, 5):
                break
            else:
                raise ValueError
        except ValueError:
            print("\nOnly enter one of the following numbers.\n")
            continue
    return choice

lift_statement = 'SELECT DISTINCT lift_log.date_recorded, routines.routine_name, exercises.exercise_name, ' \
                 'lift_log.weight, lift_log.set_no, lift_log.reps, exercises_in_routines.exercise_order ' \
                 'FROM lift_log RIGHT JOIN exercises ' \
                 'ON lift_log.exercise_ID = exercises.exercise_ID ' \
                 'RIGHT JOIN exercises_in_routines ' \
                 'ON exercises.exercise_ID = exercises_in_routines.exercise_ID ' \
                 'RIGHT JOIN routines ' \
                 'ON exercises_in_routines.routine_ID = routines.routine_ID ' \
                 'WHERE lift_log.reps IS NOT NULL ' \
                 'ORDER BY lift_log.date_recorded ASC, ' \
                 'exercises_in_routines.exercise_order ASC, ' \
                 'lift_log.set_no ASC;'

run_statement = 'SELECT * ' \
                'FROM run_log ' \
                'ORDER BY date_recorded DESC'

weight_statement = 'SELECT DISTINCT * ' \
                   'FROM weight_log ' \
                   'ORDER BY date_recorded ASC, ' \
                   'time_recorded ASC'

diet_statement = 'SELECT * ' \
                 'FROM diet_log ' \
                 'ORDER BY date_recorded ASC'

def read_lift(sql):
    df = pd.read_sql(sql, mysql_connections.connection)
    df = df.rename(columns={'date_recorded': 'Date', 'routine_name': 'Routine', 'exercise_name': 'Exercise',
                            'set_no': 'Set', 'reps': 'Reps', 'weight': 'Weight'})
    df.drop(columns=['exercise_order'], inplace=True)
    reader = pd.read_excel(r'fitness_data.xlsx', sheet_name='lift')
    df.to_excel(writer, index=False, header=False, sheet_name='lift', startrow=len(reader) + 1)
    writer.close()
    print('\nData moved into fitness_data.xlsx\n\n')

def read_run(sql):
    df = pd.read_sql(sql, mysql_connections.connection)
    df = df.rename(columns={'date_recorded': 'Date', 'miles': 'Miles', 'run_time': 'Time'})
    reader = pd.read_excel(r'fitness_data.xlsx', sheet_name='run')
    df.to_excel(writer, index=False, header=False, sheet_name='run', startrow=len(reader) + 1)
    writer.close()
    print('\nData moved into fitness_data.xlsx\n\n')

def read_weight(sql):
    df = pd.read_sql(sql, mysql_connections.connection)
    df = df.rename(columns={'date_recorded': 'Date', 'body_fat': 'Body Fat',
                            'weight': 'Weight'})
    reader = pd.read_excel(r'fitness_data.xlsx', sheet_name='weight')
    df.to_excel(writer, index=False, header=False, sheet_name='weight', startrow=len(reader) + 1)
    writer.close()
    print('\nData moved into fitness_data.xlsx\n\n')

def read_diet(sql):
    df = pd.read_sql(sql, mysql_connections.connection)
    df = df.rename(columns={'date_recorded': 'Date', 'calories': 'Calories', 'carbs': 'Carbs',
                            'fats': 'Fats', 'proteins': 'Proteins'})
    reader = pd.read_excel(r'fitness_data.xlsx', sheet_name='diet')
    df.to_excel(writer, index=False, header=False, sheet_name='diet', startrow=len(reader)+1)
    writer.close()
    print('\nData moved into fitness_data.xlsx\n\n')

def start_reader():
    table = get_table()
    if table == '1':
        read_lift(lift_statement)
    if table == '2':
        read_run(run_statement)
    if table == '3':
        read_weight(weight_statement)
    if table == '4':
        read_diet(diet_statement)

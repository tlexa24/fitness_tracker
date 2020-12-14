import mysql_connections
import functions
from itertools import cycle, islice
import datetime
import pandas as pd

def get_full_schedule(program):
    with mysql_connections.connectiondict.cursor() as cursor:
        sql = "SELECT * FROM program_schedule WHERE program_ID = {};".format(program)
        cursor.execute(sql)
        result = cursor.fetchall()
    return result

def get_list_of_days(schedule):
    days = []
    for day in schedule:
        days.append(day['day_of_week'])
    return days

def get_last_lift(program):
    with mysql_connections.connection.cursor() as cursor:
        sql = "SELECT routine_ID, routine_name FROM routines WHERE program_id = '{}';".format(program)
        cursor.execute(sql)
        result = cursor.fetchall()[:6]
        choices = [str(row[0]) for row in result]
    while True:
        try:
            for row in result:
                print(str(row[0]) + '. ' + functions.name_converter(str(row[1])))
            routine = input('Which was the last lifting routine you completed? ')
            if functions.check_if_in_list(routine, choices):
                return routine
            else:
                print('\n\nChoose only one of the given numbers.')
                raise ValueError
        except ValueError:
            continue

def get_today(recent_lift, schedule):
    last_lift = recent_lift
    for day in schedule:
        if day['lifting_routine'] is not None:
            if int(day['lifting_routine']) == int(last_lift):
                return int(day['day_of_week']) + 1

def cycled_picker_list(starting_point, starting_list, elements):
    final_list = []
    days_cycle = cycle(starting_list)
    starting_at_today = islice(days_cycle, starting_point, None)
    while len(final_list) < elements:
        final_list.append(next(starting_at_today))
    return final_list

def get_program():
    with mysql_connections.connection.cursor() as cursor:
        sql = "SELECT program_ID, program_name FROM programs;"
        cursor.execute(sql)
        result = cursor.fetchall()
        choices = [str(row[0]) for row in result]
        while True:
            try:
                for row in result:
                    print(str(row[0]) + '. ' + str(row[1]))
                program = input('Which program are you using? Enter one of the above numbers: ')
                if functions.check_if_in_list(program, choices):
                    return program
                else:
                    print('\n\nChoose only one of the given numbers.')
                    raise ValueError
            except ValueError:
                continue

def get_next_4_days():
    program = get_program()
    full_schedule = get_full_schedule(program)
    last_lift = get_last_lift(program)
    list_of_days = get_list_of_days(full_schedule)
    today = get_today(last_lift, full_schedule)
    next_4_days = cycled_picker_list(list_of_days.index(today + 1), list_of_days, 4)
    return program, next_4_days

def get_next_4_schedules():
    next_4_days = get_next_4_days()
    program = next_4_days[0]
    days_list = next_4_days[1]
    with mysql_connections.connectiondict.cursor() as cursor:
        sql = "SELECT day_of_week, lifting_routine, ab_routine, run " \
              "FROM program_schedule " \
              "WHERE program_ID = {} " \
              "AND day_of_week IN ({}, {}, {}, {});".format(program, days_list[0], days_list[1], days_list[2],
                                                            days_list[3])
        cursor.execute(sql)
        result = cursor.fetchall()
    return result

day_names = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

def change_days_to_dates():
    days = get_next_4_schedules()
    today = datetime.date.today()
    addition = 1
    for day in days:
        day_name = (today + datetime.timedelta(days=addition)).weekday()
        day['day_of_week'] = str(day_names[day_name]) + ', ' + str(today + datetime.timedelta(days=addition))
        addition += 1
    return days

def dict_to_df(sql):
    df = pd.read_sql(sql, mysql_connections.connection)
    df = df.rename(columns={'exercise_name': 'Exercise', 'sets': 'Sets', 'reps': 'Reps', 'current_weight': 'Weight',
                            'last_set_AMRAP': 'Last AMRAP'})
    df.set_index('exercise_order', inplace=True)
    df.index.name = None
    return df

def get_routine_dataframes():
    schedule = change_days_to_dates()
    for day in schedule:
        if day['lifting_routine'] is not None:
            sql = "SELECT exercise_order, exercise_name, sets, reps, current_weight, last_set_AMRAP " \
                  "FROM exercises_in_routines " \
                  "LEFT JOIN exercises ON exercises.exercise_ID = exercises_in_routines.exercise_ID " \
                  "WHERE routine_id = '{}'" \
                  "ORDER BY exercise_order ASC;".format(day['lifting_routine'])
            day['lifting_routine'] = dict_to_df(sql)
        if day['ab_routine'] is not None:
            sql = "SELECT exercise_order, exercise_name, sets, reps FROM exercises_in_routines " \
                  "LEFT JOIN exercises ON exercises.exercise_ID = exercises_in_routines.exercise_ID  " \
                  "WHERE routine_id = '{}'" \
                  "ORDER BY exercise_order ASC;".format(day['ab_routine'])
            day['ab_routine'] = dict_to_df(sql)
    return schedule

def get_next_4_routines():
    schedule = get_routine_dataframes()
    return schedule

def print_schedule():
    schedule = get_next_4_routines()
    day_string = 'RUN: {}\nLIFT: {}\nABS: {}\n'
    for day in schedule:
        print('\n' + day['day_of_week'])
        run, lift, ab = 'NO', 'NO', 'NO'
        if day['run'] is not None:
            run = 'YES'
        if day['lifting_routine'] is not None:
            lift = 'Yes'
        if day['ab_routine'] is not None:
            ab = 'YES'
        print(day_string.format(run, lift, ab))
        if day['lifting_routine'] is not None:
            print(day['lifting_routine'])
            print('\n')
        if day['ab_routine'] is not None:
            print(day['ab_routine'])

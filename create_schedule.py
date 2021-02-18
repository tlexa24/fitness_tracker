import mysql_connections
import functions
from itertools import cycle, islice
import datetime
import pandas as pd


def get_full_schedule(program):
    with mysql_connections.connectiondict.cursor() as cursor:
        sql = 'SELECT * FROM program_schedule WHERE program_ID = {};'.format(program)
        cursor.execute(sql)
        result = cursor.fetchall()
    return result


def get_list_of_days(schedule):
    days = []
    for day in schedule:
        days.append(day['day_of_week'])
    return days


def get_last_lift(program):
    with mysql_connections.connectiondict.cursor() as cursor:
        sql = "SELECT routine_ID, routine_name FROM routines WHERE program_id = '{}';".format(program)
        cursor.execute(sql)
        routines = cursor.fetchall()
    with mysql_connections.connectiondict.cursor() as cursor:
        new_sql = "SELECT * FROM lift_log ORDER BY date_recorded DESC LIMIT 1"
        cursor.execute(new_sql)
        result = cursor.fetchall()
        if len(result) == 0:
            return None
        else:
            for routine in routines:
                if routine['routine_ID'] == result[0]['routine_ID']:
                    print('Your last recorded lift was ' + functions.name_converter(routine['routine_name']))
                    print('Was today a rest day?')
                    confirm = functions.get_yn()
            return result[0]['routine_ID'], confirm


def get_day_of_last_lift(last_lift, schedule):
    for day in schedule:
        if day['lifting_routine'] is not None:
            if int(day['lifting_routine']) == int(last_lift):
                return int(day['day_of_week'])


def cycled_picker_list(starting_point, starting_list):
    days_cycle = cycle(starting_list)
    starting_at_today = islice(days_cycle, starting_point, None)
    return next(starting_at_today)


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


def get_tomorrow():
    program = get_program()
    full_schedule = get_full_schedule(program)
    last_lift_data = get_last_lift(program)
    if last_lift_data is None:
        tomorrow = 1
    else:
        last_lift = last_lift_data[0]
        today_question = last_lift_data[1]
        list_of_days = get_list_of_days(full_schedule)
        today = get_day_of_last_lift(last_lift, full_schedule)
        addition = 1
        if today_question == 'y':
            addition += 1
        tomorrow = cycled_picker_list(list_of_days.index(today), list_of_days) + addition
    return program, tomorrow


def get_tomorrow_schedule():
    tomorrow = get_tomorrow()
    program = tomorrow[0]
    day = tomorrow[1]
    with mysql_connections.connectiondict.cursor() as cursor:
        sql = "SELECT day_of_week, lifting_routine, ab_routine, run " \
              "FROM program_schedule " \
              "WHERE program_ID = {} " \
              "AND day_of_week = {};".format(program, day)
        cursor.execute(sql)
        result = cursor.fetchall()
    return result[0]


day_names = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}


def change_days_to_dates():
    tomorrow_routine = get_tomorrow_schedule()
    today = datetime.date.today()
    day_name = (today + datetime.timedelta(days=1)).weekday()
    tomorrow_routine['day_of_week'] = str(day_names[day_name]) + ', ' + str(today + datetime.timedelta(days=1))
    return tomorrow_routine


def dict_to_df(sql):
    df = pd.read_sql(sql, mysql_connections.connection)
    df = df.rename(columns={'exercise_name': 'Exercise', 'sets': 'Sets', 'reps': 'Reps', 'current_weight': 'Weight',
                            'last_set_AMRAP': 'Last AMRAP'})
    df.set_index('exercise_order', inplace=True)
    df.index.name = None
    return df


def get_routine_dataframes():
    schedule = change_days_to_dates()
    if schedule['lifting_routine'] is not None:
        with mysql_connections.connectiondict.cursor() as cursor:
            sql = "SELECT routine_name FROM routines WHERE routine_ID = {}".format(schedule['lifting_routine'])
            cursor.execute(sql)
            routine_name = cursor.fetchall()
        schedule['routine name'] = functions.name_converter(routine_name[0]['routine_name'])
        sql = "SELECT exercise_order, exercise_name, sets, reps, current_weight, last_set_AMRAP " \
              "FROM exercises_in_routines " \
              "LEFT JOIN exercises ON exercises.exercise_ID = exercises_in_routines.exercise_ID " \
              "WHERE routine_id = '{}'" \
              "ORDER BY exercise_order ASC;".format(schedule['lifting_routine'])
        schedule['lifting_routine'] = dict_to_df(sql)
    if schedule['ab_routine'] is not None:
        sql = "SELECT exercise_order, exercise_name, sets, reps FROM exercises_in_routines " \
              "LEFT JOIN exercises ON exercises.exercise_ID = exercises_in_routines.exercise_ID  " \
              "WHERE routine_id = '{}'" \
              "ORDER BY exercise_order ASC;".format(schedule['ab_routine'])
        schedule['ab_routine'] = dict_to_df(sql)
    return schedule


def print_schedule():
    schedule = get_routine_dataframes()
    day_string = 'RUN: {}\nLIFT: {}\nABS: {}\n'
    print('\n' + schedule['day_of_week'])
    run, lift, ab = 'NO', 'NO', 'NO'
    if schedule['run'] is not None:
        run = 'YES'
    if schedule['lifting_routine'] is not None:
        lift = schedule['routine name']
    if schedule['ab_routine'] is not None:
        ab = 'YES'
    print(day_string.format(run, lift, ab))
    if schedule['lifting_routine'] is not None:
        print(schedule['lifting_routine'])
        print('\n')
    if schedule['ab_routine'] is not None:
        print(schedule['ab_routine'])

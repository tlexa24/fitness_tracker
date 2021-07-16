
# This file contains functions to give the user their workout schedule for tomorrow

import mysql_connections
import functions
from itertools import cycle, islice
import datetime
import pandas as pd


def get_full_schedule(program):
    """
    Takes in a workout program, and returns a dictionary of every day's schedule
    in that program as a dictionary
    :param program: Takes in the particular workout program
    :return: The program's daily schedule as a dictionary
    """
    with mysql_connections.connectiondict.cursor() as cursor:
        sql = 'SELECT * FROM program_schedule WHERE program_ID = {};'.format(program)
        cursor.execute(sql)
        result = cursor.fetchall()
    return result


def get_list_of_days(schedule):
    """
    This function takes in a schedule, and pulls out the day ID numbers, returning them in a list.
    From the way the SQL database holds a schedule, each day in the schedule holds a unique number.
    A 6-day schedule would have IDs from 1 through 6.
    :param schedule: Takes in a program schedule
    :return: Returns a list of the day ID numbers in a list
    """
    days = []
    for day in schedule:
        days.append(day['day_of_week'])
    return days


def get_last_lift(program):
    """
    This function takes in a program ID, and reads in the lift_log table of the database to
    determine the last lifting routine completed by the user. It then displays this routine's
    name to user, and prompts them to enter whether the current day was a rest day, or a day
    without lifting. Uses the get_yn function to verify their reply
    :param program: The current workout program the user is using
    :return: Returns the ID number of the last lifting routine completed by the user
    """
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
    """Returns the schedule's day ID of the last lifting routine completed"""
    for day in schedule:
        if day['lifting_routine'] is not None:
            if int(day['lifting_routine']) == int(last_lift):
                return int(day['day_of_week'])


def cycled_picker_list(starting_point, starting_list):
    """This function returns the next time in a list, even if the starting item is the last
    element. For example, if we start at index 2 in a list of length 3, the function would
    return the element at index 0"""
    days_cycle = cycle(starting_list)
    starting_at_today = islice(days_cycle, starting_point, None)
    return next(starting_at_today)


def get_program():
    """
    This function reads in the available exercise programs from the SQL database, displaying
    these as choices to the user. The user will be prompted to enter the number that corresponds
    to their desired program, and if do not enter a valid choice, they will be prompted to try
    until their choice is valid
    :return: Returns the number corresponding to the user's current program
    """
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
                if program in choices:
                    return program
                else:
                    print('\n\nChoose only one of the given numbers.')
                    raise ValueError
            except ValueError:
                continue


def get_tomorrow():
    """
    This function determines which day of the program schedule should take place tomorrow.
    Calls get_program to find out which program the user is currently using. It then calls
    get_full_schedule to get the full daily schedule of that program, and get_last_lift to
    find out the ID of the last routine completed. If the user does not have a completed routine,
    their schedule will start on day 1. If they have completed a routine, then the function obtains
    the list of days in the schedule, and the day of the last completed routine, and we target the
    day following the day of that last routine. If the current day is a rest day, then we add one to
    the day ID and target this new day. We then call cycled picker list, to find the next day up in the
    program schedule
    :return: We return the program ID and the day ID of tomorrow in the program's schedule
    """
    program = get_program()
    full_schedule = get_full_schedule(program)
    last_lift_data = get_last_lift(program)
    if last_lift_data is None:
        tomorrow = 1
    else:
        last_lift = last_lift_data[0]
        rest_day_today = last_lift_data[1]
        list_of_days = get_list_of_days(full_schedule)
        today = get_day_of_last_lift(last_lift, full_schedule)
        addition = 1
        if rest_day_today:
            addition += 1
        tomorrow = cycled_picker_list(list_of_days.index(today), list_of_days) + addition
    return program, tomorrow


def get_tomorrow_schedule():
    """
    This function takes in the ID of tomorrow in the program's schedule, and reads in that
    day's schedule from the SQL database. Resulting dictionary includes schedule's lifting
    routine name (if any), and whether or not there is a planned run or abdominal routine
    :return: Returns tomorrow's schedule as a dictionary
    """
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


# Defining days of the week with ID numbers
day_names = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}


def change_days_to_dates():
    """
    This function determines the day of the week and date for tomorrow. It then updates the day
    in tomorrow's schedule to hold a string of the day of the week and the date. Just makes the
    final printed schedule easier to read
    :return: Returns the schedule of tomorrow with the updated day and date
    """
    tomorrow_routine = get_tomorrow_schedule()
    today = datetime.date.today()
    day_name = (today + datetime.timedelta(days=1)).weekday()
    tomorrow_routine['day_of_week'] = str(day_names[day_name]) + ', ' + str(today + datetime.timedelta(days=1))
    return tomorrow_routine


def dict_to_df(sql):
    """
    This function takes in a SQL script to read in a workout routine. It uses pandas
    read_sql method to convert the resulting data into a dataframe. The dataframe
    is then sorted by the order the exercises should be completed in
    :param sql: The SQL script to pull in routine data
    :return: Returns a dataframe containing the routine data
    """
    df = pd.read_sql(sql, mysql_connections.connection)
    df = df.rename(columns={'exercise_name': 'Exercise', 'sets': 'Sets', 'reps': 'Reps', 'current_weight': 'Weight',
                            'last_set_AMRAP': 'Last AMRAP'})
    df.set_index('exercise_order', inplace=True)
    df.index.name = None
    return df


def get_routine_dataframes():
    """
    Takes in tomorrow's workout plan from the program schedule. If a lifting routine is part
    of the plan, we use name_converter function to make the name of the routine easier to read,
    and we call dict_to_df on the routine, adding the dataframe contining the full lifting routine to
    tomorrow's schedule. If there is a planned abdominal routine, that routine is also added to
    tomorrow's schedule dictionary.
    :return: Returns the workout schedule of tomorrow in dictionary format
    """
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
    """
    This function coordinates the rest of the functions in the file. When this function is
    called, it starts by calling get_routine_dataframes, which starts a chain reaction of
    the rest of the functions in the file to construct tomorrow's schedule in a dictionary.
    In printing tomorrow's schedule: The date is printed first, then whether or not a run is
    planned, the planned lifting routine if there is indeed one planned, and finally the
    abdominal routine if there is one planned.
    :return:
    """
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
        print(schedule['lifting_routine'].to_string(index=False))
        print('\n')
    if schedule['ab_routine'] is not None:
        print(schedule['ab_routine'])


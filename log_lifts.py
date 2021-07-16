
# This file contains multiple functions and a class to collect and load data
# on weightlifting results into the SQL database

import mysql_connections
import functions


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


def get_routine():
    """
    This function calls the get_program function to obtain the user's desired program,
    and then reads in the available routines from the chosen program from the SQL database,
    displaying these as choices to the user. The user will be prompted to enter the number
    that corresponds to their desired routine, and if they do not enter a valid choice, they
    will be prompted to try until their choice is valid
    :return: Returns the corresponding number to the selected routine
    """
    with mysql_connections.connectiondict.cursor() as cursor:
        program = get_program()
        sql = "SELECT routine_ID, routine_name FROM routines WHERE program_id = '{}';".format(program)
        cursor.execute(sql)
        result = cursor.fetchall()
        choices = [str(row['routine_ID']) for row in result]
        while True:
            try:
                for row in result:
                    print(str(row['routine_ID']) + '. ' + functions.name_converter(str(row['routine_name'])))
                routine = input('Which routine are you logging results for? Enter one of the above numbers: ')
                if routine in choices:
                    for row in result:
                        if str(row['routine_ID']) == routine:
                            return routine, row['routine_name']
                else:
                    print('\n\nChoose only one of the given numbers.')
                    raise ValueError
            except ValueError:
                continue

def get_exercises():
    """
    This function calls the get_routine function which will in turn call the get_program
    function. After these two functions run, this function will use the user's choices to
    read in the exercises that make up the chosen routine. The exercises and their attributes
    are stored in a dictionary. Additionally, an entry to the exercise's dictionary will be
    made for each planned set in that routine. For example, if the bench press has 2 planned sets,
    its dictionary will have these additional pairs ('Set 1':0 and 'Set 2':0). Each individual
    exercise's dictionary is then added to a list, which by the end of the function will hold the
    dictionary of each exercise in the routine
    :return: Returns the list of log templates for each exercise in the routine
    """
    dictconn = mysql_connections.connectiondict
    with dictconn.cursor() as cursor:
        routine = get_routine()
        sql = "SELECT exercise_name, exercises.exercise_ID, reps, sets, current_weight, weight_progressor " \
              "FROM exercises_in_routines " \
              "LEFT JOIN exercises ON exercises.exercise_ID = exercises_in_routines.exercise_ID " \
              "WHERE routine_id = '{}'" \
              "ORDER BY exercise_order;".format(routine[0])
        cursor.execute(sql)
        result = cursor.fetchall()
        dictconn.close()
        log_template = []
        for d in result:
            num_sets = d['sets']
            exercise_dict = {'name': d['exercise_name'], 'routine': routine[1], 'routine_ID': routine[0],
                             'ID': d['exercise_ID'], 'progressor': d['weight_progressor'],
                             'sets': d['sets'], 'current': d['current_weight'], 'reps': d['reps']}
            for n in range(1, num_sets + 1):
                exercise_dict['Set {}'.format(n)] = 0
            log_template.append(exercise_dict)
        return log_template

def update_weight(exercise, new):
    """
    This function updates an exercise entry in the database to have an updated
    current weight
    :param exercise: The excerise_ID of the exercise to have an updated weight
    :param new: The new weight to be loaded into the database
    """
    sql = "UPDATE exercises SET current_weight = '{}' WHERE exercise_ID = '{}';".format(new, exercise)
    with mysql_connections.connection.cursor() as cursor:
        cursor.execute(sql)
        mysql_connections.connection.commit()


def get_weight(exercise):
    """This function checks if the user used the current weight in the SQL
    database for the exercise they're logging. If not, we obtain the weight
    they used, verifying that is the correct format xxx.x, and if not prompting
    the user to try until they enter a valid weight. Once the weight is obtained
    we call update_weight to update the database to hold the new correct figure"""
    print('Did you use {} lbs. for {}? '.format(exercise['current'], functions.name_converter(exercise['name'])))
    confirm = functions.get_yn()
    if not confirm:
        while True:
            try:
                weight = input('Enter the correct weight(xxx.x): ')
                if functions.float41_checker(weight):
                    update_weight(exercise['ID'], weight)
                    exercise['current'] = weight
                    break
                else:
                    raise ValueError
            except ValueError:
                print('Input again, using only numbers in xxx.x format:\n')
                continue


def get_results():
    """
    This function calls get_exercises for the list of exercise dictionaries. For each exercise,
    get_weight is called to check if the user used the current_weight figure in the database.
    If not, the current_weight is updated in both the database and the exercise dictionary.
    Using the dictionary, we obtain the number of reps planned for each set, and then prompt
    the user to input how many reps they completed for each set, verifying the entry is indeed
    an integer. If not, the user enters until they input a valid entry. As the user inputs numbers
    of reps, these entries are added to dictionary of that particular exercise. If the user completed
    at least as many reps as planned in a set, that set is considered successfull and a count of
    successfull sets is kept for each exercise. If every set of an exercise was successful, then
    the current_weight figure in the database is incremented by the progressor (unique to each
    exercise). For example, if the user successfully completes every set of bench press, then the
    current_weight figure is increased by 10, as the user should be expected to try the higher
    weight the next workout that uses bench press. Finally, the template is returned, with weight
    corrected and reps completed now added for each exercise
    :return: The list of updated exercise dictionaries is returned
    """
    template = get_exercises()
    for exercise in template:
        get_weight(exercise)
        num_sets = exercise['sets']
        successful_sets = 0
        reps_to_hit = exercise['reps']
        for n in range(1, num_sets + 1):
            while True:
                try:
                    reps = input('Input reps for {} Set #{}: '.format(exercise['name'], str(n)))
                    if functions.int_checker(reps):
                        if int(reps) >= reps_to_hit:
                            successful_sets += 1
                        exercise['Set {}'.format(str(n))] = reps
                        break
                    else:
                        raise ValueError
                except ValueError:
                    print('\nEnter only numbers.\n')
                    continue
        if successful_sets == int(num_sets):
            update_weight(exercise['ID'], float(exercise['current']) + int(exercise['progressor']))
    return template


class LiftLog:
    """Class used to collect data for insertion into SQL. Since each set of an exercise
    is its own row in the database, there will be an instance created for every set"""
    def __init__(self, date, ex_name, routine_name, routine_id, exercise_id, weight, setno, reps):
        """
        Initializes the instance, holding all of the data needed for a new row in the
        lift_log table of the database
        """
        self.date = date
        self.exercise_name = ex_name
        self.routine = routine_name
        self.routine_id = routine_id
        self.ID = exercise_id
        self.weight = weight
        self.set = setno
        self.reps = reps

    def insert_to_sql(self):
        """This method connects to the database, fills in the INSERT statment with the
        instance's data, and executes the insert statement"""
        conn = mysql_connections.connection
        with conn.cursor() as cursor:
            sql = "INSERT INTO lift_log VALUES ('{}', '{}', '{}', '{}', '{}', '{}');".format(self.date, self.routine_id,
                                                                                             self.ID, self.weight,
                                                                                             self.set, self.reps)
            cursor.execute(sql)
        conn.commit()


def create_insert_lift():
    """
    This function coordinates all of the functions and methods defined above.
    Since each set of an exercise is its own row in the database, it is much
    easier to create an instance for each set through this function than the ways
    contained in the other files of this program. Calls the get_date function to
    obtain the date of the workout, and the get_results function to obtain user
    input on the result of their workout. Once the updated list of exercise dictionaries
    has been obtained, an instance of the LiftLog is created for each set completed.
    The data on this set is then inserted into the database. This process repeats
    until each set of every exercise has been loaded in the database.
    """
    day = str(functions.get_date())
    lift_inputs = get_results()
    for lift in lift_inputs:
        for n in range(1, lift['sets'] + 1):
            lift_obj = LiftLog(day, lift['name'], lift['routine'], lift['routine_ID'], lift['ID'],
                               lift['current'], n, lift['Set {}'.format(n)])
            lift_obj.insert_to_sql()
    print('Lift data successfully inserted to SQL\n')

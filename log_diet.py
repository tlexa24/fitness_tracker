# This file contains functions and a class to handle inserting diet data into the database

import mysql_connections
import functions
from urllib import request, error
import myfitnesspal


def connect():
    """This function asks the user whether they would like to obtain their data from MyFitnessPal
    or input it manually. If they select MyFitnessPal, the function then verifies a current
    connection to the internet
    :return: True if a connection is present, False if not"""
    print('\nWould you like to download data from MyFitnessPal y/n')
    confirm = functions.get_yn()
    if confirm:
        try:
            request.urlopen('http://google.com')
            return True
        except error.URLError:
            print('Unable to establish connection, please enter manually\n')
            return False
    if not confirm:
        return False


def my_fitness_pal(date):
    """
    This function connects to MyFitnessPal and pulls out the diet info logged for a specific day
    :param date: The datetime instance representing the day the user wants diet day for
    :return: Returns a dictionary containing the calories, carbohydrates, fats, and proteins
    logged on a certain day
    """
    year, month, day = date.year, date.month, date.day
    client = myfitnesspal.Client('tlexa2497@gmail.com')
    day = client.get_date(year, month, day)
    diet = day.totals
    print('Successfully pulled information from MyFitnessPal')
    diet_info = {'cals': int(diet['calories']), 'carb': int(diet['carbohydrates']), 'fat': int(diet['fat']),
                 'protein': int(diet['protein'])}
    return diet_info


def get_diet():
    """
    In the event that the program is unable to connect with MyFitnessPal, this function has the user
    manually input their dietary information for a given day. Their entries are validated as integers
    and if the entries are invalid, the user is prompted to try until their input is valid
    :return: Returns a dictionary containing the calories, carbohydrates, fats, and proteins
    logged on a certain day
    """
    while True:
        try:
            diet_info = {'cals': input('Input today\'s calories: '), 'carb': input('Input today\'s carbs: '),
                         'fat': input('Input today\'s fat: '), 'protein': input('Input today\'s protein: ')}
            for key in diet_info.keys():
                if functions.int_checker(diet_info[key]):
                    continue
                else:
                    raise functions.InputError()
            return diet_info
        except functions.InputError():
            print('\n\nInput again, using only numbers.\n')


class DietLog:
    """Instancs of this class store all of the data needed to insert a new row into the diet_log SQL table"""

    def __init__(self):
        """Initializes the class instance. Date is obtained with the get_date function, connection_status
        is obtained from the connect function. Based on connection_status, the diet info is obtained from
        either the my_fitness_pal function or the get_diet function.
        """
        self.date = functions.get_date()
        self.connection_status = connect()
        if self.connection_status:
            self.diet = my_fitness_pal(self.date)
        else:
            self.diet = get_diet()

    def create_sql(self):
        """
        This method writes the SQL insert statement, using the data members of the DietLog class instance,
        navigating through the dictionary of the diet data member when neccessary
        :return: Returns a tuple, first element being the SQL insert statement, and the second being a y/n confirmation
        on whether the user approves the data
        """
        sql = "INSERT INTO diet_log VALUES ('{}', '{}', '{}', '{}', '{}')".format(self.date, self.diet['cals'],
                                                                                  self.diet['carb'],
                                                                                  self.diet['fat'],
                                                                                  self.diet['protein'])
        print("\n\nDate: {}\nCals: {}\nCarbs: {}\nFats: {}\nProteins: {}\nIs this info correct?".format(
                                                                                  self.date, self.diet['cals'],
                                                                                  self.diet['carb'],
                                                                                  self.diet['fat'],
                                                                                  self.diet['protein']))
        confirm = functions.get_yn()
        return sql, confirm

    def insert_to_sql(self):
        """This method establishes connection to the SQL database. It then calls the create_sql method
        to write the SQL statement, finally executing and committing the statement to have the data
        load into the diet_log database table"""
        conn = mysql_connections.connection
        with conn.cursor() as cursor:
            sql = self.create_sql()
            if sql[1]:
                cursor.execute(sql[0])
                conn.commit()
                print('\nDiet data successfully inserted to SQL')
                conn.close()
            else:
                print('Please retry with correct info')

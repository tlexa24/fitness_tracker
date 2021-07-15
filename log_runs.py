
# This file contains functions and a class to handle inserting run data into the database

import mysql_connections
import functions


def get_miles():
    """
    This function obtains the number of miles that the user ran. The correct format is
    xxx.x, which is verified using the float41_checker function. If the user inputs
    invalid data they are prompted to retry until valid data is entered
    :return: The string of how many miles is returned
    """
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
    """
    Uses the get_time function to obtain the factors of time that the run took (hours,
    minutes, seconds). These factors are then joined into one string ([01, 23, 32]
    turns into 01:23:32)
    :return: The joined string of the complete time is returned
    """
    times = functions.get_time('r')
    time = ':'.join(times)
    return time


class RunLog:
    """Instances of this class store all of the data needed to insert a new row into
    the weight_log SQL table"""

    def __init__(self):
        """Initializes the class instance. Date is obtained with the get_date function, and
        miles/time are both obtained from the above functions"""
        self.date = functions.get_date()
        self.miles = get_miles()
        self.time = run_time()

    def create_sql(self):
        """
        This method writes the SQL insert statement, using the data members of the RunLog
        class instance
        :return: Returns a tuple, first element being the SQL insert statement, and the second
        being a y/n confirmation on whether the user approves the data
        """
        sql = "INSERT INTO run_log VALUES ('{}', '{}', '{}')".format(self.date, self.miles, self.time)
        print('\n\nDate: {}\nMiles: {}\nTimes: {}'
              '\nIs this info correct? y/n'.format(self.date, self.miles, self.time))
        confirm = functions.get_yn()
        return sql, confirm

    def insert_to_sql(self):
        """This method establishes connection to the SQL database. It then calls the create_sql method
        to write the SQL statement, finally executing and committing the statement to have the data
        load into the run_log database table"""
        conn = mysql_connections.connection
        with conn.cursor() as cursor:
            sql = self.create_sql()
            if sql[1]:
                cursor.execute(sql[0])
                conn.commit()
                print('\n\nRun data successfully inserted to SQL')
                conn.close()
            else:
                print('Please retry with correct info')

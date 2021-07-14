
# This file contains functions and a class to handle inserting weight/bodyfat data into the database
import mysql_connections
import functions


def input_weight():
    """This function gets user input for their weight. Contains a try/except block to validate that the data matches the
    correct format of xxx.x. If they input invalid data, the custom InputError exception is raised and the user will be
    prompted to re-enter their data until the format is correct
    :return: Returns the input weight as a string, for proper insertion into SQL
    """
    while True:
        try:
            weight = input('Enter weight(xxx.x): ')
            if functions.float41_checker(weight):
                return str(weight)
            else:
                raise functions.InputError()
        except functions.InputError():
            print('Input again, using only numbers in xxx.x format:\n')
            continue


def input_bodyfat():
    """This function gets user input for their bodyfat. Contains a try/except block to validate that the data matches
    the correct format of xx.x. If they input invalid data, the custom InputError exception is raised and the user will
    be prompted to re-enter their data until the format is correct
    :return: Returns the input bodyfat as a string, for proper insertion into SQL
    """
    while True:
        try:
            bf = input('Enter the body fat % in xx.x format: ')
            if functions.float41_checker(bf):
                return str(bf)
            else:
                raise functions.InputError()
        except functions.InputError():
            print('Try again, using only numbers in xx.x format:\n')
            continue


class WeightLog:
    """Instancs of this class store all of the data needed to insert a new row into the weight_log SQL table"""
    def __init__(self):
        """Initializes the class instance. Date is obtained with the get_date function, and weight/bodyfat are both
        obtained from the above functions"""
        self.date = str(functions.get_date())
        self.weight = input_weight()
        self.bodyfat = input_bodyfat()

    def create_sql(self):
        """
        This method writes the SQL insert statement, using the data members of the WeightLog class instance
        :return: Returns a tuple, first element being the SQL insert statement, and the second being a y/n confirmation
        on whether the user approves the data
        """
        sql = "INSERT INTO weight_log VALUES ('{}', '{}', '{}')".format(self.date, self.weight, self.bodyfat)
        print('\n\nDate: {}\nWeight: {}\nBody Fat: {}'
              '\nIs this info correct? y/n'.format(self.date, self.weight, self.bodyfat))
        confirm = functions.get_yn()
        return sql, confirm

    def insert_to_sql(self):
        """This method establishes connection to the SQL database. It then calls the create_sql method to write the SQL
        statement, finally executing and committing the statement to have the data load into the database"""
        conn = mysql_connections.connection
        with conn.cursor() as cursor:
            sql = self.create_sql()
            if sql[1] == 'y':
                cursor.execute(sql[0])
                conn.commit()
                print('\n\nWeight data successfully inserted to SQL')
                conn.close()
            else:
                print('Please retry with correct info')

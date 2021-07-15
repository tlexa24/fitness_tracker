
# This file contains various functions used throughout the rest of the program,
# mainly for data collection, transforming, and validation

import datetime


class InputError(Exception):
    """Exception called when a user input does not fit into the accepted format"""
    pass


def int_checker(num):
    """
    This function checks that a given number is indeed an integer, rather than any other data type
    :param num: Takes in a number
    :return: Returns True if the number is an integer, False if not
    """
    result = False
    try:
        int(num)
        result = True
    except ValueError:
        pass
    return result


def name_converter(string):
    """In the SQL database, the names have '-' and '_' instead of spaces. For ease of reading while
    printing to the user, these characters are replaced with spaces
    :param string: Takes in a string
    :return: Returns the same string, with the '-'  and '_' replaced with spaces
    """
    string = string.replace('_', ' ')
    string = string.replace('-', ' ')
    return string


def check_if_in_list(var, lst):
    """
    This function checks if a given variable is an element of a given list
    :param var: Takes in a target variable
    :param lst: Takes in a list
    :return: Returns True if the variable is in the list, False if not
    """
    if var in lst:
        return True
    else:
        return False


def float_checker(num):
    """
    This function checks that a given number is indeed a float, rather than any other data type
    :param num: Takes in a number
    :return: Returns True if the number is a float, False if not
    """
    result = False
    try:
        float(num)
        result = True
    except ValueError:
        pass
    return result


def length_checker(var, needed_len):
    """
    This function verifies that a variable's length is equal to the desired length
    :param var: Takes in a variable
    :param needed_len: The desired length for the variable to match
    :return: Returns boolean depending on whether the variable's length matches the desired length
    """
    return len(var) == needed_len


def max_length_checker(var, maxi):
    """
    This function verifies that a variable's length is not greater than a desired length
    :param var: Takes in a variable
    :param maxi: The maximum length desired for the variable
    :return: Returns boolean depending on whether the variable's length is less than or equal to desired length
    """
    return len(var) <= maxi


def float41_checker(num):
    """
    This function checks if a given number is a float, speficially one that only has one number after
    the decimal point. 123.4 would return True, while 123.45 would return false. Useful because the SQL
    database has fields setup to hold data in this format only
    :param num: Takes in a number
    :return: Returns True if variable is indeed a float with one number after the decimal, False if not
    """
    if float_checker(num) and max_length_checker(num, 5):
        if max_length_checker(str(float(num)).split('.')[1], 1):
            return True
        else:
            return False
    else:
        return False


def time_checker(var):
    """
    Checks that variable is a factor of time (hours, minutes or seconds). Verified by the variable being
    an int, using the int_checker function, and is of length 2, using the length_checker function. 02 could
    be a 2 hours, 2 minutes, or 2 seconds, and would return True. 2h is not an int, and could not be a factor
    of time, and would return False
    :param var:
    :return: Returns bollean depending on whether the variable is indeed a factor or time
    """
    if int_checker(var) and length_checker(var, 2):
        return True
    else:
        return False


def get_time(w_r):
    """
    This functions collects time data from the user, in the form of hours, minutes, depending on the time's
    eventual use, seconds. Each factor of the time is validated, and if an invalid entry is made, the user
    will be prompted to try until they enter valid data.
    :param w_r: 'w', 'r'. This attribute determines whether the time is for logging weight or runs. Weight
    result in the time being a time of day (5:00:00 or 17:30:00) while Run would result in the time being
    a time as if from a stop watch (01:12:23).
    :return: Returns the entered time as string
    """
    while True:
        try:
            hours = input('Input number of hours (hh): ')
            minutes = input('Input number of minutes(mm): ')
            if w_r == 'w':
                if time_checker(hours) and time_checker(minutes):
                    time = hours + ':' + minutes + ':00'
                    return time
                else:
                    raise ValueError
            seconds = input('Input number of seconds(ss): ')
            times = [hours, minutes, seconds]
            for t in times:
                if time_checker(t):
                    continue
                else:
                    raise ValueError
            return times
        except ValueError:
            print('Input again, using only numbers and two digits for each\n')
            continue


def get_yn():
    """
    This function is used to obtain user approval at several different points in the program, most
    commonly to get their confirmation that data is correct before loading it into the database
    :return: Returns True for 'y' or False for 'n'
    """
    while True:
        try:
            y_n = input('Enter y/n: ')
            if y_n == 'y':
                return True
            if y_n == 'n':
                return False
            else:
                raise ValueError
        except ValueError:
            print('\nEnter only y/n\n')
            continue


def get_year():
    """
    This function obtains a year from the user in the process of contructing a data. Validates their input by
    verifying that the input is an integer and of length 4. If not, the user is prompted to keep trying until the
    input is of the correct format
    :return: Returns the user-inputted year once validated
    """
    while True:
        try:
            year = input('Please input the year (YYYY): ')
            if length_checker(year, 4) and int_checker(year):
                return year
            else:
                raise ValueError
        except ValueError:
            print('\n\n\nPlease try again, using (YYYY) format\n')


def get_month():
    """
    This function obtains a month from the user in the process of contructing a data. Validates their input by
    verifying that the input is an integer and of length 2. If not, the user is prompted to keep trying until the
    input is of the correct format
    :return: Returns the user-inputted month once validated
    """
    while True:
        try:
            month = input('Please input the month (MM): ')
            if length_checker(month, 2) and int_checker(month):
                return month
            else:
                raise ValueError
        except ValueError:
            print('\n\n\nPlease try again, using (MM) format\n')


def get_day():
    """
   This function obtains a day from the user in the process of contructing a data. Validates their input by
   verifying that the input is an integer and of length 2. If not, the user is prompted to keep trying until the
   input is of the correct format
   :return: Returns the user-inputted day once validated
   """
    while True:
        try:
            day = input('Please input the day (DD): ')
            if length_checker(day, 2) and int_checker(day):
                return day
            else:
                raise ValueError
        except ValueError:
            print('\n\n\nPlease try again, using (DD) format\n')


def get_date():
    """
    This function constructs a datetime instance holding a user-inputted date. In the event that the user would
    like to use the current day for their SQL insert, then datetime.date.today() is returned. If they would like
    to use another date in their insert statement, then the year, month, and day of the instance are obtained
    through the get_year, get_month, and get_day functions. If the date is not valid, then the user is prompted
    to try again until they enter a valid date
    :return: Returns the datetime instance containing the user-selected date
    """
    while True:
        try:
            print('Are you logging results for today\'s date?')
            necessary = get_yn()
            if necessary:
                return datetime.date.today()
            if not necessary:
                year = get_year()
                month = get_month()
                day = get_day()
                date = "{}-{}-{}".format(year, month, day)
                date_obj = datetime.datetime.strptime(date, '%Y-%m-%d').date()
                return date_obj
        except ValueError:
            print('\n\nNot a valid date, please try again.\n')

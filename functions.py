
# Checks if number can be converted into int
def int_checker(num):
    result = False
    try:
        int(num)
        result = True
    except ValueError:
        pass
    return result

def name_converter(string):
    string = string.replace('_', ' ')
    string = string.replace('-', ' ')
    return string

def check_if_in_list(var, lst):
    if var in lst:
        return True
    else:
        return False

def float_checker(num):
    result = False
    try:
        float(num)
        result = True
    except ValueError:
        pass
    return result

def length_checker(var, needed_len):
    return len(var) == needed_len

def max_length_checker(var, maxi):
    return len(var) <= maxi

def float41_checker(num):
    if float_checker(num) and max_length_checker(num, 5):
        if max_length_checker(str(float(num)).split('.')[1], 1):
            return True
        else:
            return False
    else:
        return False

def time_checker(var):
    if int_checker(var) and length_checker(var, 2):
        return True
    else:
        return False

def get_time(w_r):
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
            times = []
            times.extend([hours, minutes, seconds])
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
    while True:
        try:
            y_n = input('Enter y/n: ')
            if y_n == 'y' or y_n == 'n':
                return y_n
            else:
                raise ValueError
        except ValueError:
            print('\nEnter only y/n\n')
            continue

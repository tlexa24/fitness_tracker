
# Checks if number can be converted into int
def int_checker(num):
    result = False
    try:
        int(num)
        result = True
    except ValueError:
        pass
    return result

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

def max_length(var, maxi):
    return len(var) <= maxi

def float41_checker(num):
    if float_checker(num) and max_length(num, 5) and max_length(num.split('.')[1], 1):
        return True
    else:
        return False

def run_time_checker(var):
    if int_checker(var) and length_checker(var, 2):
        return True
    else:
        return False

def get_run_time():
    while True:
        try:
            hours = input('Input number of hours (hh): ')
            minutes = input('Input number of minutes(mm): ')
            seconds = input('Input number of seconds(ss): ')
            times = []
            times.extend([hours, minutes, seconds])
            for t in times:
                if run_time_checker(t):
                    continue
                else:
                    raise ValueError
            time = ':'.join(times)
            return time
        except ValueError:
            print('Input again, using only numbers and two digits for each\n')
            continue

def get_miles():
    while True:
        try:
            miles = input('How many miles (xxx.x): ')
            if float41_checker(miles):
                return str(miles)
            else:
                raise ValueError
        except ValueError:
            print('Input again, using only numbers in xxx.x format:\n')
            continue

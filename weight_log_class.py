import main
import functions
import datetime

def get_weight():
    while True:
        try:
            weight = input('Enter the correct weight(xxx.x): ')
            if functions.float41_checker(weight):
                return str(weight)
            else:
                raise ValueError
        except ValueError:
            print('Input again, using only numbers in xxx.x format:\n')
            continue

def get_bf():
    while True:
        try:
            bf = input('Enter the body fat % in xx.x format: ')
            if functions.float41_checker(bf):
                return str(bf)
            else:
                raise ValueError
        except ValueError:
            print('Input again, using only numbers in xxx.x format:\n')
            continue

def create_weight_instance():
    date_object = str(datetime.date.today())
    time = functions.get_time_of_day()
    wt = get_weight()
    bodyfat = get_bf()
    print('Did you lift yesterday?')
    lift_question = functions.get_yn()
    print('Did you run yesterday?')
    run_question = functions.get_yn()
    waight = Weight(date_object, time, wt, bodyfat, lift_question, run_question)
    return waight

class Weight:
    def __init__(self, d, t, wt, b, lft, r):
        self.date = d
        self.time = t
        self.weight = wt
        self.bodyfat = b
        self.lift = lft
        self.run = r

    def insert(self):
        conn = main.connection
        with conn.cursor() as cursor:
            sql = "INSERT INTO weight_log VALUES ('" + self.date + "', '" + self.time + "', '" + self.weight + "', '" \
                  + self.bodyfat + "', '" + self.lift + "', '" + self.run + "')"
            print('\n\n\nTime: ' + self.time + '\nWeight: ' + self.weight + '\nBody Fat: ' + self.bodyfat + '\nLift? ' +
                  self.lift + '\nRun? ' + self.run + '\nIs this info correct?')
            confirm = functions.get_yn()
            if confirm == 'y':
                cursor.execute(sql)
                conn.commit()
                print('Weight data successfully inserted')
                conn.close()
            else:
                print('Please retry with correct info')
                return ''

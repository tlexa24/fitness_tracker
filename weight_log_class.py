import main
import functions
import datetime

def create_weight_instance():
    date_object = str(datetime.date.today())
    time = functions.get_time_of_day()
    wt = functions.get_weight()
    bodyfat = functions.get_bf()
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

import mysql_connections
import functions
import datetime

def get_diet():
    while True:
        try:
            calories = input('Input today\'s calories: ')
            carb = input('Input today\'s carbs: ')
            fat = input('Input today\'s fat: ')
            protein = input('Input today\'s protein: ')
            diet_info = [calories, carb, fat, protein]
            for d in diet_info:
                if functions.int_checker(d):
                    continue
                else:
                    raise ValueError
            return diet_info
        except ValueError:
            print('\n\nInput again, using only numbers.\n')

def create_diet_instance():
    day = str(datetime.date.today())
    diet = get_diet()
    diet_obj = Diet(day, diet[0], diet[1], diet[2], diet[3])
    return diet_obj

class Diet:
    def __init__(self, date, cals, carbs, fats, proteins):
        self.date = date
        self.cals = cals
        self.carbs = carbs
        self.fats = fats
        self.proteins = proteins

    def insert_to_sql(self):
        conn = mysql_connections.connection
        with conn.cursor() as cursor:
            sql = "INSERT INTO diet_log VALUES ('" + self.date + "', '" + self.cals \
                  + "', '" + self.carbs + "', '" + self.fats + "', '" + self.proteins + "')"
            print('\n\n\nCalories: ' + self.cals + '\nCarbs: ' + self.carbs + '\nFats: '
                  + self.fats + '\nProteins: ' + self.proteins + '\nIs this info correct?')
            confirm = functions.get_yn()
            if confirm == 'y':
                cursor.execute(sql)
                conn.commit()
                print('Diet data successfully inserted')
                conn.close()
            else:
                print('Please retry with correct info')
                return ''

def create_insert_diet():
    diet = create_diet_instance()
    diet.insert_to_sql()

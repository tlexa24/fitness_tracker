import mysql_connections
import functions
from urllib import request, error
import myfitnesspal
import urllib3.exceptions
import socket
import requests

def connect():
    try:
        request.urlopen('http://google.com')
        return True
    except error.URLError:
        return False

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

def my_fitness_pal(date):
    year, month, day = date.year, date.month, date.day
    try:
        client = myfitnesspal.Client('tlexa2497@gmail.com')
        day = client.get_date(year, month, day)
        diet = day.totals
        print('Successfully pulled information from MyFitnessPal')
        return [int(diet['calories']), int(diet['carbohydrates']), int(diet['fat']), int(diet['protein'])]
    except socket.gaierror:
        return None
    except urllib3.exceptions.NewConnectionError:
        return None
    except urllib3.exceptions.MaxRetryError:
        return None
    except requests.exceptions.ConnectionError:
        return None

def create_diet_instance():
    day = functions.get_date()
    if connect():
        diet = my_fitness_pal(day)
        if diet is not None:
            diet_obj = Diet(day, diet[0], diet[1], diet[2], diet[3])
            return diet_obj
        print('\n\nCould not connect to MyFitnessPal, please input manually.\n')
    diet = get_diet()
    diet_obj = Diet(str(day), diet[0], diet[1], diet[2], diet[3])
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
            sql = "INSERT INTO diet_log VALUES ('{}', '{}', '{}', '{}', '{}')".format(self.date, self.cals,
                                                                                      self.carbs, self.fats,
                                                                                      self.proteins)
            print('\n\nDate: {}\nCals: {}\nCarbs: {}\nFats: {}\nProteins: {}\nIs this info correct?'.format(
                                                                                                    self.date,
                                                                                                    self.cals,
                                                                                                    self.carbs,
                                                                                                    self.fats,
                                                                                                    self.proteins))
            confirm = functions.get_yn()
            if confirm == 'y':
                cursor.execute(sql)
                conn.commit()
                print('\n\nDiet data successfully inserted to SQL')
                conn.close()
            else:
                print('Please retry with correct info')
                return 'n'

def create_insert_diet():
    diet = create_diet_instance()
    diet.insert_to_sql()

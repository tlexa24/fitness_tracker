
import pymysql.cursors
import pandas as pd
import datetime
import run_log_class
import functions
# date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
# print("date and time:",date_time)


pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
connection = pymysql.connect(host='localhost', user='root', password='troopsix', db='fitness', charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

if __name__ == '__main__':
    while True:
        print('1. Log lift \n'
              '2. Log run \n'
              '3. Log weight \n'
              '4. Log diet\n'
              '5. Get exercise routine for next 4 days\n'
              '6. View information')
        choice = input('Enter one of the numbers above: ')
        try:
            if int(choice) in range(1, 6):
                break
            else:
                raise ValueError
        except ValueError:
            print("\nI said one of those numbers dumbass\n")
            continue
    # if choice == 1:
    if choice == 2:
        date_object = str(datetime.date.today())
        time = functions.get_run_time()
        miles = functions.get_miles()
        run = run_log_class.Run(date_object, miles, time)
        run.insert()
    # if choice == 3:
    # if choice == 4:
    # if choice == 5:
    # if choice == 6:

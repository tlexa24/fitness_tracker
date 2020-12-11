import pymysql.cursors
import run_log_class
import weight_log_class
import diet_log_class
import lift_log

connection = pymysql.connect(host='localhost', user='root', password='troopsix', db='fitness', charset='utf8mb4',
                             cursorclass=pymysql.cursors.Cursor)

connectiondict = pymysql.connect(host='localhost', user='root', password='troopsix', db='fitness', charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

def initial_choice():
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
            print("\nOnly enter one of the following numbers.\n")
            continue
    return choice

def start_program():
    choice = initial_choice()
    if choice == '1':
        lift_log.create_insert_lift()
    if choice == '2':
        run_log_class.create_insert_run()
    if choice == '3':
        weight_log_class.create_insert_weight()
    if choice == '4':
        diet_log_class.create_insert_diet()
    # if choice == '5':
    # if choice == '6':

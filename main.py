
import pymysql.cursors
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

if __name__ == '__main__':
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='troopsix',
                                 db='fitness',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    while True:
        print('\n1. Log lift \n2. Log run \n3. Log weight \n4. Log diet\n5. View information')
        choice = input('Enter one of the numbers above: ')
        try:
            if int(choice) in range(1, 6):
                break
            else:
                raise ValueError
        except ValueError:
            print("\nI said one of those numbers dumbass\n")
            continue

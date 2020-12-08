# syntax of insert:
# sql = "INSERT INTO `table_name` (column_names) VALUES (%s, %s)"
#
#         cursor.execute(sql, (values))

import pymysql.cursors

# def sql_insert(table,):
#     try:
#         with connection.cursor() as cursor:
#             # Read a single record
#             sql = "SELECT `*`, `current_highest` FROM `exercises`"
#             cursor.execute(sql)
#             result = cursor.fetchall()
#             print(result)
#     print('r')
connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='troopsix',
                                 db='fitness',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
try:
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `*`, `current_highest` FROM `exercises`"
        cursor.execute(sql)
        result = cursor.fetchone()
        columns = tuple([key for key in result.keys()])
        print(columns)
finally:
    connection.close()
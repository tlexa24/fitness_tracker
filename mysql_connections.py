import pymysql.cursors

connection = pymysql.Connect(host='localhost', user='root', password='Sou37LKs5',
                             db='fitness', charset='utf8mb4',
                             cursorclass=pymysql.cursors.Cursor)

connectiondict = pymysql.Connect(host='localhost', user='root', password='Sou37LKs5',
                                 db='fitness', charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

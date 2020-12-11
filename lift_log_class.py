import main

class Lift:
    def __init__(self, date, exercise_id, weight, setno, reps):
        self.date = date
        self.ID = exercise_id
        self.weight = weight
        self.set = setno
        self.reps = reps

    def insert(self):
        conn = main.connection
        with conn.cursor() as cursor:
            sql = "INSERT INTO lift_log VALUES ('{}', '{}', '{}', '{}', '{}');".format(self.date, self.ID,
                                                                                       self.weight, self.set, self.reps)
            cursor.execute(sql)
            conn.commit()

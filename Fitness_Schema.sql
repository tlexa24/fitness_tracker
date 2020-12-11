DROP SCHEMA IF EXISTS fitness;
CREATE SCHEMA IF NOT EXISTS `fitness` DEFAULT CHARACTER SET utf8 ;
USE `fitness` ;

CREATE TABLE Run (
date_recorded DATE NOT NULL,
miles FLOAT(3, 1) NOT NULL,
run_time TIME NOT NULL,
PRIMARY KEY (date_recorded)
);

CREATE TABLE Weigh_In(
date_recorded DATE NOT NULL,
time_recorded TIME NOT NULL,
weight FLOAT(4, 1) NOT NULL,
lift_yesterday ENUM('Yes', 'No') NOT NULL,
run_yesterday ENUM('Yes', 'No') NOT NULL,
PRIMARY KEY (date_recorded)
);

CREATE TABLE Diet(
date_recorded DATE NOT NULL,
calories INT NOT NULL,
carbs INT NOT NULL,
fats INT NOT NULL,
proteins INT NOT NULL,
PRIMARY KEY (date_recorded)
);

CREATE TABLE programs(
program_name VARCHAR(255) NOT NULL,
program_ID INT NOT NULL,
PRIMARY KEY (program_ID)
);
INSERT INTO programs VALUES ('push-pull-legs progression', 1);

CREATE TABLE exercises(
exercise_ID INT NOT NULL,
exercise_name VARCHAR(244) NOT NULL,
weight_progressor INT NOT NULL,
PRIMARY KEY (exercise_ID)
);

CREATE TABLE routines(
routine_ID INT NOT NULL AUTO_INCREMENT,
routine_name VARCHAR(30) NOT NULL,
program_ID INT NOT NULL,
order_in_program INT NOT NULL UNIQUE,
PRIMARY KEY (routine_ID),
FOREIGN KEY (program_ID) REFERENCES programs(program_ID)
);

CREATE TABLE exercises_in_routines(
routine_ID INT,
exercise_ID INT NOT NULL,
sets INT NOT NULL,
reps INT NOT NULL,
last_set_AMRAP ENUM('yes', 'no') NOT NULL,
PRIMARY KEY (routine_ID, exercise_ID),
FOREIGN KEY (routine_ID) REFERENCES routines(routine_ID),
FOREIGN KEY (exercise_ID) REFERENCES exercises(exercise_ID)
);

CREATE TABLE lift_log(
date_recorded DATE NOT NULL,
exercise_ID INT NOT NULL,
routine_ID INT NOT NULL,
weight FLOAT(4,1) NOT NULL,
set_no INT NOT NULL,
reps INT NOT NULL,
PRIMARY KEY (date_recorded, exercise_ID, set_no),
FOREIGN KEY (routine_ID) REFERENCES routines(routine_ID),
FOREIGN KEY (exercise_ID) REFERENCES exercises(exercise_ID)
);


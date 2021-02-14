create table diet_log
(
    date_recorded date not null
        primary key,
    calories      int  not null,
    carbs         int  not null,
    fats          int  not null,
    proteins      int  not null
)
    charset = utf8;

create table exercises
(
    exercise_ID       int                     not null
        primary key,
    exercise_name     varchar(244)            not null,
    weight_progressor int                     not null,
    current_weight    float(4, 1) default 0.0 not null
)
    charset = utf8;

create table lift_log
(
    date_recorded date        not null,
    routine_ID    int         not null,
    exercise_ID   int         not null,
    weight        float(4, 1) not null,
    set_no        int         not null,
    reps          int         not null,
    primary key (date_recorded, exercise_ID, set_no),
    constraint lift_log_ibfk_2
        foreign key (exercise_ID) references exercises (exercise_ID)
)
    charset = utf8;

create index exercise_ID
    on lift_log (exercise_ID);

create table programs
(
    program_name varchar(255) not null,
    program_ID   int          not null
        primary key
)
    charset = utf8;

create table routines
(
    routine_ID   int auto_increment
        primary key,
    routine_name varchar(30) not null,
    program_ID   int         not null,
    constraint routines_ibfk_1
        foreign key (program_ID) references programs (program_ID)
)
    charset = utf8;

create table exercises_in_routines
(
    routine_ID     int                not null,
    exercise_ID    int                not null,
    sets           int                not null,
    reps           int                not null,
    last_set_AMRAP enum ('yes', 'no') not null,
    exercise_order int                not null,
    primary key (routine_ID, exercise_order),
    constraint exercises_in_routines_ibfk_1
        foreign key (routine_ID) references routines (routine_ID),
    constraint exercises_in_routines_ibfk_2
        foreign key (exercise_ID) references exercises (exercise_ID)
)
    charset = utf8;

create index exercise_ID
    on exercises_in_routines (exercise_ID);

create table program_schedule
(
    program_ID      int                not null,
    day_of_week     int                not null,
    lifting_routine int                null,
    ab_routine      int                null,
    run             enum ('yes', 'no') not null,
    primary key (program_ID, day_of_week),
    constraint program_schedule_ibfk_1
        foreign key (program_ID) references programs (program_ID),
    constraint program_schedule_ibfk_2
        foreign key (lifting_routine) references routines (routine_ID)
)
    charset = utf8;

create index program_ID
    on routines (program_ID);

create table run_log
(
    date_recorded date        not null
        primary key,
    miles         float(4, 1) not null,
    run_time      time        not null
)
    charset = utf8;

create table weight_log
(
    date_recorded  date            not null
        primary key,
    weight         float(4, 1)     not null,
    body_fat       float(4, 1)     not null,
    run_yesterday  enum ('y', 'n') not null,
    lift_yesterday enum ('y', 'n') not null
)
    charset = utf8;



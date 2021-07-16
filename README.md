# Health Tracker

A Python interface for a custom MySQL database, designed for personal tracking of fitness information (including weightlifting results, dietary information, weight/bodyfat tracking, and cardio results). 

## Frameworks
The program uses the below Python frameworks, and they must be installed in order for the program to function.


* PyMySQL
* Pandas
* itertools
* datetime
* urllib
* MyFitnessPal [Created by coddingtonbear](https://github.com/coddingtonbear/python-myfitnesspal)

## The Program
The idea behind this program first came up when I started a new weightlifting routine that utilizes linear progression. In other words, if you complete the planned amount of reps at a certain weight, then for the next workout, that exercise will be done at a higher weight, increasing a constant amount every time you are successful at this exercise is successful. 

I first created the database to store information related to this type of program, and then wrote the python script to interact with the database. I quickly decided that the final program had the potential to track much more than just weightlifting results.

## Functionality
### Weightlifting Tracking

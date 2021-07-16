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

The program is based around a command line interface once the starter.py script is ran. While this program is only for myself at the moment, I created the command line interface to be used by someone without knowledge of the program's logic. This is done with thorough validation of all user inputs. Every single time that the user inputs data, the program verifies that the entry is in the correct format, and if not, it informs the user of the correct format and prompts them to try again until their entry is valid


## Functionality
### Weightlifting Tracking
The centerpoint of the program. Based on lifting routines present in the user's current workout program, the user will be prompted to enter the results of their workout. The weight at which they should have attempted their exercises will be presented to the user, but if they elected to use a different weight, the program will take this into account and alter the database to reflect the change. After collecting the user's results, the program will determine which exercises, if any, were successful and then make appropriate updates to the expected weight used for the next workout. 

### Schedule Creation
Creates the user's exercise schedule for the next day. The program will search through the database to determine the last day of the user's program schedule that was completed, and then automatically finds the next day in the schedule. Once the day is found, multiple functions are used to format the schedule and eventually print it to the user, including the lifting routine (if any), abdominal routine (if any), and whether the user has a scheduled run or not.

### Run Logging
Allows users to input runs they go on, with collection of the number of miles, time it took, and the date that the run was completed on. 

### Diet Logging
This allows users to input the amount of calories, carbs, fats, and proteins they consumed on a given day. This information can either be captured manually through the CLI or by using the MyFitnessPal Python module. In fact, the program defaults to using MyFitnessPal, but will resort to manual collection should an internet connection not be present. 

### Weight/Bodyfat logging
This allows users to log in their weight and bodyfat percentage, along with the date and time of day. Users can see how their data changes over time, and also based on the time of day at which they measure. 


## Planned Updates
While this program is currently functional for its purpose, I plan to make several major additions in the coming months. 

Some ideas for future expansion (in order of priority):

* Add functionality to review historical data. At the moment, I am viewing my past results through SQL queries in my database client, without an option to do so in the python program. This is my next step, as storing the data is meaningless without an easy way to retrieve it. 
* Move from a command line interface to web app. This would be the first major step to making the program more accessible to others besides myself
* Add support for different workout programs, including those which do not revolve around a linear progression of weights
* A bit of a stretch goal at the moment, but I would love to begin developing a mobile app that could be used as an alternative to the CLI/future web app to log data

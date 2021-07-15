
# This file coordinates the entire program, having the user input what type
# of action they would like to take, and calling appropriate functions/methods
# to accomodate

import log_runs
import log_weight
import log_diet
import log_lifts
import create_schedule


def initial_choice():
    """
    This function provides a list of possible actions to the user. They enter a number
    corresponding to their choice. Verifies their number  is indeed an option to them,
    and if not, they must try again.
    :return: The number corresponding to their choice is returned
    """
    while True:
        print('1. Log lift \n'
              '2. Log run \n'
              '3. Log weight \n'
              '4. Log diet\n'
              '5. Get schedule for tomorrow')
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


def start_program(choice):
    """
    This function takes in the choice made by the user in the initial_choice function.
    Uses this choice to kickstart whatever file corresponds to their choice.
    :param choice: The action the user decided to undertake
    """
    if choice == '1':
        log_lifts.create_insert_lift()
    if choice == '2':
        run_log = log_runs.RunLog()
        run_log.insert_to_sql()
    if choice == '3':
        weight_log = log_weight.WeightLog()
        weight_log.insert_to_sql()
    if choice == '4':
        diet_log = log_diet.DietLog()
        diet_log.insert_to_sql()
    if choice == '5':
        create_schedule.print_schedule()


if __name__ == '__main__':
    desired_action = initial_choice()
    start_program(desired_action)

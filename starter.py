import log_runs
import log_weight
import log_diet
import log_lifts
import create_schedule

def initial_choice():
    print('while true')
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
        log_lifts.create_insert_lift()
    if choice == '2':
        log_runs.create_insert_run()
    if choice == '3':
        log_weight.create_insert_weight()
    if choice == '4':
        log_diet.create_insert_diet()
    if choice == '5':
        create_schedule.print_schedule()
    # if choice == '6':

import dateutil.parser
import datetime
import sqlite3
import sys
from aux import do_you_want_to_continue_bb

def insert_r_info():

    # shitty thing to show prompts, I couldn't come up with a better way to do it
    # pls no bully
    if sys.stdin.isatty():
        prompt = {'day': 'Día: ', 'day_sleeptime': 'Tiempo de Sueño: ', 'day_comment': 'Comentario: ', 'food_type': 'Tipo de Comida: '}
    else:
        prompt = {'day': '', 'day_sleeptime': '', 'day_comment': '', 'food_type': ''}

    # get the day we are adding
    try:
        day = None
        day = dateutil.parser.parse(input(prompt['day'])).date()
    except ValueError:
        raise
    except EOFError:
        raise

    try:
        # sleeping time
        try:
            day_sleeptime = None
            day_sleeptime = float(input(prompt['day_sleeptime']))
        except ValueError:
            pass
    
        # comment for the day
        day_comment = None
        day_comment = input(prompt['day_comment'])

        # types of food you eated that day
        food_type = do_you_want_to_continue_bb(get_food, arguments=[day, prompt['food_type']], prompt="Otra Comida?")

    except EOFError:
        pass

    # databse
    try:
        with sqlite3.connect(sys.argv[1]) as conn:
            conn.execute("INSERT INTO day(date, sleep_time, comment) VALUES(?, ?, ?)", (day, day_sleeptime, day_comment,))
            if food_type: conn.executemany("INSERT INTO daily_menu(day_id, food_id) VALUES(?, ?)", food_type)

    except IndexError:
        print("You should provide a database to save the data", file=sys.stderr)
        exit(2)


def get_food(day, prompt):
    food = input(prompt).lower()
    return (day, food)


if __name__ == '__main__':
    do_you_want_to_continue_bb(insert_r_info, prompt="Otro día?")

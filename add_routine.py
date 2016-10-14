import dateutil.parser
import sqlite3
import sys
from aux import do_you_want_to_continue_bb

def insert_r_info():
    day_date, day_sleeptime, day_comment, food_name, food_comment = None, None, None, None, None

    # shitty thing to show prompts, I couldn't come up with a better way to do it
    # pls no bully
    if sys.stdin.isatty():
        prompt = {'day_date': 'date: ', 'day_sleeptime': 'sleep time: ', 'day_comment': 'comment for date: ', 'food_name': 'food: ', 'food_comment': 'comment for food: '}
    else:
        prompt = {'day_date': '', 'day_sleeptime': '', 'day_comment': '', 'food_name': '', 'food_comment': ''}


    try:
        day_date = dateutil.parser.parse(input(prompt['day_date']))
    except ValueError:
        raise
    except EOFError:
        raise

    try:
        try:
            day_sleeptime = float(input(prompt['day_sleeptime']))
        except ValueError:
            pass

        day_comment = input(prompt['day_comment'])

        try:
            food_name = input(prompt['food_name']).lower()
        except:
            raise

        food_comment = input(prompt['food_comment'])

    except EOFError:
        pass

    # databse
    try:
        with sqlite3.connect(sys.argv[1]) as conn:
            conn.execute("INSERT INTO day(date, sleep_time, comment) VALUES(?, ?, ?)", (day_date, day_sleeptime, day_comment,))
            if food_name: conn.execute("INSERT INTO food(name, comment) VALUES(?, ?)", (food_name, food_comment,))

    except IndexError:
        print("You should provide a database to save the data", file=sys.stderr)
        exit(2)


if __name__ == '__main__':
    do_you_want_to_continue_bb(insert_r_info)

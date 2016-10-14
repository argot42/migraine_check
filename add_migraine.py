import dateutil.parser
import sqlite3
import sys
from aux import do_you_want_to_continue_bb

def insert_m_info():
    ''' Function to insert a migraine into the database '''

    start, end, intensity, duration, comment = None, None, None, None, None

    # shitty thing to show prompts, I couldn't come up with a better way to do it
    # pls no bully
    if sys.stdin.isatty():
        prompt = {'start': 'Inicio: ', 'end': 'Fin: ', 'intensity': 'Intensidad: ', 'comment': 'Comentario: '}
    else:
        prompt = {'start': '', 'end': '', 'intensity': '', 'comment': ''}

    # get start
    try:
        start = dateutil.parser.parse(input(prompt['start']))
    except ValueError:
        print("start is mandatory, please provide a correct value.", file=sys.stderr)
        exit(2)
    except EOFError:
        print("start is mandatory, please provide a correct value.", file=sys.stderr)
        exit(2)

    try:
        # get end
        try:
            end = dateutil.parser.parse(input(prompt['end']))
            duration = (end - start).total_seconds()
        except ValueError:
            pass

        # get intensity
        try:
            intensity = int(input(prompt['intensity']))
        except ValueError:
            pass

        # get comments
        comment = input(prompt['comment'])

    except EOFError:
        pass

    # open database
    try:
        with sqlite3.connect(sys.argv[1]) as conn:
            conn.execute("INSERT INTO migraine(start, end, duration, intensity, comment) VALUES(?, ?, ?, ?, ?)", (start, end, duration, intensity, comment,))

    except IndexError:
        print("You should provide a database to save the data", file=sys.stderr)
        exit(2)

if __name__ == '__main__':
    do_you_want_to_continue_bb(insert_m_info)

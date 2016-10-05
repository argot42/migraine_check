import dateutil.parser
import sqlite3
import sys

def insert_m_info():
    start, end, intensity, duration, comment = None, None, None, None, None

    # get start
    try:
        start = dateutil.parser.parse(input())
    except ValueError:
        print("start is mandatory, please provide a correct value.", file=sys.stderr)
        exit(2)
    except EOFError as e:
        print("start is mandatory, please provide a correct value.", file=sys.stderr)
        exit(2)

    try:
        # get end
        try:
            end = dateutil.parser.parse(input())
            duration = (end - start).total_seconds()
        except ValueError:
            pass

        # get intensity
        try:
            intensity = int(input())
        except ValueError:
            pass

        # get comments
        comment = input()

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
    insert_m_info()

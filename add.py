import dateutil.parser
import sqlite3
import sys

def getinfo():
    start, end, intensity, duration = None, None, None, None

    # get start
    try:
        start = dateutil.parser.parse(input())
    except ValueError:
        print("start is mandatory, please provide a correct value.", file=sys.stderr)
        exit(2)
    except EOFError as e:
        print("start is mandatory, please provide a correct value.", file=sys.stderr)
        exit(2)

    # get end
    try:
        end = dateutil.parser.parse(input())
        duration = (end - start).total_seconds()
    except ValueError:
        pass
    except EOFError:
        pass

    try:
        intensity = int(input())
    except ValueError:
        pass
    except EOFError:
        pass

    # open database
    try:
        conn = sqlite3.connect(sys.argv[1])
        with conn:
            conn.execute("INSERT INTO migraine_day(start, end, duration, intensity) VALUES(?, ?, ?, ?)", (start, end, duration, intensity,))

    except IndexError:
        print("You should provide a database to save the data", file=sys.stderr)
        exit(2)

if __name__ == '__main__':
    getinfo()

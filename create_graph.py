import numpy as np
import datetime
import sys
import sqlite3
import bokeh.plotting, bokeh.models

def plot_migr_month(year):
    try:
            year_as_datetime = datetime.datetime.strptime(year, '%Y')
            migraine_per_month = get_migraine_year(year_as_datetime, sys.argv[1])
    except:
        raise

    bokeh.plotting.output_file("testu.html")

    # x axis
    x = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']

    # y axis
    # count of migraines per month
    y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in migraine_per_month: 
        migrained = datetime.datetime.strptime(i[0], "%Y-%m-%d %H:%M:%S")
        y[migrained.month - 1] += 1

    # source for tooltip and plot
    # process daily info
    diet, sleeptime, comment = get_dailyinfo_year(year_as_datetime, sys.argv[1])
    source = bokeh.plotting.ColumnDataSource(
            data=dict(
                x=x,
                y=y,
            )
        )

    # Hover tool
    hover = bokeh.models.HoverTool(
            tooltips=[
                ("month", "@x"),
                ("quantity", "@y"),
            ]
        )

    p = bokeh.plotting.figure(plot_width=1200, plot_height=900, x_range=x, tools=[hover], title="Migrañas por Mes")

    p.line(x, y, line_width=2)
    p.circle('x', 'y', fill_color="white", size=8, alpha=0.5, source=source)
    bokeh.plotting.show(p)

def get_migraine_year(year, db):

    with sqlite3.connect(db) as conn:
        # get migraines between year and year++
        res = conn.execute("SELECT start, duration, intensity, comment FROM migraine WHERE start >= date(?) AND start < date(?)", \
                (year.isoformat(), (year+datetime.timedelta(days=365)).isoformat()))

        return res.fetchall()

    
def get_dailyinfo_year(year, db):

    with sqlite3.connect(db) as conn:
        # get daily info between year and year++
        res = conn.execute("SELECT day.date, day.sleep_time, day.comment, food.type FROM day LEFT OUTER JOIN daily_menu ON day.date = daily_menu.day_id LEFT OUTER JOIN food ON daily_menu.food_id = food.id WHERE day.date >= date(?) AND day.date < date(?)", \
                (year.isoformat(), (year + datetime.timedelta(days=365)).isoformat()))

        response_list = res.fetchall() 

    # organize info
    diet = [None, None, None, None, None, None, None, None, None, None, None, None] 
    food_type_total = [None, None, None, None, None, None, None, None, None, None, None, None]  
    comment = [None, None, None, None, None, None, None, None, None, None, None, None] 
    sleeptime = [None, None, None, None, None, None, None, None, None, None, None, None]

    #for n in range(len(response_list)):
    for row in response_list:
        date = datetime.datetime.strptime(row[0], "%Y-%m-%d")

        # counting type of food
        try:
            diet[date.month - 1][row[3]] += 1
        except TypeError:
            diet[date.month - 1] = {row[3]: 1}
        except KeyError:
            if not row[3]: continue
            diet[date.month - 1][row[3]] = 1

        # total food per month
        try:
            food_type_total[date.month - 1] += 1
        except TypeError:
            food_type_total[date.month - 1] = 1
        
        # adding comments
        comment[date.month - 1] = row[2]
        
        # couting sleeptime
        try:
            sleeptime[date.month - 1] += row[1]
        except TypeError:
            sleeptime[date.month - 1] = row[1]

    print(food_type_total)
    print(diet)
    # calculating type of food percentages
    for month in range(len(diet)): 
        try:
            for ftype in diet[month]:
                try:
                    diet[month][ftype] = diet[month][ftype] * 100 / food_type_total[month] #diet[month][ftype] * food_type_total[month] / 100
                except TypeError:
                    pass
        except TypeError:
            pass
    print(diet)
    exit()

    # calculating sleeptime percentages
    for month in range(len(sleeptime)):
        try:
            sleeptime[month] = sleeptime[month] * 30 * 8 / 100
        except TypeError:
            pass

    return diet, sleeptime, comment


if __name__ == '__main__':
    plot_migr_month('2016')

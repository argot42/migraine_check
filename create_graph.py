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
                **diet,
                sleeptime=sleeptime,
                comment=comment,
            )
        )

    # convert diet for hover tool
    diet4tooltip = tooltip_transform(diet) 
    # Hover tool
    hover = bokeh.models.HoverTool(
            tooltips=[
                ("Mes", "@x"),
                ("Migrañas", "@y"),
                ("Tiempo de Sueño", "@sleeptime"),
                ("Comentarios", "@comment"),
                *diet4tooltip
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
    diet = dict()
    total_diet = 30 * 3 * 2
    comment = [None, None, None, None, None, None, None, None, None, None, None, None]
    sleeptime = [None, None, None, None, None, None, None, None, None, None, None, None]
    good_sleep = 30 * 8

    for row in response_list:
        date = datetime.datetime.strptime(row[0], "%Y-%m-%d")

        # counting type of food
        if not row[3]: continue
        try:
            diet[row[3]][date.month - 1] += 1
        except KeyError:
            diet[row[3]] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            diet[row[3]][date.month - 1] += 1

        # adding comments
        comment[date.month - 1] = row[2]
        
        # couting sleeptime
        try:
            sleeptime[date.month - 1] += row[1]
        except TypeError:
            sleeptime[date.month - 1] = row[1]

    # calculating type of food percentages
    for _, month_list in diet.items():
        for month in range(len(month_list)):
            month_list[month] = month_list[month] * 100 / total_diet

    # calculating sleeping time percentages
    for month in range(len(sleeptime)):
        try:
            sleeptime[month] = sleeptime[month] * 100 / good_sleep
        except TypeError:
            continue

    return diet, sleeptime, comment


def tooltip_transform(diet):
    diet_tuple = list()
    for food in diet.keys():
        diet_tuple.append((food, '@'+food))
    
    return diet_tuple


if __name__ == '__main__':
    plot_migr_month('2016')

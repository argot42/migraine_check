import numpy as np
import datetime
import sys
import sqlite3
import math
import bokeh.plotting, bokeh.models

def plot_migr_month(start_year, end_year=None):
    try:
            startyear = datetime.datetime.strptime(start_year, '%Y')
            endyear = (end_year and datetime.datetime.strptime(end_year, '%Y')) or startyear
            migraines = get_migraine_year(startyear, endyear, sys.argv[1])
    except:
        raise

    bokeh.plotting.output_file("graph.html")

    # get x axis names
    x = getmonths(startyear.year, endyear.year)
    # get y axis values
    y, intensity = migraine_info(startyear.year, endyear.year, migraines)

    # source for tooltip and plot
    # process daily info
    #diet, sleeptime, comment = get_dailyinfo_year(startyear, sys.argv[1])

    source = bokeh.plotting.ColumnDataSource(
            data=dict(
                x=x,
                y=y,
                intensity=intensity,
                #**diet,
                #sleeptime=sleeptime,
                #comment=comment,
            )
        )

    # Hover tool
    hover = bokeh.models.HoverTool(
            tooltips=[
                ("Mes", "@x"),
                ("Migrañas", "@y"),
                ("Intensidad", "@intensity")
                ]
            )

    ## convert diet for hover tool
    #diet4tooltip = tooltip_transform(diet) 
    ## Hover tool
    #hover = bokeh.models.HoverTool(
    #        tooltips=[
    #            ("Mes", "@x"),
    #            ("Migrañas", "@y"),
    #            ("Tiempo de Sueño", "@sleeptime"),
    #            ("Comentarios", "@comment"),
    #            *diet4tooltip
    #        ]
    #    )

    p = bokeh.plotting.figure(plot_width=800, plot_height=600, x_range=x, tools=[hover], title="Migrañas por Mes")

    p.line(x, y, line_width=2)
    p.circle('x', 'y', fill_color="white", size=8, alpha=0.5, source=source)

    p.xaxis.major_label_orientation = math.pi/2
    bokeh.plotting.show(p)


def getmonths(syear, eyear):
    months = []
    for year in range(syear, eyear + 1):
        months.append("Enero " + str(year))
        months.append("Febrero " + str(year))
        months.append("Marzo " + str(year))
        months.append("Abril " + str(year))
        months.append("Mayo " + str(year))
        months.append("Junio " + str(year))
        months.append("Julio " + str(year))
        months.append("Agosto " + str(year))
        months.append("Septiembre " + str(year))
        months.append("Octubre " + str(year))
        months.append("Noviembre " + str(year))
        months.append("Diciembre " + str(year))

    return months


def migraine_info(syear, eyear, migraines):
    migraines_per_month = [0] * (12 * (eyear - syear + 1))
    intensity_per_month = [0] * (12 * (eyear - syear + 1))

    for migraine in migraines:
        # count migraine
        migrained = datetime.datetime.strptime(migraine[0], "%Y-%m-%d %H:%M:%S")
        migraines_per_month[migrained.month - 1 + (12 * (migrained.year - syear))] += 1

        # calculate total intensity
        intensity_per_month[migrained.month - 1 + (12 * (migrained.year - syear))] += migraine[2]   

    # calculate average intensity
    i=0
    for n_migraines in migraines_per_month:
        try:
            intensity_per_month[i] = intensity_per_month[i] / n_migraines
        except ZeroDivisionError:
            pass 
        i += 1

    return migraines_per_month, intensity_per_month


def get_migraine_year(syear, eyear, db):
    with sqlite3.connect(db) as conn:
        # get migraines between syear and eyear
        res = conn.execute("SELECT start, duration, intensity, comment FROM migraine WHERE start >= date(?) AND start < date(?)", \
                (syear.isoformat(), (eyear+datetime.timedelta(days=365)).isoformat()))

    return res.fetchall()

    
def get_dailyinfo_year(year, db):
    with sqlite3.connect(db) as conn:
        # get daily info between year and year++
        res = conn.execute("SELECT day.date, day.sleep_time, day.comment, food.type FROM day LEFT OUTER JOIN daily_menu ON day.date = daily_menu.day_id LEFT OUTER JOIN food ON daily_menu.food_id = food.type WHERE day.date >= date(?) AND day.date < date(?)", \
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
    plot_migr_month('2016', '2017')

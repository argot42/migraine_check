import numpy as np
from datetime import datetime
import sys
import sqlite3
import bokeh.plotting, bokeh.models

def plot_migr_month(year):
    try:
            year_as_datetime = datetime.strptime(year, '%Y')
            info = get_from_year(year_as_datetime, sys.argv[1])
    except:
        raise

    bokeh.plotting.output_file("testu.html")

    x = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    # count of migraines per month
    y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in info: 
        migrained = datetime.strptime(i[0], "%Y-%m-%d %H:%M:%S")
        y[migrained.month - 1] += 1

    print(y)
    # source for tooltip and plot
    source = bokeh.plotting.ColumnDataSource(
            data=dict(
                x=x,
                y=y,
            )
        )

    # Hover tool
    hover = bokeh.models.HoverTool(
            tooltips=[
                ("index", "$index"),
                ("x", "$x"),
            ]
        )

    p = bokeh.plotting.figure(plot_width=1200, plot_height=900, x_range=x, tools=[hover], title="Migraines per year")

    p.line(x, y, line_width=2)
    p.circle('x', 'y', fill_color="white", size=8, alpha=0.5, source=source)
    bokeh.plotting.show(p)

def get_from_year(year, db):
    with sqlite3.connect(db) as conn:
        res = conn.execute("SELECT start, duration, intensity, comment FROM migraine WHERE start >= date(?)", (year.year,))
        return res.fetchall()

    
if __name__ == '__main__':
    plot_migr_month('2016')

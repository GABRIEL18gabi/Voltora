from reportlab.graphics.shapes import Drawing, Line, String, Circle
from reportlab.lib import colors
import random


def create_sensor_graph(title, value, minimum, maximum):

    d = Drawing(500,180)

    d.add(
        String(
            160,
            160,
            title,
            fontSize=14,
            fillColor=colors.darkblue
        )
    )

    # Axes

    d.add(Line(50,30,450,30,strokeWidth=2))
    d.add(Line(50,30,50,140,strokeWidth=2))

    points=[]

    for i in range(12):

        noise=random.uniform(-5,5)

        v=max(minimum,min(maximum,value+noise))

        x=50+i*35

        y=30+((v-minimum)/(maximum-minimum))*100

        points.append((x,y))

    for i in range(len(points)-1):

        x1,y1=points[i]
        x2,y2=points[i+1]

        d.add(
            Line(
                x1,
                y1,
                x2,
                y2,
                strokeColor=colors.HexColor("#1565C0"),
                strokeWidth=2
            )
        )

    for x,y in points:

        d.add(
            Circle(
                x,
                y,
                3,
                fillColor=colors.red
            )
        )

    return d
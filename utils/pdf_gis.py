from reportlab.graphics.shapes import (
    Drawing,
    Circle,
    Line,
    String,
    Rect
)
from reportlab.lib import colors


def create_gis_map(df):

    drawing = Drawing(560, 420)

    # =====================================
    # Title
    # =====================================

    drawing.add(
        String(
            145,
            395,
            "TAMIL NADU SMART GRID GIS",
            fontSize=18,
            fillColor=colors.darkblue
        )
    )

    # =====================================
    # Border
    # =====================================

    drawing.add(
        Rect(
            20,
            20,
            520,
            350,
            fillColor=None,
            strokeColor=colors.grey,
            strokeWidth=1
        )
    )

    # =====================================
    # Manual Layout
    # =====================================

    positions = {

        "Chennai":(420,320),

        "Salem":(300,240),

        "Coimbatore":(170,170),

        "Erode":(220,200),

        "Tiruppur":(200,140),

        "Tiruchirappalli":(330,160),

        "Thanjavur":(380,130),

        "Madurai":(300,90),

        "Tirunelveli":(310,45),

        "Kanyakumari":(315,20)

    }

    # =====================================
    # Transmission Lines
    # =====================================

    connections=[

        ("Chennai","Salem"),

        ("Salem","Coimbatore"),

        ("Salem","Erode"),

        ("Erode","Tiruppur"),

        ("Salem","Tiruchirappalli"),

        ("Tiruchirappalli","Thanjavur"),

        ("Tiruchirappalli","Madurai"),

        ("Madurai","Tirunelveli"),

        ("Tirunelveli","Kanyakumari")

    ]

    for c1,c2 in connections:

        x1,y1=positions[c1]
        x2,y2=positions[c2]

        drawing.add(

            Line(

                x1,
                y1,
                x2,
                y2,

                strokeColor=colors.HexColor("#00AEEF"),

                strokeWidth=2

            )

        )

    # =====================================
    # Cities
    # =====================================

    for _,row in df.iterrows():

        city=row["City"]

        disaster=row["Disaster"]

        x,y=positions[city]

        if disaster=="Safe":

            color=colors.green

        elif disaster=="Flood":

            color=colors.blue

        elif disaster=="Cyclone":

            color=colors.red

        elif disaster=="Heatwave":

            color=colors.orange

        else:

            color=colors.purple

        drawing.add(

            Circle(

                x,
                y,

                7,

                fillColor=color,

                strokeColor=colors.black

            )

        )

        drawing.add(

            String(

                x+10,

                y-3,

                city,

                fontSize=8

            )

        )

    # =====================================
    # Legend
    # =====================================

    legend_x=35
    legend_y=335

    drawing.add(
        String(
            legend_x,
            legend_y,
            "Legend",
            fontSize=11
        )
    )

    legends=[

        ("Safe",colors.green),

        ("Flood",colors.blue),

        ("Cyclone",colors.red),

        ("Heatwave",colors.orange),

        ("Heavy Rain",colors.purple)

    ]

    y=legend_y-20

    for name,col in legends:

        drawing.add(
            Circle(
                legend_x+5,
                y,
                4,
                fillColor=col
            )
        )

        drawing.add(
            String(
                legend_x+18,
                y-3,
                name,
                fontSize=8
            )
        )

        y-=18

    # =====================================
    # Grid Summary
    # =====================================

    safe=len(df[df["Disaster"]=="Safe"])

    danger=len(df[df["Disaster"]!="Safe"])

    drawing.add(
        Rect(
            360,
            250,
            150,
            80,
            fillColor=colors.HexColor("#F5F5F5"),
            strokeColor=colors.grey
        )
    )

    drawing.add(
        String(
            375,
            310,
            "GRID STATUS",
            fontSize=11,
            fillColor=colors.darkblue
        )
    )

    drawing.add(
        String(
            375,
            290,
            f"Healthy Cities : {safe}",
            fontSize=9
        )
    )

    drawing.add(
        String(
            375,
            270,
            f"Disaster Zones : {danger}",
            fontSize=9
        )
    )

    drawing.add(
        String(
            375,
            250,
            "AI Monitoring : ACTIVE",
            fontSize=9
        )
    )

    return drawing
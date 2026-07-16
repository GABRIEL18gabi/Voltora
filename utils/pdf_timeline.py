from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors


def create_timeline():

    data=[

        ["Time","Event"],

        ["00:00","Sensor Reading"],

        ["00:01","AI Fault Prediction"],

        ["00:02","Risk Analysis"],

        ["00:03","Emergency Shutdown"],

        ["00:04","SCADA Updated"],

        ["00:05","PDF Report Generated"]

    ]

    table=Table(data,colWidths=[100,300])

    table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1565C0")),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("GRID",(0,0),(-1,-1),1,colors.grey),

            ("BACKGROUND",(0,1),(-1,-1),colors.HexColor("#F4F8FB")),

            ("ALIGN",(0,0),(-1,-1),"CENTER"),

            ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),

            ("BOTTOMPADDING",(0,0),(-1,-1),10)

        ])

    )

    return table
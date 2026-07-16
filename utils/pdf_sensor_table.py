from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors


def create_sensor_table(
    elements,
    voltage,
    current,
    frequency,
    temperature,
    fault,
    confidence,
    health
):

    data = [

        ["Parameter", "Value"],

        ["Voltage (V)", voltage],

        ["Current (A)", current],

        ["Frequency (Hz)", frequency],

        ["Temperature (°C)", temperature],

        ["Detected Fault", fault],

        ["AI Confidence", f"{confidence:.2f}%"],

        ["Grid Health", f"{health}%"]

    ]

    table = Table(
        data,
        colWidths=[220, 220]
    )

    table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#0B5394")),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("BACKGROUND",(0,1),(0,-1),colors.HexColor("#D9EAF7")),

            ("GRID",(0,0),(-1,-1),1,colors.grey),

            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

            ("FONTSIZE",(0,0),(-1,-1),11),

            ("BOTTOMPADDING",(0,0),(-1,0),10),

            ("ALIGN",(0,0),(-1,-1),"CENTER"),

            ("VALIGN",(0,0),(-1,-1),"MIDDLE")

        ])

    )

    elements.append(table)
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()


def create_contents_page(elements):

    elements.append(
        Paragraph(
            "<font size=24 color='#003366'><b>TABLE OF CONTENTS</b></font>",
            styles["Heading1"]
        )
    )

    elements.append(Spacer(1, 25))

    data = [

        ["Section", "Page"],

        ["Executive Dashboard", "2"],

        ["Executive Summary", "3"],

        ["Sensor Data Analysis", "4"],

        ["AI Prediction", "5"],

        ["AI Recommendation", "6"],

        ["Tamil Nadu GIS Network", "7"],

        ["Industrial SCADA", "8"],

        ["Sensor Trend Analysis", "9"],

        ["Event Timeline", "10"],

        ["QR Verification", "11"]

    ]

    table = Table(data, colWidths=[380, 80])

    table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1565C0")),

        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("BACKGROUND",(0,1),(-1,-1),colors.HexColor("#F5F9FF")),

        ("GRID",(0,0),(-1,-1),1,colors.grey),

        ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),

        ("FONTSIZE",(0,0),(-1,-1),12),

        ("BOTTOMPADDING",(0,0),(-1,-1),10),

        ("ALIGN",(1,0),(1,-1),"CENTER")

    ]))

    elements.append(table)

    elements.append(Spacer(1, 40))
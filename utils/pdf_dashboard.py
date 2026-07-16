from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer

styles = getSampleStyleSheet()


def create_dashboard(
    elements,
    fault,
    confidence,
    health,
    shutdown
):

    elements.append(
        Paragraph(
            "<font size=18 color='#003366'><b>Executive Dashboard</b></font>",
            styles["Heading1"]
        )
    )

    elements.append(Spacer(1,15))

    # -------------------------------------
    # Determine Risk Level
    # -------------------------------------

    if health >= 90:
        risk = "LOW"
        risk_color = "#00AA00"

    elif health >= 70:
        risk = "MEDIUM"
        risk_color = "#FF9900"

    else:
        risk = "HIGH"
        risk_color = "#CC0000"

    # -------------------------------------
    # Dashboard Table
    # -------------------------------------

    data = [

        [
            Paragraph("<b>Grid Health</b>",styles["BodyText"]),
            Paragraph("<b>AI Confidence</b>",styles["BodyText"])
        ],

        [
            f"{health} %",
            f"{confidence:.2f}%"
        ],

        [
            Paragraph("<b>Detected Fault</b>",styles["BodyText"]),
            Paragraph("<b>Emergency Shutdown</b>",styles["BodyText"])
        ],

        [
            fault,
            shutdown
        ],

        [
            Paragraph("<b>Overall Risk</b>",styles["BodyText"]),
            ""
        ],

        [
            Paragraph(
                f"<font color='{risk_color}'><b>{risk}</b></font>",
                styles["BodyText"]
            ),
            ""
        ]

    ]

    table = Table(data,colWidths=[230,230])

    table.setStyle(

    TableStyle([

        # Grid
        ("GRID",(0,0),(-1,-1),1,colors.grey),

        # Headers
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1565C0")),
        ("BACKGROUND",(0,2),(-1,2),colors.HexColor("#1565C0")),
        ("BACKGROUND",(0,4),(-1,4),colors.HexColor("#1565C0")),

        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("TEXTCOLOR",(0,2),(-1,2),colors.white),
        ("TEXTCOLOR",(0,4),(-1,4),colors.white),

        # Data Rows
        ("BACKGROUND",(0,1),(-1,1),colors.HexColor("#E3F2FD")),
        ("BACKGROUND",(0,3),(-1,3),colors.HexColor("#F5F5F5")),
        ("BACKGROUND",(0,5),(-1,5),colors.HexColor("#E8F5E9")),

        # Make ALL data text black
        ("TEXTCOLOR",(0,1),(-1,5),colors.black),

        ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),

        ("FONTSIZE",(0,0),(-1,-1),12),

        ("BOTTOMPADDING",(0,0),(-1,-1),12),

        ("ALIGN",(0,0),(-1,-1),"CENTER"),

        ("VALIGN",(0,0),(-1,-1),"MIDDLE")

    ])

)
    elements.append(table)

    elements.append(Spacer(1,20))
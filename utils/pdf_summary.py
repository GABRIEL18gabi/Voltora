from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer

styles = getSampleStyleSheet()


def create_summary_page(
    elements,
    voltage,
    current,
    frequency,
    temperature,
    fault,
    confidence,
    health,
    shutdown
):

    elements.append(
        Paragraph(
            "<font size=20 color='#003366'><b>Executive Summary Dashboard</b></font>",
            styles["Heading1"]
        )
    )

    elements.append(Spacer(1,15))

    # ---------------------------------------
    # Risk Level
    # ---------------------------------------

    if health >= 90:
        risk = "LOW"
        risk_color = "#4CAF50"

    elif health >= 70:
        risk = "MEDIUM"
        risk_color = "#FF9800"

    else:
        risk = "HIGH"
        risk_color = "#F44336"

    dashboard = [

        ["GRID HEALTH",
         "AI CONFIDENCE",
         "FAULT"],

        [
            f"{health} %",
            f"{confidence:.2f} %",
            fault
        ],

        ["SHUTDOWN",
         "RISK LEVEL",
         "STATUS"],

        [
            shutdown,
            risk,
            "ACTIVE"
        ]

    ]

    table = Table(
        dashboard,
        colWidths=[160,160,160]
    )

    table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1565C0")),
            ("BACKGROUND",(0,2),(-1,2),colors.HexColor("#1565C0")),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),
            ("TEXTCOLOR",(0,2),(-1,2),colors.white),

            ("BACKGROUND",(0,1),(-1,1),colors.HexColor("#E3F2FD")),
            ("BACKGROUND",(0,3),(-1,3),colors.HexColor("#F8F9FA")),

            ("TEXTCOLOR",(0,1),(-1,3),colors.black),

            ("GRID",(0,0),(-1,-1),1,colors.grey),

            ("ALIGN",(0,0),(-1,-1),"CENTER"),

            ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),

            ("BOTTOMPADDING",(0,0),(-1,-1),14),

            ("FONTSIZE",(0,0),(-1,-1),12)

        ])

    )

    elements.append(table)

    elements.append(Spacer(1,25))

    # ---------------------------------------
    # Sensor Cards
    # ---------------------------------------

    sensor_data = [

        ["Voltage (V)", voltage],

        ["Current (A)", current],

        ["Frequency (Hz)", frequency],

        ["Temperature (°C)", temperature]

    ]

    sensor = Table(
        sensor_data,
        colWidths=[220,120]
    )

    sensor.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#1976D2")),
            ("TEXTCOLOR",(0,0),(0,-1),colors.white),

            ("BACKGROUND",(1,0),(1,-1),colors.white),

            ("GRID",(0,0),(-1,-1),1,colors.grey),

            ("ALIGN",(0,0),(-1,-1),"CENTER"),

            ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),

            ("BOTTOMPADDING",(0,0),(-1,-1),10)

        ])

    )

    elements.append(
        Paragraph(
            "<font size=16 color='#003366'><b>Live Sensor Values</b></font>",
            styles["Heading2"]
        )
    )

    elements.append(sensor)

    elements.append(Spacer(1,20))

    # ---------------------------------------
    # Executive Decision
    # ---------------------------------------

    elements.append(

        Paragraph(

            "<font size=16 color='#003366'><b>Executive Decision</b></font>",

            styles["Heading2"]

        )

    )

    if shutdown=="YES":

        txt=f"""

        AI has determined that the detected fault
        requires immediate Emergency Shutdown.

        Grid Health has fallen to <b>{health}%</b>.

        Operator intervention is recommended.

        """

    else:

        txt="""

        Grid is operating normally.

        AI recommends continuous monitoring.

        Preventive maintenance schedule remains unchanged.

        """

    elements.append(
        Paragraph(
            txt,
            styles["BodyText"]
        )
    )

    elements.append(Spacer(1,20))
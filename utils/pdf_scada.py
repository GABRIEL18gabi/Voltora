from reportlab.graphics.shapes import (
    Drawing,
    Line,
    Circle,
    Rect,
    String
)
from reportlab.lib import colors


def create_scada_diagram(fault):

    d = Drawing(560,420)

    # ==========================================
    # TITLE
    # ==========================================

    d.add(
        String(
            140,
            395,
            "SMART GRID SINGLE LINE DIAGRAM",
            fontSize=18,
            fillColor=colors.darkblue
        )
    )

    # ==========================================
    # BORDER
    # ==========================================

    d.add(
        Rect(
            10,
            10,
            540,
            370,
            strokeColor=colors.grey,
            fillColor=None
        )
    )

    x = 280

    # ==========================================
    # GRID SOURCE
    # ==========================================

    d.add(
        Circle(
            x,
            360,
            18,
            fillColor=colors.HexColor("#4CAF50"),
            strokeColor=colors.black,
            strokeWidth=2
        )
    )

    d.add(
        String(
            x-28,
            335,
            "GRID SOURCE",
            fontSize=9
        )
    )

    # Main Bus

    d.add(
        Line(
            x,
            342,
            x,
            320,
            strokeColor=colors.black,
            strokeWidth=4
        )
    )

    # ==========================================
    # CIRCUIT BREAKER
    # ==========================================

    d.add(
        Rect(
            x-12,
            300,
            24,
            18,
            fillColor=colors.white,
            strokeColor=colors.black,
            strokeWidth=2
        )
    )

    d.add(
        String(
            x+20,
            304,
            "Circuit Breaker",
            fontSize=9
        )
    )

    # ==========================================
    # TRANSFORMER
    # ==========================================

    d.add(
        Line(
            x,
            300,
            x,
            275,
            strokeColor=colors.black,
            strokeWidth=4
        )
    )

    d.add(
        Circle(
            x-15,
            255,
            12,
            fillColor=colors.HexColor("#2196F3"),
            strokeColor=colors.black
        )
    )

    d.add(
        Circle(
            x+15,
            255,
            12,
            fillColor=colors.HexColor("#2196F3"),
            strokeColor=colors.black
        )
    )

    d.add(
        String(
            x-35,
            228,
            "Transformer",
            fontSize=10
        )
    )

    # ==========================================
    # FEEDER
    # ==========================================

    d.add(
        Line(
            x,
            243,
            x,
            205,
            strokeColor=colors.black,
            strokeWidth=4
        )
    )

    # ==========================================
    # POLES
    # ==========================================

    pole_y=[185,145,105]

    for i,y in enumerate(pole_y):

        d.add(
            Circle(
                x,
                y,
                8,
                fillColor=colors.green,
                strokeColor=colors.black
            )
        )

        d.add(
            String(
                x+18,
                y-5,
                f"Pole {i+1}",
                fontSize=9
            )
        )

    # Vertical line

    d.add(
        Line(
            x,
            205,
            x,
            82,
            strokeColor=colors.black,
            strokeWidth=4
        )
    )

    # ==========================================
    # CONSUMER
    # ==========================================

    d.add(
        Rect(
            x-25,
            35,
            50,
            30,
            fillColor=colors.orange,
            strokeColor=colors.black
        )
    )

    d.add(
        String(
            x-22,
            15,
            "Consumer",
            fontSize=9
        )
    )

    # ==========================================
    # STATUS PANEL
    # ==========================================

    d.add(
        Rect(
            380,
            270,
            140,
            90,
            fillColor=colors.HexColor("#F5F5F5"),
            strokeColor=colors.grey
        )
    )

    d.add(
        String(
            395,
            340,
            "SYSTEM STATUS",
            fontSize=11,
            fillColor=colors.darkblue
        )
    )

    if fault=="Normal":

        txt1="Grid : HEALTHY"
        txt2="Breaker : CLOSED"
        txt3="Power : AVAILABLE"

        color=colors.green

    else:

        txt1=f"Fault : {fault}"
        txt2="Breaker : OPEN"
        txt3="Shutdown : ACTIVE"

        color=colors.red

    d.add(String(392,320,txt1,fontSize=9,fillColor=color))
    d.add(String(392,300,txt2,fontSize=9))
    d.add(String(392,280,txt3,fontSize=9))

    # ==========================================
    # FAULT
    # ==========================================

    if fault!="Normal":

        d.add(
            Circle(
                x,
                165,
                14,
                fillColor=colors.red,
                strokeColor=colors.black
            )
        )

        d.add(
            String(
                x+18,
                160,
                "FAULT",
                fontSize=10,
                fillColor=colors.red
            )
        )

        d.add(
            String(
                120,
                375,
                "🚨 AI AUTOMATIC EMERGENCY SHUTDOWN ACTIVATED",
                fontSize=12,
                fillColor=colors.red
            )
        )

    else:

        d.add(
            String(
                150,
                375,
                "🟢 GRID OPERATING NORMALLY",
                fontSize=12,
                fillColor=colors.green
            )
        )

    # ==========================================
    # LEGEND
    # ==========================================

    d.add(
        String(
            30,
            340,
            "Legend",
            fontSize=11
        )
    )

    legends=[

        ("Healthy",colors.green),

        ("Fault",colors.red),

        ("Transformer",colors.HexColor("#2196F3")),

        ("Consumer",colors.orange)

    ]

    y=320

    for text,col in legends:

        d.add(
            Circle(
                35,
                y,
                5,
                fillColor=col
            )
        )

        d.add(
            String(
                50,
                y-3,
                text,
                fontSize=9
            )
        )

        y-=22

    return d
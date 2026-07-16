from reportlab.platypus import Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

from utils.pdf_graphs import create_sensor_graph
from utils.pdf_timeline import create_timeline

styles = getSampleStyleSheet()


def create_analysis_pages(
    elements,
    voltage,
    current,
    frequency,
    temperature
):

    # =====================================
    # SENSOR TREND ANALYSIS
    # =====================================

    elements.append(
        Paragraph(
            "<font size=18 color='#003366'><b>Sensor Trend Analysis</b></font>",
            styles["Heading1"]
        )
    )

    elements.append(Spacer(1, 12))

    elements.append(create_sensor_graph("Voltage", voltage, 180, 280))
    elements.append(Spacer(1, 10))

    elements.append(create_sensor_graph("Current", current, 0, 20))
    elements.append(Spacer(1, 10))

    elements.append(create_sensor_graph("Frequency", frequency, 45, 55))
    elements.append(Spacer(1, 10))

    elements.append(create_sensor_graph("Temperature", temperature, 20, 80))

    elements.append(PageBreak())

    # =====================================
    # EVENT TIMELINE
    # =====================================

    elements.append(
        Paragraph(
            "<font size=18 color='#003366'><b>Fault Event Timeline</b></font>",
            styles["Heading1"]
        )
    )

    elements.append(Spacer(1, 10))

    elements.append(create_timeline())

    elements.append(Spacer(1, 20))
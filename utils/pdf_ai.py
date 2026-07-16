from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()


def create_ai_section(
    elements,
    fault,
    confidence,
    health,
    shutdown
):

    # ==========================
    # AI Prediction
    # ==========================

    elements.append(
        Paragraph(
            "<font size=18 color='#003366'><b>AI Prediction</b></font>",
            styles["Heading1"]
        )
    )

    prediction = f"""

    <b>Detected Fault :</b> {fault}<br/><br/>

    <b>Prediction Confidence :</b> {confidence:.2f}%<br/><br/>

    <b>Grid Health :</b> {health}%<br/><br/>

    <b>Emergency Shutdown :</b> {shutdown}

    """

    elements.append(
        Paragraph(
            prediction,
            styles["BodyText"]
        )
    )

    elements.append(Spacer(1,20))

    # ==========================
    # AI Recommendation
    # ==========================

    elements.append(
        Paragraph(
            "<font size=18 color='#003366'><b>AI Recommendation</b></font>",
            styles["Heading1"]
        )
    )

    if fault == "Normal":

        recommendation = """
        ✔ Grid operating normally.<br/>
        ✔ Continue monitoring.<br/>
        ✔ Preventive maintenance every 30 days.
        """

    elif fault == "Overload":

        recommendation = """
        ✔ Reduce connected load.<br/>
        ✔ Inspect transformer immediately.<br/>
        ✔ Emergency shutdown executed.
        """

    elif fault == "Overvoltage":

        recommendation = """
        ✔ Check voltage regulator.<br/>
        ✔ Inspect incoming feeder.<br/>
        ✔ Verify insulation condition.
        """

    elif fault == "Undervoltage":

        recommendation = """
        ✔ Inspect feeder losses.<br/>
        ✔ Check transformer loading.<br/>
        ✔ Verify source voltage.
        """

    else:

        recommendation = """
        ✔ Dispatch maintenance team.<br/>
        ✔ Replace damaged conductor.<br/>
        ✔ Restore power after inspection.
        """

    elements.append(
        Paragraph(
            recommendation,
            styles["BodyText"]
        )
    )

    elements.append(Spacer(1,20))

    # ==========================
    # Grid Status
    # ==========================

    elements.append(
        Paragraph(
            "<font size=18 color='#003366'><b>Grid Status</b></font>",
            styles["Heading1"]
        )
    )

    if health >= 80:

        status = "<font color='green'><b>🟢 GRID OPERATING NORMALLY</b></font>"

    else:

        status = "<font color='red'><b>🔴 EMERGENCY SHUTDOWN ACTIVE</b></font>"

    elements.append(
        Paragraph(
            status,
            styles["Heading2"]
        )
    )

    elements.append(Spacer(1,20))
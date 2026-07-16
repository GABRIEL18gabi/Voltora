import pandas as pd

from reportlab.platypus import Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

from utils.pdf_gis import create_gis_map
from utils.pdf_scada import create_scada_diagram

styles = getSampleStyleSheet()


def create_network_pages(elements, fault):

    # =====================================
    # GIS MAP
    # =====================================

    elements.append(
        Paragraph(
            "<font size=18 color='#003366'><b>Tamil Nadu Power Grid GIS</b></font>",
            styles["Heading1"]
        )
    )

    elements.append(Spacer(1, 10))

    df = pd.read_csv("data/tamilnadu_cities.csv")

    elements.append(
        create_gis_map(df)
    )

    elements.append(PageBreak())

    # =====================================
    # SCADA PAGE
    # =====================================

    elements.append(
        Paragraph(
            "<font size=18 color='#003366'><b>Industrial Smart Grid SCADA</b></font>",
            styles["Heading1"]
        )
    )

    elements.append(Spacer(1, 10))

    elements.append(
        create_scada_diagram(fault)
    )

    elements.append(Spacer(1, 20))
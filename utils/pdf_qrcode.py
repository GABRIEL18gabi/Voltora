from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.platypus import Spacer


def create_qr(
    elements,
    url="https://gridguard-ai.streamlit.app"
):
    qr_code = qr.QrCodeWidget(url)

    bounds = qr_code.getBounds()

    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]

    drawing = Drawing(120, 120)

    drawing.add(qr_code)

    elements.append(drawing)

    elements.append(Spacer(1, 15))
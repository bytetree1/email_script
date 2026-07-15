from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from io import BytesIO

def create_watermark(name, email):
    packet = BytesIO()

    c = canvas.Canvas(packet)

    c.setFont("Helvetica-Bold", 28)

    c.setFillColor(Color(0.7, 0.7, 0.7, alpha=0.25))

    c.saveState()
    c.translate(300, 400)
    c.rotate(45)

    c.drawCentredString(
        0,
        0,
        "BYTE TREE CONFIDENTIAL"
    )

    c.setFont("Helvetica",18)

    c.drawCentredString(
        0,
        -40,
        f"{name}"
    )

    c.drawCentredString(
        0,
        -70,
        email
    )

    c.restoreState()

    c.save()

    packet.seek(0)

    return packet
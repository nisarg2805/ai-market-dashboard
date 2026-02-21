from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def build_pdf_report(title: str, lines: list[str]) -> bytes:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    y = height - 60
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, title)

    y -= 30
    c.setFont("Helvetica", 11)

    for line in lines:
        # wrap long lines simply
        chunks = [line[i:i+95] for i in range(0, len(line), 95)]
        for ch in chunks:
            if y < 60:
                c.showPage()
                y = height - 60
                c.setFont("Helvetica", 11)
            c.drawString(50, y, ch)
            y -= 16

    c.showPage()
    c.save()
    return buffer.getvalue()

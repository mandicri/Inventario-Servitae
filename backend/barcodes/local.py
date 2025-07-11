import io
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
from reportlab.lib.pagesizes import letter


def generate_barcode_pdf(sku: str, product_name: str) -> bytes:
    """Generate a PDF page with barcodes for the given SKU and product name.

    The page is letter sized (8.5x11 inches) and contains 4 columns by 8 rows
    of the same barcode.
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    page_width, page_height = letter
    cols, rows = 4, 8
    cell_width = page_width / cols
    cell_height = page_height / rows

    barcode_height = cell_height * 0.5
    text_y_offset = 12  # points under the barcode

    for row in range(rows):
        for col in range(cols):
            x = col * cell_width + (cell_width - cell_width * 0.8) / 2
            y = page_height - (row + 1) * cell_height + (cell_height - barcode_height) / 2

            code = code128.Code128(sku, barHeight=barcode_height, barWidth=0.4)
            code.drawOn(c, x, y)
            c.setFont("Helvetica", 8)
            c.drawCentredString(col * cell_width + cell_width / 2, y - text_y_offset, product_name)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.getvalue()
